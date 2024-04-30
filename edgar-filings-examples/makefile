PYTHON_VERSION = 3.10
PY = python$(PYTHON_VERSION)
VENV = .venv
BIN=$(VENV)/bin

.PHONY: install
install: $(VENV)
	$(VENV): requirements.txt
	$(PY) -m venv $(VENV) && \
	$(BIN)/pip install --upgrade pip && \
	$(BIN)/pip install -r requirements.txt && \
	touch $(VENV)


.PHONY: run
run: $(VENV)
	. $(BIN)/activate && \
	jupyter notebook


.PHONY: format
format: $(VENV)
	. $(BIN)/activate && \
	$(BIN)/ruff check src --fix-only --line-length 120 && \
	$(BIN)/ruff format src --line-length 120

