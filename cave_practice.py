import sys
from random import randint
import pygame
from pygame.locals import QUIT, Rect, KEYDOWN, K_SPACE

pygame.init()
pygame.key.set_repeat(5, 5)
SURFACE = pygame.display.set_mode((800, 600))
FPSCLOCK = pygame.time.Clock()

def main():
    walls = 80 #洞窟を構成する矩形の数
    ship_y = 250 #自機のY座標
    velocity = 0 #自機が上下に移動する際の速度
    score = 0 #スコア
    slope = randint(1, 6) #洞窟の傾き(隣の矩形とY軸方向にどれだけずらすか)
    sysfont = pygame.font.SysFont(None, 36)
    ship_image = pygame.image.load("/Users/satohikaru/Desktop/programing_practice/Samples/games/cave/ship.png")
    bang_image = pygame.image.load("/Users/satohikaru/Desktop/programing_practice/Samples/games/cave/bang.png")
    holes = [] #洞窟を構成する矩形を格納する配列
    #なんで*10?
    #x軸方向に10ずつずらしながら矩形をwalls個作成するためらしい。
    #wallsを2倍にしてxpos * 5にしたらどうなるか？予想は大きい矩形(2倍)で洞窟が構成される
    for xpos in range(walls):
        holes.append(Rect(xpos * 10, 100, 10, 400))
    game_over = False #ゲームオーバーか否かのフラグ

    while True:
        is_space_down = False
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == KEYDOWN:
                if event.key == K_SPACE:
                    is_space_down = True

        if not game_over:
            score += 10
            velocity += -3 if is_space_down else 3
            ship_y += velocity

            edge = holes[-1].copy()
            #Rect.move(x, y)で位置を移動させたRectオブジェクトを新規に作成する。指定した距離分移動させたRectオブジェクトを新規に作成し、戻り値として返す。x引数とy引数には正の値と負の値どちらも設定できる。
            test = edge.move(0, slope)
            if test.top <= 0 or test.bottom >= 600:
                slope = randint(1, 6) * (-1 if slope > 0 else 1)
                #Rect.inflate_ip(x, y)でRectオブジェクトの大きさを指定した値分、拡大・縮小する。この命令ではオブジェクト自身の大きさを直接変更させる。また、Rectオブジェクトは図形の中心位置を保った状態で拡大、縮小が行われる。
                #以下の文によってY軸方向のサイズを20小さくしている。
                edge.inflate_ip(0, -20)
            #右端の矩形を左端に移動？
            edge.move_ip(10, slope)
            holes.append(edge)
            del holes[0]
            holes = [x.move(-10, 0) for x in holes]

            #以下のコードで自機が洞窟の壁に衝突したか否かを判定する。
            #+80の値を調整することで衝突判定を厳しくしたり緩くしたりできる。
            if holes[0].top > ship_y or holes[0].bottom < ship_y + 80:
                game_over = True

        SURFACE.fill((0, 255, 255))
        for hole in holes:
            pygame.draw.rect(SURFACE, (0, 0, 0), hole)
        SURFACE.blit(ship_image, (0, ship_y))
        score_image = sysfont.render("score is {}".format(score),
                                     True,
                                     (0, 0, 255))
        SURFACE.blit(score_image, (600, 20))

        if game_over:
            SURFACE.blit(bang_image, (0, ship_y-40))

        pygame.display.update()
        FPSCLOCK.tick(15)

if __name__ == '__main__':
    main()
