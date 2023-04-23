#Imported Modules Being Used
import math
import pgzrun
import pygame
import pgzero
import sys
import random
from pgzero.builtins import Actor
from random import randint

#General Game Characteristics (Size, Starting Positions, Movement Speed, Actor Characteristics)
WIDTH = 800 
HEIGHT = 600
CENTER_X = WIDTH / 2
CENTER_Y = HEIGHT / 2
CENTER = (CENTER_X, CENTER_Y)
FONT_COLOR = (0, 0, 0)

EGG_TARGET = 20             #Number of Eggs needed to Win
HERO_START = (100, 200)     #Character Start Position
ATTACK_DISTANCE = 150       #Dragon Breath Distance
DRAGON_WAKE_TIME = 4        #Length of Dragon Attacks
EGG_HIDE_TIME = 2           #Dragon Egg Reveal
MOVE_DISTANCE = 6           #Hero Movement Speed

#Starting Game Characteristics
lives = 6
eggs_collected = 0
game_over = False
game_complete = False
reset_required = False

#Irregulates Dragon Behavior
x = random.randint(1, 10)
y = random.randint(1, 7)
z = random.randint(1, 5)

#Sets difficulty of each dragon
easy_lair = {
    "dragon": Actor("dragon-asleep", pos=(600, 100)),
    "eggs": Actor("one-egg", pos=(480, 100)),
    "egg_count": 1,
    "egg_hidden": False,
    "egg_hide_counter": 0,
    "sleep_length": x,
    "sleep_counter": 0,
    "wake_counter": 0
 }
medium_lair = {
    "dragon": Actor("dragon-asleep", pos=(600, 300)),
    "eggs": Actor("two-eggs", pos=(480, 300)),
    "egg_count": 2,
    "egg_hidden": False,
    "egg_hide_counter": 0,
    "sleep_length": y,
    "sleep_counter": 0,
    "wake_counter": 0
 }
hard_lair = {
    "dragon": Actor("dragon-asleep", pos=(600, 500)),
    "eggs": Actor("three-eggs", pos=(480, 500)),
    "egg_count": 3,
    "egg_hidden": False,
    "egg_hide_counter": 0,
    "sleep_length": 4,
    "sleep_counter": z,
    "wake_counter": 0
 }

#Draws the Lairs and Characters onto Board
lairs = [easy_lair, medium_lair, hard_lair]
hero = Actor("hero", pos=HERO_START)
hero2 = Actor("hero2", pos=HERO_START)

#End Game Screen Characteristics
def draw():
    global lairs, eggs_collected, lives, game_complete
    screen.clear()
    screen.blit("dungeon", (0, 0))
    if game_over:
        screen.draw.text("GAME OVER!", fontsize=60, center=CENTER, color=FONT_COLOR)
    elif game_complete:
        screen.draw.text("YOU WON!", fontsize=60, center=CENTER, color=FONT_COLOR)
    else:
        hero.draw()
        hero2.draw()
        draw_lairs(lairs)
        draw_counters(eggs_collected, lives)
        
#Draw each dragon into lair
def draw_lairs(lairs_to_draw):
    for lair in lairs_to_draw:
        lair["dragon"].draw()
        if lair["egg_hidden"] is False:
            lair["eggs"].draw()
            
#Draws Score Count of Eggs and Lives onto Screen
def draw_counters(eggs_collected, lives):
    screen.blit("egg-count", (0, HEIGHT - 30))
    screen.draw.text(str(eggs_collected),
                     fontsize=40,
                     pos=(30, HEIGHT - 30),
                     color=FONT_COLOR)
    screen.blit("life-count", (60, HEIGHT - 30))
    screen.draw.text(str(lives),
                     fontsize=40,
                     pos=(90, HEIGHT - 30),
                     color=FONT_COLOR)
    screen.draw.text(str(lives),
                     fontsize=40,
                     pos=(90, HEIGHT - 30),
                     color=FONT_COLOR)
 
