NAME = "PostureWatcher"
VENV = venv
DIST = dist
PYTHON = $(VENV)/bin/python3
PIP = $(VENV)/bin/pip
.PHONY: run build clean

run: $(VENV)/bin/activate
	$(PYTHON) app.py

build: $(VENV)/bin/activate
	make clean
	$(PIP) install -r requirements.txt
	$(PYTHON) setup.py py2app

open/macos:
	open  ./$(DIST)/app.app/Contents/MacOS/app

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
