import numpy as np
import random
import time

N = 8  

def make_board(perm, fixed_pos=None):
    board = np.zeros((N, N), dtype=int)
    for r, c in enumerate(perm):
        board[r][c] = 1
    if fixed_pos is not None:
        r0, c0 = fixed_pos
        board[r0, :] = 0 
        board[:, c0] = 0 
        board[r0, c0] = 1
    return board

def create_goals(k=8, seed=0, fixed_pos=(0,0)):
    random.seed(seed)
    goals = []
    perms = set()
    while len(goals) < k:
        perm = tuple(random.sample(range(N), N)) 
        if perm not in perms:
            perms.add(perm)
            goals.append(make_board(perm, fixed_pos))
    return goals

def random_root_belief(N=8, k=2, fixed_pos=(0,0)):
    states = set()
    boards = []
    while len(states) < k:
        board = np.zeros((N, N), dtype=int)
        r0, c0 = fixed_pos
        board[r0, c0] = 1  
        state_tuple = tuple(board.flatten())
        if state_tuple not in states:
            states.add(state_tuple)
            boards.append(board)
    return boards

def valid_board(board, fixed_pos=None):
    rows, cols = np.where(board == 1)
    if fixed_pos is not None:
        r0, c0 = fixed_pos
        if board[r0, c0] != 1:
            return False
    return len(set(rows)) == len(rows) and len(set(cols)) == len(cols)

def action(belief_state, N=8, fixed_pos=(0,0)):
    next_belief_move = []
    next_belief_place = []

    for board in belief_state:
        # --- Dời 1 quân ---
        moved_board = board.copy()
        rows_with_rook = np.where(board.sum(axis=1) > 0)[0]

        if len(rows_with_rook) > 0:
            r = random.choice(rows_with_rook)
            old_c = np.where(board[r] == 1)[0][0]

            # Nếu quân này là quân cố định thì bỏ qua
            if fixed_pos is not None and (r, old_c) == fixed_pos:
                moved_board = board.copy()
            else:
                possible_cols = [c for c in range(N) if c != old_c]
                if possible_cols:
                    new_c = random.choice(possible_cols)
                    moved_board = board.copy()
                    moved_board[r, old_c] = 0
                    moved_board[r, new_c] = 1
                    if not valid_board(moved_board, fixed_pos):
                        moved_board = board.copy()

        next_belief_move.append(moved_board)

        # --- Đặt 1 quân ---
        placed_board = board.copy()
        used_rows = np.where(board == 1)[0]
        next_row = max(used_rows) + 1 if len(used_rows) > 0 else 0

        if next_row < N:
            possible_cols = list(range(N))
            random.shuffle(possible_cols)
            for c in possible_cols:
                # Nếu trùng với quân cố định thì bỏ qua
                if fixed_pos is not None and (next_row, c) == fixed_pos:
                    continue
                new_board = board.copy()
                new_board[next_row, c] = 1
                if valid_board(new_board, fixed_pos):
                    placed_board = new_board
                    break

        next_belief_place.append(placed_board)

    return next_belief_move, next_belief_place

def is_goal(board, goals):
    return any(np.array_equal(board, g) for g in goals)

def search_with_partial_observation(root_belief, goals, max_depth=50, fixed_pos=(0,0)):
    stack = [(root_belief, 0)]
    explored = set()
    generated = 0 

    while stack:
        belief_state, depth = stack.pop()

        # Kiểm tra goal
        if all(is_goal(b, goals) for b in belief_state):
            return belief_state, generated

        if depth >= max_depth:
            continue

        state_key = tuple(tuple(b.flatten()) for b in belief_state)
        if state_key in explored:
            continue
        explored.add(state_key)

        moved, placed = action(belief_state, fixed_pos=fixed_pos)
        generated += 2
        stack.append((placed, depth+1))
        stack.append((moved, depth+1))

    return None, generated

def run_algorithm():
    fixed_pos = (0, 0) 
    goals = create_goals(k=8, seed=42, fixed_pos=fixed_pos)
    print("Tập goal sinh ra (8 trạng thái, tất cả có quân ở", fixed_pos, "):")
    for i, g in enumerate(goals, 1):
        print(f"Goal {i}:\n{g}\n")

    root_belief = random_root_belief(N=8, k=2, fixed_pos=fixed_pos)
    print("Belief state ban đầu:")
    for b in root_belief:
        print(b, "\n")

    start = time.time()
    result, generated = search_with_partial_observation(root_belief, goals, max_depth=50, fixed_pos=fixed_pos)
    end = time.time()

    print(f"Thời gian chạy: {end - start:.4f} giây")
    print(f"Số belief states sinh ra: {generated}")

    if result is not None:
        print("===> Tìm thấy kết quả:")
        for i, b in enumerate(result, 1):
            print(f"Board {i}:\n{b}\n")
    else:
        print("===> Không tìm thấy lời giải")
