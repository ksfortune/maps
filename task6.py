import os
import sys

import pygame
import requests

SIZE = WIDTH, HEIGHT = 800, 450
FPS = 50


def get_coords(name):
    geocoder_request = f"http://geocode-maps.yandex.ru/1.x/?apikey=40d1649f-0493-4b70-98ba-98533de7710b&geocode={name}&format=json"

    response = requests.get(geocoder_request)
    if response:
        json_response = response.json()
        try:
            toponym = \
                json_response["response"]["GeoObjectCollection"]["featureMember"][0][
                    "GeoObject"]
            toponym_coodrinates = toponym["Point"]["pos"]
            return toponym_coodrinates
        except IndexError:
            print("Ошибка выполнения запроса:")
            return None

    else:
        print("Ошибка выполнения запроса:")
        print(geocoder_request)
        print("Http статус:", response.status_code, "(", response.reason, ")")
        return None


def CheckWhereClicked(position, n):
    if n == 1 and 130 < position[0] < 200 and 20 < position[1] < 40:
        return True
    if n == 2:
        if 10 < position[0] < 67 and 60 < position[1] < 80:
            return 1
        if 67 < position[0] < 124 and 60 < position[1] < 80:
            return 2
        if 124 < position[0] < 181 and 60 < position[1] < 80:
            return 3
    return False

def buttons(screen):
    font = pygame.font.Font(None, 27)
    pygame.draw.rect(screen, '#9BA1A5', (10, 60, 171, 20))
    pygame.draw.rect(screen, '#000000', (10, 60, 57, 20), 1)
    pygame.draw.rect(screen, '#000000', (67, 60, 57, 20), 1)
    pygame.draw.rect(screen, '#000000', (124, 60, 57, 20), 1)

    text1 = font.render("sat", True, '#000000')
    text2 = font.render("map", True, '#000000')
    text3 = font.render("skl", True, '#000000')

    screen.blit(text1, (25, 62))
    screen.blit(text2, (75, 62))
    screen.blit(text3, (135, 62))



def place_inputting(screen, name):
    font = pygame.font.Font(None, 27)
    pygame.draw.rect(screen, '#AE604D', (130, 20, 70, 20))
    pygame.draw.rect(screen, '#000000', (130, 20, 70, 20), 1)
    pygame.draw.rect(screen, '#AE604D', (0, 0, 200, 20))
    pygame.draw.rect(screen, '#000000', (0, 0, 200, 20), 1)
    text = font.render("find", True, '#000000')
    text2 = font.render(name, True, '#000000')
    screen.blit(text2, (10, 0))
    screen.blit(text, (150, 22))


def do_map(map_file, x, y, spn, map_type, map_points):
    s = '~'.join(i for i in map_points)
    map_request = f"https://static-maps.yandex.ru/1.x/?ll={x},{y}&z={spn}&l={map_type}&pt={s}"

    response = requests.get(map_request)
    if not response:
        print("Ошибка выполнения запроса:")
        print(map_request)
        print("Http статус:", response.status_code, "(", response.reason, ")")
        return map_file

    map_file = "map.png"
    with open(map_file, "wb") as file:
        file.write(response.content)

    return map_file


def main():
    x, y = 133.794557, -28.694111
    spn = 5
    map_points = [f'{x},{y},vkbkm']
    map_type = 'sat'
    if spn < 1 or spn > 17 or spn != int(spn):
        spn = 5
    text = "Австралия"
    pygame.init()
    screen = pygame.display.set_mode(SIZE)
    map_file = do_map(0, x, y, spn, map_type, map_points)

    clock = pygame.time.Clock()
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_position = pygame.mouse.get_pos()
                if CheckWhereClicked(mouse_position, 1):
                    k = get_coords(text)
                    if k is not None:
                        k = k.split()
                        x, y = float(k[0]), float(k[1])
                        map_points.append(f'{x},{y},vkbkm')
                        map_file = do_map(map_file, x, y, spn, map_type, map_points)
                elif CheckWhereClicked(mouse_position, 2):
                    a = CheckWhereClicked(mouse_position, 2)
                    if a == 1:
                        map_type = 'sat'
                    elif a == 2:
                        map_type = 'map'
                    else:
                        map_type = 'sat,skl'
                    map_file = do_map(map_file, x, y, spn, map_type, map_points)
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_BACKSPACE:
                    text = text[:-1]
                else:
                    text += event.unicode
                if event.key == pygame.K_PAGEUP:
                    if spn < 17:
                        spn += 1
                if event.key == pygame.K_PAGEDOWN:
                    if spn > 1:
                        spn -= 1
                if event.key == pygame.K_LEFT:
                    x -= 1
                if event.key == pygame.K_RIGHT:
                    x += 1
                if event.key == pygame.K_UP:
                    y += 1
                if event.key == pygame.K_DOWN:
                    y -= 1
                if event.key == pygame.K_1:
                    map_type = 'map'
                if event.key == pygame.K_2:
                    map_type = 'sat'
                if event.key == pygame.K_3:
                    map_type = 'sat,skl'
                map_file = do_map(map_file, x, y, spn, map_type, map_points)
        clock.tick(FPS)
        screen.blit(pygame.image.load(map_file), (200, 0))
        place_inputting(screen, text)
        buttons(screen)
        pygame.display.flip()
    pygame.quit()
    os.remove(map_file)


if __name__ == '__main__':
    main()
