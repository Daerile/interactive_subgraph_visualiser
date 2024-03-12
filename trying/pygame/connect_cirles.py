import pygame

# pygame setup
pygame.init()
screen = pygame.display.set_mode((1280, 720))
clock = pygame.time.Clock()
running = True
dt = 0

player_pos = pygame.Vector2(screen.get_width() / 2, screen.get_height() / 2)

while running:
    screen.fill("purple")
    circle = pygame.draw.circle(screen, "red", pygame.Vector2(screen.get_width() / 2, screen.get_height() / 4), 40)
    circle2 = pygame.draw.circle(screen, "red", pygame.Vector2(screen.get_width() / 2, 3 * screen.get_height() / 4), 40)
    line = pygame.draw.line(screen, "blue", (circle.centerx, circle.centery), (circle2.centerx, circle2.centery), 5)

    # poll for events
    # pygame.QUIT event means the user clicked X to close your window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            if circle.collidepoint(event.pos):

            if circle2.collidepoint(event.pos):
                print("You clicked the circle2")

    pygame.display.flip()
    dt = clock.tick(60) / 1000

pygame.quit()

