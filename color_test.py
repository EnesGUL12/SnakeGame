import pygame

def image():
    pygame.init()
    wall_image = pygame.image.load("./images/body.bmp")
    w, h = wall_image.get_size()
    for y in range(h):
        print("")
        for x in range(w):
            c = wall_image.get_at((x, y))
            print(x, y, c.r, c.g, c.b, c.a)


    pygame.quit()

if __name__ == "__main__":
    image()

