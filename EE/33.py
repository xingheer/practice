import pygame
import random

# 初始化 Pygame
pygame.init()
# 定义颜色
GREEN = (0, 255, 0)

# 定义窗口大小和颜色
WIDTH, HEIGHT = 600, 600
TILE_SIZE = 80
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
YELLOW = (255, 255, 0)  # 添加绿色定义

# 创建窗口
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("喵了个喵")

# 加载字体
font = pygame.font.Font('SimHei.ttf', 50)  # 载入中文字体
small_font = pygame.font.Font('SimHei.ttf', 30)  # 载入中文字体

# 加载背景图片
background_image = pygame.image.load('background.jpg')  # 替换为你的背景图片路径

# 加载图标图片
icon_paths = [
    '1.jpg', '2.jpg', '3.jpg', '4.jpg', '5.jpg', '6.jpg'
]
patterns = [pygame.transform.scale(pygame.image.load(path), (TILE_SIZE, TILE_SIZE)) for path in icon_paths]

# 确保每个图标的数量是3的倍数
def get_correct_icon_count(patterns):
    count_per_icon = 3
    total_icons = len(patterns) * count_per_icon
    return total_icons

def create_layers():
    total_icons = get_correct_icon_count(patterns)
    all_icons = [pattern for pattern in patterns for _ in range(3)]  # 确保每种图标出现3次
    random.shuffle(all_icons)  # 随机打乱图标顺序

    layers = []
    for _ in range(3):  # 创建3层
        layer = []
        for _ in range(15):  # 每层随机放置15个图标
            if all_icons:
                tile = all_icons.pop()
                x = random.randint(0, WIDTH - TILE_SIZE)
                y = random.randint(0, HEIGHT - TILE_SIZE - 80)  # 确保图标不在底部方框区域
                layer.append((tile, x, y))
        layers.append(layer)
    return layers

layers = create_layers()

selected = []
score = 0
paused = False
timer_running = True

# 底部方框
bottom_box = []

def update_score():
    global score
    score += 10

def draw_score():
    score_text = small_font.render(f"得分: {score}", True, BLACK)
    screen.blit(score_text, (WIDTH - 150, 10))

def draw_layers():
    for layer in layers:
        for tile, x, y in layer:
            if tile is not None:
                tile.set_alpha(180)  # 设置图标透明度
                screen.blit(tile, (x, y))

def draw_bottom_box():
    pygame.draw.rect(screen, BLACK, (0, HEIGHT - 80, WIDTH, 80))
    # 显示底部方框中的图标
    for i, (tile, _) in enumerate(bottom_box):
        if i < 5:  # 只显示前5个图标
            tile.set_alpha(255)
            screen.blit(tile, (i * (TILE_SIZE + 5) + 10, HEIGHT - 70))

def check_click(pos):
    global selected
    # 从顶层往底层检查，找到可点击的图标
    for layer in reversed(layers):
        for i, (tile, x, y) in enumerate(layer):
            if tile is not None and x < pos[0] < x + TILE_SIZE and y < pos[1] < y + TILE_SIZE:
                selected.append((tile, x, y))
                if len(selected) > 5:
                    selected.pop(0)  # 保持底部框中最多5个图标
                # 移除点击的图标
                layer[i] = (None, 0, 0)
                # 移动到底部方框
                bottom_box.append((tile, (x, y)))
                if len(bottom_box) > 5:
                    bottom_box.pop(0)  # 保持底部框中最多5个图标
                return

def check_match():
    if len(bottom_box) >= 3:
        tile_counts = {}
        for tile, _ in bottom_box:
            if tile in tile_counts:
                tile_counts[tile] += 1
            else:
                tile_counts[tile] = 1
        
        to_remove = [tile for tile, count in tile_counts.items() if count >= 3]
        if to_remove:
            global score
            score += 30  # 每消除3个图标增加30分
            new_bottom_box = [item for item in bottom_box if item[0] not in to_remove]
            bottom_box.clear()
            bottom_box.extend(new_bottom_box)

