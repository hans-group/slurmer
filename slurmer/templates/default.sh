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

module purge
module add Compiler/Intel/18.0.5
module add MKL/2018.5.274
module add MPI/intel/2018.4.274

{{ exec_command }} > stdout.log