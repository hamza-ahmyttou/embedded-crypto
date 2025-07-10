test-all:
	#coverage erase --data-file=output/.coverage
	rm -rf output
	mkdir output
	coverage run --source=samples --data-file=output/.coverage -m unittest discover tests
	coverage report --data-file=output/.coverage
	coverage html --data-file=output/.coverage -d output/coverage_report

install:
	pip install PyHamcrest
	pip install coverage
	pip install sympy pytest flake8
	pip install pyasn1 pyasn1-modules
