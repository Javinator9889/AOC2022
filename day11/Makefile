PY=python

bfs:
	$(PY) setup.py build_ext --inplace

%: bfs

.PHONY: clean

clean:
	rm -rf *.so *.html *.cpp build/
