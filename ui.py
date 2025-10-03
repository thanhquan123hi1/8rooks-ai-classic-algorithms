import pygame

N = 8
SIZE = 60

def draw_Btn(screen, btn, txt, font, mouse_pos, mouse_click,
             color_nor=(250, 165, 51),
             color_hover=(255, 237, 198),
             color_click=(200, 120, 20),
             border_color=(0, 0, 0),
             border_radius=10,
             border_width=2,
             img=None):
    # Xác định trạng thái màu
    if btn.collidepoint(mouse_pos):
        if mouse_click[0]:  # Chuột trái
            color = color_click
        else:
            color = color_hover
    else:
        color = color_nor

    # Vẽ nền button
    pygame.draw.rect(screen, color, btn, border_radius=border_radius)
    # Vẽ viền button
    pygame.draw.rect(screen, border_color, btn,
                     width=border_width, border_radius=border_radius)

    # Vẽ ảnh
    if img is not None:
        img_rect = img.get_rect(center=btn.center)
        screen.blit(img, img_rect)

    # Vẽ text
    if txt:
        lbl = font.render(txt, True, border_color)
        lbl_rect = lbl.get_rect(center=btn.center)
        screen.blit(lbl, lbl_rect)


def draw_board(screen, offset_x, offset_y, mouse_pos, board=None):
    """Vẽ bàn cờ và quân xe"""
    for row in range(N):
        for col in range(N):
            x = offset_x + col * SIZE
            y = offset_y + row * SIZE

            # Màu cơ bản
            base_color = (240, 217, 178) if (row + col) % 2 == 0 else (181, 136, 96)
            rect = pygame.Rect(x, y, SIZE, SIZE)

            # Nếu chuột đang ở ô này → làm sáng màu
            if rect.collidepoint(mouse_pos):
                color = tuple(min(255, c + 40) for c in base_color)  # sáng hơn
                scale = 1.  # phóng to nhẹ
                new_size = int(SIZE * scale)
                rect = pygame.Rect(
                    x - (new_size - SIZE) // 2,
                    y - (new_size - SIZE) // 2,
                    new_size, new_size
                )
            else:
                color = base_color

            pygame.draw.rect(screen, color, rect)
            # Viền đen phía trên và trái
            pygame.draw.line(screen, (0, 0, 0), (x, y), (x + SIZE, y), 1)       # trên
            pygame.draw.line(screen, (0, 0, 0), (x, y), (x, y + SIZE), 1)       # trái
            # Viền đen phía dưới và phải
            pygame.draw.line(screen, (0, 0, 0), (x, y + SIZE), (x + SIZE, y + SIZE), 1) # dưới
            pygame.draw.line(screen, (0, 0, 0), (x + SIZE, y), (x + SIZE, y + SIZE), 1) # phải


    # Vẽ quân xe
    if board is not None:
        imgRook = pygame.image.load("imgs/w_rook.png")
        base_size = SIZE // 1.5
        imgRook = pygame.transform.smoothscale(imgRook, (base_size, base_size))

        for r in range(N):
            for c in range(N):
                if board[r][c] == 1:
                    x = offset_x + c * SIZE + (SIZE - base_size) // 2
                    y = offset_y + r * SIZE + (SIZE - base_size) // 2

                    # Nếu chuột hover ô chứa quân cờ → phóng to quân cờ
                    cell_rect = pygame.Rect(offset_x + c * SIZE, offset_y + r * SIZE, SIZE, SIZE)
                    if cell_rect.collidepoint(mouse_pos):
                        bigger = int(base_size * 1.2)
                        imgHover = pygame.transform.smoothscale(imgRook, (bigger, bigger))
                        x = offset_x + c * SIZE + (SIZE - bigger) // 2
                        y = offset_y + r * SIZE + (SIZE - bigger) // 2
                        screen.blit(imgHover, (x, y))
                    else:
                        screen.blit(imgRook, (x, y))

def draw_groupBtn(screen, title, x, y, buttons, font,
                  mouse_pos, mouse_click,
                  cols=3,
                  group_size=None, 
                  bg_color=(200, 230, 200),
                  border_color=(0, 0, 0),
                  border_radius=10,
                  border_width=2):
    # Tính toán kích thước group
    if group_size is None:
        # mỗi button cao ~40, rộng ~90
        rows = (len(buttons) + cols - 1) // cols
        w = max(100, cols * 95 + 20)   # chừa padding
        h = max(50, rows * 40 + 40)    # chừa padding + title
    else:
        w, h = group_size

    # Vẽ khung nhóm
    group_rect = pygame.Rect(x, y, w, h)
    pygame.draw.rect(screen, bg_color, group_rect, border_radius=border_radius)
    pygame.draw.rect(screen, border_color, group_rect,
                     width=border_width, border_radius=border_radius)

    # Vẽ tiêu đề
    title_surf = font.render(title, True, (0, 0, 80))
    screen.blit(title_surf, (x + 5, y + 2))

    # Vẽ từng button
    btn_rects = []
    for i, name in enumerate(buttons):
        bx = x + 10 + (i % cols) * 95
        by = y + 25 + (i // cols) * 40
        rect = pygame.Rect(bx, by, 85, 30)
        draw_Btn(screen, rect, name, font, mouse_pos, mouse_click)
        btn_rects.append((name, rect))

    return btn_rects

def drawInfor():
    pass