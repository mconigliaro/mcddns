VERSION := $(shell python -c 'import updatemyip.meta; print(updatemyip.meta.VERSION)')

release:
	git tag "$(VERSION)"
	git push --tags

	# https://packaging.python.org/tutorials/packaging-projects/
	rm -rf build dist ./*.egg-info
	./setup.py sdist bdist_wheel
	twine upload dist/*
