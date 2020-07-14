package main

type Rule struct {
	Id, Description string
	Datasets        []string
	Transformation  Transformation
	Expectations    []Expectation
	Timeframe       Timeframe
}

type Transformation struct {
	Type, Query string
}

type Expectation struct {
	Type, ColumnName, Runner, Severity string
	ThresholdPercent                   int
}

type Timeframe struct {
	Years, Months, Days int
}
