import time
import numpy as np
from algorithm import *
from localsearch import *
from nondeterministic import *
import Demo_NoOBS as NOBS
import Demo_PartialOBS as POBS
from CSP import run_algorithm as run_CSP  # ✅ alias để tránh đệ quy


def run_algorithm(name, root, goal):
    """Khởi chạy thuật toán theo tên khi người dùng click."""
    current_algo = name
    steps = None
    info_panel = {}
    detail_lines = []

    # Uninformed Search
    if name == "BFS": 
        steps = BFS(root, goal)
    elif name == "UCS": 
        steps = UCS(root, goal)
    elif name == "DFS": 
        steps = DFS(root, goal)
    elif name == "DLS": 
        steps = DLS(root, goal, 8)
    elif name == "IDS": 
        steps = IDS(root, goal, 1000)

    # Informed Search 
    elif name == "Greedy_S": 
        steps = GreedySearch(root, goal)
        current_algo = "Greedy"
    elif name == "A*": 
        steps = A_Sao(root, goal)
        current_algo = "A*"

    #  Local Search 
    elif name == "Hill_S": 
        steps = Hill_Search(root, goal)
        current_algo = "Hill Climbing"
    elif name == "S_A": 
        steps = Simulated_Annealing(root, goal)
        current_algo = "Simulated Annealing"
    elif name == "Beam_S": 
        steps = Beam_Search(root, goal, 2)
        current_algo = "Beam Search"
    elif name == "Gen_A": 
        steps = Genetic_Algorithm(root, goal)
        current_algo = "Genetic Algorithm"

    # Nondeterministic Search
    elif name == "AND_OR": 
        steps = AND_OR_Search(root, goal)
        current_algo = "AND-OR"

    elif name == "No_OBS":
        NOBS.run_algorithm()
        return None, "No Observation", None, []

    elif name == "Part_OBS":
        POBS.run_algorithm()
        return None, "Partial Observation", None, []

    # CSP (Constraint Satisfaction Problems) 
    elif name == "BackTr":
        # Gọi generator của CSP để mô phỏng từng bước
        steps = run_CSP("bt", visualize=True)
        current_algo = "Backtracking"
        return steps, current_algo, {}, []

    elif name == "ForwCh":
        steps = run_CSP("fc", visualize=True)
        current_algo = "Forward Checking"
        return steps, current_algo, {}, []
    elif name == "AC3":
        steps = run_CSP("ac3", visualize=True)
        current_algo = "AC-3"
        return steps, current_algo, {}, []


    # Trả kết quả cho các thuật toán có generator
    return steps, current_algo, info_panel, detail_lines


# HÀM TÍNH KẾT QUẢ CUỐI CÙNG
def compute_result(steps, goal, current_algo):
    """Chạy toàn bộ thuật toán và trả về kết quả cuối cùng cho UI."""
    found = False
    total_states, start_time = 1, time.time()
    last_state, last_path = next(steps, (None, []))

    try:
        while True:
            last_state, last_path = next(steps)
            total_states += 1
            if isinstance(last_state, np.ndarray) and np.array_equal(last_state, goal):
                found = True
                break
    except StopIteration:
        pass

    elapsed_time = time.time() - start_time

    info_panel = {
        "Thuật toán": current_algo,
        "Thời gian": f"{elapsed_time:.4f}s",
        "Số state": str(total_states),
        "Kết quả": "Thành công" if found else "Thất bại"
    }

    detail_lines = [
        f"Thuật toán: {current_algo}",
        f"Thời gian: {elapsed_time:.4f}s",
        f"Tổng state: {total_states}",
        f"Kết quả: {'Thành công' if found else 'Thất bại'}",
        "------ Đường đi ------",
    ]

    if isinstance(last_path, list) and last_path and isinstance(last_path[0], tuple):
        for i, pos in enumerate(last_path):
            detail_lines.append(f"Step {i+1}: {pos}")
    else:
        for i, state in enumerate(last_path):
            detail_lines.append(f"Step {i+1}: {state.tolist() if isinstance(state, np.ndarray) else state}")

    # Trả thêm trạng thái cuối cùng để main.py có thể hiển thị lên bàn cờ
    return info_panel, detail_lines, found, last_state

