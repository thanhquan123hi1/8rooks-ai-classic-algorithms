import numpy as np
import time
import copy
import random

# ---------------------------------------------------------------
# CẤU HÌNH CƠ BẢN
# ---------------------------------------------------------------
N = 8
count_bt = 0
count_fc = 0


# ---------------------------------------------------------------
# HÀM KIỂM TRA RÀNG BUỘC (không cùng hàng, không cùng cột)
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
# HÀM TỔNG HỢP: RUN ALGORITHM
# ---------------------------------------------------------------
def run_algorithm(algorithm="bt", visualize=False):
    """
    Nếu visualize=True → trả generator (để UI hiển thị từng bước).
    Nếu visualize=False → chạy toàn bộ và in ra kết quả.
    """
    global count_bt, count_fc
    count_bt = 0
    count_fc = 0

    start = time.time()
    found = False
    total_states = 0
    last_state, last_path = None, None

    # Chọn thuật toán
    if algorithm == "bt":
        steps = backtracking([])
    else:
        domains = {r: [(r, c) for c in range(N)] for r in range(N)}
        steps = forwardchecking([], domains)

    # Nếu dùng trong UI → trả generator
    if visualize:
        return steps

    # --- Nếu chạy console ---
    try:
        for state, path in steps:
            last_state, last_path = state, path
            total_states += 1
            if len(path) == N:
                found = True
                break
    except StopIteration:
        pass

    elapsed = time.time() - start
    name = "BACKTRACKING" if algorithm == "bt" else "FORWARD CHECKING"

    if found:
        print(f"=== {name} ===")
        print(f"Thời gian chạy: {elapsed:.4f}s")
        print(f"Số trạng thái duyệt: {count_bt if algorithm == 'bt' else count_fc}")
        print("\nĐường đi (các vị trí đặt quân):")
        for i, pos in enumerate(last_path, 1):
            print(f"Step {i}: {pos}")
        print("\nBoard kết quả:")
        print(last_state)
    else:
        print(f"{name}: Không tìm thấy nghiệm!")

    return last_state, last_path, elapsed
