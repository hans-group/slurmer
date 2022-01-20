# slurmer

Automatic generation of `SLURM` job script based on `jinja` template engine


## Install

Install `master` branch: `pip install git+https://github.com/mjhong0708/slurmer`

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
  import os
  from slurmer.job import SlurmJob

  job_dir = "my_job"
  os.mkdir(job_dir)

  job = SlurmJob(job_dir, "default.sh", "myjob", "g1", 2, 32, exec_command="echo 'Hello'")

  job.submit(write_job_script=True)
  ```
