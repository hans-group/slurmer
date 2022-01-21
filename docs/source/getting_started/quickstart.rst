Quickstart
==========

In this tutorial, you can create simple job ``echo Hello,world!``.
For creating job script, ``default.sh`` template will be used, which is shipped with package by default.

The list of templates available can be shown by running the code below.

.. code-block:: python

    >>> import slurmer
    >>> slurmer.list_templates()
    directory: {path_to_site-packages}/slurmer/templates file: default.sh

Currently, ``default.sh`` template is the only template available.

Creating ``SlurmJob`` object
----------------------------

Create a new ``SlurmJob`` object to prepare a batch job.

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

Submitting batch job 
----------------------------

To submit job:

.. code-block:: python

    job.submit()
