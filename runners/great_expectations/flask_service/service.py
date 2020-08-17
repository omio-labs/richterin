from flask import request, Flask, jsonify

from job_config import JobConfigSchema, JobConfig
from runner import GERunner

ge_runner_service = Flask(__name__)
ge_runner_service.config.from_envvar('GE_SERVICE_SETTINGS')
ge_runner = GERunner(ge_runner_service.config)


@ge_runner_service.route('/runner/great-expectations/submit-job', methods=['POST'])
def submit_ge_job():
    try:
        job_config_dict = request.get_json()
        job_config: JobConfig = JobConfigSchema().load(job_config_dict)
        ge_runner_service.logger.info("Received job config for GE: {}".format(job_config))
        # TODO: Add websocket/async support?
        result = ge_runner.run(job_config)
    except Exception as e:
        # TODO: Return meaningful error responses
        return jsonify(error=str(e)), 500
    return result


ge_runner_service.run()
