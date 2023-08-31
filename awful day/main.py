import pygame
import sys
from math import ceil 
from pygame.locals import *

pygame.mixer.pre_init(44100,-16,2,512)
pygame.init()
pygame.mixer.set_num_channels(64)


print('\n - Autor: Sebastian Alejadro Morales Torres \n - Seccion: 220 \n - Videojuego: Awful Day >:(')

path = __file__.replace("main.py", "")

fps = pygame.time.Clock()
screen_size = (800,640)
screen = pygame.display.set_mode(screen_size)
pygame.display.set_caption('AWFUL DAY')
icon = pygame.image.load(f'{path}/data/spr/icon.png')
pygame.display.set_icon(icon) 

font = pygame.font.SysFont('Arial',40)

def draw_text(text, font, color, surface, x, y):
    textobj = font.render(text, 1, color)
    textrect = textobj.get_rect()
    textrect.topleft = (x, y)
    surface.blit(textobj, textrect)

def main_menu():
    pygame.mixer.music.load(f'{path}/data/music/menu.wav')
    pygame.mixer.music.play(-1)
    volumen=0.5
    pygame.mixer.music.set_volume(volumen)

    click = False
    running = True
    while running:
        screen.fill((0,0,0))

        bg_spr = pygame.image.load(f'{path}/data/spr/menu_bg.png')
        title_spr = pygame.image.load(f'{path}/data/spr/title.png')
        play_spr=pygame.image.load(f'{path}/data/spr/play.png')
        quit_spr=pygame.image.load(f'{path}/data/spr/quit.png')

        mx, my = pygame.mouse.get_pos()
        
        button_1 = pygame.Rect(260, 250, 300, 80)
        button_3 = pygame.Rect(260, 380, 300, 80)

        screen.blit(pygame.transform.scale(bg_spr,screen_size),(0,0))
        screen.blit(title_spr,(190,80))
        screen.blit(play_spr,button_1)
        screen.blit(quit_spr,button_3)

        if button_1.collidepoint((mx, my)):
            if click:
                game()
            click = False
        if button_3.collidepoint((mx,my)):
            if click:
                sys.exit()
            click = False

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    sys.exit()
            if event.type == MOUSEBUTTONDOWN:
                if event.button == 1:
                    click = True

        pygame.display.update()
        fps.tick(60)

