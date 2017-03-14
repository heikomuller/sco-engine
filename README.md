# Standard Cortical Observer - Predictive Model Workflow Engine and Worker

The workflow engine is used to run predictive models for experiments that are defined in the SCO Data Store. The classes in this package define client interfaces to the engine. The actual workflow is executed by workers that are defined in the workflow module. These workers may run locally on the same machine as the engine client (and the web server) or on remote machines.

The SCO Engine package is intended to decouple the web server code from the predictive model code.

The default engine uses RabbitMQ to communicate between the client and the worker. This configuration is intended for scalability as it makes it easy to have multiple workers running (on different machines).

Implementation of workers is moved to separate packages.

## Instalation

The easiest way to install the SCO engine package is by using `pip install sco-engine`. Alternatively, you can clone the package on [GitHub](https://github.com/heikomuller/sco-engine)  and run `python setup.py install` in the project home directory.
