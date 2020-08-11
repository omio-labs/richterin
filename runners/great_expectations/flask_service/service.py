import logging

from flask import request, Flask, jsonify

from runners.great_expectations.job_config import JobConfigSchema, JobConfig
from runners.great_expectations.runner import GERunner

ge_runner_service = Flask(__name__)
ge_runner_service.config["DEBUG"] = True

ge_runner = GERunner()


@ge_runner_service.route('/runner/great-expectations/submit-job', methods=['POST'])
def submit_ge_job():
    try:
        job_config_dict = request.get_json()
        job_config: JobConfig = JobConfigSchema().load(job_config_dict)
        logging.info("Received job config for GE: {}".format(job_config))
        result = ge_runner.run(job_config)
    except Exception as e:
        # TODO: Return meaningful error responses
        return jsonify(error=str(e)), 500
    return result


ge_runner_service.run()
