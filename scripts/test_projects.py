"""Regression checks for numbering, README generation, and invalid metadata."""

import argparse
import contextlib
import io
import json
from pathlib import Path
import shutil
import tempfile
import unittest

import projects


class ProjectTests(unittest.TestCase):
    def setUp(self):
        original = projects.ROOT
        temporary = tempfile.TemporaryDirectory(prefix="research-index-")
        self.addCleanup(temporary.cleanup)
        self.addCleanup(setattr, projects, "ROOT", original)
        self.root = Path(temporary.name).resolve()
        shutil.copyfile(original / "README.md", self.root / "README.md")
        shutil.copytree(original / "templates", self.root / "templates")
        (self.root / "projects").mkdir()
        projects.ROOT = self.root
        with contextlib.redirect_stdout(io.StringIO()):
            projects.sync()

    def create(self, slug="example", **overrides):
        values = dict(slug=slug, title="研究项目", summary="研究摘要", upstream="https://github.com/owner/repo")
        values.update(overrides)
        with contextlib.redirect_stdout(io.StringIO()):
            projects.create(argparse.Namespace(**values))
        return next((self.root / "projects").glob(f"*-{slug}"))

    def update(self, directory, **values):
        path = directory / "project.json"
        data = json.loads(path.read_text(encoding="utf-8"))
        data.update(values)
        path.write_text(json.dumps(data, ensure_ascii=False), encoding="utf-8")

    def test_numbering_and_archive_order(self):
        first = self.create("zeta")
        self.update(first, status="已归档")
        second = self.create("alpha")
        self.assertEqual(first.name, "001-zeta")
        self.assertEqual(second.name, "002-alpha")
        self.assertEqual([p["slug"] for p in projects.projects()], ["zeta", "alpha"])
        with contextlib.redirect_stdout(io.StringIO()):
            projects.sync(check=True)

    def test_new_project_after_gap_uses_maximum(self):
        first = self.create()
        renamed = first.with_name("007-example")
        first.rename(renamed)
        self.update(renamed, id="007")
        self.assertEqual(self.create("next").name, "008-next")

    def test_sync_detects_drift_and_preserves_manual_text(self):
        directory = self.create()
        readme = self.root / "README.md"
        readme.write_text("自定义介绍\n\n" + readme.read_text(encoding="utf-8"), encoding="utf-8")
        self.update(directory, summary="更新后的研究摘要")
        with self.assertRaisesRegex(ValueError, "索引需要更新"):
            projects.sync(check=True)
        with contextlib.redirect_stdout(io.StringIO()):
            projects.sync()
        self.assertTrue(readme.read_text(encoding="utf-8").startswith("自定义介绍"))
        self.assertIn("更新后的研究摘要", readme.read_text(encoding="utf-8"))

    def test_cover_and_demo_links(self):
        directory = self.create()
        (directory / "assets" / "cover.svg").write_text(
            '<svg xmlns="http://www.w3.org/2000/svg" width="1" height="1"/>', encoding="utf-8")
        self.update(directory, cover="assets/cover.svg", demo_url="https://example.com/demo/")
        content = projects.rendered_readme(projects.projects())
        self.assertIn("projects/001-example/assets/cover.svg", content)
        self.assertIn("[在线演示](https://example.com/demo/)", content)

    def test_duplicate_id_is_rejected(self):
        self.create("first")
        second = self.create("second")
        renamed = second.with_name("001-second")
        second.rename(renamed)
        self.update(renamed, id="001")
        with self.assertRaisesRegex(ValueError, "重复的项目编号"):
            projects.projects()

    def test_missing_and_escaping_cover_are_rejected(self):
        directory = self.create()
        for cover in ("assets/missing.png", "../../README.md"):
            self.update(directory, cover=cover)
            with self.assertRaisesRegex(ValueError, "cover"):
                projects.projects()

    def test_invalid_input_leaves_no_project(self):
        for values in ({"slug": "../outside"}, {"upstream": "javascript:alert(1)"}, {"title": ""}):
            with self.assertRaises(ValueError):
                self.create(**values)
        self.assertEqual(list((self.root / "projects").iterdir()), [])

    def test_markdown_characters_are_escaped(self):
        self.create(title="项目 | [链接]", summary="研究 <script> & *内容*")
        content = (self.root / "README.md").read_text(encoding="utf-8")
        self.assertIn(r"项目 \| \[链接\]", content)
        self.assertIn("&lt;script&gt; &amp;", content)

    def test_broken_markers_block_creation(self):
        readme = self.root / "README.md"
        readme.write_text("无生成标记", encoding="utf-8")
        with self.assertRaisesRegex(ValueError, "标记"):
            self.create()
        self.assertEqual(list((self.root / "projects").iterdir()), [])


if __name__ == "__main__":
    unittest.main()
