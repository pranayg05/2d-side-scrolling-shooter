
import pygame
import os 
import random
import csv 
import button
 

pygame.init()

#block of code for game window
screen_width=800                    
screen_height=int(screen_width*0.8) 

screen=pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('star wars') 
#-----------------------------------------------

clock=pygame.time.Clock()
fps=60


gravity=0.5 #variable for gravity (how quick the player falls down
scroll_thresh=200
ROWS=16
COLS=150
tile_size=screen_height//ROWS
tile_types=21
max_levels=2
screen_scroll=0
bg_scroll=0
level=1
start_game= False

#player action variables for keyboard movement
moving_left=False 
moving_right=False
shoot=False
grenade=False
grenade_thrown=False

# Scale the grenade image to the desired size
grenade_img=pygame.image.load('img/icons/grenade.png').convert_alpha()
# New width and height for the grenade image
new_grenade_width = 30
new_grenade_height = 10

#load images
#button images
start_img=pygame.image.load('img/start_btn.png').convert_alpha()
exit_img=pygame.image.load('img/exit_btn.png').convert_alpha()
restart_img=pygame.image.load('img/restart_btn.png').convert_alpha()

#background
pine1_img=pygame.image.load('img/Background/pine1.png').convert_alpha()
pine2_img=pygame.image.load('img/Background/pine2.png').convert_alpha()
mountain_img=pygame.image.load('img/Background/mountain.png').convert_alpha()
sky_img=pygame.image.load('img/Background/sky.png').convert_alpha()
#store tiles in  a list

img_list=[]
for x in range(tile_types):
    img=pygame.image.load(f'img/tile/{x}.png')
    img=pygame.transform.scale(img,(tile_size, tile_size))
    img_list.append(img)


grenade_img = pygame.transform.scale(grenade_img, (new_grenade_width, new_grenade_height))
bullet_img=pygame.image.load('img/icons/bullets.png').convert_alpha()
health_box_img=pygame.image.load('img/icons/health_box.png').convert_alpha()
ammo_box_img=pygame.image.load('img/icons/ammo_box.png').convert_alpha()
grenade_box_img=pygame.image.load('img/icons/grenade_box.png').convert_alpha()
item_boxes={
    'Health'  :health_box_img,
    'Ammo'    :ammo_box_img,
    'Grenade' :grenade_box_img

}



#defining colours
BG=(144,201,120) #RGB Value for colours and background
RED=(255,0,0) #Red line for floor colour
WHITE=(255,255,255)
GREEN=(0,255,0)
BLACK=(0,0,0)

font=pygame.font.SysFont('Futura',30)

def draw_text(text,font,text_col,x,y):
    img=font.render(text,True,text_col)
    screen.blit(img,(x,y))



def draw_bg():
	screen.fill(BG) 
	width = sky_img.get_width()
	for x in range(5):
		screen.blit(sky_img, ((x * width) - bg_scroll * 0.5, 0))
		screen.blit(mountain_img, ((x * width) - bg_scroll * 0.6, screen_height - mountain_img.get_height() - 300))
		screen.blit(pine1_img, ((x * width) - bg_scroll * 0.7, screen_height - pine1_img.get_height() - 150))
		screen.blit(pine2_img, ((x * width) - bg_scroll * 0.8, screen_height - pine2_img.get_height()))
    
#function to reset level
def reset_level():
	enemy_group.empty()
	bullet_group.empty()
	grenade_group.empty()
	explosion_group.empty()
	item_box_group.empty()
	decoration_group.empty()
	water_group.empty()
	exit_group.empty()

	#create empty tile list
	data = []
	for row in range(ROWS):
		r = [-1] * COLS
		data.append(r)

	return data


