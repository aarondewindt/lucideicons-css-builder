import shutil
import base64

from git import Repo
from pathlib import Path
from jinja2 import Environment, FileSystemLoader



def build(url: str="https://github.com/lucide-icons/lucide.git",
          branch: str="master",
          class_prefix: str="lc"):

    # Define paths
    repo_path = Path(__file__).parent.absolute()
    lucide_path = repo_path / "lucide"
    icons_path = lucide_path / "icons"
    lucide_css_path = repo_path / "lucide.css"

    if lucide_path.exists():
        shutil.rmtree(lucide_path)

    # Clone repository
    Repo.clone_from(url, lucide_path, multi_options=["--single-branch", "--branch", branch])

    # Load template
    env = Environment(loader=FileSystemLoader(str(repo_path)))
    lucide_css_template = env.get_template("template.css")

    icons = []
    for icon_path in icons_path.glob("*.svg"):
        with icon_path.open("rb") as f:
            icons.append((icon_path.stem, base64.b64encode(f.read()).decode("utf-8")))

    # Render template
    with lucide_css_path.open("w") as f:
        f.write(lucide_css_template.render(
            class_prefix=class_prefix,
            icons=icons))


if __name__ == "__main__":
    build()
