PYTHON      = python3
PIP         = pip
VENV        = .venv
BIN         = $(VENV)/bin

MAIN        = a_maze_ing.py
CONFIG      = config.txt

FLAKE8      = flake8
MYPY        = mypy

MYPY_FLAGS  = --warn-return-any \
              --warn-unused-ignores \
              --ignore-missing-imports \
              --disallow-untyped-defs \
              --check-untyped-defs

.PHONY: install build run debug clean lint lint-strict

install:
	$(PYTHON) -m venv $(VENV)
	$(BIN)/$(PIP) install --upgrade pip
	$(BIN)/$(PIP) install flake8 mypy mlx-2.2-py3-none-any.whl setuptools wheel
	@if [ -f requirements.txt ]; then $(BIN)/$(PIP) install -r requirements.txt; fi

# mazegen package
build:
	$(BIN)/$(PYTHON) setup.py sdist bdist_wheel
	mv dist/*.whl .
	mv dist/*.tar.gz .
	rm -rf dist build *.egg-info

run:
	$(BIN)/$(PYTHON) $(MAIN) $(CONFIG)

debug:
	$(BIN)/$(PYTHON) -m pdb $(MAIN) $(CONFIG)

clean:
	rm -rf $(VENV)
	rm -rf .mypy_cache
	rm -rf build dist *.egg-info
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete

lint:
	$(BIN)/$(FLAKE8) . --exclude=$(VENV)
	$(BIN)/$(MYPY) . --exclude $(VENV) $(MYPY_FLAGS)

lint-strict:
	$(BIN)/$(FLAKE8) . --exclude=$(VENV)
	$(BIN)/$(MYPY) . --exclude $(VENV) --strict