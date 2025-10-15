import pygame, sys, numpy as np, time
from ui import *
from controller import run_algorithm, compute_result

N = 8
SIZE = 15
MARGIN = 160
WIDTH, HEIGHT = 1450, 750


def init_game():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("8 Rooks")

    root = np.zeros((8, 8), dtype=int)
    goal = np.array([
        [0,0,0,0,0,0,1,0],
        [0,0,0,0,0,1,0,0],
        [0,0,0,0,1,0,0,0],
        [1,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,1],
        [0,0,0,1,0,0,0,0],
        [0,1,0,0,0,0,0,0],
        [0,0,1,0,0,0,0,0],
    ])

    groups = [
        ("Uninformed Search", 25, 540, 300, 105, ["BFS", "UCS", "DFS", "DLS", "IDS"]),
        ("Informed Search", 350, 670, 300, 65, ["Greedy_S", "A*"]),
        ("Local Search", 350, 540, 300, 105, ["Hill_S", "S_A", "Beam_S", "Gen_A"]),
        ("Nondeterministic", 25, 670, 300, 65, ["AND_OR", "No_OBS", "Part_OBS"]),
        ("CSP", 675, 540, 300, 140, ["BackTr", "ForwCh", "AC3"]),
    ]

    lblEmpty = pygame.font.SysFont("Cambria", 30, bold=True).render("BÀN CỜ RỖNG", True, (0, 0, 80))
    lblGoal = pygame.font.SysFont("Cambria", 30, bold=True).render("BÀN CỜ MẪU", True, (0, 0, 80))

    btnRefresh = pygame.Rect(WIDTH - 50, 10, 40, 40)
    btnResult = pygame.Rect(SIZE + 1000, 680, 150, 50)
    return screen, root, goal, groups, lblEmpty, lblGoal, btnRefresh, btnResult


def main():
    screen, root, goal, groups, lblEmpty, lblGoal, btnRefresh, btnResult = init_game()
    clock = pygame.time.Clock()
    steps = current_step = current_algo = None
    path_generator = None
    info_panel = {"Thuật toán": "Chưa chọn", "Thời gian": "0.0s", "Số state": "0", "Kết quả": "—"}
    result_message, show_mes = "", 0
    show_detail, detail_lines = False, []
    start_time = 0

    while True:
        mouse_pos, mouse_click = pygame.mouse.get_pos(), pygame.mouse.get_pressed()
        font = pygame.font.SysFont("Cambria", 18, bold=True)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            # --- Click chọn thuật toán ---
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                for title, gx, gy, gw, gh, btns in groups:
                    rects = draw_groupBtn(screen, title, gx, gy, btns, font, mouse_pos, mouse_click, group_size=(gw, gh))
                    for name, rect in rects:
                        if rect.collidepoint(event.pos):
                            result = run_algorithm(name, root, goal)
                            if result is None:
                                continue
                            steps, current_algo, new_info, detail_lines = result
                            path_generator = steps
                            if new_info:
                                info_panel = new_info
                            if steps is not None:
                                current_step = next(steps, (root, []))
                                start_time = time.time()  # bắt đầu tính giờ
                                result_message = ""

                # --- Nút KẾT QUẢ ---
                if btnResult.collidepoint(event.pos) and path_generator is not None:
                    info_panel, detail_lines, found, final_state = compute_result(path_generator, goal, current_algo)
                    result_message = f"{current_algo} {'thành công!' if found else 'thất bại!'}"
                    show_mes = pygame.time.get_ticks() + 4000
                    steps = None

                    # ✅ Hiển thị trạng thái cuối cùng lên bàn cờ rỗng
                    if isinstance(final_state, np.ndarray):
                        root = final_state.copy()

                # --- REFRESH ---
                if btnRefresh.collidepoint(event.pos):
                    root = np.zeros((8, 8), dtype=int)
                    steps = current_step = current_algo = path_generator = None
                    info_panel = {"Thuật toán": "Chưa chọn", "Thời gian": "0.0s", "Số state": "0", "Kết quả": "—"}
                    result_message = ""

        # --- Cập nhật từng bước ---
        if steps is not None and current_step is not None:
            root, path = current_step
            try:
                current_step = next(steps)
            except StopIteration:
                if path:
                    elapsed_time = time.time() - start_time
                    total_states = len(path)
                    found = np.array_equal(path[-1], goal)

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

                    for i, state in enumerate(path):
                        if isinstance(state, np.ndarray):
                            detail_lines.append(f"Step {i+1}: {state.tolist()}")
                        else:
                            detail_lines.append(f"Step {i+1}: {state}")

                    result_message = f"{current_algo} {'thành công!' if found else 'thất bại!'}"
                    show_mes = pygame.time.get_ticks() + 4000

                steps = None

        # --- Vẽ giao diện ---
        screen.fill((130, 148, 96))
        draw_board(screen, SIZE, SIZE + 30, mouse_pos, board=root)
        draw_board(screen, N * SIZE + 2.5 * MARGIN, SIZE + 30, mouse_pos, board=goal)
        screen.blit(lblEmpty, (SIZE + 150, 4))
        screen.blit(lblGoal, (N * SIZE + 2.5 * MARGIN + 150, 4))

        # Các nhóm nút thuật toán
        for title, gx, gy, gw, gh, btns in groups:
            draw_groupBtn(screen, title, gx, gy, btns, font, mouse_pos, mouse_click, group_size=(gw, gh))

        # --- Nút refresh & kết quả ---
        imgRefresh = pygame.image.load("imgs/refresh.png")
        imgRefresh = pygame.transform.smoothscale(imgRefresh, (20, 20))
        draw_Btn(screen, btnRefresh, "", font, mouse_pos, mouse_click, img=imgRefresh)
        draw_Btn(screen, btnResult, "KẾT QUẢ", font, mouse_pos, mouse_click)

        # --- Panel thông tin lớn hơn ---
        btn_detail = draw_info_panel(screen, pygame.font.SysFont("Cambria", 20, bold=True),
                                     WIDTH - 380, 60, 350, 400, info_panel, mouse_pos, mouse_click)

        # ✅ Xử lý click cho nút DETAIL (sử dụng đúng btn_detail trả về)
        if pygame.mouse.get_pressed()[0] and btn_detail.collidepoint(mouse_pos):
            show_detail = True

        # ✅ Hiển thị panel chi tiết
        if show_detail:
            btn_exit = draw_detail_board(screen, font, detail_lines)
            if mouse_click[0] and btn_exit.collidepoint(mouse_pos):
                show_detail = False

        # --- Dòng kết quả nhấp nháy đỏ ---
        now = pygame.time.get_ticks()
        if result_message and now < show_mes and (now // 100) % 2 == 0:
            lblMsg = pygame.font.SysFont("Cambria", 22, bold=True).render(result_message, True, 'Red')
            screen.blit(lblMsg, (WIDTH//2 - lblMsg.get_width()//2 + 100, HEIGHT - 60))

        pygame.display.update()
        clock.tick(30)


if __name__ == "__main__":
    main()
