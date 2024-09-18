
# game_settings.py
import pygame

# 初始化 Pygame
pygame.init()

# 定义窗口大小
WIDTH, HEIGHT = 600, 600

# 创建窗口
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("喵了个喵")

# 设置背景图片（请替换 'background.png' 为你的背景图片文件名）
background_image = pygame.image.load('background.jpg')
