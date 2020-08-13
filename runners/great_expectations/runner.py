from great_expectations.dataset import SqlAlchemyDataset
from jinja2 import Template
from sqlalchemy import create_engine

from runners.great_expectations.job_config import *

DEFAULT_GE_RESULT_FORMAT = "SUMMARY"


class GERunner:
    def __init__(self, config: Dict[str, str]):
        credentials_path = config.get('GOOGLE_APPLICATION_CREDENTIALS')
        project_id = config.get('GCP_PROJECT_ID')
        temp_table_dataset = config.get('BIGQUERY_TEMP_TABLE_DATASET')
        if project_id is None or temp_table_dataset is None or credentials_path is None:
            raise Exception("Invalid configuration(s) provided. Please check the configuration set-up.")
        self.bq_engine = create_engine('bigquery://' + project_id + '/' + temp_table_dataset,
                                       credentials_path=credentials_path)

    @staticmethod
    def __filter_dataset_instance(dataset: Dataset, dataset_type: DatasetType):
        filtered_instances = filter(lambda instance: instance.type == dataset_type, dataset.instances)
        if not filtered_instances:
            raise Exception("No {} instances found".format(dataset_type))
        return next(filtered_instances)

    def __run_expectation_bigquery(self, expectation: Expectation, table_name: Optional[str] = None,
                                   sql: Optional[str] = None):
        if sql is None:
            dataset = SqlAlchemyDataset(table_name=table_name, engine=self.bq_engine)
        else:
            dataset = SqlAlchemyDataset(custom_sql=sql, engine=self.bq_engine)
        basic_options = {'mostly': expectation.threshold_percent * 0.01, 'result_format': DEFAULT_GE_RESULT_FORMAT}
        expectation_function = expectation.type.value
        result = expectation_function(dataset, {**basic_options, **expectation.parameters})
        return result

    def run(self, config: JobConfig):
        """
        Executes the provided JobConfig using Great Expectations
        :param config: JobConfig which has the Dataset(s) and its data expectation configured
        :return: Execution results as Json
        """
        is_sql_based = False if config.transformation is None else True
        if not is_sql_based:
            name, dataset = config.datasets.popitem()
            table_name = self.__filter_dataset_instance(dataset, DatasetType.BIGQUERY).table
            result = self.__run_expectation_bigquery(config.expectation, table_name=table_name)
        else:
            substitutions = {}
            for name, dataset in config.datasets.items():
                table_name = self.__filter_dataset_instance(dataset, DatasetType.BIGQUERY).table
                substitutions[name] = table_name
            sql_query_template = Template(config.transformation.query)
            sql = sql_query_template.render(**substitutions)
            result = self.__run_expectation_bigquery(config.expectation, sql=sql)
        return result.to_json_dict()
