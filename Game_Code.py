import pygame
import random
import csv
from pygame import mixer
import Game_UI
# ///////////////////// OUTER GAME FUNCTIONS //////////////////// #

def get_sprite(file, width, height, frames, row):

    # places measuring point at the bottom left corner of each sprite in the sheet
    x_coord = width*frames

    if row:
        y_coord = height*frames
    else:
        y_coord = 0 # value set to zero since the sheet only has 1 row

    # Load the sheet and records dimensions
    sheet = pygame.image.load(file).convert_alpha()

    # highlights and 'cuts out' area with needed sprite
    sprite = sheet.subsurface(pygame.Rect(x_coord, y_coord, width, height))

    return sprite


def draw_text(text, font, colour, x, y):

    # draws text onto the screen
    sentence = font.render(text, True, colour)
    screen.blit(sentence, (x, y))


def draw_background():

    # draws the background (in various layers from descending order)
    screen.fill(BG)
    screen.blit(bg_backdrop, (0, 0))
    screen.blit(bg_buildings, (0, SCREEN_HEIGHT - bg_street.get_height()+100))


def spawn_enemy(data, avatars, chosen_avatar, max_tile):

    # spawns enemies at random intervals

    # argument max level creates a limit on the strength of enemies spawned
    # (as the score progresses, the max_level increases)
    not_spawned = True

    temp = [*avatars]  # creates a list from the dictionary keys

    # reformats lists and chooses a random monster to spawn
    temp.remove('choices')
    temp.remove(chosen_avatar.replace('_', ' '))  # removes the player's avatar choice from the proposed list
    random_spawn = str(random.choice(temp)).replace(' ', '_')


    while not_spawned:

        tile_count = 0  # keeps a linear count of every tile in the cvs file
        spawn_tile = random.randint(1, max_tile)  # chooses a random tile for the enemy to spawn in

        for y, row in enumerate(data):
            for x, tile in enumerate(row):

                tile_count += 1

                if tile_count == spawn_tile:
                    if tile == -1:  # makes sure the enemy spawns in midair (and not in the middle of a platform)
                        enemies.add(Enemy(random_spawn, x * tile_size, y * tile_size, 3, 2, 300))

                        not_spawned = False

def spawn_item():

    # spawns potions at random intervals
    not_spawned = True

    while not_spawned:

        spawn_tile = random.randint(0, len(world.walls))  # chooses a random tile for the potion to spawn in
        count = 0  # creates a pointer that looks through the list

        for tile in world.walls:

            count += 1

            if count == spawn_tile:
                position = tile[1]  # collects the rectangle dimensions for the tile

                # - height to make sure that the position spawns on top of the tile
                potion = Potion(position.x - position.height, position.y - position.height)

                potions.add(potion)
                not_spawned = False


def bg_resizer(image, scale):

    # resizes given image files
    image = pygame.transform.scale(image, (int(image.get_width() * scale), int(image.get_width() * scale - 0.6)))
    return image

def contains_number(word):
    for i in range(len(word)):
        if word[i].isdigit() == True:
            return True

    return False


def create_block_list():

    block_list = []
    with open('Terms-to-Block.csv', newline='') as csvfile:
        reader = csv.reader(csvfile, delimiter=',')

        # enumarate adds a running count to the for loop (since we arent given a specific numerical range
        # allows for the variables x, y to be created which acts as makeshift co-ordinates
        for x, row in enumerate(reader):
            for y, col in enumerate(row):
                if y == 1:
                    block_list.append(row[y])

    new_list = []

    for i, word in enumerate(block_list):

        if len(block_list[i]) <= 7 and not contains_number(word):
            new_list.append(block_list[i].title())

    print(new_list)
    return new_list


# ///////////////////// SETUP //////////////////////// #


# ////// INITIALISATIONS //////
mixer.init()
pygame.init()


# ////// MUSIC //////
#load music
pygame.mixer.music.load('aud/Overcome (This Time).mp3')  # music to load
pygame.mixer.music.set_volume(0.1)  # volume for the music

#load sfx
fx_jump = pygame.mixer.Sound('aud/sfx/Jump.mp3')  # music to load
fx_jump.set_volume(0.1)  # volume for the music

