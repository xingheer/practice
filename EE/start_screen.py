import pygame

# 不再需要初始化字体，这里只使用
font = pygame.font.SysFont('Arial', 50)
small_font = pygame.font.SysFont('Arial', 30)

def main_menu():
    menu_running = True
    while menu_running:
        screen.fill(WHITE)
        title_text = font.render('喵了个喵', True, BLACK)
        screen.blit(title_text, (WIDTH // 2 - title_text.get_width() // 2, HEIGHT // 3))

        # 绘制“开始游戏”按钮
        start_text = font.render('开始游戏', True, BLACK)
        start_button_rect = start_text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
        screen.blit(start_text, start_button_rect.topleft)

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                menu_running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if start_button_rect.collidepoint(event.pos):
                    menu_running = False
                    game_loop()  # 点击进入游戏循环
