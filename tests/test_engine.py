"""Test SCO Engine -

There is not much to test here without a worker. Basically used to test if allows
classes compile.
"""

import json
from pymongo import MongoClient
import unittest

from scodata.modelrun import ModelRunHandle, ModelRunIdle
import scodata.mongo as mongo
import scoengine as engine

MODELS_FILE = './data/models.json'

class TestSCOEngine(unittest.TestCase):
    """Test the SCO engine. Here we only test behaviour in error situations."""

    def setUp(self):
        """Connect to MongoDB and clear an existing model collection.
        Create model regisrty manager"""
        # Read model definitions
        with open(MODELS_FILE, 'r') as f:
            self.models = json.load(f)
        m = mongo.MongoDBFactory(db_name='test_sco')
        db = m.get_database()
        db.models.drop()
        self.engine = engine.SCOEngine(m)

    def tearDown(self):
        """Delete data store directory and database."""
        MongoClient().drop_database('test_sco')

    def test_run_model(self):
        """Test encoding and decoding model run requests."""
        # Register a model
        model = self.engine.registry.from_json(self.models[0])
        self.engine.register_model(
            model.identifier,
            model.properties,
            model.parameters,
            model.outputs,
            model.connector
        )
        # Run prediction for unknown model
        with self.assertRaises(ValueError):
            self.engine.run_model(
                ModelRunHandle(
                    'fake_id',
                    {'name':'My Run'},
                    '',
                    ModelRunIdle(),
                    'experiment_id',
                    'unknown model',
                    {}
                ),
                'some url'
            )
        # Run prediction for known model but with invalid connection parameters
        with self.assertRaises(engine.EngineException):
            self.engine.run_model(
                ModelRunHandle(
                    'fake_id',
                    {'name':'My Run'},
                    '',
                    ModelRunIdle(),
                    'experiment_id',
                    model.identifier,
                    {}
                ),
                'some url'
            )

if __name__ == '__main__':
    unittest.main()
