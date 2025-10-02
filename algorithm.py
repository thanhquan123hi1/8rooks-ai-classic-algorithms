from collections import deque
import random
import numpy as np
import heapq
N = 8

def sinh(state):
    gen = []
    soXe = np.sum(state)
    if soXe >= N:
        return gen
    used_Col = np.where(state == 1)[1]
    for c in range(N):
        if c not in used_Col:
            new_State = state.copy()
            new_State[soXe][c] = 1
            gen.append(new_State)
    return gen

def Cost(state):
    base = 1
    r, c = np.where(state == 1)
    conflicts = 0
    for i in range(len(r)):
        for j in range(i + 1, len(r)):
            if r[i] == r[j] or c[i] == c[j]:
                conflicts += 1
    return base + conflicts

def Heuristic(state, goal):
    matches = np.sum((state == 1) & (goal == 1))
    return N - matches

def BFS(root, goal):
    queue = deque()
    queue.append((root, [root]))
    visited = set()
    visited.add(tuple(root.flatten()))
    while queue:
        state, path = queue.popleft()
        yield state, path
        if np.array_equal(state, goal):
            return
        for st in sinh(state):
            st_tuple = tuple(st.flatten())
            if st_tuple not in visited:
                queue.append((st, path + [st]))
                visited.add(st_tuple)

def UCS(root, goal):
    pq = []
    counter = 0
    heapq.heappush(pq, (0, counter, tuple(root.flatten()), [root]))
    visited = set()
    while pq:
        cost, _, state_tuple, path = heapq.heappop(pq)
        state = np.array(state_tuple).reshape(N, N)
        yield state, path
        if np.array_equal(state, goal):
            return
        for st in sinh(state):
            st_tuple = tuple(st.flatten())
            if st_tuple not in visited:
                g = cost + Cost(st)
                counter += 1
                heapq.heappush(pq, (g, counter, st_tuple, path + [st]))
                visited.add(st_tuple)

def DFS(root, goal):
    stack = []
    stack.append((root, [root]))
    visited = set()
    while stack:
        state, path = stack.pop()
        yield state, path
        if np.array_equal(state, goal):
            return
        for st in sinh(state):
            st_tuple = tuple(st.flatten())
            if st_tuple not in visited:
                stack.append((st, path + [st]))
                visited.add(st_tuple)

def DLS(state, goal, limit, path=None, visited=None):
    if path is None:
        path = [state]
    if visited is None:
        visited = set()
    state_tuple = tuple(state.flatten())
    visited.add(state_tuple)
    yield state, path
    if np.array_equal(state, goal):
        return
    if limit <= 0:
        return
    for child in sinh(state):
        child_tuple = tuple(child.flatten())
        if child_tuple not in visited:
            yield from DLS(child, goal, limit - 1, path + [child], visited.copy())

def IDS(root, goal, max_Depth):
    for depth in range(max_Depth + 1):
        visited = set()
        for state, path in DLS(root, goal, depth, [root], visited):
            yield state, path
            if np.array_equal(state, goal):
                return

def GreedySearch(root, goal):
    pq = []
    counter = 0
    heapq.heappush(pq, (Heuristic(root, goal), counter, tuple(root.flatten()), [root]))
    visited = set()
    while pq:
        heu, _, state_tuple, path = heapq.heappop(pq)
        state = np.array(state_tuple).reshape(N, N)
        yield state, path
        if np.array_equal(state, goal):
            return
        for st in sinh(state):
            st_tuple = tuple(st.flatten())
            if st_tuple not in visited:
                counter += 1
                heapq.heappush(pq, (Heuristic(st, goal), counter, st_tuple, path + [st]))
                visited.add(st_tuple)

def A_Sao(root, goal):
    pq = []
    counter = 0
    heapq.heappush(pq, (Heuristic(root, goal) + Cost(root), counter, tuple(root.flatten()), [root]))
    visited = set()
    while pq:
        f, _, state_tuple, path = heapq.heappop(pq)
        state = np.array(state_tuple).reshape(N, N)
        yield state, path
        if np.array_equal(state, goal):
            return
        for st in sinh(state):
            st_tuple = tuple(st.flatten())
            if st_tuple not in visited:
                counter += 1
                fn = Heuristic(st, goal) + Cost(st)
                heapq.heappush(pq, (fn, counter, st_tuple, path + [st]))
                visited.add(st_tuple)





