import pygame
import random

# 初始化 Pygame
pygame.init()

# 定义窗口大小和颜色
WIDTH, HEIGHT = 600, 600
TILE_SIZE = 100
ROWS, COLS = 6, 6
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# 创建窗口
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("喵了个喵")

# 加载字体
font = pygame.font.Font('SimHei.ttf', 50)  # 载入中文字体
small_font = pygame.font.Font('SimHei.ttf', 30)  # 载入中文字体

# 加载背景图片
background_image = pygame.image.load(r'C:\Users\lenovo\Desktop\rj\background.jpg')

# 加载图标图片
icon_paths = [
    r'C:\Users\lenovo\Desktop\rj\1.jpg',
    r'C:\Users\lenovo\Desktop\rj\2.jpg',
    r'C:\Users\lenovo\Desktop\rj\3.jpg',
    r'C:\Users\lenovo\Desktop\rj\4.jpg',
    r'C:\Users\lenovo\Desktop\rj\5.jpg',
    r'C:\Users\lenovo\Desktop\rj\6.jpg'
]
patterns = [pygame.transform.scale(pygame.image.load(path), (TILE_SIZE, TILE_SIZE)) for path in icon_paths]

# 创建游戏板，确保每个图案成对出现
num_tiles = ROWS * COLS
num_pairs = num_tiles // 2
pattern_pairs = (patterns * (num_pairs // len(patterns) + 1))[:num_pairs] * 2  # 确保有足够的图案对并成对
random.shuffle(pattern_pairs)

board = []
for row in range(ROWS):
    board.append([pattern_pairs.pop() for _ in range(COLS)])

selected = []
score = 0

def update_score():
    global score
    score += 10

def draw_score():
    score_text = small_font.render(f"得分: {score}", True, BLACK)
    screen.blit(score_text, (WIDTH - 150, 10))

def draw_board():
    for row in range(ROWS):
        for col in range(COLS):
            tile = board[row][col]
            if tile is not None:
                screen.blit(tile, (col * TILE_SIZE, row * TILE_SIZE))

def check_match():
    if len(selected) == 2:
        r1, c1 = selected[0]
        r2, c2 = selected[1]
        if (r1, c1) != (r2, c2) and board[r1][c1] == board[r2][c2]:  # 防止选择同一个格子两次
            board[r1][c1] = None  # 移除匹配的图案
            board[r2][c2] = None
            update_score()  # 增加得分
        selected.clear()

def check_win():
    for row in board:
        for tile in row:
            if tile is not None:
                return False
    return True

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
                pygame.quit()
                quit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if start_button_rect.collidepoint(event.pos):
                    menu_running = False
                    game_loop()  # 点击进入游戏循环

def game_over(win=False):
    over_running = True
    while over_running:
        screen.fill(WHITE)
        if win:
            over_text = font.render('恭喜喵喵成功！', True, BLACK)
        else:
            over_text = font.render('游戏结束', True, BLACK)
        
        score_text = small_font.render(f'最终得分: {score}', True, BLACK)
        restart_text = small_font.render('点击任意键重新开始', True, BLACK)
        
        screen.blit(over_text, (WIDTH // 2 - over_text.get_width() // 2, HEIGHT // 3))
        screen.blit(score_text, (WIDTH // 2 - score_text.get_width() // 2, HEIGHT // 2))
        screen.blit(restart_text, (WIDTH // 2 - restart_text.get_width() // 2, HEIGHT // 1.5))
        
        pygame.display.flip()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            elif event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:
                over_running = False
                main_menu()  # 返回主菜单

def game_loop():
    global selected, score
    running = True
    timer = 60  # 倒计时60秒
    clock = pygame.time.Clock()
    score = 0
    selected = []

    while running:
        dt = clock.tick(30) / 1000  # 每帧的时间
        timer -= dt  # 更新倒计时
        if timer <= 0:
            running = False
            game_over()  # 显示游戏结束画面

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos
                col, row = x // TILE_SIZE, y // TILE_SIZE
                if board[row][col] is not None:
                    if (row, col) not in selected:
                        selected.append((row, col))
                if len(selected) == 2:
                    check_match()

        # 检查是否全部消除
        if check_win():
            running = False
            game_over(win=True)  # 显示游戏成功画面

        # 绘制背景
        screen.blit(background_image, (0, 0))

        # 绘制游戏板
        draw_board()

        # 显示倒计时
        timer_text = small_font.render(f"倒计时: {int(timer)}", True, BLACK)
        screen.blit(timer_text, (10, 10))

        # 显示得分
        draw_score()

        pygame.display.flip()

main_menu()