def check_bottom_box():
    # 检查底部方框中是否有三个相同的图标
    if len(bottom_box) == 5:
        tile_counts = {}
        for tile, _ in bottom_box:
            if tile in tile_counts:
                tile_counts[tile] += 1
            else:
                tile_counts[tile] = 1
        
        for count in tile_counts.values():
            if count >= 3:
                return True
        return False
    return True

def check_win():
    for layer in layers:
        for tile, _, _ in layer:
            if tile is not None:
                return False
    return True
def draw_button(rect, text, font, text_color=BLACK, bg_color=YELLOW):
    pygame.draw.ellipse(screen, bg_color, rect)
    pygame.draw.ellipse(screen, WHITE, rect, 2)  # 绘制按钮边框
    text_surf = font.render(text, True, text_color)
    text_rect = text_surf.get_rect(center=rect.center)
    screen.blit(text_surf, text_rect)

# 使用示例
def draw_pause_button():
    button_rect = pygame.Rect(WIDTH - 60, 38, 50, 50)
    draw_button(button_rect, 'P' if not paused else 'S', small_font)



def game_loop():
    global selected, score, paused, timer_running
    running = True
    timer = 60  # 倒计时60秒
    clock = pygame.time.Clock()
    score = 0
    selected = []
    paused = False
    timer_running = True

    while running:
        dt = clock.tick(30) / 1000  # 每帧的时间
        if timer_running:
            timer -= dt  # 更新倒计时
        if timer <= 0:
            running = False
            game_over()  # 显示游戏结束画面

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                pos = event.pos
                if pygame.Rect(WIDTH - 60, 10, 50, 50).collidepoint(pos):
                    # 切换暂停和继续
                    paused = not paused
                    timer_running = not paused
                elif not paused:
                    check_click(pos)
                    check_match()  # 检查底部方框中是否有可消除的图标
                    if not check_bottom_box():
                        running = False
                        game_over()  # 显示游戏失败画面

        # 检查是否全部消除
        if check_win():
            running = False
            game_over(win=True)  # 显示游戏成功画面

        # 绘制背景
        screen.blit(background_image, (0, 0))

        # 绘制堆叠图标
        draw_layers()

        # 绘制底部框
        draw_bottom_box()

        # 显示倒计时
        timer_text = small_font.render(f"倒计时: {int(timer)}", True, BLACK)
        screen.blit(timer_text, (10, 10))

        # 显示得分
        draw_score()

        # 绘制暂停按钮
        draw_pause_button()

        pygame.display.flip()