fx_gameover = pygame.mixer.Sound('aud/sfx/Game Over.mp3')  # music to load

fx_hit = pygame.mixer.Sound('aud/sfx/Hit #1.mp3')  # music to load
fx_hit.set_volume(0.15)  # volume for the music

fx_shoot = pygame.mixer.Sound('aud/sfx/Sfx/Laser or Shoot/Shoot_001.wav')  # music to load
fx_shoot.set_volume(0.07)  # volume for the music

fx_fall = pygame.mixer.Sound('aud/sfx/Sfx/Hit or Hurt/003.wav')  # music to load
fx_fall.set_volume(0.1)  # volume for the music

fx_dead = pygame.mixer.Sound('aud/sfx/Sfx/Random/Randomize9.wav')  # music to load
fx_dead.set_volume(0.1)  # volume for the music

fx_potion = pygame.mixer.Sound('aud/sfx/Sfx/Jump/Jump_002.wav')  # music to load
fx_potion.set_volume(0.15)  # volume for the music

# ////// WINDOWS //////
# window setup (at a specific ratio)
SCREEN_WIDTH = 800
SCREEN_HEIGHT = int(SCREEN_WIDTH * 0.8)

# screen sections
screen_game = False
screen_main = True
screen_score = False

# creates game window with a title caption
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Monster Rumble')


# ////// GAME PHYSICS //////

# Frame Rate setup
clock = pygame.time.Clock()
FPS = 60

# Physics variables
GRAVITY = 0.75


# ////// LEVEL CREATION //////

tile_size = SCREEN_HEIGHT // 16  # makes sure the level is as wide as the screen - no cut-off
tile_types = 21  # how many different tiles in the level - important because tiles are identified as numbers in a csv file

# load tile images
tile_img_list = []
for x in range(tile_types):
    img = pygame.image.load(f'img/tile/{x}.png')
    img = pygame.transform.scale(img, (tile_size, tile_size))
    tile_img_list.append(img)


# ////// COLOURS & FONTS //////

# colour setup
BG = (144, 201, 120)
EMPTY_HP = (255, 0, 0)
CURRENT_HP = (0, 255, 0)
BORDER = (0, 0, 0)
SCORE_COLOUR = (255, 255, 255)

GAME_FONT = pygame.font.Font('img/Tiny Hero/Font/04B_30__.ttf', 30)  # installs a font


# ////// BACKGROUND //////
# background image files
bg_backdrop = pygame.image.load('img/Background/Cyberpunk Street/PNG/far-buildings.png').convert_alpha()
bg_backdrop = bg_resizer(bg_backdrop, (SCREEN_WIDTH / bg_backdrop.get_width()))

bg_buildings = pygame.image.load('img/Background/Cyberpunk Street/PNG/back-buildings.png').convert_alpha()
bg_buildings = bg_resizer(bg_buildings, (SCREEN_WIDTH / bg_buildings.get_width()))

bg_street = pygame.image.load('img/Background/Cyberpunk Street/PNG/foreground.png').convert_alpha()
bg_street = bg_resizer(bg_street, (SCREEN_WIDTH / bg_street.get_width()))

# item image files
bullet_img = pygame.image.load('img/Gunner/EXTRAS/rsz_bluebullet.png').convert_alpha()
potion_img = pygame.image.load('img/Assets/Fancy Potion.png').convert_alpha()
potion_img = pygame.transform.scale(potion_img, (int(potion_img.get_width() * 0.1), int(potion_img.get_width() * 0.1)))


# ///////////////////// ACTION VARIABLE SETUP //////////////////////// #

# Player actions - Set to false for 'Idle'
move_left = False
move_right = False
shoot = False
attack = False


# ///////////////////// CLASSES //////////////////////// #


