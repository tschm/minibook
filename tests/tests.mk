## Makefile.tests - Testing and benchmarking targets
# This file is included by the main Makefile.
# It provides targets for running the test suite with coverage and
# executing performance benchmarks.

# Declare phony targets (they don't produce files)
.PHONY: test benchmark watch

# Default directory for tests
TESTS_FOLDER := tests

##@ Development and Testing

# The 'test' target runs the complete test suite.
# 1. Cleans up any previous test results in _tests/.
# 2. Creates directories for HTML coverage and test reports.
# 3. Invokes pytest via the local virtual environment.
# 4. Generates terminal output, HTML coverage, JSON coverage, and HTML test reports.
test: install ## run all tests
	@rm -rf _tests;

	@if [ -d ${TESTS_FOLDER} ]; then \
	  mkdir -p _tests/html-coverage _tests/html-report; \
	  ${VENV}/bin/python -m pytest ${TESTS_FOLDER} --ignore=${TESTS_FOLDER}/benchmarks --cov=${SOURCE_FOLDER} --cov-report=term --cov-report=html:_tests/html-coverage --cov-report=json:_tests/coverage.json --html=_tests/html-report/report.html; \
	else \
	  printf "${YELLOW}[WARN] Test folder ${TESTS_FOLDER} not found, skipping tests${RESET}\n"; \
	fi

# The 'benchmark' target runs performance benchmarks using pytest-benchmark.
# 1. Installs pytest-benchmark dependency.
# 2. Executes benchmarks found in the benchmarks/ subfolder.
# 3. Generates JSON results in _benchmarks/ directory.
benchmark: install ## run performance benchmarks
	@if [ -d "${TESTS_FOLDER}/benchmarks" ]; then \
	  printf "${BLUE}[INFO] Running performance benchmarks...${RESET}\n"; \
	  ${UV_BIN} pip install pytest-benchmark>=5.1.0; \
	  mkdir -p _benchmarks; \
	  ${VENV}/bin/python -m pytest "${TESTS_FOLDER}/benchmarks/" \
	  		--benchmark-only \
			--benchmark-json=_benchmarks/results.json \
			--benchmark-columns=min,max,mean,stddev,rounds; \
	else \
	  printf "${YELLOW}[WARN] Benchmarks folder not found, skipping benchmarks${RESET}\n"; \
	fi

# The 'watch' target runs tests in watch mode for continuous feedback during development.
# Uses pytest-watch to automatically re-run tests when source files change.
watch: install ## run tests in watch mode (auto-rerun on file changes)
	@if [ -d ${TESTS_FOLDER} ]; then \
	  printf "${BLUE}[INFO] Starting test watch mode...${RESET}\n"; \
	  printf "${YELLOW}[INFO] Tests will auto-rerun when files change. Press Ctrl+C to stop.${RESET}\n"; \
	  ${VENV}/bin/python -m pytest_watch ${TESTS_FOLDER} --ignore=${TESTS_FOLDER}/benchmarks -- --tb=short; \
	else \
	  printf "${YELLOW}[WARN] Test folder ${TESTS_FOLDER} not found${RESET}\n"; \
	fi

