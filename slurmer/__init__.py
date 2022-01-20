from .config import TemplateManager

__version__ = "0.2.0"


def list_templates():
    """Show list of templates.
    Directory and filename are displayed.
    """
    m = TemplateManager()
    m.show_templates()
