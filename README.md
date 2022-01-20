# slurmer

Automatic generation of `SLURM` job script based on `jinja` template engine


## Install

Install `master` branch: `pip install git+https://github.com/mjhong0708/slurmer`

Install latest version(0.2.0): `pip install git+https://github.com/mjhong0708/slurmer.git@v0.2.0`

Or, download wheel from `release` tab and `pip install` it.


## Usage

By default, [`default.sh`](https://github.com/mjhong0708/slurmer/blob/master/slurmer/templates/default.sh) is available as template.

- Show list of available templates

  ```python
  import slurmer

  slurmer.list_templates()
  ```
- Add directory to seek template files

  ```python
  from slurmer.config import TemplateManager

  m = TemplateManager()
  m.add_path('path/to/template')
  ```
- Submit job
  
  ```python
  from slurmer.job import SlurmJob

  job_dir = "my_job"

  job = SlurmJob(
      workdir=job_dir,
      template_file="default.sh",
      job_name="my_slurm_job",
      node_partition="g1",
      num_nodes=2,
      num_tasks=32,
      exec_command="echo Hello,world!", # this is required by default.sh
  )

  job.submit()
  ```
  The keyword argument `exec_command` is required by `default.sh`.
  If you use your custom template, it is not required.
