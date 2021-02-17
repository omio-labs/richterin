package models

import (
	"encoding/json"
	"github.com/stretchr/testify/assert"
	"testing"
)

func TestExpecationTemplateMarshal(t *testing.T) {
	assert := assert.New(t)

	expectationTemplateJson := `{
    "id": "NOT_NULL",
    "name": "Column is not null",
    "level": "record",
    "runners": ["GREAT_EXPECTATIONS", "DATAPROC_SPARK"]
  }`

	var expectationTemplate ExpectationTemplate

	json.Unmarshal([]byte(expectationTemplateJson), &expectationTemplate)

	assert.Equal("NOT_NULL", expectationTemplate.Id, "ID should be Unmarshaled correctly")
	assert.Equal("Column is not null", expectationTemplate.Name, "Name should be Unmarshaled correctly")
}
