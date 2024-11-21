import pygame
pygame.init()
screen= pygame.display.set_mode((100,100))
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            break
        elif event.type == pygame.KEYDOWN:
            print(event)

pygame.quit()