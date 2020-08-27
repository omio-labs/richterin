from enum import Enum
from functools import partial
from typing import Dict, Any

from great_expectations.dataset import SqlAlchemyDataset


def not_null(dataset: SqlAlchemyDataset, options: Dict[str, Any]):
    return dataset.expect_column_values_to_not_be_null(**options)


def is_null(dataset: SqlAlchemyDataset, options: Dict[str, Any]):
    return dataset.expect_column_values_to_be_null(**options)


def values_between(dataset: SqlAlchemyDataset, options: Dict[str, Any]):
    return dataset.expect_column_values_to_be_between(**options)


class ExpectationType(Enum):
    NOT_NULL = partial(not_null)
    NULL = partial(is_null)
    VALUES_BETWEEN = partial(values_between)
