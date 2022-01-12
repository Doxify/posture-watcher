NAME = "PostureWatcher"
VENV = venv
DIST = dist
PYTHON = $(VENV)/bin/python3
PIP = $(VENV)/bin/pip
.PHONY: run build clean

run: $(VENV)/bin/activate
	$(PYTHON) src/app.py

test: $(VENV)/bin/activate
	$(PYTHON) -m unittest discover -s "tests" -p "*_test.py"

build: $(VENV)/bin/activate
	make clean
	$(PIP) install -r requirements.txt
	$(PYTHON) setup.py py2app

open/macos:
	open  ./$(DIST)/$(NAME).app/Contents/MacOS/$(NAME)

setup: requirements.txt
	pip install --upgrade pip
	pip install -r requirements.txt

venv/bin/activate: requirements.txt
	python3 -m venv $(VENV)
	$(PIP) install -r requirements.txt

clean:
	rm -rf __pycache__
	rm -rf build
	rm -rf dist
	rm -rf .eggs
