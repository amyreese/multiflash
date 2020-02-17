build:
	python setup.py build

dev:
	python setup.py develop

setup:
	python -m pip install -Ur requirements-dev.txt
	python -m pip install -Ur requirements.txt

venv:
	python -m venv .venv
	source .venv/bin/activate && make setup dev
	echo 'run `source .venv/bin/activate` to use virtualenv'

release: lint test clean
	python setup.py sdist bdist_wheel
	python -m twine upload dist/*

format:
	python -m isort --apply --recursive multiflash setup.py
	python -m black multiflash setup.py

lint:
	python -m pylint --rcfile .pylint multiflash setup.py
	python -m isort --diff --recursive multiflash setup.py
	python -m black --check multiflash setup.py

test:
	python -m coverage run -m multiflash.tests
	python -m coverage report
	python -m mypy multiflash

app:
	python3 -m PyInstaller --name Multiflash --noconfirm --windowed scripts/run.py

clean:
	rm -rf build dist README MANIFEST *.egg-info