def game_over(win=False):
    over_running = True
    while over_running:
        if win:
            screen.blit(pygame.image.load('success_background.jpg'), (0, 0))  # 成功页面背景
            over_text = font.render('恭喜喵喵成功！', True, BLACK)
            over_text_rect = over_text.get_rect(center=(WIDTH // 2, HEIGHT // 3))
        else:
            screen.blit(pygame.image.load('failure_background.jpg'), (0, 0))  # 失败页面背景
            over_text = font.render('游戏失败！', True, BLACK)
            over_text_rect = over_text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
            
            fail_text = small_font.render('你不要在这里和我喵喵叫~', True, BLACK)
            fail_text_rect = fail_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 150))
            screen.blit(fail_text, fail_text_rect)

        score_text = small_font.render(f'最终得分: {score}', True, BLACK)
        score_text_rect = score_text.get_rect(center=(WIDTH // 2, HEIGHT // 1.5))
        restart_text = small_font.render('点击空白处重新开始', True, BLACK)
        restart_text_rect = restart_text.get_rect(center=(WIDTH // 2, HEIGHT // 1.2))

        screen.blit(over_text, over_text_rect)
        screen.blit(score_text, score_text_rect)
        screen.blit(restart_text, restart_text_rect)

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                over_running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                over_running = False
                main_menu()  # 返回主菜单

def enter_meow_group():
    entering_meow_running = True
    while entering_meow_running:
        screen.fill(WHITE)
        screen.blit(background_image, (0, 0))

        enter_button_rect = pygame.Rect(WIDTH // 2 - 100, HEIGHT // 2 - 25, 200, 50)
        mode_button_rect = pygame.Rect(WIDTH // 2 - 100, HEIGHT // 2 + 50, 200, 50)  # 模式选择按钮

        pygame.draw.rect(screen, BLACK, enter_button_rect)
        pygame.draw.rect(screen, BLACK, mode_button_rect)

        enter_text = small_font.render('进入喵群', True, WHITE)
        mode_text = small_font.render('选择模式', True, WHITE)
        screen.blit(enter_text, (enter_button_rect.x + 50, enter_button_rect.y + 10))
        screen.blit(mode_text, (mode_button_rect.x + 50, mode_button_rect.y + 10))

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                entering_meow_running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if enter_button_rect.collidepoint(event.pos):
                    entering_meow_running = False
                    game_loop()  # 开始游戏
                elif mode_button_rect.collidepoint(event.pos):
                    select_mode()  # 选择模式
def select_mode():
    mode_running = True
    while mode_running:
        screen.fill(WHITE)
        screen.blit(background_image, (0, 0))

        easy_button_rect = pygame.Rect(WIDTH // 2 - 100, HEIGHT // 2 - 25, 200, 50)
        difficult_button_rect = pygame.Rect(WIDTH // 2 - 100, HEIGHT // 2 + 50, 200, 50)

        pygame.draw.rect(screen, BLACK, easy_button_rect)
        pygame.draw.rect(screen, BLACK, difficult_button_rect)

        easy_text = small_font.render('简单模式', True, WHITE)
        difficult_text = small_font.render('困难模式', True, WHITE)
        screen.blit(easy_text, (easy_button_rect.x + 50, easy_button_rect.y + 10))
        screen.blit(difficult_text, (difficult_button_rect.x + 50, difficult_button_rect.y + 10))

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                mode_running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if easy_button_rect.collidepoint(event.pos):
                    mode_running = False
                    enter_meow_group()  # 进入喵群页面，选择简单模式
                elif difficult_button_rect.collidepoint(event.pos):
                    mode_running = False
                    print("困难模式代码暂时未实现")
                    # 你可以在这里添加困难模式代码

        settings_background = pygame.image.load('background_image.jpg')
           
def settings_page():
    running = True
    while running:
        screen.blit(settings_background, (0, 0))
        
        draw_button(pygame.Rect(WIDTH // 4 - 100, HEIGHT // 4, 200, 50), '游戏说明', font, BLACK, YELLOW)
        draw_button(pygame.Rect(WIDTH // 4 - 100, HEIGHT // 2, 200, 50), '游戏商店', font, BLACK, YELLOW)
        draw_button(pygame.Rect(WIDTH // 4 - 100, HEIGHT * 3 // 4, 200, 50), '星河之家', font, BLACK, YELLOW)

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                pos = event.pos
                if pygame.Rect(WIDTH // 4 - 100, HEIGHT // 4, 200, 50).collidepoint(pos):
                    game_instructions()
                elif pygame.Rect(WIDTH // 4 - 100, HEIGHT // 2, 200, 50).collidepoint(pos):
                    game_store()
                elif pygame.Rect(WIDTH // 4 - 100, HEIGHT * 3 // 4, 200, 50).collidepoint(pos):
                    # 星河之家，暂时不设计
                    pass

def game_instructions():
    running = True
    while running:
        screen.blit(background_image, (0, 0))
        
        instruction_text = """
        欢迎来到《喵了个喵》！

        在这个游戏中，你将面临各种各样的图标挑战。游戏的目标是通过点击并消除底部方框中的相同图标来获得高分。底部方框中最多显示5个图标，如果有三个相同的图标，就会消除它们。游戏时间有限，快来挑战自己的高分吧！

        快速点击和策略是获得高分的关键。希望你能在游戏中找到乐趣！

        祝好运！
        """
        instructions_surf = small_font.render(instruction_text, True, BLACK)
        instructions_rect = instructions_surf.get_rect(center=(WIDTH // 2, HEIGHT // 2))
        screen.blit(instructions_surf, instructions_rect)

        draw_button(pygame.Rect(WIDTH // 2 - 100, HEIGHT * 3 // 4, 200, 50), '返回', font, BLACK, YELLOW)
        
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                pos = event.pos
                if pygame.Rect(WIDTH // 2 - 100, HEIGHT * 3 // 4, 200, 50).collidepoint(pos):
                    return

def game_store():
    running = True
    while running:
        screen.blit(background_image, (0, 0))

        items = [
            ("道具1", 5),
            ("道具2", 7),
            ("道具3", 10)
        ]

        y_offset = HEIGHT // 6
        for item, price in items:
            draw_button(pygame.Rect(WIDTH // 4 - 100, y_offset, 200, 50), f"{item} - {price}元", font, BLACK, YELLOW)
            y_offset += 60

        draw_button(pygame.Rect(WIDTH // 2 - 100, HEIGHT * 3 // 4, 200, 50), '返回', font, BLACK, YELLOW)
        
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                pos = event.pos
                if pygame.Rect(WIDTH // 2 - 100, HEIGHT * 3 // 4, 200, 50).collidepoint(pos):
                    return
import pygame
import random

# 初始化 Pygame
pygame.init()
# 定义颜色
GREEN = (0, 255, 0)

# 定义窗口大小和颜色
WIDTH, HEIGHT = 600, 600
TILE_SIZE = 80
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
YELLOW = (255, 255, 0)  # 添加绿色定义

# 创建窗口
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("喵了个喵")

# 加载字体
font = pygame.font.Font('SimHei.ttf', 50)  # 载入中文字体
small_font = pygame.font.Font('SimHei.ttf', 30)  # 载入中文字体

# 加载背景图片
background_image = pygame.image.load('background.jpg')  # 替换为你的背景图片路径

# 加载图标图片
icon_paths = [
    '1.jpg', '2.jpg', '3.jpg', '4.jpg', '5.jpg', '6.jpg'
]
patterns = [pygame.transform.scale(pygame.image.load(path), (TILE_SIZE, TILE_SIZE)) for path in icon_paths]

# 确保每个图标的数量是3的倍数
def get_correct_icon_count(patterns):
    count_per_icon = 3
    total_icons = len(patterns) * count_per_icon
    return total_icons

def create_layers():
    total_icons = get_correct_icon_count(patterns)
    all_icons = [pattern for pattern in patterns for _ in range(3)]  # 确保每种图标出现3次
    random.shuffle(all_icons)  # 随机打乱图标顺序

    layers = []
    for _ in range(3):  # 创建3层
        layer = []
        for _ in range(15):  # 每层随机放置15个图标
            if all_icons:
                tile = all_icons.pop()
                x = random.randint(0, WIDTH - TILE_SIZE)
                y = random.randint(0, HEIGHT - TILE_SIZE - 80)  # 确保图标不在底部方框区域
                layer.append((tile, x, y))
        layers.append(layer)
    return layers

layers = create_layers()

selected = []
score = 0
paused = False
timer_running = True

# 底部方框
bottom_box = []

def update_score():
    global score
    score += 10

def draw_score():
    score_text = small_font.render(f"得分: {score}", True, BLACK)
    screen.blit(score_text, (WIDTH - 150, 10))

def draw_layers():
    for layer in layers:
        for tile, x, y in layer:
            if tile is not None:
                tile.set_alpha(180)  # 设置图标透明度
                screen.blit(tile, (x, y))

def draw_bottom_box():
    pygame.draw.rect(screen, BLACK, (0, HEIGHT - 80, WIDTH, 80))
    # 显示底部方框中的图标
    for i, (tile, _) in enumerate(bottom_box):
        if i < 5:  # 只显示前5个图标
            tile.set_alpha(255)
            screen.blit(tile, (i * (TILE_SIZE + 5) + 10, HEIGHT - 70))

def check_click(pos):
    global selected
    # 从顶层往底层检查，找到可点击的图标
    for layer in reversed(layers):
        for i, (tile, x, y) in enumerate(layer):
            if tile is not None and x < pos[0] < x + TILE_SIZE and y < pos[1] < y + TILE_SIZE:
                selected.append((tile, x, y))
                if len(selected) > 5:
                    selected.pop(0)  # 保持底部框中最多5个图标
                # 移除点击的图标
                layer[i] = (None, 0, 0)
                # 移动到底部方框
                bottom_box.append((tile, (x, y)))
                if len(bottom_box) > 5:
                    bottom_box.pop(0)  # 保持底部框中最多5个图标
                return

def check_match():
    if len(bottom_box) >= 3:
        tile_counts = {}
        for tile, _ in bottom_box:
            if tile in tile_counts:
                tile_counts[tile] += 1
            else:
                tile_counts[tile] = 1
        
        to_remove = [tile for tile, count in tile_counts.items() if count >= 3]
        if to_remove:
            global score
            score += 30  # 每消除3个图标增加30分
            new_bottom_box = [item for item in bottom_box if item[0] not in to_remove]
            bottom_box.clear()
            bottom_box.extend(new_bottom_box)

def check_bottom_box():
    # 检查底部方框中是否有三个相同的图标
    if len(bottom_box) == 5:
        tile_counts = {}
        for tile, _ in bottom_box:
            if tile in tile_counts:
                tile_counts[tile] += 1
            else:
                tile_counts[tile] = 1
        
        for count in tile_counts.values():
            if count >= 3:
                return True
        return False
    return True

def check_win():
    for layer in layers:
        for tile, _, _ in layer:
            if tile is not None:
                return False
    return True
def draw_button(rect, text, font, text_color=BLACK, bg_color=YELLOW):
    pygame.draw.ellipse(screen, bg_color, rect)
    pygame.draw.ellipse(screen, WHITE, rect, 2)  # 绘制按钮边框
    text_surf = font.render(text, True, text_color)
    text_rect = text_surf.get_rect(center=rect.center)
    screen.blit(text_surf, text_rect)

# 使用示例
def draw_pause_button():
    button_rect = pygame.Rect(WIDTH - 60, 38, 50, 50)
    draw_button(button_rect, 'P' if not paused else 'S', small_font)



def game_loop():
    global selected, score, paused, timer_running
    running = True
    timer = 60  # 倒计时60秒
    clock = pygame.time.Clock()
    score = 0
    selected = []
    paused = False
    timer_running = True

    while running:
        dt = clock.tick(30) / 1000  # 每帧的时间
        if timer_running:
            timer -= dt  # 更新倒计时
        if timer <= 0:
            running = False
            game_over()  # 显示游戏结束画面

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                pos = event.pos
                if pygame.Rect(WIDTH - 60, 10, 50, 50).collidepoint(pos):
                    # 切换暂停和继续
                    paused = not paused
                    timer_running = not paused
                elif not paused:
                    check_click(pos)
                    check_match()  # 检查底部方框中是否有可消除的图标
                    if not check_bottom_box():
                        running = False
                        game_over()  # 显示游戏失败画面

        # 检查是否全部消除
        if check_win():
            running = False
            game_over(win=True)  # 显示游戏成功画面

        # 绘制背景
        screen.blit(background_image, (0, 0))

        # 绘制堆叠图标
        draw_layers()

        # 绘制底部框
        draw_bottom_box()

        # 显示倒计时
        timer_text = small_font.render(f"倒计时: {int(timer)}", True, BLACK)
        screen.blit(timer_text, (10, 10))

        # 显示得分
        draw_score()

        # 绘制暂停按钮
        draw_pause_button()

        pygame.display.flip()


def game_over(win=False):
    over_running = True
    while over_running:
        if win:
            screen.blit(pygame.image.load('success_background.jpg'), (0, 0))  # 成功页面背景
            over_text = font.render('恭喜喵喵成功！', True, BLACK)
            over_text_rect = over_text.get_rect(center=(WIDTH // 2, HEIGHT // 3))
        else:
            screen.blit(pygame.image.load('failure_background.jpg'), (0, 0))  # 失败页面背景
            over_text = font.render('游戏失败！', True, BLACK)
            over_text_rect = over_text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
            
            fail_text = small_font.render('你不要在这里和我喵喵叫~', True, BLACK)
            fail_text_rect = fail_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 150))
            screen.blit(fail_text, fail_text_rect)

        score_text = small_font.render(f'最终得分: {score}', True, BLACK)
        score_text_rect = score_text.get_rect(center=(WIDTH // 2, HEIGHT // 1.5))
        restart_text = small_font.render('点击空白处重新开始', True, BLACK)
        restart_text_rect = restart_text.get_rect(center=(WIDTH // 2, HEIGHT // 1.2))

        screen.blit(over_text, over_text_rect)
        screen.blit(score_text, score_text_rect)
        screen.blit(restart_text, restart_text_rect)

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                over_running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                over_running = False
                main_menu()  # 返回主菜单

def enter_meow_group():
    entering_meow_running = True
    while entering_meow_running:
        screen.fill(WHITE)
        screen.blit(background_image, (0, 0))

        enter_button_rect = pygame.Rect(WIDTH // 2 - 100, HEIGHT // 2 - 25, 200, 50)
        mode_button_rect = pygame.Rect(WIDTH // 2 - 100, HEIGHT // 2 + 50, 200, 50)  # 模式选择按钮

        pygame.draw.rect(screen, BLACK, enter_button_rect)
        pygame.draw.rect(screen, BLACK, mode_button_rect)

        enter_text = small_font.render('进入喵群', True, WHITE)
        mode_text = small_font.render('选择模式', True, WHITE)
        screen.blit(enter_text, (enter_button_rect.x + 50, enter_button_rect.y + 10))
        screen.blit(mode_text, (mode_button_rect.x + 50, mode_button_rect.y + 10))

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                entering_meow_running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if enter_button_rect.collidepoint(event.pos):
                    entering_meow_running = False
                    game_loop()  # 开始游戏
                elif mode_button_rect.collidepoint(event.pos):
                    select_mode()  # 选择模式
def select_mode():
    mode_running = True
    while mode_running:
        screen.fill(WHITE)
        screen.blit(background_image, (0, 0))

        easy_button_rect = pygame.Rect(WIDTH // 2 - 100, HEIGHT // 2 - 25, 200, 50)
        difficult_button_rect = pygame.Rect(WIDTH // 2 - 100, HEIGHT // 2 + 50, 200, 50)

        pygame.draw.rect(screen, BLACK, easy_button_rect)
        pygame.draw.rect(screen, BLACK, difficult_button_rect)

        easy_text = small_font.render('简单模式', True, WHITE)
        difficult_text = small_font.render('困难模式', True, WHITE)
        screen.blit(easy_text, (easy_button_rect.x + 50, easy_button_rect.y + 10))
        screen.blit(difficult_text, (difficult_button_rect.x + 50, difficult_button_rect.y + 10))

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                mode_running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if easy_button_rect.collidepoint(event.pos):
                    mode_running = False
                    enter_meow_group()  # 进入喵群页面，选择简单模式
                elif difficult_button_rect.collidepoint(event.pos):
                    mode_running = False
                    print("困难模式代码暂时未实现")
                    # 你可以在这里添加困难模式代码

        settings_background = pygame.image.load('background_image.jpg')
           
def settings_page():
    running = True
    while running:
        screen.blit(settings_background, (0, 0))
        
        draw_button(pygame.Rect(WIDTH // 4 - 100, HEIGHT // 4, 200, 50), '游戏说明', font, BLACK, YELLOW)
        draw_button(pygame.Rect(WIDTH // 4 - 100, HEIGHT // 2, 200, 50), '游戏商店', font, BLACK, YELLOW)
        draw_button(pygame.Rect(WIDTH // 4 - 100, HEIGHT * 3 // 4, 200, 50), '星河之家', font, BLACK, YELLOW)

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                pos = event.pos
                if pygame.Rect(WIDTH // 4 - 100, HEIGHT // 4, 200, 50).collidepoint(pos):
                    game_instructions()
                elif pygame.Rect(WIDTH // 4 - 100, HEIGHT // 2, 200, 50).collidepoint(pos):
                    game_store()
                elif pygame.Rect(WIDTH // 4 - 100, HEIGHT * 3 // 4, 200, 50).collidepoint(pos):
                    # 星河之家，暂时不设计
                    pass

def game_instructions():
    running = True
    while running:
        screen.blit(background_image, (0, 0))
        
        instruction_text = """
        欢迎来到《喵了个喵》！

        在这个游戏中，你将面临各种各样的图标挑战。游戏的目标是通过点击并消除底部方框中的相同图标来获得高分。底部方框中最多显示5个图标，如果有三个相同的图标，就会消除它们。游戏时间有限，快来挑战自己的高分吧！

        快速点击和策略是获得高分的关键。希望你能在游戏中找到乐趣！

        祝好运！
        """
        instructions_surf = small_font.render(instruction_text, True, BLACK)
        instructions_rect = instructions_surf.get_rect(center=(WIDTH // 2, HEIGHT // 2))
        screen.blit(instructions_surf, instructions_rect)

        draw_button(pygame.Rect(WIDTH // 2 - 100, HEIGHT * 3 // 4, 200, 50), '返回', font, BLACK, YELLOW)
        
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                pos = event.pos
                if pygame.Rect(WIDTH // 2 - 100, HEIGHT * 3 // 4, 200, 50).collidepoint(pos):
                    return

def game_store():
    running = True
    while running:
        screen.blit(background_image, (0, 0))

        items = [
            ("道具1", 5),
            ("道具2", 7),
            ("道具3", 10)
        ]

        y_offset = HEIGHT // 6
        for item, price in items:
            draw_button(pygame.Rect(WIDTH // 4 - 100, y_offset, 200, 50), f"{item} - {price}元", font, BLACK, YELLOW)
            y_offset += 60

        draw_button(pygame.Rect(WIDTH // 2 - 100, HEIGHT * 3 // 4, 200, 50), '返回', font, BLACK, YELLOW)
        
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                pos = event.pos
                if pygame.Rect(WIDTH // 2 - 100, HEIGHT * 3 // 4, 200, 50).collidepoint(pos):
                    return

def main_menu():
    menu_running = True
    while menu_running:
        screen.fill(WHITE)
        screen.blit(background_image, (0, 0))  # 设置背景图

        title_text = font.render('喵了个喵', True, BLACK)
        screen.blit(title_text, (WIDTH // 2 - title_text.get_width() // 2, HEIGHT // 4))

        start_button_rect = pygame.Rect(WIDTH // 2 - 100, HEIGHT // 2 - 50, 200, 50)
        settings_button_rect = pygame.Rect(WIDTH // 2 - 100, HEIGHT // 2 + 20, 200, 50)
        quit_button_rect = pygame.Rect(WIDTH // 2 - 100, HEIGHT // 2 + 90, 200, 50)

        pygame.draw.rect(screen, BLACK, start_button_rect)
        pygame.draw.rect(screen, BLACK, settings_button_rect)
        pygame.draw.rect(screen, BLACK, quit_button_rect)

        start_text = small_font.render('开始游戏', True, WHITE)
        settings_text = small_font.render('设置', True, WHITE)
        quit_text = small_font.render('退出游戏', True, WHITE)

        screen.blit(start_text, (start_button_rect.x + 50, start_button_rect.y + 10))
        screen.blit(settings_text, (settings_button_rect.x + 80, settings_button_rect.y + 10))
        screen.blit(quit_text, (quit_button_rect.x + 60, quit_button_rect.y + 10))

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                pos = event.pos
                if pygame.Rect(WIDTH // 4 - 100, HEIGHT // 4, 200, 50).collidepoint(pos):
                    # 游戏主循环
                    pass
                elif pygame.Rect(WIDTH // 4 - 100, HEIGHT // 2, 200, 50).collidepoint(pos):
                    settings_page()  # 处理点击“设置”按钮，调用 settings_page()
                elif pygame.Rect(WIDTH // 4 - 100, HEIGHT * 3 // 4, 200, 50).collidepoint(pos):
                    running = False
    pygame.quit()

main_menu()

