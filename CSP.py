import numpy as np
import time
import random
from collections import deque

N = 8
count_bt = 0
count_fc = 0
count_ac3 = 0

def consistent(assignment, value):
    r1, c1 = value
    for (r2, c2) in assignment:
        if r1 == r2 or c1 == c2:  # trùng hàng hoặc trùng cột
            return False
    return True

def backtracking(assignment):
    global count_bt

    board = np.array([[1 if (r, c) in assignment else 0 for c in range(N)] for r in range(N)])
    yield board, assignment[:]

    if len(assignment) == N:
        return

    r = len(assignment)
    domain = [(r, c) for c in range(N)]
    random.shuffle(domain)

    for value in domain:
        if consistent(assignment, value):
            count_bt += 1
            yield from backtracking(assignment + [value])

def forwardchecking(assignment, domains):
    global count_fc

    board = np.array([[1 if (r, c) in assignment else 0 for c in range(N)] for r in range(N)])
    yield board, assignment[:]

    if len(assignment) == N:
        return

    var = len(assignment)
    domain_var = domains[var][:]
    random.shuffle(domain_var)

    for (r, c) in domain_var:
        if all(c != col for (_, col) in assignment):
            count_fc += 1

            new_domains = {k: v[:] for k, v in domains.items()}
            valid = True
            for future_var in range(var + 1, N):
                new_domains[future_var] = [
                    (future_var, c2)
                    for (r2, c2) in new_domains[future_var]
                    if c2 != c
                ]
                if not new_domains[future_var]:
                    valid = False
                    break

            if valid:
                yield from forwardchecking(assignment + [(r, c)], new_domains)
    return


# Thuộc AC-3
def solve_from_domains(domains):
    order = sorted(range(N), key=lambda r: len(domains[r]))
    used_cols = set()
    assignment = [None] * N

    def dfs(idx):
        if idx == N:
            return True
        r = order[idx]
        for (_, c) in sorted(domains[r], key=lambda x: x[1]):
            if c in used_cols:
                continue
            assignment[r] = (r, c)
            used_cols.add(c)
            if dfs(idx + 1):
                return True
            used_cols.remove(c)
            assignment[r] = None
        return False

    ok = dfs(0)
    if not ok:
        return None
    return [assignment[r] for r in range(N)]

def consistent_ac3(vi, vj):
    r1, c1 = vi
    r2, c2 = vj
    return not (r1 == r2 or c1 == c2)


def ac3(domains):
    global count_ac3
    queue = deque([(xi, xj) for xi in range(N) for xj in range(N) if xi != xj])
    queue = deque(random.sample(list(queue), len(queue)))

    board = np.zeros((N, N), dtype=int)
    yield board, []

    while queue:
        xi, xj = queue.popleft()
        count_ac3 += 1
        removed = False
        new_domain_xi = []

        for vi in domains[xi]:
            if any(consistent_ac3(vi, vj) for vj in domains[xj]):
                new_domain_xi.append(vi)

        if len(new_domain_xi) < len(domains[xi]):
            domains[xi] = new_domain_xi
            removed = True

        if not domains[xi]:
            board = np.zeros((N, N), dtype=int)
            yield board, []
            return

        if removed:
            for xk in range(N):
                if xk != xi and xk != xj:
                    queue.append((xk, xi))

        # -------------------------------
        # CHỈNH CHỖ RANDOM Ở ĐÂY 👇
        # -------------------------------
        board = np.zeros((N, N), dtype=int)
        temp_assignment = []

        for r, vals in domains.items():
            if len(vals) == 1:
                _, c = vals[0]
                board[r, c] = 1
                temp_assignment.append((r, c))
            elif len(vals) > 1:
                vi = random.choice(vals)
                _, c = vi
                board[r, c] = 1
        # -------------------------------

        yield board, temp_assignment

    # Sau khi hết queue
    sol = solve_from_domains({k: v[:] for k, v in domains.items()})
    if sol is None or len(sol) < N:
        board = np.zeros((N, N), dtype=int)
        yield board, []
        return

    rows = [r for (r, c) in sol]
    cols = [c for (r, c) in sol]
    if len(set(rows)) == N and len(set(cols)) == N:
        board = np.zeros((N, N), dtype=int)
        for (r, c) in sol:
            board[r, c] = 1
        yield board, sol[:]
    else:
        board = np.zeros((N, N), dtype=int)
        yield board, []



def run_algorithm(algorithm="bt", visualize=False):
    global count_bt, count_fc, count_ac3
    count_bt = count_fc = count_ac3 = 0

    start = time.time()
    found = False
    total_states = 0
    last_state, last_path = None, None

    if algorithm == "bt":
        steps = backtracking([])
        name = "BACKTRACKING"
    elif algorithm == "fc":
        domains = {r: [(r, c) for c in range(N)] for r in range(N)}
        steps = forwardchecking([], domains)
        name = "FORWARD CHECKING"
    elif algorithm == "ac3":
        domains = {r: [(r, c) for c in range(N)] for r in range(N)}
        steps = ac3(domains)
        name = "AC-3 (Arc Consistency)"
    else:
        raise ValueError("Thuật toán không hợp lệ!")

    if visualize:
        return steps

    try:
        for state, path in steps:
            last_state, last_path = state, path
            total_states += 1
            if algorithm != "ac3" and len(path) == N:
                found = True
                break
    except StopIteration:
        pass

    elapsed = time.time() - start

    if algorithm == "bt":
        count = count_bt
    elif algorithm == "fc":
        count = count_fc
    else:
        count = count_ac3

    print(f"=== {name} ===")
    print(f"Thời gian chạy: {elapsed:.4f}s")
    print(f"Số trạng thái duyệt: {count}")
    if last_state is not None:
        print("\nBoard kết quả:")
        print(last_state)
    else:
        print("Không tìm thấy nghiệm!")

    return last_state, last_path, elapsed
