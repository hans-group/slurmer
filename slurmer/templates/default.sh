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

{{ exec_command }} > stdout.log