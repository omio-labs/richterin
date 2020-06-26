package main

import (
	"testing"
	"github.com/stretchr/testify/assert"
)

func TestValidateAlwaysReturnsTrue(t *testing.T) {
	assert := assert.New(t)
	
	validateResult := validate("A Dataset")
	
	assert.True(validateResult)
}