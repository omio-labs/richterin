package models

type ExpectationTemplate struct {
	Id, Name, Level string
	Runners         []string
}