class World:

    def __init__(self):
        self.walls = []  # stores all of the floor/platform tile locations

    def proccess_data(self, data):
        # turns csv list into image data

        tile_count = -1

        for y,row in enumerate(data):
            for x, tile in enumerate(row):
                tile_count += 1  # keeps a count of the linear position of the tile

                if tile >= 0:  # -1 are negative space so are ignored

                    # generates a graphic for the given tile
                    # (loads the image associated with the number in the level editor)
                    graphic = tile_img_list[tile]
                    graphic_rect = graphic.get_rect()

                    # allows the tiles to be resized to ensure dimensions stay the same
                    graphic_rect.x = x * tile_size
                    graphic_rect.y = y * tile_size

                    # tuple: (image, dimensions, tile number and place in csv sheet)
                    tile_data = (graphic, graphic_rect, tile, tile_count)

                    if tile <= 8:  # makes sure the correct tiles are recorded as walls for collision detection
                        self.walls.append(tile_data)

        return tile_count

    def draw(self):  # draws the level
        for tile in self.walls:
            screen.blit(tile[0], tile[1])  # blit arguments for image and rectangle size

# ----------------------

class Fighter(pygame.sprite.Sprite):
    # creates a blueprint to be used for character creation (includes sprite, size, hitbox and starting co-ordinates)

    def __init__(self, character_type, x, y, scale, speed, health):
        pygame.sprite.Sprite.__init__(self)

        # //////// STATS //////////
        self.health = health  # the current amount of hp the character has
        self.max_health = health  # the original amount of hp
        self.speed = speed  # how many pixels the rectangle is transposed by per input
        self.character_type = character_type  # used for leaderboard, given by screen_main_avatar
        self.velocity = 0  # how quickly the player jumps

        # //////// COUNTERS //////////
        self.shoot_cooldown = 0  # limits how many bullets can be fired per second
        self.attack_cooldown = 0
        # death_counter = starts a countdown for character de-loading from memory after they've been killed
        self.death_counter = 60
        self.score = 8

        # //////// BOOLEAN CHECKS //////////
        # sets the direction that the sprite is facing (multiplies movement by value)
        self.direction = 1  # (boolean 1, -1)

        self.jump = False  # states if the character is about to jump
        self.fall = False  # states if the character is about to fall
        self.gap = False  # states if the player is trying to fall through platforms (pass through a gap)
        self.airborne = True  # states if the player is midair
        self.flip = False  # states whether the sprite pixels should be flipped horizontally
        self.edge = False  # tells the code that the player has reached the edge of the screen
        self.alive = True  # records if health is more than 0 (not game over)

        # //////// ANIMATIONS //////////
        # collects all the individually cut frames and points to the starting frame
        self.frames = []  # stores loaded frames to create an animation
        self.frame_index = 0  # acts as a pointer to run animation

        self.animation = 0  # records the current action of the sprite

        # records the current time to see whether or not an animation is finished (by comparing to a set given time)
        self.update_time = pygame.time.get_ticks()

        animation_types = ['Idle', 'Run', 'Jump', 'Death', 'Attack_1']  # list of different actions

        for motions in animation_types:

            frame = 0
            temp_list = []  # empty list to house frames during the cutting process

            # gains dimensions of the sprite sheet
            sheet = pygame.image.load(f'img/Tiny Hero/{self.character_type}/{self.character_type}_'
                                      f'{motions}.png').convert_alpha()

            sheet_rect = sheet.get_rect()

            # uses these dimensions to cycle through the sheet an appropriate amount of times
            # to 'cut out' the individual sprites
            for i in range(sheet_rect.width // sheet_rect.height):
                sprite = get_sprite(f'img/Tiny Hero/{self.character_type}/{self.character_type}_{motions}.png',
                                    sheet_rect.height, sheet_rect.height, frame, False).convert_alpha()

                sprite = pygame.transform.scale(sprite, (int(sprite.get_width() * (scale - 0.6)),
                                                         int(sprite.get_width() * (scale - 0.6))))
                temp_list.append(sprite)
                frame += 1

            self.frames.append(temp_list)

        # //////// CREATING THE SPRITE (AND HITBOXES) //////////
        self.sprite = self.frames[self.animation][self.frame_index]  # displays the animation for the inputted action

        self.rect = self.sprite.get_rect()
        self.rect.center = (x, y)
        self.width = self.sprite.get_width()
        self.height = self.sprite.get_height()

    def update(self):

        # checks and updates everything

        self.update_frames()
        self.dead()

        if self.shoot_cooldown > 0:
            self.shoot_cooldown -= 1

    def move(self, move_left, move_right):

        # ///////// PLAYER MOVEMENT /////////
        # proposed movement variables
        # variables are set to zero to make sure the proposed movement amount is reset for each press
        dx = 0
        dy = 0

        if move_left:
            dx = -self.speed
            self.direction = -1
            self.flip = True

        if move_right:
            dx = self.speed
            self.direction = 1
            self.flip = False

        if self.jump and not self.airborne:  # if player has not jumped after key has been pressed
            self.velocity = -16
            self.jump = False
            self.airborne = True

        if self.fall and not self.airborne:  # if player has not fallen after key has been pressed
            self.velocity = 5
            self.fall = False
            self.airborne = True

        self.velocity += GRAVITY  # creating a jump curve

        if self.velocity > 14:  # terminal velocity
            self.velocity += 0.05  # incrementing to mimic the transference of kinetic energy to gravitational

        dy += self.velocity

        # ///////// COLLISSION CHECKS /////////

        for tile in world.walls:
            # checks for collision before the player actual moves (uses dx/dy for the 'proposed movements')

            # checks for vertical collisions
            if tile[1].colliderect(self.rect.x, self.rect.y + dy, self.width, self.height):

                if tile[2] in (6, 7, 8):
                    # physics operate differently on platforms

                    if self.gap:
                        # makes sure the following code only activates when the player is trying to fall through the gap

                        if self.velocity >= 15:
                            # stops the program as registering any further falls (bottom platform has been reached)
                            self.velocity = 0  # stops the character from falling
                            self.gap = False
                            self.airborne = False  # character no longer in the air

                    else:  # activates for all other methods of falling (falling when down key is not pressed)
                        if self.velocity > 0:
                            self.velocity = 0  # stops the character from moving (turns speed to 0)
                            self.airborne = False
                            self.gap = False

                            dy = tile[1].top - self.rect.bottom
                            # in this case dy value = decreasing distance between
                            # the top of the tile and the bottom of the character
                            # allows them to be stationary once the difference is 0 (reached floor)


                else:
                    # state how there's possibly a better way at coding this to remove the redudancy
                    # But it'll rely on figuring out how to effectivly activate the gap checker

                    if self.velocity >= 15:

                        self.velocity = 0
                        self.gap = False  # gap checker is de-activated to make sure character can climb back up onto platform
                        self.airborne = False

                    elif self.velocity > 0:

                        self.velocity = 0
                        self.airborne = False
                        self.gap = False

                        # caps the fall to prevent player from sinking through platform
                        dy = tile[1].top - self.rect.bottom

        # prevents the characters from walking offscreen and deloding
        if self.rect.left > SCREEN_WIDTH or self.rect.right < 0:
            self.edge = True

        if self.edge:

            # has the player exit through the other side of the screen
            if self.flip:  # flip states direction player exited
                self.rect.x = SCREEN_WIDTH
            elif not self.flip:
                self.rect.x = -50  # teleports them to opposite side of screen
            self.edge = False
        else:
            self.rect.x += dx  # confirms movement

        self.rect.y += dy  # confirms movement

    def shoot(self):

        if self.shoot_cooldown == 0:
            fx_shoot.play()
            self.shoot_cooldown = 20  # reload speed

            # places bullet spawn point almost on the edge of the sprite's boarders
            bullet = Bullet((self.rect.centerx + (0.6 * self.direction * self.rect.size[1])), self.rect.centery,
                            self.direction)
            bullets.add(bullet)

    def attack(self):

        hit_enemies = pygame.sprite.spritecollide(self, enemies,
                                                  False)  # creates a list of all the enemies in the group that are currently being interacted with

        for enemy in hit_enemies:
            if enemy.alive and self.rect.colliderect(
                    enemy.rect):  # checks each enemy to make sure that the enemy that dies is the one the player is attacking
                enemy.health -= 6

    def update_frames(self):
        # runs the selected animation

        cooldown = 100  # animation speed

        if self.animation == 4:  # speeds up attack animation
            cooldown = 65

        # updates the frame currently being used in the current animation
        self.sprite = self.frames[self.animation][self.frame_index]

        # checks how long has passed since the frame was updated
        if pygame.time.get_ticks() - self.update_time > cooldown:

            self.update_time = pygame.time.get_ticks()
            self.frame_index += 1  # points to the next frame

            # resets loop
            if self.frame_index >= len(self.frames[self.animation]):

                if self.animation == 3:  # prevents the death animation from looping
                    self.frame_index = len(self.frames[self.animation]) - 1
                else:
                    self.frame_index = 0

                    if self.animation == 4:
                        fx_hit.play()

    def update_animation(self, new_animation):
        # changes to a new animation

        if new_animation != self.animation:
            self.animation = new_animation

            # updates the index to point/get ready for a new animation
            self.frame_index = 0
            self.update_time = pygame.time.get_ticks()

    def dead(self):

        # checks if the player/enemy is dead
        # resets control stats
        if self.health <= 0:
            self.health = 0
            self.speed = 0
            self.death_counter -= 1
            self.alive = False
            self.update_animation(3)

            if self.death_counter <= 0:  # allows for the death animation to fully play before killing player
                self.kill()

    def draw(self):

        # places an image in the screen in the rectangle area specified
        # 4 arguments: Image location, True or False to flipping image, False to prevent img from being flipped on y-axis, sprite area on screen

        screen.blit(pygame.transform.flip(self.sprite, self.flip, False), self.rect)

    def update_score(self):

        total_score = str(self.score).zfill(8)  # adds zeroes to the string until it reaches a character length of 8

        draw_text(f'{total_score}', GAME_FONT, SCORE_COLOUR, 570, 10)
    # creates a blueprint to be used for character creation (includes sprite, size, hitbox and starting co-ordinates)

class Enemy(Fighter):

    def __init__(self, character_type, x, y, scale, speed, health):
        super().__init__(character_type, x, y, scale, speed, health)

        # //////// AI CONTROLS //////////
        self.idle = False  # States whether or not the character is idle
        self.idle_counter = 0  # counts how long the character has been idle
        self.move_counter = 0  # counts how far the character is from their spawn / guard point

        # //////// RADARS/PLAYER DETECTION //////////
        # The larger the radar, easier the detection
        self.shoot_radar = pygame.Rect(0, 0, 150, 20)
        self.attack_radar = pygame.Rect(0, 0, 40, 10)

        self.death_music_played = False # prevents the death music from looping

    def attack(self):

        # designed to be co-op compatable (makes a list of all 'players' that are currently being hit)
        # overrides fighter attack to aim at player
        hit_players = pygame.sprite.spritecollide(self, players, False)

        for player in hit_players:

            if player.alive and self.rect.colliderect(player.rect):
                player.health -= 0.2

    def ai(self):

        # generates enemy ai
        if self.alive and player.alive:

            if random.randint(1,
                              500) <= 3 and not self.idle and not self.airborne:  # causes the ai to stop moving at random intervals
                self.update_animation(0)
                self.idle = True
                self.idle_counter = 50

            if self.attack_radar.colliderect(player.rect):  # player has stepped into the attack range of the ai
                self.update_animation(4)
                self.attack()

            elif self.shoot_radar.colliderect(player.rect):  # player has stepped into the shooting range of the ai
                self.update_animation(0)  # difficulty QoL, prevents the enemy from moving while shooting
                self.shoot()

            else:
                if not self.idle:
                    if self.direction == 1:  # if the spirite is currently facing right
                        ai_move_right = True
                    else:
                        ai_move_right = False

                    ai_move_left = not ai_move_right  # prevents enemy from trying to walk in both directions at once

                    self.move(ai_move_left, ai_move_right)
                    self.update_animation(1)
                    self.move_counter += 1

                    # creates the radar
                    self.shoot_radar.center = (self.rect.centerx + 75 * self.direction, self.rect.centery)
                    self.attack_radar.center = (self.rect.centerx + 10 * self.direction, self.rect.centery)

                    if self.move_counter > tile_size:  # gets the enemy to return to its spawn point
                        self.direction *= -1  # goes in the opposite direction
                        self.move_counter *= -1

                else:
                    self.idle_counter -= 1

                    if self.idle_counter == 0:  # prevents the enemy from beingn permanently idle
                        self.idle = False

    def dead(self):

        # checks if the enemy is dead
        # overwritten to update the player's score count per death
        if self.health <= 0:
            self.health = 0
            self.speed = 0
            self.death_counter -= 1
            self.alive = False
            self.update_animation(3)

            if not self.death_music_played:
                fx_dead.play()
                self.death_music_played = True


            if self.death_counter <= 0:
                player.score += 1
                self.kill()  # removes the enemy from the sprite group



# ----------------------

class Potion(pygame.sprite.Sprite):

    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)

        self.image = potion_img
        self.rect = self.image.get_rect()
        self.rect.midtop = (x + tile_size // 2, y + (tile_size - self.image.get_height()))

    def update(self):

        if pygame.sprite.collide_rect(self,
                                      player) and player.health != player.max_health:  # increases player health upon impact

            if (player.health + 25) > player.max_health:  # caps regeneration
                player.health = player.max_health
            else:
                player.health += 25

            self.kill()
            fx_potion.play()


class Bullet(pygame.sprite.Sprite):

    # creates objects for the bullets shot (general template)

    def __init__(self, x, y, direction):

        pygame.sprite.Sprite.__init__(self)
        self.speed = 10  # bullet speed
        self.image = bullet_img  # pre-loaded bullet image
        self.direction = direction  # the pathway of the bullet
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)

    def update(self):

        self.rect.x += (self.direction * self.speed)  # bullet movement

        # remove bullet from group if it goes off-screen
        if self.rect.right < 0 or self.rect.left > SCREEN_WIDTH:
            self.kill()

        hit_players = pygame.sprite.spritecollide(self, players, False)

        for player in hit_players:
            if player.alive and self.rect.colliderect(player.rect):

                if player.score > 15:  # difficulty spike
                    player.health -= 7

                else:
                    player.health -= 5

                print(player.health)
                self.kill()

        hit_enemies = pygame.sprite.spritecollide(self, enemies, False)

        for enemy in hit_enemies:
            if enemy.alive and self.rect.colliderect(enemy.rect):
                if enemy.alive:
                    enemy.health -= 50
                    self.kill()


