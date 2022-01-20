import os
from pathlib import Path
from typing import Union
from tinydb import Query, TinyDB

config_dir = Path.home() / ".config" / "slurmer"
user_template_dir = config_dir / "templates"
default_template_dir = Path(__file__).parent / "templates"

if not config_dir.is_dir():
    config_dir.mkdir(parents=True)
if not user_template_dir.is_dir():
    user_template_dir.mkdir(parents=True)


class TemplateManager:
    """Manages template file path"""

    _db_path: Path = config_dir / "config.json"
    _db: TinyDB = TinyDB(_db_path)

    def __init__(self):
        self._update_dirs()

    def _update_dirs(self):
        """Updates template dirs with config db"""
        self.template_dirs = [default_template_dir.absolute(), user_template_dir.absolute()]
        for d in self._db.all():
            self.template_dirs.append(Path(d["path"]))

    def show_dirs(self):
        """Show directories for finding template files."""
        for d in self.template_dirs:
            print(d)

    def show_templates(self):
        """Show full list of template files."""
        for d in self.template_dirs:
            for f in os.listdir(d):
                print("directory:", d, "file:", f)

    def add_path(self, path: Union[str, os.PathLike]):
        """Add path to config.

        Args:
          path: Directory to find templates in.

        Raises:
          ValueError: Raised if path already exists in config.
        """
        abs_path = Path(path).absolute()
        if abs_path not in self.template_dirs:
            self._db.insert({"path": abs_path.__str__()})
        else:
            raise ValueError("Path already exists: {}".format(abs_path))
        self._update_dirs()

    def remove_path(self, path: Union[str, os.PathLike]):
        """Remove path from config.

        Args:
          path:  Directory to remove.

        Raises:
          ValueError: Raised if path does not exists in config.
        """
        abs_path = Path(path).absolute()
        q = Query()
        return_code = self._db.remove(q.path == abs_path.__str__())
        if not return_code:
            raise ValueError("Path does not exists in config.json")
        self._update_dirs()

    def clear(self):
        """Reset to default"""
        self._db.truncate()
        self._update_dirs()