def game():
    main=pygame.mixer.music;main.load(f'{path}/data/music/play.wav');main.play(-1)


    class Score():
        score=0
    class Button():
        def __init__(self,x,y,image):
            self.image=image
            self.rect=self.image.get_rect()
            self.rect.x=x;self.rect.y=y
            self.clicked=False
        def draw(self):
            action=False
            pos=pygame.mouse.get_pos()
            if self.rect.collidepoint(pos):
                if pygame.mouse.get_pressed()[0]==1 and self.clicked==False:
                    action=True
                    self.clicked=True
            if pygame.mouse.get_pressed()[0]==0:
                self.clicked=False
            #Dibujar el Botón:
            screen.blit(self.image,self.rect)
            #Dar el resultado de a qué se está clickeando:
            return action
    #Game Over:
    game_over=0
    class Sound():
        die=pygame.mixer.Sound(f'{path}/data/sfx/die.wav')
        jump=pygame.mixer.Sound(f'{path}/data/sfx/jump_0.wav')
        restart=pygame.mixer.Sound(f'{path}/data/sfx/restart.ogg')
    #Personaje jugable:
    class Player():
        def __init__(self,x,y):
            self.reset(x,y)
        #Definir el diccionario de Frames:
        global animation_frames
        animation_frames = {}
        #Carga de animaciones:
        def load_animation(path,frame_durations):
            global animation_frames
            animation_name = path.split('/')[-1]
            animation_frame_data = []
            n = 0
            for frame in frame_durations:
                animation_frame_id = animation_name + '_' + str(n)
                img_loc = path + '/' + animation_frame_id + '.png'
                # player_animations/idle/0.png
                animation_image = pygame.image.load(img_loc)
                animation_frames[animation_frame_id] = animation_image.copy()
                for i in range(frame):
                    animation_frame_data.append(animation_frame_id)
                n += 1
            return animation_frame_data
        #Cambio de acciones:
        def change_action(action,frame,new_action):
            if action != new_action:
                action = new_action
                frame = 0
            return action,frame
        #Acciones de animacion:
        animation_database={}
        animation_database['run']=load_animation(f'{path}/data/player_animations/run',[3,3,3,3,3,3,3,3,3,3,3,3])
        animation_database['jump']=load_animation(f'{path}/data/player_animations/jump',[3,3,3,3,3,3])
        animation_database['idle']=load_animation(f'{path}/data/player_animations/idle',[6,6,6,6,6,6,6,6,6,6,6,6])
        #Accion default:
        player_action = 'idle'
        #Index de la animacion:
        player_frame = 0
        #Flipear el personaje:
        player_flip = False
        #Loop del personaje:
        def move(self,game_over):
            #Coordenadas direccionales:
            dx=0; dy=0
            #Jugador==Vivo
            if game_over==0:
                #Controles:
                key=pygame.key.get_pressed()
                #Izquierda y Derecha:
                if key[pygame.K_LEFT]:
                    dx-=4
                    Player.player_action,Player.player_frame=Player.change_action(Player.player_action,Player.player_frame,'run')
                    self.flip=True
                if key[pygame.K_RIGHT]:
                    dx+=4
                    Player.player_action,Player.player_frame=Player.change_action(Player.player_action,Player.player_frame,'run')
                    self.flip=False
                #Idle:
                elif key[pygame.K_RIGHT] == False and key[pygame.K_LEFT] == False:
                    Player.player_action,Player.player_frame=Player.change_action(Player.player_action,Player.player_frame,'idle')
                if key[pygame.K_RIGHT] == True and key[pygame.K_LEFT] == True:
                    Player.player_action,Player.player_frame=Player.change_action(Player.player_action,Player.player_frame,'idle')
                #Salto:
                if key[pygame.K_UP] and self.jumped==False and self.on_ground==True:
                    self.vel_y=-10
                    self.jumped=True
                    self.on_ground=False
                    Sound.jump.play()
                elif key[pygame.K_UP]==False:
                    self.jumped=False            
                if self.on_ground==False:
                    Player.player_action,Player.player_frame=Player.change_action(Player.player_action,Player.player_frame,'jump')
                #Gravedad:
                self.vel_y+=self.gravity
                dy+=self.vel_y
                #Loop Animaciones:
                Player.player_frame += 1
                if Player.player_frame >= len(Player.animation_database[Player.player_action]):
                    Player.player_frame = 0
                #Update Animaciones:
                self.player_img_id = Player.animation_database[Player.player_action][Player.player_frame]
                self.player_img = animation_frames[self.player_img_id]
                #Colisiones
                for tile in world.tile_list:
                    if tile[1].colliderect(self.rect.x + dx, self.rect.y, self.width, self.height):
                        dx = 0
                    if tile[1].colliderect(self.rect.x, self.rect.y + dy, self.width, self.height):
                        if self.vel_y < 0:
                            dy = tile[1].bottom - self.rect.top
                            self.vel_y = 0
                            self.on_ground=False
                        elif self.vel_y >= 0:
                            dy = tile[1].top - self.rect.bottom
                            self.vel_y = 0
                            self.on_ground=True
                #Coordenadas Actualizadas del jugador:
                self.rect.x+=dx 
                self.rect.y+=dy
            #Tp de extremo a extremo de la pantalla:
            if self.rect.x <= 0:
                self.rect.x = screen_size[0]
                dx = 0
            if self.rect.x > screen_size[0]:
                self.rect.x = 0
                dx=0
            #Muerte por sobre pasar los bordes verticales:
            if self.rect.y > 608 or self.rect.y < 0:
                game_over=-1
            #Game Over:    
            if game_over==-1:
                self.player_img=self.dead_image
                self.rect.y-=4
                self.bg_image=pygame.image.load(f'{path}/data/spr/fondo_dead.png').convert_alpha()
                screen.blit(pygame.transform.scale(self.bg_image,screen_size),(0,0))
            #Ingreso del Jugador:
            screen.blit(pygame.transform.flip(self.player_img,self.flip,False),(self.rect.x-2,self.rect.y-2))
            return game_over
        #Reinicio del personaje/juego:
        def reset(self,x,y):
            self.image=pygame.image.load(f'{path}/data/spr/player.png')
            self.width=self.image.get_width()-4
            self.height=self.image.get_height()-2
            self.rect=pygame.Rect(0,0,self.width,self.height)
            self.rect.center=(x,y)
            self.vel_y=0
            self.jumped=False
            self.flip=False
            self.gravity=0.4
            self.on_ground=True
            self.dead_image=pygame.image.load(f'{path}/data/spr/dead.png')
            self.in_air=True           
    #El mundo y sus caracteristicas:        
    class World():
        def __init__(self,data):
            #Tamaño de la tile:
            tile_size=32
            #Plataformas:
            plat_a=pygame.image.load(f'{path}/data/spr/platform_a.png')
            plat_b=pygame.image.load(f'{path}/data/spr/platform_b.png')
            plat_c=pygame.image.load(f'{path}/data/spr/platform_c.png')
            #Grupos:
            fitosis_group=Enemy.fitosis_group;saw_group=Saw.saw_group;sawh_group=SawH.sawh_group
            #Lista de las tiles en el mapa:
            self.tile_list=[]
            #Empieza en y=0
            row_count=0
            #Identificador de tiles en el mapa:
            for row in data:
                #Empieza en x=0
                col_count=0
                for tile in row:
                    #'2'=Sierra Horizontal:
                    if tile == '2':
                        sawh=SawH(col_count*tile_size,row_count*tile_size)
                        sawh_group.add(sawh) #Volver valor al grupo
                    #'5'=Fitosis(Enemigo)
                    if tile == '5':
                        fitosis=Enemy(col_count*tile_size,row_count*tile_size)
                        fitosis_group.add(fitosis) #Volver valor al grupo
                    #'6'Sierras(Enemigo)
                    if tile == '6':
                        saw=Saw(col_count*tile_size,row_count*tile_size)
                        saw_group.add(saw) #Volver valor al grupo
                    #Plataforma:
                    if tile == '7':
                        img = pygame.transform.scale(plat_a,(tile_size,tile_size))
                        img_rect = img.get_rect()
                        img_rect.x = col_count*tile_size
                        img_rect.y = row_count*tile_size
                        tile = (img,img_rect)
                        self.tile_list.append(tile) #Volver valor a la lista
                    if tile == '8':
                        img = pygame.transform.scale(plat_b,(tile_size,tile_size))
                        img_rect = img.get_rect()
                        img_rect.x = col_count*tile_size
                        img_rect.y = row_count*tile_size
                        tile = (img,img_rect)
                        self.tile_list.append(tile) #Volver valor a la lista
                    if tile == '9':
                        img = pygame.transform.scale(plat_c,(tile_size,tile_size))
                        img_rect = img.get_rect()
                        img_rect.x = col_count*tile_size
                        img_rect.y = row_count*tile_size
                        tile = (img,img_rect)
                        self.tile_list.append(tile) #Volver valor a la lista
                    col_count+=1
                #Avanza en y la grid
                row_count+=1    
        #Dibujar las tiles en pantalla:
        def draw(self):
            #Dibujar tiles en el mapa según su coordenada:
            for tile in self.tile_list:
                screen.blit(tile[0],tile[1])
    #Enemigo generico:
    class Enemy(pygame.sprite.Sprite):
        def __init__(self,x,y):
            pygame.sprite.Sprite.__init__(self)
            self.image=pygame.image.load(f'{path}/data/spr/enemy.png')
            self.rect=self.image.get_rect()
            self.rect.x=x;self.rect.y=y
            self.move_x=3;self.move_y=3
        #Grupo de sprites y entidades de Fitosis:
        fitosis_group=pygame.sprite.Group()
        #Loop enemigo:
        def update(self):
            if pygame.sprite.spritecollide(grumpy, self.fitosis_group, False):
                self.move_y=3
                self.move_x=-3
                self.rect.x+=self.move_x
                self.rect.y-=self.move_y
            else:
                #Movimiento:
                self.rect.x+=self.move_x
                self.rect.y-=self.move_y
                if self.rect.x > 768 or self.rect.x < 0:
                    if self.move_x>0:
                        self.move_x+=0.1
                    else:
                        self.move_x-=0.1
                    self.move_x *= -1
                if self.rect.y > 608 or self.rect.y < 0:
                    if self.move_y>0:
                        self.move_y+=0.1
                    else:
                        self.move_y-=0.1
                    self.move_y *= -1
    #Objeto estatico letal:
    class Saw(pygame.sprite.Sprite):
        def __init__(self,x,y):
            tile_size=32
            pygame.sprite.Sprite.__init__(self)
            img=pygame.image.load(f'{path}/data/spr/saw.png')
            self.image=pygame.transform.scale(img,(tile_size,tile_size))
            self.rect=self.image.get_rect()
            self.rect.x=x;self.rect.y=y
            self.move_x=1;self.move_y=1
            self.move_direction=1;self.move_counter=0
        #Grupo de sierras en el mapa:
        saw_group=pygame.sprite.Group()
        def update(self):
            self.rect.y-=self.move_direction
            self.move_counter+=1
            if abs(self.move_counter)>30:
                self.move_direction*=-1
                self.move_counter*=-1
    class SawH(pygame.sprite.Sprite):
        def __init__(self,x,y):
            tile_size=32
            pygame.sprite.Sprite.__init__(self)
            img=pygame.image.load(f'{path}/data/spr/saw.png')
            self.image=pygame.transform.scale(img,(tile_size,tile_size))
            self.rect=self.image.get_rect()
            self.rect.x=x;self.rect.y=y
            self.move_x=3;self.move_y=3
            self.move_counter=0
        #Grupo de sierras en el mapa:
        sawh_group=pygame.sprite.Group()
        def update(self):
            self.rect.x+=self.move_x
            if self.rect.x > 768 or self.rect.x < 0:
                self.move_x *= -1
    #El fondo:
    class BG():
        #Simplemente, dibujar el fondo :3
        def __init__(self):
            self.bg_image=pygame.image.load(f'{path}/data/spr/fondo.png').convert_alpha()
        def draw(self):
                screen.blit(pygame.transform.scale(self.bg_image,screen_size),(0,0))
    #Carga de Mapa:
    class Map:
        def load_map(path):
            #Abrir y leer:
            f = open(path);data = f.read()
            #Cerrar y separar la info:
            f.close();data = data.split('\n')
            #Identificar las columnas y filas del .txt:
            game_map = []
            for row in data:
                game_map.append(list(row))
            return game_map
        game_map = load_map(f'{path}/data/txt/map.txt')
    #DataMap:
    data = Map.game_map;world_data=data
    #Ingreso de el jugador y sus coordenadas:
    grumpy = Player(400,300)
    #ocean = Ocean(400,400)
    score = Score.score
    #Simplemente, el fondo:
    background = BG()
    #Hederar todo lo que sea group:
    saw_group=Saw.saw_group;fitosis_group=Enemy.fitosis_group;sawh_group=SawH.sawh_group
    #Definicion del mundo y sus datos
    world=World(world_data)
    #Game over y sus botónes:
    game_over_button=Button(230,150,pygame.image.load(f'{path}/data/spr/game_over.png'))
    restart_button=Button(380,350,pygame.image.load(f'{path}/data/spr/replay.png'))
    quit_button=Button(110,350,pygame.image.load(f'{path}/data/spr/quit.png'))
    #Definir que el mejor puntaje es la row seleccionada
    #Loop Principal:
    running = True
    while running:
        #Dibujar el fondo en el Loop:
        background.draw()
        #Dibujar al personaje y sus estados en el Loop (Game Over y sus variables):
        game_over=grumpy.move(game_over)
        #Ingreso de sierras:
        sawh_group.draw(screen)
        sawh_group.update()
        saw_group.draw(screen)
        saw_group.update()
        #Dibujar las Tiles y el mundo:
        if game_over==0:
            score+=(1/10)
            score_real=ceil(score)
        #Dibujar el mundo:
        world.draw()
        #Si aún no mueres, lo siguiente se actualiza:
        if game_over==0:
            #Grupo de enemigos:
            #Score total de la partida:
            draw_text('SCORE: '+str("{:.0f}".format(score_real)),font,(0,0,0),screen,50,50)
            #--Muerte
            if score_real>5:
                if pygame.sprite.spritecollide(grumpy, fitosis_group, False):
                    game_over=-1
                    hit=pygame.mixer.Sound(f'{path}/data/sfx/die.wav')
                    hit.play()
                #--Muerte
                if pygame.sprite.spritecollide(grumpy, saw_group, False):
                    game_over=-1
                    hit=pygame.mixer.Sound(f'{path}/data/sfx/die.wav')
                    hit.play()
                #--Muerte
                if pygame.sprite.spritecollide(grumpy, sawh_group, False):
                    game_over=-1
                    hit=pygame.mixer.Sound(f'{path}/data/sfx/die.wav')
                    hit.play()
        #Dibujar los enemigos:
        fitosis_group.draw(screen)
        fitosis_group.update()
        #Si mueres, entonces lo siguiente pasa:
        if game_over==-1:
            #Si eliges reiniciar, se reinicia el personaje:
            if restart_button.draw():
                grumpy.reset(400,300);game_over = 0
                score = 0
                Sound.restart.play()
            #Si eliges salir, vuelves al menú prinicipal, matando el loop principal:
            if quit_button.draw():
                running=False
                mainmenu=pygame.mixer.music
                mainmenu.load(f'{path}/data/music/menu.wav')
                mainmenu.play(-1)
            #Simplemente, botón de game over
            game_over_button.draw()
            draw_text('TOTAL SCORE: '+str("{:.0f}".format(score_real)),font,(0,0,0),screen,260,250)
        #Handler de eventos:
        for event in pygame.event.get():
            #Auto-Kill:
            if event.type == pygame.QUIT and game_over==0:
                game_over = -1;hit=pygame.mixer.Sound(f'{path}/data/sfx/die.wav');hit.play()
            #Auto-Kill:
            if event.type == KEYDOWN and game_over==0:
                if event.key == K_k:
                    game_over = -1;hit=pygame.mixer.Sound(f'{path}/data/sfx/die.wav');hit.play()
            #Reset:
            if event.type == KEYDOWN and game_over==-1:
                #Reset:
                if event.key == K_SPACE:
                    grumpy.reset(400,300);game_over=0;score=0
                    Sound.restart.play()
                #Menú:
                if event.key == K_ESCAPE:
                    running=False;mainmenu=pygame.mixer.music;mainmenu.load(f'{path}/data/music/menu.wav');mainmenu.play(-1)

        pygame.display.update()
        fps.tick(60)
        

main_menu()