# block of code below is for all the variables that need to made for each process
class soldier(pygame.sprite.Sprite):                # block of code which allows me to create players/enemies
    def __init__(self,char_type,x,y,scale,speed,ammo,grenade):  #without creating a seperate code for each player example is player 1 and player 2 are the same charcter so i dont need to create 2 differnt loaction of where they are saved i can use this code to output them onto tyhe screen 
        pygame.sprite.Sprite.__init__(self)
        self.alive=True #current set to true so he doesnt die and only when a projetile touches him it will be st to false after
        self.char_type=char_type
        self.speed=speed #player speed can chnage how quicly he goes in player variable below
        self.ammo= ammo
        self.start_ammo=ammo
        self.shoot_cooldown=0
        self.grenade=grenade
        self.health=100
        self.max_health=self.health
        self.direction=1
        self.vel_y=0 #how quick the player falls down after jumping set to 0 and can change below on player variable
        self.jump=False #sets the jump to false so he not floating away
        self.in_air=True #
        self.flip=False #sets it false so he flips direction when key is pressed
        self.is_dead = False 
        self.animation_list=[] #list for animations e.g. run jump idle
        self.frame_index=0
        self.action=0
        self.update_time=pygame.time.get_ticks()
        #ai specific variables
        self.move_counter=0
        self.vision = pygame.Rect(0, 0, 150, 20)
        self.idling=False
        self.idling_counter=0
       
        


        #load all images for players
        animation_types=['Idle','Run','Jump','Death']
        for animation in animation_types:
            #reset temporary list of images
            temp_list=[]
            #count number of files in the folder
            num_of_frames=os.listdir(f'img/{self.char_type}/{animation}')
            for i in range(len(num_of_frames)):#loops the picture i saved in a file
                img= pygame.image.load(f'img/{self.char_type}/{animation}/{i}.png').convert_alpha()  # gets the image of player where i saved and outputs to screen
                img=pygame.transform.scale(img,(int(img.get_width()*scale),int(img.get_height()*scale)))  #how big i want the player img variable
                temp_list.append(img)
            self.animation_list.append(temp_list)
        self.image=self.animation_list[self.action][self.frame_index]
        self.rect=temp_list[i].get_rect() 
        self.rect.center=(x,y)
        self.width=self.image.get_width()
        self.height=self.image.get_height() 
