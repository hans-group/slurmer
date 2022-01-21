Creating and Submitting a Job
=============================

Creating ``SlurmJob`` object
----------------------------

``SlurmJob`` is a class to manage SLURM job.

Required arguments for initiating ``SlurmJob`` object:

- ``workdir``: Working directory for the job.
- ``template_file``: The name of template file(not full path) to use. Available templates are listed in ``slurmer.list_templates()``
- ``job_name``, ``node_partition``, ``num_nodes``, ``num_tasks``

Optional arguments:

- ``node_list``: List of nodes to use in a batch job. It corresponds to ``--nodelist`` option in ``srun`` and ``sbatch``
- ``node_exclude list``: List of nodes to exclude in a batch job. It corresponds to ``--exclude`` option in ``srun`` and ``sbatch``
- These two options cannot be used together.

Any additional keyword arguments will be used to substituting placeholder variables in user template, thus enabling the creation of arbitrary template.
Here is an example:

.. code-block:: python

    from slurmer.job import SlurmJob


    job = SlurmJob(
        workdir="my_job",
        template_file="default.sh",
        job_name="my_slurm_job",
        node_partition="g1",              # example.
        num_nodes=2,                      
        num_tasks=32,
        node_list=[1, 2],
        exec_command="echo Hello,world!", # optional, but this is required by default.sh
    )

Submitting the job
------------------

To submit the batch job, call ``submit()`` method.

.. code-block:: python

    job.submit()

By default, the job script is temporarily created and won't be written to the working directory. 
However, you can persist it with optional argument ``write_job_script``. To write the job script in the file system:

.. code-block:: python

    job.submit(write_job_script=True, job_script_name="my_slurm_job.sh")
