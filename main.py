import pygame as pm
from pygame.locals import *
import os
import random
import asyncio
import time

class Assets:
    assets = []
    def __init__(self,screen,image = None,pos = None,size = None,velocity = (0,0), acceleration = (0,0),flipx = False,flipy = False):
        Assets.assets.append(self)
        self.velocity, self.acceleration = (velocity, acceleration)
        self.objects = {}
        self.screen = screen
        self.fixed_size = size
        self._size = size
        if self._size:
            self.width,self.height = self._size
        self._folder = None
        self.rate = 30
        self.count = 0
        self.frame_count = 0
        self._image = image
        self.pos = pos
        self.folder_once = True
        self.previous_size = None
        if self._image:
            self.image_blit = pm.transform.flip(pm.image.load(self._image).convert_alpha(),flipx,flipy)
            if self._size:
                self.image_blit = pm.transform.scale(self.image_blit,size)
            self.width, self.height = (self.image_blit.get_width(),self.image_blit.get_height())

        pass
    def collision(self,object):
        self.objects[f'{object}'] = object
        self.objects[f'{object}'].right_collide = False
        self.objects[f'{object}'].left_collide = False
        self.objects[f'{object}'].up_collide = False
        self.objects[f'{object}'].down_collide = False
        if self.pos[1] + self.height > object.pos[1] and self.pos[1] < object.pos[1] + object.height:
            if self.pos[0] + self.width > object.pos[0] and self.pos[0] < object.pos[0]:
                self.objects[f'{object}'].right_collide = True
                
                pass
            else:
                self.objects[f'{object}'].right_collide = False
            if self.pos[0] < object.pos[0] + object.width and self.pos[0] + self.width > object.pos[0] + object.width:
                self.objects[f'{object}'].left_collide = True
            else:
                self.objects[f'{object}'].left_collide = False

                pass
        if self.pos[0] + self.width > object.pos[0] and self.pos[0] < object.pos[0] + object.width:
            if self.pos[1] + self.height > object.pos[1] and self.pos[1] < object.pos[1] + object.height:
                self.objects[f'{object}'].up_collide = True
            else:
                self.objects[f'{object}'].up_collide = False
                pass
            if self.pos[1] < object.pos[1] + object.height and self.pos[1] + self.height > object.pos[1]:
                self.objects[f'{object}'].down_collide = True
            else:
                self.objects[f'{object}'].down_collide = False

    @property
    def size(self):
        return self._size
    @size.setter
    def size(self,value):
        if self._size != value:
            self._size = value
            if self._size != None:
                self.image_blit = pm.transform.scale(self.image_blit,self._size)
                self.width, self.height = (self.image_blit.get_width(),self.image_blit.get_height())
    @property
    def image(self):
        return self._image
    @image.setter
    def image(self,value):
        if self._image != value:
            self._image = value
            if self._image:
                self.image_blit = pm.image.load(self._image).convert_alpha()
                if self.fixed_size == None:
                    self.size = self.image_blit.get_size()
                else:
                    self.image_blit = pm.transform.scale(self.image_blit,self._size)
                if self.previous_size:
                    self.pos = (self.pos[0] + self.previous_size[0] - self.size[0],self.pos[1] + self.previous_size[1] - self.size[1])
    @property
    def folder(self):
        return self._folder
    @folder.setter
    def folder(self,value):
        if self._folder != value:
            self._folder = value
            self.count = 0
            self.frame_count = 0
            self.folder_once = True
            self.animate(self._folder,self.rate)
    def show(self):
        if self._image:
            self.previous_size = self.size
            self.velocity = (self.velocity[0] + self.acceleration[0], self.velocity[1] + self.acceleration[1])
            self.pos = (self.pos[0] + self.velocity[0],self.pos[1] + self.velocity[1])
            self.screen.blit(self.image_blit,self.pos)

    def animate(self,folder,rate = 40,adjust_size = True,flip = False):
        self.rate = rate
        if self.folder_once == True:
            self._folder = folder
            self.folder_once = False
        self.file_list = os.listdir(self.folder)
        if self.count == rate:
            self.frame_count += 1
            self.count = 0
        if self.frame_count == len(self.file_list):
            self.frame_count = 0
        self.image = f'{self._folder}//{self.file_list[self.frame_count]}'
        # print(self.image)
        if flip == True:
            self.image_blit = pm.transform.flip(pm.image.load(self._image).convert_alpha(),flip_x = True,flip_y = False)
        
        self.count += 1


