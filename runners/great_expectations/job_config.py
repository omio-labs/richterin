from dataclasses import dataclass, field
from enum import Enum
from typing import List, Dict, Optional, Any

import marshmallow_dataclass
from marshmallow.validate import Range, Equal, ContainsNoneOf, Length

from runners.great_expectations.expectations import ExpectationType


@dataclass
class DatasetType(Enum):
    BIGQUERY = 1


@dataclass
class DatasetInstance:
    type: DatasetType


@dataclass
class BigQueryInstance(DatasetInstance):
    table: str = field(metadata={"validate": ContainsNoneOf([""])})


@dataclass
class Dataset:
    id: str
    schema: str
    instances: List[BigQueryInstance]


@dataclass
class Expectation:
    type: ExpectationType
    parameters: Dict[str, Any]
    threshold_percent: float = field(metadata={"validate": Range(min=0.0, max=100.0)})
    runner: str
    severity: str


@dataclass
class SQLTransformation:
    type: str = field(metadata={"validate": Equal("SQL")})
    query: str = field(metadata={"validate": ContainsNoneOf([""])})


@dataclass
class Timeframe:
    months: int
    column: str


@dataclass
class JobConfig:
    datasets: Dict[str, Dataset] = field(metadata={"validate": Length(min=1)})
    transformation: Optional[SQLTransformation]
    expectation: Expectation
    timeframe: Optional[Timeframe]


JobConfigSchema = marshmallow_dataclass.class_schema(JobConfig)
