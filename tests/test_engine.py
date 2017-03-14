"""Test SCO Engine -

There is not much to test here without a worker. Basically used to test if allows
classes compile.
"""

import unittest

from scoengine import EngineException
from scoengine import DefaultSCOEngineClient,  RabbitMQClient
from scoengine import ModelRunRequest, RequestFactory

class DummyReferenceFactory(object):
    """Dummy reference factory for model run Urls to avoid that we have to
    import the SCO server package.
    """
    def experiments_prediction_reference(self, run_id, experiment_id):
        return run_id + ':' + experiment_id


class ModelRunHandle(object):
    """Dummy model run handle."""
    def __init__(self, identifier, experiment):
        self.identifier = identifier
        self.experiment = experiment


class TestSCOEngine(unittest.TestCase):
    """Test teh SCO engine. Make sure we can instantiate all classes. Any
    communication attempt will fail because of missing environment.
    """
    def test_request_factory(self):
        """Test encoding and decoding model run requests."""
        # Create request factory instance
        request_factory = RequestFactory(DummyReferenceFactory())
        req = request_factory.get_request(ModelRunHandle('ID', 'EXPERIMENT'))
        json_obj = req.to_json()
        # Ensure that all elements in the Json requst object are set as expected
        self.assertEquals(json_obj['run_id'], 'ID')
        self.assertEquals(json_obj['experiment_id'], 'EXPERIMENT')
        self.assertEquals(json_obj['href'], 'EXPERIMENT:ID')
        # Convert Json request into model run request
        mr = ModelRunRequest.from_json(json_obj)
        self.assertEquals(mr.run_id, 'ID')
        self.assertEquals(mr.experiment_id, 'EXPERIMENT')
        self.assertEquals(mr.resource_url, 'EXPERIMENT:ID')

    def test_rabbitmq_client(self):
        """Test if we can instantiate the RabbitMQ client."""
        # Create RabbitMQ engine client
        client = RabbitMQClient('dummy', 'dummy', DummyReferenceFactory())
        # Run Model request. Expect EngineException due to missing enviroment.
        with self.assertRaises(EngineException):
            client.run_model(ModelRunHandle('ID', 'EXPERIMENT'))

    def test_socket_client(self):
        """Test if we can instantiate the socket IO client."""
        # Create RabbitMQ engine client
        client = DefaultSCOEngineClient('localhost', 8080, DummyReferenceFactory())
        # Run Model request. Expect EngineException due to missing enviroment.
        with self.assertRaises(EngineException):
            client.run_model(ModelRunHandle('ID', 'EXPERIMENT'))

if __name__ == '__main__':
    unittest.main()
