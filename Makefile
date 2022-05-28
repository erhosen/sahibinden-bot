clean:
	@rm -rf build dist .eggs *.egg-info
	@rm -rf .coverage coverage.xml htmlcov report.xml .tox
	@find . -type d -name '.mypy_cache' -exec rm -rf {} +
	@find . -type d -name '__pycache__' -exec rm -rf {} +
	@find . -type d -name '*pytest_cache*' -exec rm -rf {} +
	@find . -type d -name "tmp" -exec rm -rf {} +
	@find . -type f -name "*.session" -exec rm -rf {} +
	@find . -type f -name "*.py[co]" -exec rm -rf {} +

format: clean
	@pre-commit run --all-files

generate_requirements:
	@poetry export --without-hashes -f requirements.txt > sahibinden_bot/requirements.txt

check_requirements:	generate_requirements
	@git diff --quiet sahibinden_bot/requirements.txt
