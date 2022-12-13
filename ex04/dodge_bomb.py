import pygame as pg
import sys
import random
import tkinter.messagebox as tkm

def check_bound(obj_rct, scr_rct):
    yoko, tate = +1, +1
    if obj_rct.left < scr_rct.left or scr_rct.right < obj_rct.right:
        yoko = -1
    if obj_rct.top < scr_rct.top or scr_rct.bottom < obj_rct.bottom:
        tate = -1
    return yoko, tate

def main():
    #スクリーン定義
    clock = pg.time.Clock()
    pg.display.set_caption("逃げろ！こうかとん")
    scrn_sfc = pg.display.set_mode((1600, 900))
    scrn_rct = scrn_sfc.get_rect()
    pgbg_sfc = pg.image.load("fig/pg_bg.jpg")
    pgbg_rct = pgbg_sfc.get_rect()

    #こうかとん定義
    tori_sfc = pg.image.load("fig/6.png")
    tori_sfc = pg.transform.rotozoom(tori_sfc, 0, 2.0)
    tori_rct = tori_sfc.get_rect()
    tori_rct.center = 900, 400
    scrn_sfc.blit(tori_sfc, tori_rct)

    #爆弾定義
    bomb_sfc = pg.Surface((20, 20))
    bomb_sfc.set_colorkey((0, 0, 0))
    pg.draw.circle(bomb_sfc, (255, 0, 0), (10, 10), 10)
    bomb_rct = bomb_sfc.get_rect()
    bomb_rct.centerx = random.randint(0, scrn_rct.width)
    bomb_rct.centery = random.randint(0, scrn_rct.height)
    scrn_sfc.blit(bomb_sfc, bomb_rct)

    #ボールを増やす
    bomb_sfc1 = pg.Surface((20, 20)) 
    bomb_sfc1.set_colorkey((0, 0, 0)) 
    pg.draw.circle(bomb_sfc1, (0, 0, 255), (10, 10), 10) 
    bomb_rct1 = bomb_sfc1.get_rect()
    bomb_rct1.centerx = random.randint(0, scrn_rct.width)
    bomb_rct1.centery = random.randint(0, scrn_rct.height)
    vx, vy = 1, 1
    vx1, vy1 = 1, 1

    #ループ
    while True:
        scrn_sfc.blit(pgbg_sfc, pgbg_rct)
        for event in pg.event.get():
            if event.type == pg.QUIT:
                return

        #こうかとんの移動定義
        #wasdでも移動できるように設定
        key_dct = pg.key.get_pressed()
        if key_dct[pg.K_UP] or key_dct[pg.K_w]:
            tori_rct.centery -= 1
        if key_dct[pg.K_DOWN] or key_dct[pg.K_s]:
            tori_rct.centery += 1
        if key_dct[pg.K_LEFT] or key_dct[pg.K_a]:
            tori_rct.centerx -= 1
        if key_dct[pg.K_RIGHT] or key_dct[pg.K_d]:
            tori_rct.centerx += 1
            
        #Spaceが押されたら加速
        if key_dct[pg.K_UP] and key_dct[pg.K_SPACE]:    
            tori_rct.centery -= 5
        if key_dct[pg.K_DOWN] and key_dct[pg.K_SPACE]:  
            tori_rct.centery += 5
        if key_dct[pg.K_LEFT] and key_dct[pg.K_SPACE]:  
            tori_rct.centerx -= 5
        if key_dct[pg.K_RIGHT] and key_dct[pg.K_SPACE]: 
            tori_rct.centerx += 5
        
        if check_bound(tori_rct, scrn_rct) != (+1, +1):
            # どこかしらはみ出ていたら
            if key_dct[pg.K_UP] or key_dct[pg.K_w]:
                tori_rct.centery += 1
            if key_dct[pg.K_DOWN] or key_dct[pg.K_s]:
                tori_rct.centery -= 1
            if key_dct[pg.K_LEFT] or key_dct[pg.K_a]:
                tori_rct.centerx += 1
            if key_dct[pg.K_RIGHT] or key_dct[pg.K_d]:
                tori_rct.centerx -= 1            
        scrn_sfc.blit(tori_sfc, tori_rct)

        #爆弾の動きの定義
        bomb_rct.move_ip(vx, vy)
        yoko, tate = check_bound(bomb_rct, scrn_rct)
        vx *= yoko
        vy *= tate
        bomb_rct.move_ip(vx, vy)
        scrn_sfc.blit(bomb_sfc, bomb_rct)

        #ボール2つの呼び出し
        bomb_rct1.move_ip(vx1, vy1)
        yoko1, tate1 = check_bound(bomb_rct1, scrn_rct)
        vx1 *= yoko1
        vy1 *= tate1
        bomb_rct1.move_ip(vx1, vy1)
        scrn_sfc.blit(bomb_sfc1, bomb_rct1)

        if pg.time.get_ticks(): #時間とともに爆弾のスピードが早くなる
            if vx < 0 or vx1 < 0:
                vx -= 0.001
                vx1 -= 0.005
            else:
                vx += 0.0001
                vx1 += 0.0005
            if vy < 0 or vy1 < 0:
                vy -= 0.0001
                vy1 -= 0.0005
            else:
                vy += 0.0001
                vy1 += 0.0005

        if tori_rct.colliderect(bomb_rct): #ボールに当たったら終わり
            txt = "ゲームオーバー"
            tkm.showinfo(txt, f"{txt}です")
            return

        if tori_rct.colliderect(bomb_rct1): #ボールに当たったら終わり
            txt = "ゲームオーバー"
            tkm.showinfo(txt, f"{txt}です")
            return

        pg.display.update()
        clock.tick(250)

if __name__ == "__main__":
    pg.init()
    main()
    pg.quit()
    sys.exit()