class Manager:
    def __init__(self,screen,image = None,repeat_pos = [],repeated = [],size = None):
        self.screen = screen
        self.size = size
        self.image = image
        self.repeat_pos = repeat_pos
        self.repeated = repeated
        self.once_till = True
        pass
    def repeat(self,gap,range_to,till,erase_before = None,velocity = 0):
        if self.once_till == True:
            self.till = till
            self.once_till = False
        dis = self.till[1] - self.till[0]
        self.repeat_num = int(dis/gap) + 1
        count = 0
        for i in range(self.repeat_num):
            try:
                object = self.repeated[count]
            except:
                object = Assets(self.screen,image = self.image,size = self.size)
                self.repeated.append(object)
            posx = self.till[0] + count * gap
            if not object.pos:
                try:
                    posy = self.repeat_pos[count]
                except:
                    posy = random.randint(range_to[0],range_to[1])
            else:
                posy = object.pos[1]
            pos = (posx,posy)
            object.size = self.size
            object.velocity = (velocity,0)
            object.pos = pos
            object.show()
            # if erase_before:
            #     if posx < erase_before:
            #         self.repeated.remove(object)
            count += 1
            pass
        if erase_before:
            if self.till[0] < erase_before:
                self.till = (self.till[0] + gap,self.till[1])
                try:
                    self.repeated.remove(self.repeated[0])
                except:
                    pass
        self.till = (self.till[0] + velocity,self.till[1])
        return self.repeated
        pass


