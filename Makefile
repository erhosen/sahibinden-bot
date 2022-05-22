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

deploy: clean generate_requirements
	@yc serverless function version create --folder-id=b1galdj3l4r95kd20qe0 --function-name=sahibindobot --runtime python39 --entrypoint main.handler --memory 128m --execution-timeout 25s --source-path ./sahibinden_bot

run:
	@yc serverless function invoke --folder-id=b1galdj3l4r95kd20qe0 --name=sahibindobot

generate_requirements:
	@poetry export --without-hashes -f requirements.txt > sahibinden_bot/requirements.txt

check_requirements:	generate_requirements
	@git diff --quiet sahibinden_bot/requirements.txt
