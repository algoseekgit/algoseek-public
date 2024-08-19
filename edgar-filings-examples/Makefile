PYTHON_VERSION = 3.10
PY = python$(PYTHON_VERSION)
VENV = .venv
BIN=$(VENV)/bin

.PHONY: install
install: $(VENV)/bin/activate

$(VENV)/bin/activate: requirements.txt
	$(PY) -m venv $(VENV) && \
	$(BIN)/pip install --upgrade pip && \
	$(BIN)/pip install -r requirements.txt && \
	touch $(VENV)/bin/activate

.PHONY: run
run: $(VENV)
	. $(BIN)/activate && \
	jupyter notebook

