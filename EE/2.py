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
pygame.display.set_caption("羊了个羊小游戏")

# 字体
font = pygame.font.SysFont('Arial', 50)
small_font = pygame.font.SysFont('Arial', 30)

# 加载或生成图案（这里用不同颜色的矩形来代替图案）
patterns = [pygame.Surface((TILE_SIZE, TILE_SIZE)) for _ in range(6)]
colors = [(255, 0, 0), (0, 255, 0), (0, 0, 255), (255, 255, 0), (0, 255, 255), (255, 0, 255)]
for i, pattern in enumerate(patterns):
    pattern.fill(colors[i])

# 创建音效
match_sound = pygame.mixer.Sound('match.wav')
click_sound = pygame.mixer.Sound('click.wav')
game_over_sound = pygame.mixer.Sound('game_over.wav')

# 创建游戏板，确保每个图案成对出现
board = []
pattern_pairs = patterns * (ROWS * COLS // (2 * len(patterns)))
random.shuffle(pattern_pairs)
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
            match_sound.play()  # 播放匹配音效
        selected.clear()

def main_menu():
    menu_running = True
    while menu_running:
        screen.fill(WHITE)
        title_text = font.render('羊了个羊', True, BLACK)
        screen.blit(title_text, (WIDTH // 2 - title_text.get_width() // 2, HEIGHT // 3))

        start_text = font.render('开始游戏', True, BLACK)
        screen.blit(start_text, (WIDTH // 2 - start_text.get_width() // 2, HEIGHT // 2))

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                menu_running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                click_sound.play()  # 播放点击音效
                menu_running = False
                game_loop()  # 点击进入游戏循环

    pygame.quit()

def game_over():
    game_over_sound.play()  # 播放游戏结束音效
    over_running = True
    while over_running:
        screen.fill(WHITE)
        over_text = font.render('游戏结束', True, BLACK)
        score_text = small_font.render(f'最终得分: {score}', True, BLACK)
        restart_text = small_font.render('点击任意键重新开始', True, BLACK)
        
        screen.blit(over_text, (WIDTH // 2 - over_text.get_width() // 2, HEIGHT // 3))
        screen.blit(score_text, (WIDTH // 2 - score_text.get_width() // 2, HEIGHT // 2))
        screen.blit(restart_text, (WIDTH // 2 - restart_text.get_width() // 2, HEIGHT // 1.5))
        
        pygame.display.flip()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                over_running = False
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
                        click_sound.play()  # 播放点击音效
                if len(selected) == 2:
                    check_match()

        screen.fill(WHITE)
        draw_board()

        # 显示倒计时
        timer_text = small_font.render(f"倒计时: {int(timer)}", True, BLACK)
        screen.blit(timer_text, (10, 10))

        # 显示得分
        draw_score()

        pygame.display.flip()

main_menu()