#Enable Co-Op Character Movement    
def update():
    
    #Hero One Character Movement
    if keyboard.right:
        hero.x += MOVE_DISTANCE
        if hero.x > WIDTH:
            hero.x = WIDTH
    elif keyboard.left:
        hero.x -= MOVE_DISTANCE
        if hero.x < 0:
            hero.x = 0
    elif keyboard.down:
            hero.y += MOVE_DISTANCE
            if hero.y > HEIGHT:
                hero.y = HEIGHT
    elif keyboard.up:
        hero.y -= MOVE_DISTANCE
        if hero.y < 0:
            hero.y = 0

    check_for_collisions()
    
    #Hero Two Character Movement 
    if keyboard.d:
        hero2.x += MOVE_DISTANCE
        if hero.x > WIDTH:
            hero.x = WIDTH
    elif keyboard.a:
        hero2.x -= MOVE_DISTANCE
        if hero2.x < 0:
            hero.x = 0
    elif keyboard.s:
            hero2.y += MOVE_DISTANCE
            if hero.y > HEIGHT:
                hero2.y = HEIGHT
    elif keyboard.w:
        hero2.y -= MOVE_DISTANCE
        if hero2.y < 0:
            hero2.y = 0

    #Enables Collision Module       
    check_for_collisions()
    
def update_lairs():
    global lairs, hero, hero2, lives
    for lair in lairs:
        if lair["dragon"].image == "dragon-asleep":
            update_sleeping_dragon(lair)
        elif lair["dragon"].image == "dragon-awake":
            update_waking_dragon(lair)
        update_egg(lair)
clock.schedule_interval(update_lairs, 1)

#Sets Dragon Awake and Sleeping Duration
def update_sleeping_dragon(lair):
    if lair["sleep_counter"] >= lair["sleep_length"]:
        lair["dragon"].image = "dragon-awake"
        lair["sleep_counter"] = 0
    else:
        lair["sleep_counter"] += 1
        
def update_waking_dragon(lair):
    if lair["wake_counter"] >= DRAGON_WAKE_TIME:
        lair["dragon"].image = "dragon-asleep"
        lair["wake_counter"] = 0
    else:
        lair["wake_counter"] += 1

#Sets Egg Duration of Appearance and Disappearance        
def update_egg(lair):
    if lair["egg_hidden"] is True:
        if lair["egg_hide_counter"] >= EGG_HIDE_TIME:
            lair["egg_hidden"] = False
            lair["egg_hide_counter"] = 0    
        else:
            lair["egg_hide_counter"] += 1
            
#Sets Collisions of Eggs and Dragon Breath                
def check_for_collisions():
    global lairs, eggs_collected, lives, reset_required, game_complete
    for lair in lairs:
        if lair["egg_hidden"] is False:
            check_for_egg_collision(lair)
        if lair["dragon"].image == "dragon-awake" and reset_required is False:
            check_for_dragon_collision(lair)

#Sets Dragon Range of Attacks            
def check_for_dragon_collision(lair):
    x_distance = hero.x - lair["dragon"].x
    y_distance = hero.y - lair["dragon"].y
    distance = math.hypot(x_distance, y_distance)
    if distance < ATTACK_DISTANCE:
        handle_dragon_collision()
    
    x_distance = hero2.x - lair["dragon"].x
    y_distance = hero2.y - lair["dragon"].y
    distance = math.hypot(x_distance, y_distance)
    if distance < ATTACK_DISTANCE:
        handle_dragon_collision()
        
#Resets Character Position After Collision        
def handle_dragon_collision():
    global reset_required
    reset_required = True
    animate(hero, pos=HERO_START, on_finished=subtract_life)
    animate(hero2, pos=HERO_START, on_finished=subtract_life)
    
#Adds Egg Count For Each Egg Collected for each character
def check_for_egg_collision(lair):
    global eggs_collected, game_complete
    if hero.colliderect(lair["eggs"]):
        lair["egg_hidden"] = True
        eggs_collected += lair["egg_count"]
        
    if hero2.colliderect(lair["eggs"]):
        lair["egg_hidden"] = True
        eggs_collected += lair["egg_count"]
        if eggs_collected >= EGG_TARGET:
            game_complete = True
            
#Decreases total amount of lives when character comes into contact with fire            
def subtract_life():
    global lives, reset_required, game_over
    lives -= 1
    if lives == 0:
        game_over = True
    reset_required = False   

#Runs Game
pgzrun.go()