import time
import numpy as np
from algorithm import *
from localsearch import *
from nondeterministic import *
import Demo_NoOBS as NOBS
import Demo_PartialOBS as POBS
from CSP import *


def run_algorithm(name, root, goal):
    """Khởi chạy thuật toán theo tên khi người dùng click."""
    current_algo = name
    steps = None
    info_panel = {}
    detail_lines = []

    # --- Uninformed Search ---
    if name == "BFS": steps = BFS(root, goal)
    elif name == "UCS": steps = UCS(root, goal)
    elif name == "DFS": steps = DFS(root, goal)
    elif name == "DLS": steps = DLS(root, goal, 8)
    elif name == "IDS": steps = IDS(root, goal, 1000)

    # --- Informed Search ---
    elif name == "Greedy_S": steps = GreedySearch(root, goal); current_algo = "Greedy"
    elif name == "A*": steps = A_Sao(root, goal); current_algo = "A*"

    # --- Local Search ---
    elif name == "Hill_S": steps = Hill_Search(root, goal); current_algo = "Hill Climbing"
    elif name == "S_A": steps = Simulated_Annealing(root, goal); current_algo = "Simulated Annealing"
    elif name == "Beam_S": steps = Beam_Search(root, goal, 2); current_algo = "Beam Search"
    elif name == "Gen_A": steps = Genetic_Algorithm(root, goal); current_algo = "Genetic Algorithm"

    # --- Nondeterministic ---
    elif name == "AND_OR": steps = AND_OR_Search(root, goal); current_algo = "AND-OR"
    elif name == "No_OBS":
        NOBS.run_algorithm()
        return None, "No Observation", None, []
    elif name == "Part_OBS":
        POBS.run_algorithm()
        return None, "Partial Observation", None, []

    # --- CSP ---
    elif name == "BackTr":
        start = time.time()
        steps_bt = backtrack([], giatri)
        for last_state, last_path in steps_bt:
            pass
        elapsed = time.time() - start
        current_algo = "Backtracking"
        info_panel = {
            "Thuật toán": current_algo,
            "Thời gian": f"{elapsed:.4f}s",
            "Số state": str(count_bt),
            "Kết quả": "Thành công"
        }
        detail_lines = [f"Step {i+1}: {p}" for i, p in enumerate(last_path)]
        return last_state, current_algo, info_panel, detail_lines

    elif name == "ForwCh":
        start = time.time()
        steps_fc = forwardchecking([], giatri)
        for last_state, last_path in steps_fc:
            pass
        elapsed = time.time() - start
        current_algo = "Forward Checking"
        info_panel = {
            "Thuật toán": current_algo,
            "Thời gian": f"{elapsed:.4f}s",
            "Số state": str(count_fc),
            "Kết quả": "Thành công"
        }
        detail_lines = [f"Step {i+1}: {p}" for i, p in enumerate(last_path)]
        return last_state, current_algo, info_panel, detail_lines

    return steps, current_algo, info_panel, detail_lines


def compute_result(steps, goal, current_algo):
    """Chạy toàn bộ thuật toán và trả về kết quả cuối."""
    found = False
    total_states, start_time = 1, time.time()
    last_state, last_path = next(steps, (None, []))

    try:
        while True:
            last_state, last_path = next(steps)
            total_states += 1
            if np.array_equal(last_state, goal):
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
    ] + [f"Step {i+1}: {state.tolist()}" for i, state in enumerate(last_path)]

    return info_panel, detail_lines, found
