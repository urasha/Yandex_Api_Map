import os
import sys
import pygame
import requests
import menu

ll, spn = menu.start_menu()
CONST_LL = ll
maps = ['map', 'sat', 'sat,skl']
num = 0
map_request = f"http://static-maps.yandex.ru/1.x/?ll={ll}&spn={spn}&l={maps[num]}&pt={CONST_LL}"
response = requests.get(map_request)

if not response:
    print("Ошибка выполнения запроса:")
    print(map_request)
    print("Http статус:", response.status_code, "(", response.reason, ")")
    sys.exit(1)

map_file = "map.png"
with open(map_file, "wb") as file:
    file.write(response.content)

pygame.init()
screen = pygame.display.set_mode((600, 450))
screen.blit(pygame.image.load(map_file), (0, 0))

run = True
while run:
    for i in pygame.event.get():
        if i.type == pygame.QUIT:
            run = False
        if i.type == pygame.KEYDOWN:
            if i.key == pygame.K_PAGEUP:
                if float(spn.split(',')[0]) > 0.01:
                    spn = ','.join([str(i - 0.03) for i in map(float, spn.split(','))])
            if i.key == pygame.K_PAGEDOWN:
                if float(spn.split(',')[0]) < 0.7:
                    spn = ','.join([str(i + 0.03) for i in map(float, spn.split(','))])

            num1 = float(ll.split(',')[0])
            num2 = float(ll.split(',')[1])
            delta = 0.05
            if i.key == pygame.K_UP:
                if num2 < 180:
                    num2 += delta
            if i.key == pygame.K_DOWN:
                if 0 < num2 < 180:
                    num2 -= delta
            if i.key == pygame.K_LEFT:
                if num1 > 1:
                    num1 -= delta
            if i.key == pygame.K_RIGHT:
                if 0 < num1 < 180:
                    num1 += delta
            if i.key == pygame.K_SPACE:
                if num == 2:
                    num = 0
                else:
                    num += 1

            ll = ','.join([str(num1), str(num2)])

            map_request = f"http://static-maps.yandex.ru/1.x/?ll={ll}&spn={spn}&l={maps[num]}&pt={CONST_LL}"
            response = requests.get(map_request)
            map_file = "map.png"
            with open(map_file, "wb") as file:
                file.write(response.content)
            screen.blit(pygame.image.load(map_file), (0, 0))
    pygame.display.flip()
os.remove(map_file)
