import os
import subprocess
from typing import Optional, Sequence, Union
from pathlib import Path
from shutil import copyfile
from tempfile import NamedTemporaryFile

from jinja2 import Environment, FileSystemLoader, select_autoescape

from .config import TemplateManager

m = TemplateManager()
loader = FileSystemLoader(m.template_dirs)
env = Environment(loader=loader, autoescape=select_autoescape())


class SlurmJob:
    """Slurm job class.

    Args:
        workdir (Union[str, os.PathLike]): Working directory for slurm jon.
        template_file (str): Path of template file.
        job_name (str): Name of job.
        node_partition (str): Partition of nodes.
        num_nodes (int): The number of nodes.
        num_tasks (int): The number of tasks(threads).
        node_list (Optional[Sequence[int]], optional): List of nodes to use. Defaults to None.
        node_exclude_list (Optional[str], optional): List of nodes to exclude. Defaults to None.
        kwargs: Optional arguments, which are passed into ``generate_jobscript``.
    """

    def __init__(
        self,
        workdir: Union[str, os.PathLike],
        template_file: str,
        job_name: str,
        node_partition: str,
        num_nodes: int,
        num_tasks: int,
        node_list: Optional[Sequence[int]] = None,
        node_exclude_list: Optional[str] = None,
        **kwargs,
    ):

        if not isinstance(workdir, Path):
            self.workdir = Path(workdir)
        else:
            self.workdir = workdir
        self.template_file = template_file
        self.job_name = job_name
        self.node_partition = node_partition
        self.num_nodes = num_nodes
        self.num_tasks = num_tasks
        self.node_list = node_list
        self.node_exclude_list = node_exclude_list
        self.extra_args = kwargs
        self.__job_script: Optional[str] = None

    @property
    def job_script(self) -> str:
        """Job script.

        Returns:
            str: Generated job script from instance attributes.
        """
        if self.__job_script is not None:
            return self.__job_script
        else:
            job_script = generate_jobscript(
                template_file=self.template_file,
                job_name=self.job_name,
                node_partition=self.node_partition,
                num_nodes=self.num_nodes,
                num_tasks=self.num_tasks,
                node_list=self.node_list,
                node_exclude_list=self.node_exclude_list,
                **self.extra_args,
            )
            return job_script

    def submit(self, write_job_script: bool = False, job_script_name: str = "job_script.sh"):
        """Submit batch job via slurm workload manager.

        Args:
            write_job_script (bool, optional): Whether to write the job script in ``self.workdir``.
            Defaults to False.
            job_script_name (str, optional): Name of the job script. Defaults to "job_script.sh".

        Raises:
            RuntimeError: Raised if the working directory does not exist.
        """
        cwd = Path.cwd()
        if not self.workdir.is_dir():
            raise RuntimeError("Workdir does not exists.")

        os.chdir(self.workdir)
        with NamedTemporaryFile("w") as f:
            f.write(self.job_script)
            f.file.close()

            subprocess.check_call(["sbatch", f.name])
            if write_job_script:
                copyfile(f.name, job_script_name)
        os.chdir(cwd)


def generate_jobscript(
    template_file: str,
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
        template_file (str): Path of template file.
        job_name (str): Name of job.
        node_partition (str): Partition of nodes.
        num_nodes (int): The number of nodes.
        num_tasks (int): The number of tasks(threads).
        node_list (Optional[Sequence[int]], optional): List of nodes to use. Defaults to None.
        node_exclude_list (Optional[str], optional): List of nodes to exclude. Defaults to None.
        kwargs: Optional template identifiers.

    Raises:
        ValueError: Raised when both node_list and node_exclude_list are specified.

    Returns:
        str: Rendered job script as string.
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
