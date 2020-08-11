import os

from great_expectations.dataset import SqlAlchemyDataset
from sqlalchemy import create_engine

from runners.great_expectations.job_config import *

DEFAULT_GE_RESULT_FORMAT = "SUMMARY"


class GERunner:
    def __init__(self):
        # TODO: Get properties through service/configuration file
        project_id = os.getenv('GCP_PROJECT_ID')
        temp_table_dataset = os.getenv('BIGQUERY_TEMP_TABLE_DATASET')
        if project_id is None or temp_table_dataset is None:
            raise Exception("Please set Env, variables")
        self.bq_engine = create_engine('bigquery://' + project_id + '/' + temp_table_dataset)

    def run(self, config: JobConfig):
        is_sql_based = False if config.transformation is None else True
        if not is_sql_based:
            name, dataset = config.datasets.popitem()
            bq_instances: List[BigQueryInstance] = list(
                filter(lambda x: x.type == DatasetType.BIGQUERY, dataset.instances))
            if not bq_instances:
                raise Exception("No BigQuery instances found")
            table_name = bq_instances.pop().table
            dataset = SqlAlchemyDataset(table_name=table_name, engine=self.bq_engine)
            expectation = config.expectation
            basic_options = {'column': expectation.column_name, 'mostly': expectation.threshold_percent * 0.01,
                             'result_format': DEFAULT_GE_RESULT_FORMAT}
            expectation_function = expectation.type.value
            result = expectation_function(dataset, {**basic_options, **expectation.properties})
            return result.to_json_dict()
        else:
            # TODO: SQL Execution
            raise Exception("SQL not yet supported")

