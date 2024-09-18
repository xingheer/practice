import pygame
import random
PINK = (255, 182, 193)  # 粉色
PURPLE = (128, 0, 128)  # 紫色
# 初始化 Pygame
pygame.init()
# 定义颜色
GREEN = (0, 255, 0)
pygame.mixer.init()  # 初始化音频

# 加载音效
click_sound = pygame.mixer.Sound('click_sound.mp3')
# 定义窗口大小和颜色
WIDTH, HEIGHT = 600, 600
TILE_SIZE = 80
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
YELLOW = (255, 255, 0)  # 添加绿色定义

# 创建窗口
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("喵了个喵")
instruction_image = pygame.image.load('instruction_image.jpg')  # 替换为你的游戏说明图片路径
shop_image = pygame.image.load('shop_image.jpg')  # 替换为你的商店图片路径
# 加载字体
font = pygame.font.Font('SimHei.ttf', 50)  # 载入中文字体
small_font = pygame.font.Font('SimHei.ttf', 30)  # 载入中文字体
eliminate_background_image = pygame.image.load('new_eliminate_background.jpg')  # 替换为新的消除页面背景图片路径

# 加载背景图片
background_image = pygame.image.load('background1.jpg')  # 替换为你的背景图片路径

is_difficult_mode =True
# 加载图标图片
# 更新图标路径
icon_paths = [
    '1.jpg', '2.jpg', '3.jpg', '4.jpg', '5.jpg', '6.jpg',
    '7.jpg', '8.jpg', '9.jpg', '10.jpg'
]

