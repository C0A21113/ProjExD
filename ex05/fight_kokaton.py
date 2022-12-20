import pygame as pg
import random
import sys
import os


class Screen:
    def __init__(self, title, wh, img_path):
        pg.display.set_caption(title) 
        self.sfc = pg.display.set_mode(wh)
        self.rct = self.sfc.get_rect()
        self.bgi_sfc = pg.image.load(img_path)
        self.bgi_rct = self.bgi_sfc.get_rect() 

    def blit(self):
        self.sfc.blit(self.bgi_sfc, self.bgi_rct) 


class Bird:
    key_delta = {
        pg.K_UP:    [0, -1],
        pg.K_DOWN:  [0, +1],
        pg.K_LEFT:  [-1, 0],
        pg.K_RIGHT: [+1, 0],
        pg.K_w:     [0, -1],
        pg.K_s:     [0, +1],
        pg.K_a:     [-1, 0],
        pg.K_d:     [+1, 0]
    }

    def __init__(self, img_path, ratio, xy):
        self.sfc = pg.image.load(img_path)
        self.sfc = pg.transform.rotozoom(self.sfc, 0, ratio)
        self.rct = self.sfc.get_rect()
        self.rct.center = xy

    def blit(self, scr:Screen):
        scr.sfc.blit(self.sfc, self.rct)

    def update(self, scr:Screen):
        key_dct = pg.key.get_pressed()
        for key, delta in Bird.key_delta.items():
            if key_dct[key]:
                if key_dct[pg.K_SPACE]: #スペースキーを押すと加速
                    self.rct.centerx += delta[0] * 2
                    self.rct.centery += delta[1] * 2
                else:
                    self.rct.centerx += delta[0]
                    self.rct.centery += delta[1]
            if check_bound(self.rct, scr.rct) != (+1, +1):
                self.rct.centerx -= delta[0]
                self.rct.centery -= delta[1]
        self.blit(scr)                    


class Bomb:
    def __init__(self, color, rad, vxy, scr:Screen):
        self.sfc = pg.Surface((2*rad, 2*rad)) # 正方形の空のSurface
        self.sfc.set_colorkey((0, 0, 0))
        pg.draw.circle(self.sfc, color, (rad, rad), rad)
        self.rct = self.sfc.get_rect()
        self.rct.centerx = random.randint(0, scr.rct.width)
        self.rct.centery = random.randint(0, scr.rct.height)
        self.vx, self.vy = vxy

    def blit(self, scr:Screen):
        scr.sfc.blit(self.sfc, self.rct)

    def update(self, scr:Screen):
        self.rct.move_ip(self.vx, self.vy)
        yoko, tate = check_bound(self.rct, scr.rct)
        self.vx *= yoko
        self.vy *= tate
        self.blit(scr)


def check_bound(obj_rct, scr_rct):
    """
    第1引数：こうかとんrectまたは爆弾rect
    第2引数：スクリーンrect
    範囲内：+1／範囲外：-1
    """
    yoko, tate = +1, +1
    if obj_rct.left < scr_rct.left or scr_rct.right < obj_rct.right:
        yoko = -1
    if obj_rct.top < scr_rct.top or scr_rct.bottom < obj_rct.bottom:
        tate = -1
    return yoko, tate


class Enemy(): # ダミー爆弾
    def __init__(self, img, zoom, xy, vxy):
        sfc = pg.image.load(img) 
        self.sfc = pg.transform.rotozoom(sfc, 0, zoom) 
        self.rct = self.sfc.get_rect()
        self.rct.center = xy
        self.vx, self.vy = vxy

    def blit(self, scr:Screen):
        scr.sfc.blit(self.sfc, self.rct)

    def update(self, scr:Screen):
        self.rct.move_ip(self.vx, self.vy)
        yoko, tate = check_bound(self.rct, scr.rct)
        self.vx *= yoko
        self.vy *= tate
        self.blit(scr) # =scr.sfc.blit(self.sfc, self.rct)


class GameOver:
    def __init__(self, title, width_height, background_image, kokaton_image, tori_location):
        pg.display.set_caption(title)
        self.sfc = pg.display.set_mode(width_height)
        self.rct = self.sfc.get_rect()
        self.bg_sfc = pg.image.load(background_image)
        self.bg_rct = self.bg_sfc.get_rect()
        self.tori_sfc = pg.image.load(kokaton_image)
        self.tori_sfc = pg.transform.rotozoom(self.tori_sfc, 0, 4.0)
        self.tori_rct = self.tori_sfc.get_rect()
        self.tori_rct.center = tori_location

    def blit(self):
        self.sfc.blit(self.bg_sfc, self.bg_rct)
        self.sfc.blit(self.tori_sfc, self.tori_rct)


def load_image(file):
    """loads an image, prepares it for play"""
    file = os.path.join(main_dir, "data", file)
    try:
        surface = pg.image.load(file)
    except pg.error:
        raise SystemExit('Could not load image "%s" %s' % (file, pg.get_error()))
    return surface.convert()


main_dir = os.path.split(os.path.abspath(__file__))[0]


def load_sound(file): # BGM追加
    if not pg.mixer:
        return None
    file = os.path.join(main_dir, "data", file)
    try:
        sound = pg.mixer.Sound(file)
        return sound
    except pg.error:
        print("Warning, unable to load, %s" % file)
    return None


def gameover():
    """
    ゲームオーバー画面の表示
    """
    g_scr = GameOver("GameOver", (1600, 900), "fig/gameover2.jpeg", "fig/1.png", (800, 450))
    clock =pg.time.Clock()
    while True:
        g_scr.blit()
        for event in pg.event.get():
            if event.type == pg.QUIT:
                return
        key_state = pg.key.get_pressed()
        if key_state[pg.K_c]: # コンテニュー
            main()
            return
        if key_state[pg.K_ESCAPE]:
            return
        pg.display.update()
        clock.tick(1000)


def main():
    clock = pg.time.Clock()

    scr = Screen("逃げろ！こうかとん", (1600,900), "fig/pg_bg.jpg")

    if pg.mixer:
        music = os.path.join(main_dir, "data", "house_lo.wav")
        pg.mixer.music.load(music)
        pg.mixer.music.play(-1)

    kkt = Bird("fig/6.png", 2.0, (900,400))
    kkt.update(scr)

    boom_sound = load_sound("boom.wav")

    kkt = Bird("fig/6.png", 2.0, (900, 400))
    bkd1 = Bomb((255, 0, 0), 10, (+1, +1), scr)
    bkd2 = Bomb((0, 255, 0), 30, (+1.7, +1.7), scr)
    enm = Enemy("fig/enemy.gif", 2.0, (800, 100), (+1, +1))


    # 練習２
    while True:        
        scr.blit()

        for event in pg.event.get():
            if event.type == pg.QUIT:
                return

        kkt.update(scr)
        bkd1.update(scr)
        bkd2.update(scr)
        enm.update(scr)

        if kkt.rct.colliderect(bkd1.rct): 
            boom_sound.play()
            gameover()
            return

        if kkt.rct.colliderect(bkd2.rct): 
            boom_sound.play()
            gameover()
            return

        pg.display.update() 
        clock.tick(1000)


if __name__ == "__main__":
    pg.init()
    main()
    pg.quit()
    sys.exit()