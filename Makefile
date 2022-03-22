init:
	pip install .
deps:
	pip install -r requirements.txt
test:
	python tests/basic.test.py
run:
	python visual_novel/
clean:
	rm -rf __pycache__