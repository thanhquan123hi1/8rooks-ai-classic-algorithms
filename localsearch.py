from algorithm import *
from math import exp



def Hill_Search(root, goal):
    state = root
    path = [root]
    visited = set()
    visited.add(tuple(root.flatten()))
    counter = 0
    while True:
        yield state, path
        if np.array_equal(state, goal):
            return
        pq = []
        for st in sinh(state):
            st_tuple = tuple(st.flatten())
            if st_tuple not in visited:
                counter += 1
                heapq.heappush(pq, (Heuristic(st, goal), counter, st_tuple))
        if not pq:
            return
        heu, _, best_tuple = heapq.heappop(pq)
        best_st = np.array(best_tuple).reshape(N, N)
        if heu < Heuristic(state, goal):
            state = best_st
            path.append(state)
            visited.add(best_tuple)
        else:
            return
        
def Beam_Search(root, goal, k):
    queue = deque()
    queue.append((root, [root]))
    visited = set()
    visited.add(tuple(root.flatten()))
    while queue:
        state, path = queue.popleft()
        yield state, path
        if np.array_equal(state, goal):
            return

        candidates = []
        for x in sinh(state):
            if tuple(x.flatten()) not in visited:
                candidates.append((x, path + [x]))
                visited.add(tuple(x.flatten()))

        best = sorted(candidates, key=lambda item: Heuristic(item[0], goal))[:k]
        queue.extend(best)

def Simulated_Annealing(root, goal, T=100, Tmin=1e-3, alpha=0.95, K=100):
    state = root.copy()
    path = [state.copy()]
    yield state, path  # hiển thị trạng thái đầu tiên

    while T > Tmin:
        for _ in range(K):
            if np.array_equal(state, goal):
                return

            E = -Heuristic(state, goal)
            neighbors = sinh(state)
            if not neighbors:
                continue  

            st_new = random.choice(neighbors)
            Ep = -Heuristic(st_new, goal)

            if Ep - E <= 0:
                state = st_new
                path.append(state.copy())
            else:
                p = exp(-(Ep - E) / T)
                if random.random() < p:
                    state = st_new
                    path.append(state.copy())

            yield state, path

        T *= alpha

def Genetic_Algorithm(root, goal):
    # 1. Khởi tạo k quần thể
    k = 100000
    population = []
    for _ in range(k):
        cathe = np.random.randint(N, size=N)
        state = np.zeros((N, N), dtype=int)
        for r, c in enumerate(cathe):
            state[r, c] = 1
        yield state, [state]
        if np.array_equal(state, goal):
            return
        population.append(state)

    while True:
        # 2. Đánh giá độ thích nghi (fitness)
        fitness = [Heuristic(st, goal) for st in population]

        # 3. Chọn lọc 
        pop_fit = list(zip(population, fitness))  
        pop_fit.sort(key=lambda x: x[1]) 

        parents = []
        for i in range(0, len(pop_fit) - 1, 2):
            parent1 = pop_fit[i][0]   
            parent2 = pop_fit[i + 1][0]
            parents.append((parent1, parent2))

        # 4. Lai ghép (crossover)
        new_population = []
        for parent1, parent2 in parents:
            p1_cols = list(np.where(parent1 == 1)[1])
            p2_cols = list(np.where(parent2 == 1)[1])
            child_cols = p1_cols[:(N // 2)] + p2_cols[(N // 2):]
            child = np.zeros((N, N), dtype=int)
            for r, c in enumerate(child_cols):
                child[r, c] = 1
            yield child, [child]
            if np.array_equal(child, goal):
                return
            new_population.append(child)

        # 5. Đột biến (mutation)
        for i in range(len(new_population)):
            if np.random.random() < 0.1:
                child_db = new_population[i]
                cols = list(np.where(child_db == 1)[1])
                j = np.random.randint(0, N)
                cols[j] = (cols[j] + 1) % N
                mutated = np.zeros((N, N), dtype=int)
                for r, c in enumerate(cols):
                    mutated[r, c] = 1
                new_population[i] = mutated
                yield mutated, [mutated]
                if np.array_equal(mutated, goal):
                    return

        # 6. Cập nhật quần thể
        population = new_population 
        if not population:
            return
        