class HealthBar:

    # creates a health bar object (to be interacted with)

    def __init__(self, x, y, health, max_health):
        # x,y co-ordinates for the health bar
        self.x = x
        self.y = y

        self.health = health  # players current health
        self.max_hp = max_health  # players starting hp

    def draw(self, health):  # animates the health bar
        self.health = health  # makes sure the health bar ratio is constantly updated

        ratio = self.health / self.max_hp  # creates a ratio used by the health bar to proportionally show hp

        pygame.draw.rect(screen, BORDER, (self.x - 2, self.y - 2, 154, 24))
        pygame.draw.rect(screen, EMPTY_HP, (self.x, self.y, 150, 20))
        pygame.draw.rect(screen, CURRENT_HP, (self.x, self.y, 150 * ratio, 20))

# --------------------

# sprite groups - group sprites so that methods work as a collective
bullets = pygame.sprite.Group()
players = pygame.sprite.Group()
potions = pygame.sprite.Group()
enemies = pygame.sprite.Group()


# ///////////////////// MAIN CODE //////////////////// #

world_data = []  # csv tile list

# level loader
# opens the csv file under the given name, identifying the 'delimiter' as the symbol that seperates each value (in this case, a comma)
with open('level0_data.csv', newline = '') as csvfile:
    reader = csv.reader(csvfile, delimiter = ',')

    #enumarate adds a running count to the for loop (since we arent given a specific numerical range
    #allows for the variables x, y to be created which acts as makeshift co-ordinates
    for x, row in enumerate(reader):
        line = []
        for y, tile in enumerate(row):
            line.append(int(tile))

        world_data.append(line)