#E:\alevelcsproject\img\mando\Idle\0.png.png

        
        if self.char_type == 'enemy':  # Check if the character is an enemy/droid
            new_width = 58  # New width for the hitbox
            new_height = 87  # New height for the hitbox
            self.rect.width = new_width
            self.rect.height = new_height

        if self.char_type == 'player':
                new_width = 35  # New width for the hitbox
                new_height = 75  # New height for the hitbox
                self.rect.width = new_width
                self.rect.height = new_height

    def update(self):
        self.update_animation()
        self.check_alive()
        if self.shoot_cooldown > 0:
            self.shoot_cooldown -=1
        if self.health <= 0:
            self.health = 0
            self.speed = 0
            self.alive = False
            self.is_dead = True  # Set is_dead to True when the enemy dies
            self.update_action(3)
            explosion = Explosion(self.rect.x, self.rect.y, 2)
            explosion_group.add(explosion)
            self.kill()  # Remove the enemy from the sprite groups when it dies





    # code which allows player movement
    def move(self,moving_left,moving_right): 
        #reset moving variables
        screen_scroll=0
        dx=0
        dy=0



        #moving variables if they are moving left or right
        if moving_left:
            dx= -self.speed
            self.flip=True #if he moves left player will flip and face other direction
            self.direction=-1 
        if moving_right:
            dx=self.speed
            self.flip=False #if he moves right player will flip back and move to original position
            self.direction=1 

        if self.jump==True and self.in_air==False:
            self.vel_y=-11
            self.jump=False
            self.in_air=True

        #apply gravity
        self.vel_y+=gravity
        if self.vel_y>10:
            self.vel_y
        dy+=self.vel_y

        #checks collision with floor with the level and boxes
        for tile in world.obstacle_list: # collision in x direction
            if tile[1].colliderect(self.rect.x + dx, self.rect.y, self.width, self.height):
                dx=0
                #if ai has hit wall make it turn around
                if self.char_type =='enemy':
                    self.direction *=-1
                    self.move_counter=0
            if tile[1].colliderect(self.rect.x, self.rect.y + dy, self.width, self.height):
                if self.vel_y < 0: # checks if its below the ground when jumping
                    self.vel_y=0
                    dy=tile[1].bottom-self.rect.top
                elif self.vel_y >=0: # checks if above the ground when falling
                    self.vel_y=0
                    self.in_air=False
                    dy=tile[1].top - self.rect.bottom


        if pygame.sprite.spritecollide(self,water_group,False):
            self.health=0

        level_complete = False
        if pygame.sprite.spritecollide(self,exit_group,False):
            level_complete = True

        if self.rect.bottom > screen_height:
            self.health=0




        #code which updates position of player
        self.rect.x +=dx
        self.rect.y +=dy

        #update scroll on player position
        if self.char_type =='player':
            if (self.rect.right > screen_width - scroll_thresh and bg_scroll <(world.level_length * tile_size)- screen_width)\
                or (self.rect.left < scroll_thresh and bg_scroll > abs(dx)):
                self.rect.x -=dx
                screen_scroll= -dx

        return screen_scroll, level_complete
        
    #----------------------------------------------
    def shoot(self):
        if self.shoot_cooldown==0 and self.ammo>0:
            self.shoot_cooldown=20
            bullet=Bullet(self.rect.centerx +(0.75*self.rect.size[0]*self.direction),self.rect.centery,self.direction)
            bullet_group.add(bullet)
            self.ammo-=1


    def ai(self):
        if self.alive and player.alive:
            if self.idling == False and  random.randint(1,200)==1:
                self.update_action(0)
                self.idling=True
                self.idling_counter=50
            #check if ai is near the player
            if self.vision.colliderect(player.rect):
                #stop running and face the player
                self.update_action(0)#0 is idle
                #shoot
                self.shoot()
            else:
                if self.idling==False:
                    if self.direction==1:
                        ai_moving_right=True
                    else:
                        ai_moving_right=False
                    ai_moving_left= not ai_moving_right
                    self.move(ai_moving_left, ai_moving_right)
                    self.update_action(1)#1:run
                    self.move_counter +=1
                    #update ai vison as the enemy moves
                    self.vision.center=(self.rect.centerx + 75 *self.direction, self.rect.centery)
                    #pygame.draw.rect(screen,RED,self.vision)

                    if self.move_counter > tile_size:
                        self.direction *=-1
                        self.move_counter *=-1

                else:
                    self.idling_counter-=1
                    if self.idling_counter<=0:
                        self.idling=False

            self.rect.x +=screen_scroll
            








    def update_animation(self):
        ANIMATION_COOLDOWN=80 #how quickly the code cycles through the images
        self.image=self.animation_list[self.action][self.frame_index]
        if pygame.time.get_ticks()-self.update_time > ANIMATION_COOLDOWN:
            self.update_time=pygame.time.get_ticks()
            self.frame_index+=1
        if self.frame_index>=len(self.animation_list[self.action]):
            if self.action==3:
                self.frame_index=len(self.animation_list[self.action])-1
            else:
                self.frame_index=0 





    def update_action(self, new_action): # checks if new action is different to previous one
        if new_action !=self.action:
                self.action=new_action
                #update animation settings
                self.frame_index=0
                self.update_time=pygame.time.get_ticks()


    def check_alive(self):
        if self.health<=0:
            self.health=0
            self.speed=0
            self.alive=False
            self.update_action(3)



    def draw(self): #code draws player onto screen
        screen.blit(pygame.transform.flip(self.image,self.flip,False),self.rect)
        #pygame.draw.rect(screen,RED,self.rect,1)
       
class World():
    def __init__(self):
        self.obstacle_list=[]

    def process_data(self,data):
        self.level_length=len(data[0])
        #iterate through each value in level data file
        for y, row in enumerate(data):
            for x, tile in enumerate(row):
                if tile >= 0:
                    img = img_list[tile]
                    img_rect=img.get_rect()
                    img_rect.x=x*tile_size
                    img_rect.y=y*tile_size
                    tile_data=(img, img_rect)
                    if tile >= 0 and tile <= 8:
                        self.obstacle_list.append(tile_data)
                    elif tile >= 9 and tile <= 10:
                        water=Water(img,x * tile_size, y*tile_size)
                        water_group.add(water)
                    elif tile >=11 and tile <=14:
                        decoration=Decoration(img,x * tile_size, y*tile_size)
                        decoration_group.add(decoration)
                    elif tile ==15:
                        player=soldier('player', x * tile_size, y*tile_size, 1.35, 4, 20, 5) #the player itself if you look at def __init__ function you will see what ecah number is used for
                        health_bar=HealthBar(10,10,player.health,player.health)
                    elif tile == 16:#create enemys
                        enemy=soldier('enemy', x * tile_size, y*tile_size, 1.65, 2, 30, 0) #enemy variables and what he should do same with player
                        enemy_group.add(enemy)
                    elif tile==17:#create ammo box
                        item_box=ItemBox('Ammo',x * tile_size, y*tile_size)
                        item_box_group.add(item_box)
                    elif tile==18:#create ammo box
                        item_box=ItemBox('Grenade',x * tile_size, y*tile_size)
                        item_box_group.add(item_box) 
                    elif tile==19:#create ammo box
                        item_box=ItemBox('Health',x * tile_size, y*tile_size)
                        item_box_group.add(item_box) 
                    elif tile == 20:# creates exit
                        exit=Exit(img,x * tile_size, y*tile_size)
                        exit_group.add(exit)

        return player, health_bar
    
    def draw(self):
        for tile in self.obstacle_list:
            tile[1][0] += screen_scroll
            screen.blit(tile[0],tile[1])


