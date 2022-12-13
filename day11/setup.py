import numpy as np
from Cython.Build import cythonize
from setuptools import setup

setup(
    ext_modules=cythonize(
        "bfs.pyx",
        compiler_directives={
            "language_level": 3,
            "infer_types": True,
            "optimize.use_switch": True,
        },
        include_path=[np.get_include()],
        annotate=True,
    ),
)