# 初始化图标列表
pygame.mixer.music.load('background_music.wav')  
eliminate_sound = pygame.mixer.Sound('eliminate_sound.wav')  # 加载消除音效
def select_mode():
    global is_difficult_mode
    global patterns
    mode_running = True
    while mode_running:
        screen.fill(WHITE)
        screen.blit(background_image, (0, 0))

        easy_button_rect = pygame.Rect(WIDTH // 2 - 100, HEIGHT // 2 - 25, 200, 50)
        difficult_button_rect = pygame.Rect(WIDTH // 2 - 100, HEIGHT // 2 + 50, 200, 50)

        draw_button(easy_button_rect, '简单模式', small_font)  # 使用粉色背景和紫色字体
        draw_button(difficult_button_rect, '困难模式', small_font)  # 使用粉色背景和紫色字体

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                mode_running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                click_sound.play()  # 播放点击音效
                if easy_button_rect.collidepoint(event.pos):
                    is_difficult_mode = False
                    patterns = get_patterns()
                    mode_running = False
                    create_layers()
                    enter_meow_group()
                elif difficult_button_rect.collidepoint(event.pos):
                    is_difficult_mode = True
                    patterns = get_patterns()
                    mode_running = False
                    create_layers()
                    enter_meow_group()


def get_patterns():
    if is_difficult_mode:
        print("获取困难模式图标")
        return [pygame.transform.scale(pygame.image.load(path), (TILE_SIZE, TILE_SIZE)) for path in icon_paths]
    else:
        print("获取简单模式图标")
        return [pygame.transform.scale(pygame.image.load(path), (TILE_SIZE, TILE_SIZE)) for path in icon_paths[:6]]

patterns = get_patterns()
def get_correct_icon_count(patterns):
    count_per_icon = 3
    if is_difficult_mode:
        count_per_icon = 30  # 困难模式下每种图标出现3次
    total_icons = len(patterns) * count_per_icon
    return total_icons

def create_layers():
    global patterns  # 确保可以访问 patterns
    count_per_icon = 3
    num_layers = 3

    if is_difficult_mode:
        count_per_icon = 3
        num_layers = 5  # 困难模式下增加至5层

    total_icons = len(patterns) * count_per_icon
    all_icons = [pattern for pattern in patterns for _ in range(count_per_icon)]  # 确保每种图标出现3次
    random.shuffle(all_icons)  # 随机打乱图标顺序

    layers = []
    for _ in range(num_layers):
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
                tile.set_alpha(200)  # 设置图标透明度
                screen.blit(tile, (x, y))
def draw_bottom_box():
    deep_pink = (255, 20, 147)  # 深粉色
    # 定义淡灰色
    LIGHT_GRAY = (211, 211, 211)

    pygame.draw.rect(screen, LIGHT_GRAY, (0, HEIGHT - 80, WIDTH, 80))  # 修改为淡灰色
    # 显示底部方框中的图标
    # 显示底部方框中的图标


    for i, (tile, _) in enumerate(bottom_box):
        if i < 5:  # 只显示前5个图标
            tile.set_alpha(255)
            screen.blit(tile, (i * (TILE_SIZE + 5) + 10, HEIGHT - 70))
def check_click(pos):
    global selected
    for layer in reversed(layers):
        for i, (tile, x, y) in enumerate(layer):
            if tile is not None and x < pos[0] < x + TILE_SIZE and y < pos[1] < y + TILE_SIZE:
                click_sound.play()  # 播放点击音效
                selected.append((tile, x, y))
                if len(selected) > 5:
                    selected.pop(0)
                layer[i] = (None, 0, 0)
                bottom_box.append((tile, (x, y)))
                if len(bottom_box) > 5:
                    bottom_box.pop(0)
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
eliminate_sound.set_volume(1.0)  # 将音量设置为最大


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
                eliminate_sound.play()
                return True
        return False
    return True


def check_win():
    for layer in layers:
        for tile, _, _ in layer:
            if tile is not None:
                return False
    return True

def draw_button(rect, text, font, text_color=PURPLE, bg_color=PINK):
    pygame.draw.rect(screen, bg_color, rect)
    pygame.draw.rect(screen, WHITE, rect, 2)  # 绘制按钮边框
    text_surf = font.render(text, True, text_color)
    text_rect = text_surf.get_rect(center=rect.center)
    screen.blit(text_surf, text_rect)

# 使用示例
def draw_pause_button():
    button_rect = pygame.Rect(WIDTH - 60, 38, 50, 50)
    draw_button(button_rect, 'P' if not paused else 'S', small_font)


def game_loop():
    screen.blit(eliminate_background_image, (0, 0))

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
    pygame.mixer.music.stop() 
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
    pygame.mixer.music.play(-1)  # 播放音乐，-1 表示循环播放
    entering_meow_running = True
    
    while entering_meow_running:
        screen.fill(WHITE)
         
        screen.blit(background_image, (0, 0))

        enter_button_rect = pygame.Rect(WIDTH // 2 - 100, HEIGHT // 2 - 25, 200, 50)
        mode_button_rect = pygame.Rect(WIDTH // 2 - 100, HEIGHT // 2 + 50, 200, 50)  # 模式选择按钮

        draw_button(enter_button_rect, '进入喵群', small_font)  # 使用粉色背景和紫色字体
        draw_button(mode_button_rect, '选择模式', small_font)  # 使用粉色背景和紫色字体

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






# 加载按钮图片
start_button_image = pygame.image.load('start_button.jpg')  # 替换为本地的开始按钮图片路径
settings_button_image = pygame.image.load('settings_button.jpg')  # 替换为本地的设置按钮图片路径
quit_button_image = pygame.image.load('quit_button.jpg')  # 替换为本地的退出按钮图片路径

# 缩放按钮图片到适合的大小
start_button_image = pygame.transform.scale(start_button_image, (200, 60))
settings_button_image = pygame.transform.scale(settings_button_image, (200, 60))
quit_button_image = pygame.transform.scale(quit_button_image, (200, 60))
# 定义是否显示设置页面的变量
showing_settings = False

def draw_button(rect, text, font, text_color=PURPLE, bg_color=PINK):  # 修改按钮背景和字体颜色
    pygame.draw.ellipse(screen, bg_color, rect)
    pygame.draw.ellipse(screen, WHITE, rect, 2)
    text_surf = font.render(text, True, text_color)
    text_rect = text_surf.get_rect(center=rect.center)
    screen.blit(text_surf, text_rect)

def show_instruction():
    showing_instruction = True
    while showing_instruction:
        screen.blit(instruction_image, (0, 0))  # 显示游戏说明图片
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                showing_instruction = False  # 点击屏幕返回主菜单
        
        pygame.display.update()

def show_shop():
    showing_shop = True
    while showing_shop:
        screen.blit(shop_image, (0, 0))  # 显示商店图片
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                showing_shop = False  # 点击屏幕返回主菜单
        
        pygame.display.update()

def main_menu():
    global showing_settings

    menu_running = True
    while menu_running:
        screen.fill(WHITE)
        
        if not showing_settings:  # 当不在设置页面时，显示主菜单按钮
            screen.blit(background_image, (0, 0))  # 显示主菜单背景图片
                # 按钮的位置
          
          
            # 绘制按钮
            screen.blit(start_button_image, (200, 250))  # 替换为实际位置坐标
            screen.blit(settings_button_image, (200, 350))  # 替换为实际位置坐标
            screen.blit(quit_button_image, (200, 450))  # 确保退出按钮也在屏幕上绘制


        else:  # 在设置页面时，显示游戏说明和商店按钮
            draw_button(pygame.Rect(200, 100, 200, 60), "游戏说明", font)
            draw_button(pygame.Rect(200, 200, 200, 60), "商店", font)
            draw_button(pygame.Rect(200, 300, 200, 60), "返回", font)  # 返回主菜单按钮

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = event.pos
                if not showing_settings:  # 主菜单按钮点击事件
                    if pygame.Rect(200, 100, 200, 60).collidepoint(mouse_pos):
                        enter_meow_group()  # 进入游戏
                    elif pygame.Rect(200, 200, 200, 60).collidepoint(mouse_pos):
                        showing_settings = True  # 进入设置页面
                    elif pygame.Rect(200, 300, 200, 60).collidepoint(mouse_pos):
                        menu_running = False  # 退出游戏
                else:  # 设置页面按钮点击事件
                    if pygame.Rect(200, 100, 200, 60).collidepoint(mouse_pos):
                        show_instruction()  # 显示游戏说明
                    elif pygame.Rect(200, 200, 200, 60).collidepoint(mouse_pos):
                        show_shop()  # 显示商店
                    elif pygame.Rect(200, 300, 200, 60).collidepoint(mouse_pos):
                        showing_settings = False  # 返回主菜单

        pygame.display.update()

    pygame.quit()

main_menu()