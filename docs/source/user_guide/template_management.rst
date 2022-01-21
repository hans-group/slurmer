Template Management
===================

Once installed, ``slurmer`` only contains ``default.sh`` as available template.
By default, ``slurmer`` find template files in ``$HOME/.config/slurmer/templates``.
All template files in this directory are detected by ``slurmer``.
Users can also add custom directories to find templates in.

Show the list of available templates
------------------------------------

The full list of templates available can be shown by calling the function ``slurmer.list_templates()``.
Directory and filename are presented respectively.

.. code-block:: python

    >>> import slurmer
    >>> slurmer.list_templates()
    directory: {path_to_site-packages}/slurmer/templates file: default.sh


Add directory to look up templates
----------------------------------

To add directory to find templates, use ``TemplateManager`` object.

.. code-block:: python

    from slurmer.config import TemplateManager

    m = TemplateManager()
    m.add_path('path/to/template')
