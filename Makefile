.PHONY: setup clean

.venv:
	python3 -m venv `pwd`/.venv

setup: .venv
	. .venv/bin/activate && pip install --upgrade pip
	. .venv/bin/activate && pip install -e .
	. .venv/bin/activate && nodeenv -p
	. .venv/bin/activate && npm i -g @jakzo/aoc
	. .venv/bin/activate && pre-commit install

clean:
	/bin/rm -rf .venv
