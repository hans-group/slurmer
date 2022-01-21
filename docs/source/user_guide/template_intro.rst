Introduction to Template
========================

Brief introduction to ``jinja`` template
----------------------------------------

``jinja`` provides template syntax for easy creation of document with template. The variables in template are placed within two curly brackets.

For example, let`s consider a simple text file (``hello.txt``).

.. code-block::

    Hello, my name is {{ name }}.


Here, the placeholder variable is ``name``. To substitute ``name`` to real value, ``jinja`` does:

.. code-block:: python

    >>> template = env.get_template("hello.txt")
    >>> rendered = template.render(name=Minjoon)
    >>> print(rendered)
    Hello, my name is Minjoon.

See the `official documentation <https://jinja.palletsprojects.com/en/3.0.x/templates/>`_ for more detail.

Slurm job script template format
--------------------------------

``slurmer`` uses ``jinja`` template language to manage templates for the job scripts.
The job script can be crated and managed with ``SlurmJob`` object, which will be discussed in the section **Creating and Submitting a Job**.
The template for slurm job script looks like following:

.. code-block:: bash

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

    # commands goes here...

Here, the placeholder variables are:

- ``job_name`` is the name of job
- ``node_partition`` is the partition of node, depending on your organization's slurm configuration.
- ``num_nodes`` is the number of nodes to use in a batch job.
- ``num_tasks`` is the number of tasks(threads) to use in a batch job.
- ``node_list`` is the list of nodes to use in a batch job.
- ``node_exclude_list`` is the string which represents the nodes to exclude. (see slurm documentation)

These 6 variables are required fields for constructing ``SlurmJob`` object. User can add additional variables to the template.


Explaining the structure of ``default.sh``
------------------------------------------

The template file ``default.sh``:

.. code-block:: bash

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

Note that this template has one additional variable ``exec_command``. By using it, user can execute arbitrary command with this template.
