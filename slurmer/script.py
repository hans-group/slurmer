import os
from typing import Sequence, Optional

from jinja2 import Environment, FileSystemLoader, select_autoescape

from .config import TemplateManager

m = TemplateManager()
loader = FileSystemLoader(m.template_dirs)
env = Environment(loader=loader, autoescape=select_autoescape())


def get_script(
    template_file: os.PathLike,
    job_name: str,
    node_partition: str,
    num_nodes: int,
    num_tasks: int,
    node_list: Optional[Sequence[int]] = None,
    node_exclude_list: Optional[str] = None,
    **kwargs,
) -> str:
    """Get slurm job script.

    Args:
        template_file (os.PathLike): Path of template file.
        job_name (str): Name of job.
        node_partition (str): Partition of nodes.
        num_nodes (int): The number of nodes.
        num_tasks (int): The number of tasks(threads).
        node_list (Optional[Sequence[int]], optional): List of nodes to use. Defaults to None.
        node_exclude_list (Optional[str], optional): List of nodes to exclude. Defaults to None.

    Raises:
        ValueError: Raised when both node_list and node_exclude_list are specified.

    Returns:
        str: Rendered job script.
    """
    if node_list is not None and node_exclude_list is not None:
        raise ValueError("node_list and node_exclude list cannot be specified simultaneously.")

    if node_list is None:
        _node_list = "none"
    else:
        _node_list = ",".join([f"n{node:0>3}" for node in node_list])

    if node_exclude_list is None:
        _node_exclude_list = "none"
    else:
        _node_exclude_list = node_exclude_list

    template = env.get_template(template_file.__str__())
    rendered = template.render(
        job_name=job_name,
        node_partition=node_partition,
        num_nodes=num_nodes,
        num_tasks=num_tasks,
        node_list=_node_list,
        node_exclude_list=_node_exclude_list,
        **kwargs,
    )
    return rendered
