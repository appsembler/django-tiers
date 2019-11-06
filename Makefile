.PHONY: install-dev test


install-dev:
	@pip install --editable .

install-test-deps:
	@pip install -r test_requirements.txt

test:
	@tox

clean:
	@rm -rf .cache
	@rm -rf .tox
	@find . -name "*.pyc" -delete
	@find . -name "__pycache__" -delete

