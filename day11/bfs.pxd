# distutils: language=c++
import cython
import numpy as np

cimport numpy as np
from libcpp cimport bool
from libcpp.pair cimport pair

# It's necessary to call "import_array" if you use any part of the
# numpy PyArray_* API. From Cython 3, accessing attributes like
# ".shape" on a typed Numpy array use this API. Therefore we recommend
# always calling "import_array" whenever you "cimport numpy"
np.import_array()

# We now need to fix a datatype for our arrays. I've used the variable
# DTYPE for this, which is assigned to the usual NumPy runtime
# type info object.
DTYPE = np.int32

# "ctypedef" assigns a corresponding compile-time type to DTYPE_t. For
# every type in the numpy module there's a corresponding compile-time
# type with a _t-suffix.
ctypedef np.int32_t DTYPE_t

cpdef int bfs(np.ndarray view, pair[int, int] start, pair[int, int] end, bool is_part_2)
cpdef int bfs_2(np.ndarray view, pair[int, int] start)
