init:
	pip install -r requirements.txt

test:
	nosetests tests
run:
	python visual-novel/__init__.py
clean:
	rm -rf __pycache__