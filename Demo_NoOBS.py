import numpy as np
import random
import time   
N = 8  

def make_board(perm):
    """Tạo ma trận 8x8 từ một hoán vị."""
    board = np.zeros((N, N), dtype=int)
    for r, c in enumerate(perm):
        board[r][c] = 1
    return board

def create_goals(k=8, seed=0):
    random.seed(seed)
    goals = []
    perms = set()
    
    while len(goals) < k:
        perm = tuple(random.sample(range(N), N)) 
        if perm not in perms:  
            perms.add(perm)
            goals.append(make_board(perm))
    
    return goals
def random_root_belief(N=8, k=2):
    states = set()
    boards = []
    while len(states) < k:
        board = np.zeros((N, N), dtype=int)
        if random.choice([True, False]): 
            col = random.randint(0, N-1)
            board[0, col] = 1
        state_tuple = tuple(board.flatten())
        if state_tuple not in states:
            states.add(state_tuple)
            boards.append(board)
    return boards

def valid_board(board):
    rows, cols = np.where(board == 1)
    return len(set(rows)) == len(rows) and len(set(cols)) == len(cols)

def action(belief_state, N=8):
    next_belief_move = []
    next_belief_place = []

    for board in belief_state:
        # --- Dời 1 quân ---
        moved_board = board.copy()
        rows_with_rook = np.where(board.sum(axis=1) > 0)[0]
        if len(rows_with_rook) > 0:
            r = random.choice(rows_with_rook)
            old_c = np.where(board[r] == 1)[0][0]
            possible_cols = [c for c in range(N) if c != old_c]
            if possible_cols:
                new_c = random.choice(possible_cols)
                moved_board = board.copy()
                moved_board[r, old_c] = 0
                moved_board[r, new_c] = 1
                if not valid_board(moved_board):
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
                new_board = board.copy()
                new_board[next_row, c] = 1
                if valid_board(new_board):
                    placed_board = new_board
                    break
        next_belief_place.append(placed_board)

    return next_belief_move, next_belief_place

def is_goal(board, goals):
    return any(np.array_equal(board, g) for g in goals)

def search_no_observation(root_belief, goals, max_depth=50):

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

        moved, placed = action(belief_state)
        generated += 2   # mỗi lần sinh ra 2 tập
        stack.append((placed, depth+1))
        stack.append((moved, depth+1))

    return None, generated

def run_algorithm():
    goals = create_goals(k=8, seed=42)
    print("Tập goal sinh ra (8 trạng thái):")
    for i, g in enumerate(goals, 1):
        print(f"Goal {i}:\n{g}\n")

    root_belief = random_root_belief(N=8, k=2)
    print("Belief state ban đầu:")
    for b in root_belief:
        print(b, "\n")

    start = time.time()
    result, generated = search_no_observation(root_belief, goals, max_depth=50)
    end = time.time()

    print(f"Thời gian chạy: {end - start:.4f} giây")
    print(f"Số belief states sinh ra: {generated}")

    if result is not None:
        print("===> Tìm thấy kết quả:")
        for i, b in enumerate(result, 1):
            print(f"Board {i}:\n{b}\n")
    else:
        print("===> Không tìm thấy lời giải")
