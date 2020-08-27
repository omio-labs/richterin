import unittest
import os
import json

from marshmallow import ValidationError

from expectations import ExpectationType
from job_config import JobConfigSchema, JobConfig, DatasetType

RESOURCES_PATH = os.path.join(os.path.dirname(__file__), 'resources', 'job_input')


class JobConfigTest(unittest.TestCase):

    def test_invalid(self):
        with open(os.path.join(RESOURCES_PATH, "invalid-input.json"), "r") as config:
            job_config_dict = json.loads(config.read())
        with self.assertRaises(ValidationError):
            JobConfigSchema().load(job_config_dict)

    def test_valid_no_optionals(self):
        with open(os.path.join(RESOURCES_PATH, "valid-input-no-optionals.json"), "r") as config:
            job_config_dict = json.loads(config.read())
        job_config: JobConfig = JobConfigSchema().load(job_config_dict)
        self.assertEqual(1, len(job_config.datasets))
        self.assertEqual(ExpectationType.NOT_NULL, job_config.expectation.type)

    def test_valid_all(self):
        with open(os.path.join(RESOURCES_PATH, "valid-input.json"), "r") as config:
            job_config_dict = json.loads(config.read())
        job_config: JobConfig = JobConfigSchema().load(job_config_dict)
        self.assertEqual(2, len(job_config.datasets))
        self.assertEqual(ExpectationType.NOT_NULL, job_config.expectation.type)


if __name__ == '__main__':
    unittest.main()