class Main:
    def __init__(self):
        pm.init()
        screen_info = pm.display.Info()
        self._screenheight  = screen_info.current_h
        self._screenwidth = screen_info.current_w
        self.groundy_list = [self.screenheight - 100,self.screenheight - 100,self.screenheight - 100]
        pass
    @property
    def screenheight(self):
        return self._screenheight
    @screenheight.setter
    def screenheight(self,value):
        if self._screenheight != value:
            self._screenheight = value
            self.screen = pm.display.set_mode((self._screenwidth,self._screenheight))
    @property
    def screenwidth(self):
        return self._screenwidth
    @screenwidth.setter
    def screenwidth(self,value):
        if self._screenwidth != value:
            self._screenwidth = value
            self.screen = pm.display.set_mode((self._screenwidth,self._screenheight))
    def ground(self,gap,range_to,till):
        self.ground_num = int(till/gap) + 1
        self.ground_count = 0
        ground_list = []
        for i in range(self.ground_num):
            posx = self.ground_count * gap
            try:
                posy = self.groundy_list[self.ground_count]
            except:
                posy = random.randint(range_to[0],range_to[1])
                self.groundy_list.append(posy)
            pos = (posx,posy)
            ground_list.append(pos)
            self.ground_count += 1
        return ground_list
        pass
    async def main(self):
        print('working....')
        self.screen = pm.display.set_mode((self._screenwidth,self._screenheight))
        player = Assets(self.screen,velocity = (0,0),pos = (50,50))
        player_flip = False
        landed = False
        launched = False
        move_for = False
        move_back = False
        slide = False
        gr = {}
        ground = Manager(self.screen,image = 'land3.png',size = (900,100))
        ground_start = 0
        ground_vel = 0
        def ground_interaction(player,i):
            nonlocal landed,launched,blocked
            player.collision(i)
            if player.objects[f'{i}'].right_collide == True and player.objects[f'{i}'].left_collide == False and i.pos[1] <= player.pos[1] + (player.height/2):
                blocked = True
                player.pos = (i.pos[0] - player.width,player.pos[1])
                player.objects[f'{i}'].down_collide = False
            if player.objects[f'{i}'].left_collide == True and player.objects[f'{i}'].right_collide == False and i.pos[1] <= player.pos[1] + (player.height/2):
                player.pos = (i.pos[0] + i.width,player.pos[1])
                player.objects[f'{i}'].down_collide = False
            if player.objects[f'{i}'].down_collide == True and i.pos[1] > player.pos[1] + (player.height/2):
                if launched == False:
                    # print(True)
                    landed = True
                    player.velocity = (player.velocity[0],0)
                player.pos = (player.pos[0],i.pos[1] - player.height)

        def obstacles(screen,ground,obs_list = [None]):
            try:
                obstacle = ground.obstacle
            except AttributeError:
                object = random.choice(obs_list)
                if object:
                    obstacle = ground.obstacle = Assets(screen,image = object.get('image',None),
                                         pos = (ground.pos[0] + ground.size[0] + object.get('posbiasx',0),ground.pos[1] + object.get('posbiasy',0)),
                                         size = object.get('size',None),
                                         velocity=(object.get('velocityx',0) + ground.velocity[0],object.get('velocityy',0) + ground.velocity[1]),
                                         flipx = object.get('flipx',False),flipy = object.get('flipy',False))
                    obstacle.vel = (object.get('velocityx',0),object.get('velcoityy',0))
                    obstacle.folder = object.get('folder',None)
                    obstacle.rate = object.get('rate',0)
                    obstacle.flip = (object.get('flipx',False),object.get('flipy',False))
                    obstacle.shoot = object.get('shoot',None)
                else:
                    obstacle = ground.obstacle = object
            if obstacle:
                if obstacle.folder:
                    obstacle.animate(obstacle.folder,rate=obstacle.rate,flip = obstacle.flip[0])
                obstacle.velocity = (obstacle.vel[0] + ground.velocity[0],obstacle.vel[1] + ground.velocity[1])
                obstacle.show()
                if obstacle.shoot:
                    obstacles(screen,obstacle,obstacle.shoot)
        fireball = {'folder' : 'fire_ball','size' : (10,10),'posbiasy' : 10,'posbiasx' : -25,'velocityx' : -1}
        statue = {'image' : 'ancientdog_statue.png','size' : (25,50),'posbiasx' : -25,'posbiasy' : -50,'flipx' : True,'shoot' : [fireball]}
        while True:
            blocked = False
            self.screen.fill((0,0,0))
            player.show()
            # ground.show()
            player.animate('walking',flip = False)
            grounds = ground.repeat(ground.size[0],(self.screenheight - 100,self.screenheight - 50),(ground_start,self.screenwidth),velocity = ground_vel,erase_before=-1400)
            # grounds = self.ground(150,(600,700),1400)
            landed = False
            # print(player.velocity[1])
            if player.velocity[1] >= 0:
                launched = False
            for i in grounds:
                ground_interaction(player,i)
                obstacles(self.screen,i,[statue,None])
            # for i in range(len(grounds)):
            #     gr[i] = Assets(self.screen,image = 'land.png',pos = grounds[i],size = (150,100))
            #     gr[i].show()
            #     player.collision(gr[i])
            #     if player.objects[f'{gr[i]}'].down_collide == True:
            #         landed = True
            #         player.velocity = (player.velocity[0],0)
            #         player.pos = (player.pos[0],gr[i].pos[1] - player.height)
            if landed == False:
                # if player.velocity[1] >= 0:
                #     print('yes')
                #     player.velocity = (player.velocity[0],1)
                #     player.acceleration = (0,0)
                # else:
                player.acceleration = (player.acceleration[0],+0.01)
            
            # if move_for == True:
            if player.pos[0] < 150 and blocked == False:
                player.velocity = (0.5,player.velocity[1])
                ground_vel = 0
            else:
                ground_vel = -0.5
                if blocked:
                    player.folder = 'standing'
                    player.velocity = (ground_vel,player.velocity[1])
                else:
                    if slide:
                        player.folder = 'sliding'
                    else:
                        player.folder = 'walking'
                    player.velocity = (0,player.velocity[1])
            # else:
            #     player.velocity = (0,player.velocity[1])

            # elif move_back == True:
            #     if player.pos[0] > 100:
            #         player.velocity = (-1,player.velocity[1])
            #         ground_vel = 0
            #     else:
            #         player.velocity = (0,player.velocity[1])
            #         ground_vel = 1
            #     player_flip = True
            # else:
            #     player.velocity = (0,player.velocity[1])
            #     player.folder = 'standing'
            #     ground_vel = 0
            if player.pos[1] > self.screenheight:
                quit()
            for event in pm.event.get():
                if event.type == pm.QUIT:
                    quit()
                if event.type == pm.KEYDOWN:
                    if event.key == pm.K_SPACE and landed == True and not slide:
                        player.velocity = (player.velocity[0],-1)
                        launched = True
                    if event.key == pm.K_DOWN and landed:
                        slide = True
                elif event.type == pm.KEYUP:
                    if event.key == pm.K_DOWN:
                        slide = False
            pm.display.update()
            await asyncio.sleep(0)
            pass
        pass
game = Main()
asyncio.run(game.main())
# game.main()