block_list = create_block_list()
world = World()

# Avatar Selection -------
avatars = {
    'Pink Monster' : pygame.image.load('img/Tiny Hero/Pink_Monster/Pink_Monster.png').convert_alpha(),
    'Dude Monster' : pygame.image.load('img/Tiny Hero/Dude_Monster/Dude_Monster.png').convert_alpha(),
    'Owlet Monster' : pygame.image.load('img/Tiny Hero/Owlet_Monster/Owlet_Monster.png').convert_alpha(),
    'choices' : [False, False, False]
}
chosen_avatar = ''

tile_number = world.proccess_data(world_data)

# Spawn Timers -------
spawn_timer_enemy = 120
spawn_timer_potion = 300
total_score = str(0).zfill(8)

# insures that the player, health bar and scores are only spawned once
player_spawned = False
bar_spawned = False

# Page Setup -------
# makes sure multi-page sections start on their homepages
page_number = 1
increment = False

# UI Timers -------
to_leaderboard_timer = 80
username = []
flash_ticker = 255
fade_switch = 1

next_page = 'title'
menu_proceed = False
reset_game = False

gm_music_played = False
death_fade = Game_UI.ScreenFade(2, (0, 0, 0), 4)

# game loop
run = True
clicker_buffer = 0  # acts as a hold delay timer to prevent multiple clicks registering at once
menu_buffer = 0  # basically a clicker buffer for the main function

