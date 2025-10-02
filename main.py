import pygame
import sys
import numpy as np
import time

from algorithm import *
from localsearch import *
from nondeterministic import *
import Demo_NoOBS as NOBS
import Demo_PartialOBS as POBS
from CSP import *

from ui import *

N = 8
SIZE = 40
MARGIN = 155
WIDTH, HEIGHT = 1250, 750   

def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("8 Rooks")

    # state root và goal
    root = np.zeros((8, 8), dtype=int)
    goal = np.array([
        [0, 0, 0, 0, 0, 0, 1, 0],
        [0, 0, 0, 0, 0, 1, 0, 0],
        [0, 0, 0, 0, 1, 0, 0, 0],
        [1, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 1],
        [0, 0, 0, 1, 0, 0, 0, 0],
        [0, 1, 0, 0, 0, 0, 0, 0],
        [0, 0, 1, 0, 0, 0, 0, 0],
    ])

    # Label
    lblEmptyBoard = pygame.font.SysFont("Cambria", 30, bold=True).render("BÀN CỜ RỖNG", True, (0, 0, 80))
    lbl8rooks = pygame.font.SysFont("Cambria", 30, bold=True).render("BÀN CỜ MẪU", True, (0, 0, 80))

    # Nút chức năng
    btnRefresh = pygame.Rect(WIDTH - 50, 10, 40, 40)
    btnResult = pygame.Rect(SIZE + 1000, 680, 150, 50)

    # --- Nhóm thuật toán (6 nhóm, bạn có thể chỉnh x, y, w, h tùy ý) ---
    groups = [
        # title, x,   y,   w,   h,   buttons
        ("Uninformed Search",  25,  540, 300, 105, ["BFS", "UCS", "DFS", "DLS", "IDS"]),
        ("Informed Search",    350, 670, 300, 65, ["Greedy_S", "A*"]),
        ("Local Search",       350, 540, 300, 105, ["Hill_S", "S_A", "Beam_S", "Gen_A"]),
        ("Nondeterministic",    25, 670, 300, 65, ["AND_OR", "No_OBS", "Part_OBS"]),
        ("CPS", 675, 540, 300, 105, ["BackTr", "ForwCh"])
    ]

    # Biến trạng thái
    steps = None
    current_step = None
    current_algo = None
    result_message = ""
    found = False
    show_mes = 0
    clock = pygame.time.Clock()

    while True:
        mouse_pos = pygame.mouse.get_pos()
        mouse_click = pygame.mouse.get_pressed()
        font = pygame.font.SysFont("Cambria", 18, bold=True)

        # Event xử lý
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                # Nhóm nút thuật toán
                for title, gx, gy, gw, gh, btns in groups:
                    rects = draw_groupBtn(
                        screen, title, gx, gy, btns, font, mouse_pos, mouse_click,
                        group_size=(gw, gh) if gw and gh else None
                    )
                    for name, rect in rects:
                        if rect.collidepoint(event.pos):
                            if name == "BFS": steps = BFS(root, goal); current_algo = "BFS"
                            elif name == "UCS": steps = UCS(root, goal); current_algo = "UCS"
                            elif name == "DFS": steps = DFS(root, goal); current_algo = "DFS"
                            elif name == "DLS": steps = DLS(root, goal, 8); current_algo = "DLS"
                            elif name == "IDS": steps = IDS(root, goal, 1000); current_algo = "IDS"
                            elif name == "Greedy_S": steps = GreedySearch(root, goal); current_algo = "Greedy"
                            elif name == "A*": steps = A_Sao(root, goal); current_algo = "A*"
                            elif name == "Beam_S": steps = Beam_Search(root, goal, 1); current_algo = "Beam"
                            elif name == "Hill_S": steps = Hill_Search(root, goal); current_algo = "Hill"
                            elif name == "S_A": steps = Simulated_Annealing(root, goal); current_algo = "SA"
                            elif name == "Gen_A": steps = Genetic_Algorithm(root, goal); current_algo = "Genetic"
                            elif name == "AND_OR": steps = AND_OR_Search(root, goal); current_algo = "AND_OR"
                            elif name == "No_OBS": NOBS.run_algorithm()
                            elif name == "Part_OBS": POBS.run_algorithm()

                            elif name == "BackTr":
                                start = time.time()
                                steps = backtrack([], giatri)
                                last_state, last_path = None, None
                                total_states = 0
                                try:
                                    while True:
                                        last_state, last_path = next(steps)
                                        total_states += 1
                                        if len(last_path) == N:
                                            break
                                except StopIteration:
                                    pass
                                elapsed = time.time() - start
                                if last_state is not None:
                                    root = last_state  
                                    print("\n=== BACKTRACKING ===")
                                    print(f"Thời gian chạy: {elapsed:.4f}s")
                                    print(f"Tổng số state duyệt: {count_bt}")
                                    print("Đường đi (các vị trí đặt quân xe):")
                                    for i, pos in enumerate(last_path, 1):
                                        print(f"Step {i}: {pos}")
                                    print("\nBoard kết quả:")
                                    print(last_state)
                                steps = None   

                            elif name == "ForwCh":
                                start = time.time()
                                steps = forwardchecking([], giatri)
                                last_state, last_path = None, None
                                total_states = 0
                                try:
                                    while True:
                                        last_state, last_path = next(steps)
                                        total_states += 1
                                        if len(last_path) == N:
                                            break
                                except StopIteration:
                                    pass
                                elapsed = time.time() - start
                                if last_state is not None:
                                    root = last_state   
                                    print("\n=== FORWARD CHECKING ===")
                                    print(f"Thời gian chạy: {elapsed:.4f}s")
                                    print(f"Tổng số state duyệt: {count_fc}")
                                    print("Đường đi (các vị trí đặt quân xe):")
                                    for i, pos in enumerate(last_path, 1):
                                        print(f"Step {i}: {pos}")
                                    print("\nBoard kết quả:")
                                    print(last_state)
                                steps = None
                            if steps is not None:
                                current_step = next(steps, (None, []))
                                result_message, found = "", False

                # Refresh
                if btnRefresh.collidepoint(event.pos):
                    root = np.zeros((8, 8), dtype=int)
                    steps = current_step = current_algo = None
                    result_message, found, show_mes = "", False, 0

                # Xem kết quả cuối
                if btnResult.collidepoint(event.pos) and steps is not None:
                    last_state, last_path = current_step
                    found = False
                    total_states, start_time = 1, time.time()
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

                    if found and last_path:
                        root = last_path[-1]
                        result_message = f"{current_algo} giải được!"
                        show_mes = pygame.time.get_ticks() + 4000
                        print(f"--- {current_algo} path to goal ---")
                        for i, state in enumerate(last_path):
                            print(f"Step {i+1}:\n{state}\n")
                        print(f"Thời gian: {elapsed_time:.4f}s, tổng state: {total_states}")
                    else:
                        result_message = f"{current_algo}: Không tìm thấy!"
                        show_mes = pygame.time.get_ticks() + 5000
                    steps = None

        # Step by step
        if steps is not None and current_step is not None:
            root, path = current_step
            if np.array_equal(root, goal): found = True
            try:
                current_step = next(steps)
            except StopIteration:
                if found:
                    result_message = f"{current_algo} giải thành công!"
                    show_mes = pygame.time.get_ticks() + 4000
                else:
                    result_message = f"{current_algo}: Thất bại!"
                    show_mes = pygame.time.get_ticks() + 5000
                steps = None

        # ============ DRAW ============
        screen.fill((130, 148, 96))
        draw_board(screen, SIZE, SIZE, mouse_pos, board=root)
        draw_board(screen, N * SIZE + 2.5 * MARGIN, SIZE, mouse_pos, board=goal)
        screen.blit(lblEmptyBoard, (SIZE + 150, 4))
        screen.blit(lbl8rooks, (N * SIZE + 2.5 * MARGIN + 150, 4))

        # Nhóm nút
        for title, gx, gy, gw, gh, btns in groups:
            draw_groupBtn(
                screen, title, gx, gy, btns, font, mouse_pos, mouse_click,
                group_size=(gw, gh) if gw and gh else None
            )

        # Nút refresh
        imgRefresh = pygame.image.load("imgs/refresh.png")
        imgRefresh = pygame.transform.smoothscale(imgRefresh, (20, 20))
        draw_Btn(screen, btnRefresh, "", font, mouse_pos, mouse_click, img=imgRefresh)
        draw_Btn(screen, btnResult, "KẾT QUẢ", font, mouse_pos, mouse_click)

        # Thông báo kết quả nhấp nháy
        now = pygame.time.get_ticks()
        if result_message and now < show_mes and (now // 100) % 2 == 0:
            lblMsg = pygame.font.SysFont("Cambria", 22, bold=True).render(result_message, True, 'Red')
            screen.blit(lblMsg, (SIZE + 450, SIZE))

        pygame.display.update()
        clock.tick(15)

if __name__ == "__main__":
    main()
