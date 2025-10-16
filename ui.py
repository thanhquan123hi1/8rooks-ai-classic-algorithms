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

def draw_info_panel(screen, font, x, y, w, h, info, mouse_pos, mouse_click):
    """Vẽ panel thông tin bên phải"""
    pygame.draw.rect(screen, (230, 230, 230), (x, y, w, h), border_radius=12)
    pygame.draw.rect(screen, (0, 0, 0), (x, y, w, h), 2, border_radius=12)

    # Tiêu đề
    title = font.render("THÔNG TIN THUẬT TOÁN", True, (20, 20, 120))
    screen.blit(title, (x + 10, y + 10))

    # Vẽ từng dòng thông tin
    offset_y = y + 45
    for key, value in info.items():
        text = font.render(f"{key}: {value}", True, (0, 0, 0))
        screen.blit(text, (x + 15, offset_y))
        offset_y += 28

    # Nút DETAIL
    btn_detail = pygame.Rect(x + w // 2 - 60, y + h - 60, 120, 40)
    draw_Btn(screen, btn_detail, "DETAIL", font, mouse_pos, mouse_click)
    return btn_detail


def draw_detail_board(screen, font, detail_texts):
    overlay = pygame.Surface(screen.get_size(), pygame.SRCALPHA)
    overlay.fill((0, 0, 0, 180))
    screen.blit(overlay, (0, 0))

    # Kích thước bảng mở rộng
    box_w, box_h = 700, 500
    box_x = (screen.get_width() - box_w) // 2
    box_y = (screen.get_height() - box_h) // 2

    # Vẽ khung nền
    pygame.draw.rect(screen, (255, 255, 255), (box_x, box_y, box_w, box_h), border_radius=10)
    pygame.draw.rect(screen, (0, 0, 0), (box_x, box_y, box_w, box_h), 2, border_radius=10)

    title = font.render("CHI TIẾT THUẬT TOÁN", True, (0, 0, 80))
    screen.blit(title, (box_x + box_w // 2 - title.get_width() // 2, box_y + 15))

    btn_exit = pygame.Rect(box_x + box_w - 90, box_y + 15, 70, 35)
    draw_Btn(screen, btn_exit, "EXIT", font, pygame.mouse.get_pos(), pygame.mouse.get_pressed())
    
    # Nội dung chi tiết
    y_offset = box_y + 65
    for line in detail_texts:
        if line.startswith("Step") and "[[" in line:
            try:
                # Lấy ma trận từ chuỗi
                matrix_str = line.split(":")[1].strip()
                matrix = eval(matrix_str)
                coords = [(r, c) for r in range(len(matrix))
                          for c in range(len(matrix[r])) if matrix[r][c] == 1]
                text = f"{line.split(':')[0]}: {coords}"
            except Exception:
                text = line
        else:
            text = line

        wrapped = wrap_text(text, font, box_w - 40)
        for subline in wrapped:
            text_surf = font.render(subline, True, (0, 0, 0))
            screen.blit(text_surf, (box_x + 20, y_offset))
            y_offset += 24
            if y_offset > box_y + box_h - 50:
                break

    return btn_exit


def wrap_text(text, font, max_width):
    """Tự động xuống dòng khi text quá dài."""
    words = text.split(' ')
    lines = []
    current_line = ""
    for word in words:
        test_line = current_line + word + " "
        if font.size(test_line)[0] < max_width:
            current_line = test_line
        else:
            lines.append(current_line)
            current_line = word + " "
    lines.append(current_line)
    return lines
