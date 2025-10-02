import numpy as np
import time

N = 8
giatri = [(i, j) for i in range(N) for j in range(N)]

count_bt = 0
count_fc = 0

def consistent(a, value):
    r1, c1 = value
    for (r2, c2) in a:
        if r1 == r2 or c1 == c2:
            return False
    return True

# Backtracking 
def backtrack(a, giatri):
    global count_bt
    if len(a) == N:
        board = np.array([[1 if (r,c) in a else 0 for c in range(N)] for r in range(N)])
        yield board, a[:]
        return

    values = giatri[:]
    np.random.shuffle(values)
    for v in values:
        if consistent(a, v):
            a.append(v)
            count_bt += 1
            yield from backtrack(a, giatri)
            a.pop()
    return

# Forward Checking 
def f(tapGiaTri, value):
    r1, c1 = value
    new = []
    for (r2, c2) in tapGiaTri:
        if r1 != r2 and c1 != c2:
            new.append((r2, c2))
    return new

def forwardchecking(a, tapGiaTri):
    global count_fc
    if len(a) == N:
        board = np.array([[1 if (r,c) in a else 0 for c in range(N)] for r in range(N)])
        yield board, a[:]
        return

    values = tapGiaTri[:]
    np.random.shuffle(values)
    for v in values:
        if consistent(a, v):
            a.append(v)
            count_fc += 1
            yield from forwardchecking(a, f(tapGiaTri, v))
            a.pop()
    return

def run_algorithm(algorithm="bt"):
    global count_bt, count_fc
    count_bt = 0
    count_fc = 0

    if algorithm == "bt":
        steps = backtrack([], giatri)
    else:
        steps = forwardchecking([], giatri)

    start = time.time()
    last_state, last_path = None, None
    total_states = 0
    found = False

    try:
        while True:
            state, path = next(steps)   # lấy ra đúng 2 giá trị
            last_state, last_path = state, path
            total_states += 1
            if len(path) == N:
                found = True
                break
    except StopIteration:
        pass

    elapsed = time.time() - start

    if found:
        print(f"=== {algorithm.upper()} tìm thấy nghiệm ===")
        print(f"Thời gian chạy: {elapsed:.4f}s")
        if algorithm == "bt":
            print(f"Tổng số state duyệt: {count_bt}")
        else:
            print(f"Tổng số state duyệt: {count_fc}")

        print("\nĐường đi (các vị trí đặt quân xe):")
        for i, pos in enumerate(last_path, 1):
            print(f"Step {i}: {pos}")

        print("\nBoard kết quả:")
        print(last_state)
    else:
        print(f"{algorithm.upper()} không tìm thấy nghiệm!")


