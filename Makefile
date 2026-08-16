.PHONY: install test evaluate baseline run

install:
	python -m pip install -e '.[api]'

test:
	python -m unittest discover -s tests -v

evaluate:
	infraguard evaluate

baseline:
	python scripts/generate_baseline.py

run:
	uvicorn infraguard.api:app --reload
