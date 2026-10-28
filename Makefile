# Сборка не требуется: команды запуска эмулятора, тестов и демонстраций.

.PHONY: run test demo clean

PYTHON ?= python3
STAGE ?= 5
VFS ?=
PROMPT ?=
SCRIPT ?=

ARGS := $(if $(VFS),--vfs $(VFS),) $(if $(PROMPT),--prompt "$(PROMPT)",) \
        $(if $(SCRIPT),--script $(SCRIPT),)

run:
	$(PYTHON) -m src.stage$(STAGE) $(ARGS)

test:
	$(PYTHON) -m pytest -v

demo:
	sh scripts/test_stages.sh

clean:
	find . -type d -name __pycache__ -exec rm -rf {} +
	rm -rf .pytest_cache htmlcov .coverage
