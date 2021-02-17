package main

import (
	"encoding/json"
	"github.com/stretchr/testify/assert"
	"testing"
)

func TestRuleUnmarshal(t *testing.T) {
	assert := assert.New(t)

	ruleJson := `{
    "id": "RULE1",
    "description": "Every Journey must contain a valid search",
    "datasets": ["searches", "journeys"],
    "transformation": {
      "type": "SQL_QUERY",
      "query": "SELECT * FROM {{ journeys }} LEFT JOIN {{ searches }} where search_id = search_id"
    },
    "expectations": [
      {
        "type": "NOT_NULL",
        "columnName": "search_id",
        "thresholdPercent": 90,
        "runner": "GREAT_EXPECTATIONS",
        "severity": "WARNING"
      }
    ],
    "timeframe": {
      "months": 1
    }
  }`

	var rule Rule

	json.Unmarshal([]byte(ruleJson), &rule)

	assert.Equal("RULE1", rule.Id, "ID should be Unmarshaled correctly")
	assert.Equal("Every Journey must contain a valid search", rule.Description, "Description should be Unmarshaled correctly")
	assert.Equal([]string{"searches", "journeys"}, rule.Datasets, "Datasets should be Unmarshaled correctly")
	assert.Equal(&Timeframe{Months: 1, Years: 0, Days: 0}, &rule.Timeframe, "Timeframe should be Unmarshaled correctly")
	assert.Equal([]Expectation{{Type: "NOT_NULL", ColumnName: "search_id", ThresholdPercent: 90, Runner: "GREAT_EXPECTATIONS", Severity: "WARNING"}}, rule.Expectations, "Expectations should be Unmarshaled correctly")
	assert.Equal(Transformation{Type: "SQL_QUERY", Query: "SELECT * FROM {{ journeys }} LEFT JOIN {{ searches }} where search_id = search_id"}, rule.Transformation, "Transformation should be Unmarshaled correctly")
}
