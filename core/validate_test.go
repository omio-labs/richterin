package main

import (
	"github.com/stretchr/testify/assert"
	"testing"
)

func TestValidateAlwaysReturnsTrue(t *testing.T) {
	assert := assert.New(t)

	validateResult := validate("A Dataset")

	assert.True(validateResult)
}
