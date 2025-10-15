import numpy as np
import time
import random
from collections import deque

# ---------------------------------------------------------------
# CẤU HÌNH CƠ BẢN
# ---------------------------------------------------------------
N = 8
count_bt = 0
count_fc = 0
count_ac3 = 0


# ---------------------------------------------------------------
# HÀM KIỂM TRA RÀNG BUỘC CHUNG (Backtracking & Forward Checking)
# ---------------------------------------------------------------
def consistent(assignment, value):
    """Kiểm tra xem value có hợp lệ với các giá trị đã gán không."""
    r1, c1 = value
    for (r2, c2) in assignment:
        if r1 == r2 or c1 == c2:  # trùng hàng hoặc trùng cột
            return False
    return True


# ---------------------------------------------------------------
# ALGORITHM 6.3: BACKTRACKING-SEARCH (Russell & Norvig 2016)
# ---------------------------------------------------------------
def backtracking(assignment):
    """
    Backtracking chuẩn theo AIMA.
    Mỗi biến là một hàng r → chỉ chọn cột cho hàng đó.
    Có yield để hiển thị từng bước và tránh treo máy.
    """
    global count_bt

    # Hiển thị trạng thái hiện tại
    board = np.array([[1 if (r, c) in assignment else 0 for c in range(N)] for r in range(N)])
    yield board, assignment[:]

    # Nếu đã gán đủ 8 biến (8 hàng)
    if len(assignment) == N:
        return

    # --- Chọn biến (hàng r) ---
    r = len(assignment)
    domain = [(r, c) for c in range(N)]
    random.shuffle(domain)  # chọn giá trị ngẫu nhiên

    # --- Duyệt từng giá trị (cột c) ---
    for value in domain:
        if consistent(assignment, value):
            count_bt += 1
            yield from backtracking(assignment + [value])


# ---------------------------------------------------------------
# ALGORITHM 6.5: FORWARD CHECKING (Russell & Norvig 2016)
# ---------------------------------------------------------------
def forwardchecking(assignment, domains):
    """Forward Checking (phiên bản tối ưu, không dùng deepcopy)."""
    global count_fc

    # Hiển thị trạng thái hiện tại
    board = np.array([[1 if (r, c) in assignment else 0 for c in range(N)] for r in range(N)])
    yield board, assignment[:]

    if len(assignment) == N:
        return

    var = len(assignment)
    domain_var = domains[var][:]  # sao chép domain riêng cho biến hiện tại
    random.shuffle(domain_var)    # xáo trộn thứ tự

    for (r, c) in domain_var:
        # Kiểm tra hợp lệ theo cột
        if all(c != col for (_, col) in assignment):
            count_fc += 1

            # ✅ chỉ sao chép shallow, không deepcopy toàn bộ
            new_domains = {k: v[:] for k, v in domains.items()}

            # Cập nhật domain của các biến chưa gán
            valid = True
            for future_var in range(var + 1, N):
                new_domains[future_var] = [
                    (future_var, c2)
                    for (r2, c2) in new_domains[future_var]
                    if c2 != c
                ]
                if not new_domains[future_var]:  # nếu biến nào mất hết domain → cắt tỉa
                    valid = False
                    break

            if valid:
                yield from forwardchecking(assignment + [(r, c)], new_domains)
    return


# ---------------------------------------------------------------
# ALGORITHM 6.2: AC-3 (Arc Consistency) — FIXED for UI visualization
# ---------------------------------------------------------------
def consistent_ac3(vi, vj):
    """Ràng buộc: không trùng hàng hoặc trùng cột."""
    r1, c1 = vi
    r2, c2 = vj
    return not (r1 == r2 or c1 == c2)


def ac3(domains):
    """
    Thuật toán AC-3 (Arc Consistency) — Duy trì tính nhất quán cung.
    Có yield để visualize từng bước giống Backtracking và Forward Checking.
    """
    global count_ac3
    queue = deque([(xi, xj) for xi in range(N) for xj in range(N) if xi != xj])

    # Hiển thị trạng thái ban đầu
    board = np.zeros((N, N), dtype=int)
    yield board, []

    while queue:
        xi, xj = queue.popleft()
        count_ac3 += 1

        removed = False
        new_domain_xi = []
        for vi in domains[xi]:
            # Giữ lại các giá trị còn tương thích với ít nhất một giá trị của xj
            if any(consistent_ac3(vi, vj) for vj in domains[xj]):
                new_domain_xi.append(vi)

        # Nếu có giá trị bị loại bỏ khỏi domain
        if len(new_domain_xi) < len(domains[xi]):
            domains[xi] = new_domain_xi
            removed = True

        # Nếu domain bị rỗng → không có nghiệm
        if not domains[xi]:
            board = np.zeros((N, N), dtype=int)
            yield board, []  # visualize thất bại
            return

        # Nếu có giá trị bị loại bỏ → thêm lại các cung liên quan
        if removed:
            for xk in range(N):
                if xk != xi and xk != xj:
                    queue.append((xk, xi))

        # Cập nhật board để visualize
        board = np.zeros((N, N), dtype=int)
        for r, vals in domains.items():
            if len(vals) == 1:
                _, c = vals[0]
                board[r, c] = 1

        # ✅ Trả danh sách các giá trị hiện còn trong domain (để UI thấy thay đổi)
        flat_values = list(sum(domains.values(), []))
        yield board, flat_values

    # ✅ Sau khi AC-3 kết thúc, sinh một lời giải hợp lệ (nếu có)
    assignment = []
    for r in range(N):
        if len(domains[r]) == 1:
            assignment.append(domains[r][0])
        else:
            assignment.append(random.choice(domains[r]))

    board = np.zeros((N, N), dtype=int)
    for (r, c) in assignment:
        board[r, c] = 1

    yield board, assignment[:]  # trạng thái cuối để hiển thị lên bàn cờ rỗng


# ---------------------------------------------------------------
# HÀM TỔNG HỢP: RUN ALGORITHM (dùng chung)
# ---------------------------------------------------------------
def run_algorithm(algorithm="bt", visualize=False):
    """
    Nếu visualize=True → trả generator (để UI hiển thị từng bước).
    Nếu visualize=False → chạy toàn bộ và in ra kết quả.
    """
    global count_bt, count_fc, count_ac3
    count_bt = count_fc = count_ac3 = 0

    start = time.time()
    found = False
    total_states = 0
    last_state, last_path = None, None

    # --- Chọn thuật toán ---
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

    # --- Nếu visualize trên UI ---
    if visualize:
        return steps

    # --- Nếu chạy console ---
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

    # --- In kết quả ---
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
