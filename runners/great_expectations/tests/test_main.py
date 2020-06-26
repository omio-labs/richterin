from main import validate

def test_validate_always_returns_true():
	assert validate("A Dataset") == True