import numpy as np
from itertools import product
N = 8


import numpy as np
import random

def sinh_nondeterministic(state):
    gen = []
    soXe = np.sum(state)
    error_rate=0.3
    if soXe >= N:
        return gen

    used_Col = np.where(state == 1)[1]
    
    for c in range(N):
        if c not in used_Col:
            new_State = state.copy()
            new_State[soXe][c] = 1
            gen.append(new_State)

            if random.random() < error_rate:
                candidates = [i for i in range(N) if i != c and i not in used_Col]
                if candidates: 
                    wrong_c = random.choice(candidates)
                    wrong_State = state.copy()
                    wrong_State[soXe][wrong_c] = 1
                    gen.append(wrong_State)

    return gen

def AND_OR_Search(root, goal):
    visited = set()
    yield from OR_Search(root, goal, [root], visited)

def OR_Search(state, goal, path, visited):
    if np.array_equal(state, goal):
        yield (state, path)
        return

    if tuple(state.flatten()) in [tuple(s.flatten()) for s in path[:-1]]:
        return  
    
    for child in sinh_nondeterministic(state):
        key = tuple(child.flatten())
        if key not in visited:
            yield (child, path + [child])
        new_visited = visited.copy()
        new_visited.add(key)
        for plan in AND_Search([child], goal, path + [child], new_visited):
            yield plan

def AND_Search(states, goal, path, visited):
    all_plans_per_s = []
    for s in states:
        plans_for_s = list(OR_Search(s, goal, path, visited.copy()))
        if not plans_for_s:
            return
        all_plans_per_s.append(plans_for_s)

    for combo in product(*all_plans_per_s):
        merged_path = path[:] 
        final_state = None
        for (st, p) in combo:
            merged_path.extend(p[len(path):])  
            final_state = st
        yield final_state, merged_path

