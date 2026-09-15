"""Stage only this project's static assets for Sites; parent build uses app directly."""
from pathlib import Path
import shutil

project = Path(__file__).resolve().parents[1]
shutil.copytree(project / 'app', project / 'dist', dirs_exist_ok=True)
print('Staged independent static site in dist/')
