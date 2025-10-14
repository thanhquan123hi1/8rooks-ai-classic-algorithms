import pygame, sys, numpy as np
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
        ("CPS", 675, 540, 300, 105, ["BackTr", "ForwCh"]),
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
    info_panel = {"Thuật toán": "Chưa chọn", "Thời gian": "0.0s", "Số state": "0", "Kết quả": "—"}
    result_message, show_mes = "", 0
    show_detail, detail_lines = False, []

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
                            if new_info:
                                info_panel = new_info
                            if steps is not None:
                                current_step = next(steps, (root, []))
                                result_message = ""

                # --- Nút KẾT QUẢ ---
                if btnResult.collidepoint(event.pos) and steps is not None:
                    info_panel, detail_lines, found = compute_result(steps, goal, current_algo)
                    result_message = f"{current_algo} {'thành công!' if found else 'thất bại!'}"
                    show_mes = pygame.time.get_ticks() + 4000
                    steps = None

                # --- DETAIL ---
                if pygame.Rect(WIDTH - 310 + 100, 100 + 240, 120, 40).collidepoint(event.pos):
                    show_detail = True
                    
                if show_detail:
                    btn_exit = draw_detail_board(screen, font, detail_lines)
                    if event.type == pygame.MOUSEBUTTONDOWN and btn_exit.collidepoint(event.pos):
                        show_detail = False


                # --- REFRESH ---
                if btnRefresh.collidepoint(event.pos):
                    root = np.zeros((8, 8), dtype=int)
                    steps = current_step = current_algo = None
                    info_panel = {"Thuật toán": "Chưa chọn", "Thời gian": "0.0s", "Số state": "0", "Kết quả": "—"}
                    result_message = ""

        # --- Cập nhật bước kế tiếp ---
        if steps is not None and current_step is not None:
            root, path = current_step
            try:
                current_step = next(steps)
            except StopIteration:
                steps = None

        # --- Vẽ giao diện ---
        screen.fill((130, 148, 96))
        draw_board(screen, SIZE, SIZE + 30, mouse_pos, board=root)
        draw_board(screen, N * SIZE + 2.5 * MARGIN, SIZE + 30, mouse_pos, board=goal)
        screen.blit(lblEmpty, (SIZE + 150, 4))
        screen.blit(lblGoal, (N * SIZE + 2.5 * MARGIN + 150, 4))

        for title, gx, gy, gw, gh, btns in groups:
            draw_groupBtn(screen, title, gx, gy, btns, font, mouse_pos, mouse_click, group_size=(gw, gh))

        imgRefresh = pygame.image.load("imgs/refresh.png")
        imgRefresh = pygame.transform.smoothscale(imgRefresh, (20, 20))
        draw_Btn(screen, btnRefresh, "", font, mouse_pos, mouse_click, img=imgRefresh)
        draw_Btn(screen, btnResult, "KẾT QUẢ", font, mouse_pos, mouse_click)
        draw_info_panel(screen, font, WIDTH - 310, 100, 280, 300, info_panel, mouse_pos, mouse_click)

        if show_detail:
            draw_detail_board(screen, font, detail_lines)

        now = pygame.time.get_ticks()
        if result_message and now < show_mes and (now // 100) % 2 == 0:
            lblMsg = pygame.font.SysFont("Cambria", 22, bold=True).render(result_message, True, 'Red')
            screen.blit(lblMsg, (SIZE + 450, SIZE))

        pygame.display.update()
        clock.tick(30)


if __name__ == "__main__":
    main()
