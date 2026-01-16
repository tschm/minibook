## Makefile (repo-owned)
# Keep this file small. It can be edited without breaking template sync.

# Always include the Rhiza API (template-managed)
include .rhiza/rhiza.mk

# Optional: developer-local extensions (not committed)
-include local.mk

##@ Quick Development

.PHONY: quick-test watch typecheck

quick-test: ## Run tests fast (stop on first failure, short traceback)
	@${VENV}/bin/python -m pytest tests/ -x --tb=short -q

watch: ## Run tests in watch mode (auto-rerun on changes)
	@${VENV}/bin/python -m pytest_watch tests/ -- -x --tb=short

typecheck: ## Run mypy type checker
	@${VENV}/bin/python -m mypy src/minibook/ --ignore-missing-imports