class Decoration(pygame.sprite.Sprite):
    def __init__(self,img,x,y):
        pygame.sprite.Sprite.__init__(self)
        self.image=img
        self.rect=self.image.get_rect()
        self.rect.midtop=(x + tile_size // 2, y +(tile_types-self.image.get_height()))

      

    def update(self):
        self.rect.x +=screen_scroll

class Water(pygame.sprite.Sprite):
    def __init__(self,img,x,y):
        pygame.sprite.Sprite.__init__(self)
        self.image=img
        self.rect=self.image.get_rect()
        self.rect.midtop=(x+tile_size//2, y + tile_size)

    def update(self):
        self.rect.x +=screen_scroll


class Exit(pygame.sprite.Sprite):
    def __init__(self,img,x,y):
        pygame.sprite.Sprite.__init__(self)
        self.image=img
        self.rect=self.image.get_rect()
        self.rect.midtop=(x+tile_size//2, y +(tile_types-self.image.get_height()))

    def update(self):
        self.rect.x +=screen_scroll





class ItemBox(pygame.sprite.Sprite):
    def __init__(self,item_type,x,y):
        pygame.sprite.Sprite.__init__(self)
        self.item_type=item_type
        self.image=item_boxes[self.item_type]
        self.rect=self.image.get_rect()
        self.rect.midtop=(x+tile_size//2,y+(tile_size-self.image.get_height()))


    
    def update(self):
        #scrolling
        self.rect.x +=screen_scroll

        if pygame.sprite.collide_rect(self,player):
            if self.item_type=='Health':
                player.health+=25
                if player.health>player.max_health:
                    player.health=player.max_health
            elif self.item_type=='Ammo':
                player.ammo+=15
            elif self.item_type=='Grenade':
                player.grenade+=3
            self.kill()#this deletes the item box when it gets colleted


class HealthBar():
    def __init__(self,x,y,health,max_health):
        self.x=x
        self.y=y
        self.health=health
        self.max_health=max_health

    def draw(self,health):
        self.health=health

        ratio=self.health/self.max_health
        pygame.draw.rect(screen, BLACK,(self.x-2,self.y-2,154,24))
        pygame.draw.rect(screen, RED,(self.x,self.y,150,20))
        pygame.draw.rect(screen, GREEN,(self.x,self.y,150*ratio,20))

class Bullet(pygame.sprite.Sprite):
    def __init__(self,x,y,direction):
        pygame.sprite.Sprite.__init__(self)
        self.speed=10
        self.image=bullet_img
        self.rect=self.image.get_rect()
        self.rect.center=(x,y)
        self.direction=direction

    def update(self):
        self.rect.x +=(self.direction*self.speed) + screen_scroll
        #check if bullet has gome off screen
        if self.rect.right<0 or self.rect.left > screen_width:
            self.kill()
        #checks for collision with blocks
        for tile in world.obstacle_list:
            if tile[1].colliderect(self.rect):
                self.kill()
        #check if it hits enemy or player 
        if pygame.sprite.spritecollide(player,bullet_group,False):
            if player.alive:
                player.health-=5
                self.kill()
        for enemy in enemy_group:
            if pygame.sprite.spritecollide(enemy,bullet_group,False):
                if enemy.alive:
                    enemy.health-=25
                    print(enemy.health)
                    self.kill()


class Grenade(pygame.sprite.Sprite):
    def __init__(self,x,y,direction):
        pygame.sprite.Sprite.__init__(self)
        self.timer=100
        self.vel_y=-11 
        self.speed=7
        self.image=grenade_img
        self.rect=self.image.get_rect()
        self.rect.center=(x,y)
        self.width=self.image.get_width()
        self.height=self.image.get_height()

        self.direction=direction



    def update(self):
        self.vel_y+=gravity
        dx=self.direction*self.speed
        dy=self.vel_y

        #check for collison with floor
        for tile in world.obstacle_list:
            #check collision with wall
            if tile[1].colliderect(self.rect.x +dx, self.rect.y, self.width, self.height):
                self.direction*=-1
                dx=self.direction*self.speed
                #check collision in y direction
            if tile[1].colliderect(self.rect.x, self.rect.y + dy, self.width, self.height):
                self.speed=0
                if self.vel_y < 0: # checks if its below the ground when thrown
                    self.vel_y=0
                    dy=tile[1].bottom-self.rect.top
                elif self.vel_y >=0: # checks if above the ground when falling
                    self.vel_y=0
                    dy=tile[1].top - self.rect.bottom

        


          #update grenade position
        self.rect.x+=dx + screen_scroll
        self.rect.y+=dy

        #countdown timer
        self.timer-=1
        if self.timer<=0:
            self.kill()
            explosion=Explosion(self.rect.x, self.rect.y, 2)
            explosion_group.add(explosion)
            #does damage in the radius ive set
            if abs(self.rect.centerx - player.rect.centerx) < tile_size*2 and \
                abs(self.rect.centerx - player.rect.centerx) < tile_size*2:
                player.health-=50
            for enemy in enemy_group:
                if abs(self.rect.centerx - enemy.rect.centerx) < tile_size*2 and \
                    abs(self.rect.centerx - enemy.rect.centerx) < tile_size*2:
                    enemy.health-=50
                    




            
class Explosion(pygame.sprite.Sprite):
    def __init__(self,x,y,scale):
        pygame.sprite.Sprite.__init__(self)
        self.images=[]
        for num in range(1,5):
            img=pygame.image.load(f'img/explosion/{num}.png').convert_alpha()
            img=pygame.transform.scale(img,(int(img.get_width()*scale),int(img.get_height()*scale)))
            self.images.append(img)
        self.frame_index=0
        self.image=self.images[self.frame_index]
        self.rect=self.image.get_rect()
        self.rect.center=(x,y)
        self.counter=0

    def update(self):
        self.rect.x +=screen_scroll # scrolling
        explosion_speed=5
        #update explosion animation
        self.counter+=1

        if self.counter>= explosion_speed:
            self.counter=0
            self.frame_index+=1
            #if animation finished delete explosion
            if self.frame_index>=len(self.images):
                self.kill()
            else:
                self.image=self.images[self.frame_index]

start_button= button.Button(screen_width // 2 -130, screen_height // 2 - 150, start_img, 1)
exit_button= button.Button(screen_width // 2 -110, screen_height // 2 + 50, exit_img, 1)
restart_button= button.Button(screen_width // 2 - 100, screen_height // 2 - 50, restart_img, 2)




#create sprite groups
enemy_group=pygame.sprite.Group()
bullet_group=pygame.sprite.Group()
grenade_group=pygame.sprite.Group()
explosion_group=pygame.sprite.Group()
item_box_group=pygame.sprite.Group()
decoration_group=pygame.sprite.Group()
water_group=pygame.sprite.Group()
exit_group=pygame.sprite.Group()














#create empty tile list
world_data=[]
for row in range (ROWS):
    r = [-1]*COLS
    world_data.append(r)
# load in level data and creatw world
with open(f'level{level}_data.csv', newline='') as csvfile:
    reader=csv.reader(csvfile,delimiter=',')
    for x, row in enumerate(reader):
        for y, tile in enumerate (row):
            world_data[x][y]=int(tile)
world=World()
player, health_bar = world.process_data(world_data)




#whole block of code will make sure everthing runs in the loop and gets outputed onto the pygame shooter screen
run=True
while run:


    clock.tick(fps)

    if start_game==False:
        screen.fill(BG)
        if start_button.draw(screen):
            start_game= True
        if exit_button.draw(screen):
            run =False

    else:
        draw_bg() #print the background 

        world.draw()# loads the level in


        health_bar.draw(player.health)#shows health bar



        draw_text('AMMO:',font,WHITE,10,35)#shows me the ammo available
        for x in range(player.ammo):
            screen.blit(bullet_img,(90+(x*17),40))
        draw_text('GRENADES:',font,WHITE,10,60)
        for x in range(player.grenade):
            screen.blit(grenade_img,(135+(x*36),60))



        player.update() #this prints the animation, puts it in the loop 
        player.draw() #player itself goes to block of code and loads the character from there and runs it



        for enemy in enemy_group: # code to call enemy so they ge updated on to the screen
            if not enemy.is_dead:  # Only update and draw enemies that are not dead
                enemy.ai()
                enemy.update()#updates enemy actions
                enemy.draw() #this prints the enemy



        bullet_group.update()
        grenade_group.update()
        explosion_group.update()
        item_box_group.update()
        decoration_group.update()
        water_group.update()
        exit_group.update()
        bullet_group.draw(screen)
        grenade_group.draw(screen)
        explosion_group.draw(screen)
        item_box_group.draw(screen)
        decoration_group.draw(screen)
        water_group.draw(screen)
        exit_group.draw(screen)
        





        if player.alive:
            if shoot:
                player.shoot()
            elif grenade and grenade_thrown==False and player.grenade>0:
                grenade=Grenade(player.rect.centerx+(0.1*player.rect.size[0]*player.direction),\
                        player.rect.top,player.direction)
                grenade_group.add(grenade)
                grenade_thrown=True
                #reduce grenades 
                player.grenade-=1
            if player.in_air:# if staement so that if player in the air it prints the jump image i saved in a file
                player.update_action(2)#2 means jump
            elif moving_left or moving_right:
                player.update_action(1)#1 means run
            else:
                player.update_action(0)#0 means idle
            screen_scroll, level_complete  = player.move(moving_left,moving_right)
            bg_scroll-=screen_scroll
            #check if player finished level
            if level_complete:
                level +=1
                bg_scroll=0
                world_data=reset_level()
                if level<=max_levels:
                    # load in level data and creatw world
                    with open(f'level{level}_data.csv', newline='') as csvfile:
                        reader=csv.reader(csvfile,delimiter=',')
                        for x, row in enumerate(reader):
                            for y, tile in enumerate (row):
                                world_data[x][y]=int(tile)
                    world=World()
                    player, health_bar = world.process_data(world_data)
        else:
            screen_scroll = 0
            if restart_button.draw(screen):
                bg_scroll = 0
                world_data=reset_level()
                # load in level data and creatw world
                with open(f'level{level}_data.csv', newline='') as csvfile:
                    reader=csv.reader(csvfile,delimiter=',')
                    for x, row in enumerate(reader):
                        for y, tile in enumerate (row):
                            world_data[x][y]=int(tile)
                world=World()
                player, health_bar = world.process_data(world_data)
   

         


    #code to close game
    for event in pygame.event.get():
        if event.type==pygame.QUIT:
            run=False
    #--------------------------------


        #block of code to say to say key has been pressed
        if event.type==pygame.KEYDOWN:
            if event.key==pygame.K_a: #defines what key=K i press in this case d to move left
                moving_left=True
            if event.key==pygame.K_d: #defines what key=K i press in this case a to move right
                moving_right=True
            if event.key==pygame.K_SPACE: #jump
                shoot=True 
            if event.key==pygame.K_q: #throw grenades
                grenade=True 
            if event.key==pygame.K_w and player.alive:
                player.jump=True      
        #-------------------------------------------



        #block of code from to say key has been let go 
        if event.type==pygame.KEYUP:
            if event.key==pygame.K_a: #left movment
                moving_left=False
            if event.key==pygame.K_d: #right movement
                moving_right=False
            if event.key==pygame.K_SPACE:
                shoot=False
            if event.key==pygame.K_q:
                grenade=False
                grenade_thrown=False
        #-------------------------------------------


    pygame.display.update() #updates sprite so it loads onto screen
#--------------------------------------------------------------------------------------------------------
pygame.quit()
