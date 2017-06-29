import json
from pymongo import MongoClient
import unittest

import scodata.mongo as mongo
import scoengine as engine
from scoengine.model import ModelOutputs

MODELS_FILE = './data/models.json'

class TestModelRegistryMethods(unittest.TestCase):

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

    def test_delete_models(self):
        """Test creation of model objects."""
        # Create model from Json document
        count = 0
        models = []
        for i in range(len(self.models)):
            model = self.engine.registry.from_json(self.models[i])
            self.engine.register_model(
                model.identifier,
                model.properties,
                model.parameters,
                model.outputs,
                model.connector
            )
            count += 1
            models.append(model.identifier)
        # Make sure that we can get all the models
        for id in models:
            self.assertIsNotNone(self.engine.get_model(id))
        # Delete unknown model should return False
        self.assertIsNone(self.engine.delete_model('unknown model'))
        # Delete one model after the other
        while count > 0:
            self.assertIsNotNone(self.engine.delete_model(models[count - 1]))
            count -= 1
            listing = self.engine.list_models()
            self.assertEqual(len(listing.items), count)
            self.assertEqual(listing.total_count, count)
            self.assertIsNone(self.engine.get_model(models[count]))
	# We need to be able to register a model with the same
	# identifier as a previously registered one
       	for i in range(len(self.models)):
     	    model = self.engine.registry.from_json(self.models[i])
            self.engine.register_model(
                model.identifier,
                model.properties,
                model.parameters,
                model.outputs,
                model.connector
            )

    def test_list_models(self):
        """Test creation of model objects."""
        # Create model from Json document
        count = 0
        for i in range(len(self.models)):
            model = self.engine.registry.from_json(self.models[i])
            self.engine.register_model(
                model.identifier,
                model.properties,
                model.parameters,
                model.outputs,
                model.connector
            )
            count += 1
        listing = self.engine.list_models()
        self.assertEqual(len(listing.items), count)
        self.assertEqual(listing.total_count, count)

    def test_register_model(self):
        """Test creation of model objects."""
        # Create model from Json document
        for i in range(len(self.models)):
            model = self.engine.registry.from_json(self.models[i])
            # Insert model
            m = self.engine.register_model(
                model.identifier,
                model.properties,
                model.parameters,
                model.outputs,
                model.connector
            )
            # Assert that identifier and name
            self.assertEqual(m.identifier, model.identifier)
            self.assertEqual(m.name, model.name)
            # Get model
            m = self.engine.get_model(model.identifier)
            # Assert that identifier and name are the same
            self.assertEqual(m.identifier, model.identifier)
            self.assertEqual(m.name, model.name)
        # Create duplicate model should raise ValueError
        for i in range(len(self.models)):
            model = self.engine.registry.from_json(self.models[i])
            # Insert model
            with self.assertRaises(ValueError):
                m = self.engine.register_model(
                    model.identifier,
                    model.properties,
                    model.parameters,
                    model.outputs,
                    model.connector
                )
        # Register model with empty connector should raise ValueError
        model = self.engine.registry.from_json(self.models[0])
        with self.assertRaises(ValueError):
            m = self.engine.register_model(
                model.identifier,
                model.properties,
                model.parameters,
                model.outputs,
                {}
            )
        # Register model with unknown connector should raise ValueError
        with self.assertRaises(ValueError):
            m = self.engine.register_model(
                model.identifier,
                model.properties,
                model.parameters,
                model.outputs,
                {'connector' : 'unknown'}
            )
        # Register model with duplicate attachments should raise a ValueError
        with self.assertRaises(ValueError):
            m = self.engine.register_model(
                model.identifier,
                model.properties,
                model.parameters,
                ModelOutputs(
                    model.outputs.prediction_filename,
                    model.outputs.attachments + model.outputs.attachments
                ),
                {'connector' : 'unknown'}
            )

    def test_upsert_model_properties(self):
        """Test creation of model objects."""
        # Register a model
        model = self.engine.registry.from_json(self.models[0])
        self.engine.register_model(
            model.identifier,
            {'name' : 'Some name'},
            model.parameters,
            model.outputs,
            model.connector
        )
        m = self.engine.get_model(model.identifier)
        self.assertEqual(m.properties['name'], 'Some name')
        # Update the name
        self.engine.upsert_model_properties(
            model.identifier,
            {'name' : 'Another name', 'p2' : 'nothing'}
        )
        m = self.engine.get_model(model.identifier)
        self.assertEqual(m.properties['name'], 'Another name')
        self.assertEqual(m.properties['p2'], 'nothing')


if __name__ == '__main__':
    unittest.main()
