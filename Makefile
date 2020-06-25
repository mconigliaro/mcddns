VERSION := $(shell python -c 'import mcddns.meta; print(mcddns.meta.VERSION)')

release:
	git tag "$(VERSION)"
	git push --tags

	# https://packaging.python.org/tutorials/packaging-projects/
	rm -rf build dist ./*.egg-info
	./setup.py sdist bdist_wheel
	twine upload dist/*
