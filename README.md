# slurmer

Automatic generation of `SLURM` job script based on `jinja` template engine


## Install

Clone repository, install `poetry` and run `poetry install`.


## Usage

Prepare a template file in `~/.config/slurmer/templates`.

Example: `run_slurm.sh`

```bash
#!/bin/bash
#SBATCH -J {{ job_name }}
#SBATCH -o myMPI.o%j       # output and error file name (%j expands to jobID)
#SBATCH -p {{ node_partition }}
#SBATCH -N {{ num_nodes }}
#SBATCH -n {{ num_tasks }}
{% if node_list == 'none' %}
##SBATCH -w, --nodelist=
{% else %}
#SBATCH -w, --nodelist={{ node_list }}
{% endif %}
{% if node_exclude_list != 'none' %}
#SBATCH -x, --exclude={{ node_exclude_list }}
{% endif %}

mpiexec.hydra -np $SLURM_NTASKS path/to/vasp > stdout.log
```

Then, call `get_script` to render template as job script.
```python
from slurmer.script import get_script
script = get_script(
    template_file="run_slurm.sh",
    job_name="myjob",
    node_partition="g1",
    num_nodes=2,
    num_tasks=32,
    node_list=[10, 12, 15], # optional
)
print(script)
```

Now you can see output:

```bash
#!/bin/bash
#SBATCH -J myjob
#SBATCH -o myMPI.o%j       # output and error file name (%j expands to jobID)
#SBATCH -p g1
#SBATCH -N 2
#SBATCH -n 32

#SBATCH -w, --nodelist=n010,n012,n015

mpiexec.hydra -np $SLURM_NTASKS path/to/vasp > stdout.log
```
