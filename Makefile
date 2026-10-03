# Makefile для эмулятора командной строки

.PHONY: run test clean

# Параметры по умолчанию
STAGE ?= 1
VFS ?=
PROMPT ?=
SCRIPT ?=

# Формирование аргументов
ARGS := $(if $(VFS),--vfs $(VFS),) $(if $(PROMPT),--prompt "$(PROMPT)",) $(if $(SCRIPT),--script $(SCRIPT),)

run:
	python -m src.stage$(STAGE) $(ARGS)

test:
	pytest tests/ -v

clean:
	find . -type d -name __pycache__ -exec rm -rf {} +
	rm -rf .pytest_cache htmlcov .coverage
