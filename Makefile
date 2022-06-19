#run:
#	python __main__.py

# Configs
PORT=9000
APP_NAME=book-import
DOCKER_REPO=093798420628.dkr.ecr.us-east-1.amazonaws.com
AWS_CLI_REGION=us-east-1

# HELP
# This will output the help for each task
# thanks to https://marmelab.com/blog/2016/02/29/auto-documented-makefile.html
.PHONY: help

help: ## This help.
	@awk 'BEGIN {FS = ":.*?## "} /^[a-zA-Z_-]+:.*?## / {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}' $(MAKEFILE_LIST)

.DEFAULT_GOAL := help

# DOCKER TASKS
# Build the container
build: ## Build the container
	docker build -t $(APP_NAME) .

run: ## Run container on port configured in `config.env`
	docker run -p=$(PORT):8080 --name="$(APP_NAME)" $(APP_NAME):latest

build-run: build run ## Build and run

stop: ## Stop and remove a running container
	docker stop $(APP_NAME); docker rm $(APP_NAME)

release: build publish ## Make a release by building and publishing the `{version}` ans `latest` tagged containers to ECR

# Docker publish
publish: repo-login tag-latest ## Publish the `latest` tagged containers to ECR
	@echo 'publish latest to $(DOCKER_REPO)'
	docker push $(DOCKER_REPO)/$(APP_NAME):latest
	aws lambda update-function-code --function-name $(APP_NAME) --image-uri $(DOCKER_REPO)/$(APP_NAME):latest

# Docker tagging

tag-latest: ## Generate container `latest` tag
	@echo 'create tag latest'
	docker tag $(APP_NAME) $(DOCKER_REPO)/$(APP_NAME):latest

# login to AWS-ECR
repo-login: ## Auto login to AWS-ECR unsing aws-cli
	aws ecr get-login-password --region $(AWS_CLI_REGION) | docker login --username AWS --password-stdin $(DOCKER_REPO)