while run:
    # print(screen_score, start_game)
    # screen switcher

    clock.tick(FPS)

    if screen_main and not screen_score and not screen_game:
        # load the menu screens
        # arguments and return values are used to update the UI statuses
        # uses the next_page variables to cycle through the different menu options
        # uses ticker variable to delay click-through rate
        if next_page == 'title':
            screen_main, screen_game, screen_score, next_page = Game_UI.screen_menu_main(screen_main, screen_game, screen_score, next_page)

        elif next_page == 'avatar' and menu_buffer <= 0:

            screen_main, screen_game, screen_score, next_page, menu_buffer, chosen_avatar = Game_UI.screen_menu_avatar(screen_main, screen_game, screen_score, next_page, menu_buffer, avatars, chosen_avatar)

        elif next_page == 'instruction' and menu_buffer <= 0:

            screen_main, screen_game, screen_score, next_page, menu_buffer = Game_UI.screen_menu_instruction(screen_main, screen_game, screen_score, next_page, menu_buffer)

        elif next_page == 'game':

            screen_game = True
            screen_main = False
            screen_score = False

            # game music played at this point to insure the music starts when the game starts
            pygame.mixer.music.play(-1, 0.0, 5000)  # (how many times to loop, delay between loops, length of fade_)

        menu_buffer -= 1

    if screen_score and not screen_main and not screen_game:
        # loads the leaderboard screen
        screen_main, screen_game, screen_score, page_number, increment = Game_UI.screen_leaderboard_main(
            screen_main, screen_game, screen_score, page_number, increment)

        clicker_buffer += 1

        if clicker_buffer == 45:  # delays the mouse click to allow slow traversal of leaderboard
            increment = False
            clicker_buffer = 0

        if reset_game:  # resets game variables

            # empties groups
            players.empty()
            enemies.empty()
            bullets.empty()
            potions.empty()

            # resets timers and game data
            world = World()
            player = world.proccess_data(world_data)
            player_spawned = False
            bar_spawned = False
            spawn_timer_enemy = 120
            spawn_timer_potion = 300
            to_leaderboard_timer = 80


            total_score = str(0).zfill(8)
            username = []

            reset_game = False
            next_page = 'title'
            pygame.mixer.music.load('aud/Overcome (This Time).mp3')  # music to load
            pygame.mixer.music.set_volume(0.1)  # volume for the music
            gm_music_played = False

            death_fade.fade_counter = 0  # death_fade counter reset to prevent looping

    if screen_game and not screen_main and not screen_score:

        if not player_spawned:  # spawns player
            player = Fighter(chosen_avatar, 400, 250, 3, 5, 150)
            players.add(player)
            player_spawned = True

        if not bar_spawned:  # spawns health bar
            health_bar = HealthBar(10, 10, player.health, player.health)
            bar_spawned = True

        # update background
        draw_background()  # redraws the background each frame to ensure there are no smears with the sprites
        health_bar.draw(player.health)
        world.draw()

        # update timers
        spawn_timer_enemy -= 1
        spawn_timer_potion -= 1

        # update player actions
        player.update()
        player.update_score()
        player.draw()

        if player.alive:

            if spawn_timer_enemy == 0:  # spawns health bar
                spawn_enemy(world_data, avatars, chosen_avatar, tile_number)

                # spawn time decreases gradually as player score increases
                # caps the spawn timer at 200
                if spawn_timer_enemy >= 200:
                    spawn_timer_enemy = 300 - (player.score // 5) * 50
                else:
                    spawn_timer_enemy = 200 - (player.score // 5) * 20

            if spawn_timer_potion == 0:
                spawn_item()

                # caps the spawn timer at 300
                if spawn_timer_potion >= 300:  # caps the spawn timer at 150
                    spawn_timer_potion = 500 - (player.score // 5) * 100
                else:
                    spawn_timer_potion = 300 - (player.score // 5) * 20

            for enemy in enemies:  # update enemy actions
                enemy.ai()
                enemy.update()
                enemy.draw()

            # update items
            bullets.update()
            potions.update()
            bullets.draw(screen)
            potions.draw(screen)

            # update animations
            # changes animations based on inputs
            # restricts movement to only working while 'alive'

            if shoot:
                player.shoot()

            # done in a separate selection to allow the player to shoot while jumping/falling
            if player.airborne:  # jump of fall
                player.update_animation(2)
            elif move_left or move_right:
                player.update_animation(1)
            elif attack:
                player.update_animation(4)
                player.attack()
            else:
                player.update_animation(0)

            player.move(move_left, move_right)
        else:
            # activates once player dies (player.alive == False)

            # always makes sure that the leaderboard from the game over screen points to the first page
            # added to curb possibility of leaderboard being accessed in title screen and exited on another page

            page_number = 1
            to_leaderboard_timer -= 1

            pygame.mixer.music.unload()  # stops the game music and de-loads it (to free up resources)

            if not gm_music_played:  # prevents the game_over music from looping
                fx_gameover.play()
                gm_music_played = True


            if death_fade.fade():  # equivalent of if death_fade.fade() is True (means is finished)

                if to_leaderboard_timer < 0: #the repeated loop means that timer goes into negative, so less than gives a barrier of entry
                    screen_main, screen_game, screen_score, username, flash_ticker, fade_switch, reset_game = Game_UI.screen_leaderboard_entry(screen_main, screen_game, screen_score, username, flash_ticker, fade_switch, player.score, chosen_avatar, block_list)

    # event handler
    for event in pygame.event.get():

        # event to close the game by closing the window
        if event.type == pygame.QUIT:
            run = False

        # event for keyboard presses
        # nameError exception excepted to stop the code from trying to reference game inputs
        try:
            if event.type == pygame.KEYDOWN:

                # specifying actions for A,S,D,W movement
                if event.key == pygame.K_n:
                    player.health = 0
                if event.key == pygame.K_a:
                    move_left = True
                if event.key == pygame.K_d:
                    move_right = True
                if event.key == pygame.K_w and player.alive:  # restricts jumping to only happening while alive
                    player.jump = True
                    fx_jump.play()

                if event.key == pygame.K_s and player.alive:  # restricts falling to only happening while alive
                    player.fall = True
                    player.gap = True
                    fx_fall.play()

                if event.key == pygame.K_j:
                    shoot = True

                if event.key == pygame.K_i:
                    attack = True

                # specifying actions for quiting using ESC
                if event.key == pygame.K_ESCAPE:
                    run = False

        except NameError:  # stops the game from crashing if a movement input is entered in the main menu
            pass
        # event for keyboard releases
        if event.type == pygame.KEYUP:

            # specifying actions for A,S,D,W movement
            # allows for actions to be run only while key is being pressed
            if event.key == pygame.K_a:
                move_left = False
            if event.key == pygame.K_d:
                move_right = False

            if event.key == pygame.K_j:
                shoot = False

            if event.key == pygame.K_i:
                attack = False
    pygame.display.update()

pygame.quit()
