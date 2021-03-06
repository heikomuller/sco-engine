# Standard Cortical Observer Workflow Engine - Changelog

### 0.1.0 - 2017-03-13

* Initial Version

### 0.1.1 - 2017-03-16

* Bug-fix in ModelRunRequest.from_json()

### 0.1.2 - 2017-05-18

* Added export_sco_parameters.py to create description of registered SCO models and image group parameters
* Adjust to changes in SCO Data Store (0.5.0)

### 0.2.0 - 2017-06-28

* Add model registry to engine (merge from sco-models)

### 0.2.1 - 2017.06-30

* Add model description property

### 0.2.2 - 2017.06-30

* Fix bug (missing init parameter for EngineException)

### 0.3.0 - 2017-07-01

* Add update connector API call
* Rename to_json/from_json to to_dict/from_dict
* Updated unit tests to API changes

### 0.3.1 - 2017-07-01

* Add buffered RabbitMQ connector to avoid ConnectionClosed exceptions
* Add worker for request buffer

### 0.3.2 - 2017-07-02

* Replace is_model property of model resources with type according to changes in sco-datastore
* Change description of model attachments by adding a path property that contains the path to an attachment in the model output directory.
* Rename prediction_filename to prediction_file in ModelOutputs and change type to ModelOutputFile (instead of string) to allow prediction results to be in sub-folders of the model run output directory
