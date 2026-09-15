"""Pin and run the original kit alongside a local Chinese capability guide."""
import argparse
from functools import partial
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
import json
import os
from pathlib import Path
import shutil
import socket
import subprocess
import sys
import time
from urllib.error import URLError
from urllib.request import urlopen

ROOT = Path(__file__).resolve().parents[1]
UPSTREAM = ROOT / "upstream"
REVISION = "d5f62cb074b506697fb035c420415026bafbe792"
REPOSITORY = "https://github.com/vibegameengine/web-starter-kit.git"
COURTYARD_PATCH = ROOT / "patches/courtyard.patch"


def tool(name):
    found = shutil.which(name)
    if not found:
        raise RuntimeError(f"Required tool is missing: {name}")
    return found


def run(args, cwd=ROOT, env=None):
    subprocess.run(args, cwd=cwd, check=True, env=env)


def prepare_courtyard():
    if not COURTYARD_PATCH.exists():
        raise RuntimeError("Missing courtyard patch; restore patches/courtyard.patch before launching.")
    git = tool("git")
    patch_args = [git, "apply", "--ignore-space-change"]
    already_applied = subprocess.run(
        [*patch_args, "--reverse", "--check", str(COURTYARD_PATCH)],
        cwd=UPSTREAM, capture_output=True,
    )
    if already_applied.returncode == 0:
        return
    can_apply = subprocess.run(
        [*patch_args, "--check", str(COURTYARD_PATCH)],
        cwd=UPSTREAM, capture_output=True,
    )
    if can_apply.returncode != 0:
        raise RuntimeError("Courtyard patch conflicts with the checkout. Local changes have been preserved; review them before retrying.")
    run([*patch_args, str(COURTYARD_PATCH)], UPSTREAM)


def setup():
    git = tool("git")
    if not UPSTREAM.exists():
        run([git, "clone", "--depth", "1", REPOSITORY, str(UPSTREAM)])
    if not (UPSTREAM / ".git").exists():
        raise RuntimeError("upstream exists but is not a Git checkout; preserve it and use a separate folder.")
    current = subprocess.check_output([git, "rev-parse", "HEAD"], cwd=UPSTREAM, text=True).strip()
    if current != REVISION:
        dirty = subprocess.check_output([git, "status", "--porcelain"], cwd=UPSTREAM, text=True).strip()
        if dirty:
            raise RuntimeError("Upstream has local changes; refusing to change revision.")
        run([git, "fetch", "--depth", "1", "origin", REVISION], UPSTREAM)
        run([git, "checkout", "--detach", REVISION], UPSTREAM)
    install_env = os.environ.copy()
    # The pinned upstream invokes .ts scripts directly. Node 22.15 requires
    # this opt-in; newer Node 22 releases enable type stripping by default.
    install_env["NODE_OPTIONS"] = (install_env.get("NODE_OPTIONS", "") + " --experimental-strip-types").strip()
    run([tool("npm.cmd" if sys.platform == "win32" else "npm"), "ci",
         "--prefer-offline", "--fetch-timeout=45000", "--fetch-retries=1",
         "--no-audit", "--no-fund"], UPSTREAM, env=install_env)
    prepare_courtyard()
    print("Setup complete. Run: python scripts/demo.py serve", flush=True)


def check_port(port):
    with socket.socket() as sock:
        sock.bind(("127.0.0.1", port))


class GuideHandler(SimpleHTTPRequestHandler):
    runtime_base = ""

    def do_GET(self):
        if self.path.split("?", 1)[0] == "/runtime-config.js":
            body = f"window.DEMO_RUNTIME_BASE = {json.dumps(self.runtime_base)};\n".encode()
            self.send_response(200)
            self.send_header("Content-Type", "text/javascript; charset=utf-8")
            self.send_header("Cache-Control", "no-store")
            self.send_header("Content-Length", str(len(body)))
            self.end_headers()
            self.wfile.write(body)
            return
        super().do_GET()


def serve(args):
    if not (UPSTREAM / "node_modules/vite").exists():
        raise RuntimeError("Dependencies are missing. First run: python scripts/demo.py setup")
    prepare_courtyard()
    for port in (args.port, args.runtime_port):
        check_port(port)
    if args.port == args.runtime_port:
        raise RuntimeError("Guide and runtime ports must be different.")
    runtime_base = f"http://127.0.0.1:{args.runtime_port}"
    GuideHandler.runtime_base = runtime_base
    runtime = subprocess.Popen(
        [tool("node"), str(UPSTREAM / "node_modules/vite/bin/vite.js"),
         "--host", "127.0.0.1", "--port", str(args.runtime_port), "--strictPort"],
        cwd=UPSTREAM,
        creationflags=subprocess.CREATE_NO_WINDOW if sys.platform == "win32" else 0,
    )
    server = None
    try:
        deadline = time.monotonic() + 120
        while time.monotonic() < deadline:
            if runtime.poll() is not None:
                raise RuntimeError("The upstream runtime exited during startup.")
            try:
                with urlopen(runtime_base, timeout=2) as response:
                    if response.status == 200:
                        break
            except (URLError, TimeoutError):
                time.sleep(0.5)
        else:
            raise RuntimeError("Timed out waiting for the upstream runtime.")
        handler = partial(GuideHandler, directory=str(ROOT / "demo"))
        server = ThreadingHTTPServer(("127.0.0.1", args.port), handler)
        server.timeout = 0.5
        print(f"\nCapability guide: http://127.0.0.1:{args.port}/", flush=True)
        print(f"Original runtime: {runtime_base}/\nPress Ctrl+C to stop both servers.", flush=True)
        while runtime.poll() is None:
            server.handle_request()
        raise RuntimeError("The upstream runtime stopped. Restart the launcher to recover.")
    except KeyboardInterrupt:
        print("Stopping local demo.", flush=True)
    finally:
        if server:
            server.server_close()
        runtime.terminate()
        try:
            runtime.wait(timeout=10)
        except subprocess.TimeoutExpired:
            runtime.kill()
            runtime.wait()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    commands = parser.add_subparsers(dest="command", required=True)
    commands.add_parser("setup")
    serve_parser = commands.add_parser("serve")
    serve_parser.add_argument("--port", type=int, default=5175)
    serve_parser.add_argument("--runtime-port", type=int, default=5174)
    args = parser.parse_args()
    if args.command == "setup":
        setup()
    else:
        serve(args)


if __name__ == "__main__":
    try:
        main()
    except (RuntimeError, OSError, subprocess.CalledProcessError) as error:
        print(f"Error: {error}", file=sys.stderr)
        sys.exit(1)
