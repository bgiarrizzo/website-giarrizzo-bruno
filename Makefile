.DEFAULT_GOAL := help

help:
	@grep -E '(^[a-zA-Z0-9_-]+:.*?##)|(^##)' $(firstword $(MAKEFILE_LIST)) | awk 'BEGIN {FS = ":.*?## "; printf "Usage: make \033[32m<target>\033[0m\n"}{printf "\033[32m%-20s\033[0m %s\n", $$1, $$2}' | sed -e 's/\[32m## /\n[33m/'

.PHONY: build
build: ## Build the project
	@rm -rf build/
	@mkdir -p build
	@cp -r src/* build/
	@rm -rf src/stats/

.PHONY: serve
serve: build ## Serve the project locally
	@echo "Serving project at http://localhost:8000"
	python3 -m http.server 8000 --directory build