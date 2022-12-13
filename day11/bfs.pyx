# distutils: language=c++
import cython
import numpy as np

cimport numpy as np
from libcpp.deque cimport deque
from libcpp.list cimport list
from libcpp.pair cimport pair


cpdef int bfs(np.ndarray view, pair[int, int] start, pair[int, int] end):
    cdef deque[pair[int, int]] open_list
    cdef np.ndarray visited = np.zeros([view.shape[0], view.shape[1]], dtype=np.bool_)
    cdef np.ndarray cost = np.zeros([view.shape[0], view.shape[1]], dtype=np.uint32)
    cdef list[pair[int, int]] positions = [(0, 1), (0, -1), (1, 0), (-1, 0)]
    cdef pair[int, int] node
    cdef pair[int, int] xy

    open_list.push_back(start)
    visited[start.first, start.second] = True

    while open_list.size() > 0:
        node = open_list.front()
        if node == end:
            return cost[node.first, node.second]

        for position in positions:
            xy = (node.first + position.first, node.second + position.second)
            if (
                xy.first >= 0
                and xy.second >= 0
                and xy.first < view.shape[0]
                and xy.second < view.shape[1]
                and (
                    view[xy.first, xy.second] == view[node.first, node.second] + 1
                    or view[xy.first, xy.second] <= view[node.first, node.second]
                )
                and not visited[xy.first, xy.second]
            ):
                cost[xy.first, xy.second] = cost[node.first, node.second] + 1
                open_list.push_back(xy)
                visited[xy.first, xy.second] = True

        open_list.pop_front()

    return -1


cpdef int bfs_2(np.ndarray view, pair[int, int] start):
    cdef deque[pair[int, int]] open_list
    cdef np.ndarray visited = np.zeros([view.shape[0], view.shape[1]], dtype=np.bool_)
    cdef np.ndarray cost = np.zeros([view.shape[0], view.shape[1]], dtype=np.uint32)
    cdef list[pair[int, int]] positions = [(0, 1), (0, -1), (1, 0), (-1, 0)]
    cdef pair[int, int] node
    cdef pair[int, int] xy
    cdef DTYPE_t end = ord("a")

    open_list.push_back(start)
    visited[start.first, start.second] = True

    while open_list.size() > 0:
        node = open_list.front()
        if view[node.first, node.second] == end:
            return cost[node.first, node.second]

        for position in positions:
            xy = (node.first + position.first, node.second + position.second)
            if (
                xy.first >= 0
                and xy.second >= 0
                and xy.first < view.shape[0]
                and xy.second < view.shape[1]
                and (
                    view[xy.first, xy.second] == view[node.first, node.second] - 1
                    or view[xy.first, xy.second] >= view[node.first, node.second]
                )
                and not visited[xy.first, xy.second]
            ):
                cost[xy.first, xy.second] = cost[node.first, node.second] + 1
                open_list.push_back(xy)
                visited[xy.first, xy.second] = True

        open_list.pop_front()

    return -1
