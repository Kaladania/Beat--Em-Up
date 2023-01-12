# note, a benifit for having the ui be in seperate functions is that all buttons created are now local varaibles (meaning that duplicate leadboardoard buttons wont have to be named button1/button2/etc due to only being referenced in the function)

import pygame
import Game_Leaderboard

pygame.init()

SCREEN_WIDTH = 800
SCREEN_HEIGHT = int(SCREEN_WIDTH * 0.8)
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

#GAME_FONT = pygame.font.Font('img/Tiny Hero/Font/04B_30__.ttf', 25)
#GAME_TITLE_FONT = pygame.font.Font('img/Tiny Hero/Font/04B_30__.ttf', 60)
#LEADERBOARD_DOTS = pygame.font.Font('img/Tiny Hero/Font/04B_30__.ttf', 60) #Chose to use font full stops for a more aesthetic look

WHITE = (255, 255, 255)
GREY = (150, 150, 150)

database_solo_names = []
database_solo_avatars = []
database_solo_scores = []

print_names = True

def get_outline(image):

    tolerance = 127  # the alpha level of the colours that are ignored
    mask = pygame.mask.from_surface(image, tolerance)
    outlines = pygame.Surface(image.get_size()).convert_alpha()
    outlines.fill((0, 0, 0, 0))

    for point in mask.outline():  # equivalent to tracing over a picture
        outlines.set_at(point, (255, 255, 255))

    return outlines

def font_customisation(path, size):

    # chose to use a function instead of a constant due to the amount of varying font sizes
    return pygame.font.Font(path, size)


def bg_resizer(image, scale):

    image = pygame.transform.scale(image, (int(image.get_width() * scale), int(image.get_height() * scale)))
    return image


def draw_text(text, font, colour, x, y):

    sentence = font.render(text, True, colour)
    screen.blit(sentence, (x,y))


def screen_menu_main(screen_main, screen_game, screen_score, next_page):

    bg_menu = pygame.image.load('img/Background/Red City.jpg').convert_alpha()
    bg_menu = bg_resizer(bg_menu, 1.5)

    # button creation
    b_start = Button(SCREEN_WIDTH // 2 - 130, SCREEN_HEIGHT // 2 - 120, button_start, 0.3)
    b_board = Button(SCREEN_WIDTH // 2 - 130, SCREEN_HEIGHT // 2 + 40, button_board, 0.3)

    screen.blit(bg_menu, (0, 0))

    TITLE_FONT = font_customisation('img/Tiny Hero/Font/04B_30__.ttf', 55)

    draw_text('MONSTER RUMBLE', TITLE_FONT, WHITE, 50, 60)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                next_page = 'avatar'


    # allows the button's to be clicked and proceed with a given action
    if b_start.draw(screen):
        next_page = 'avatar'

    if b_board.draw(screen):
        screen_score = True
        screen_game = False
        screen_main = False

    return screen_main, screen_game, screen_score, next_page

def screen_menu_avatar(screen_main, screen_game, screen_score, next_page, ticker, avatars, chosen_avatar):
    #player chooses the avatar they use in-game

    bg_menu = pygame.image.load('img/Background/Red City.jpg').convert_alpha()
    bg_menu = bg_resizer(bg_menu, 1.5)

    TITLE_FONT = font_customisation('img/Tiny Hero/Font/04B_30__.ttf', 40)
    BODY_FONT = font_customisation('img/Tiny Hero/Font/04B_30__.ttf', 20)

    # button creation
    b_start = Button(325, 510, button_start, 0.2)

    screen.blit(bg_menu, (0, 0))

    draw_text('CHOOSE YOUR AVATAR', TITLE_FONT, WHITE, 80, 40)
    draw_text('TO CHOOSE A CHARACTER', BODY_FONT, WHITE, 220, 120)
    draw_text('PRESS A, S OR D', BODY_FONT, WHITE, 285, 160)

    # displays pictures of avatar choices
    screen.blit(bg_resizer(avatars["Pink Monster"], 6), (110, 210))
    screen.blit(bg_resizer(avatars["Dude Monster"], 6), (330, 210))
    screen.blit(bg_resizer(avatars["Owlet Monster"], 6), (560, 210))

    # outlines the current selected character
    # proccess - resizes the result of the get_outline function
    # (which uses a mask to create an outline of each monster)
    if avatars["choices"][0]:
        screen.blit(bg_resizer((get_outline(avatars["Pink Monster"])), 6), (110, 210))
        chosen_avatar = 'Pink_Monster'

    elif avatars["choices"][1]:
        screen.blit(bg_resizer((get_outline(avatars["Dude Monster"])), 6), (330, 210))
        chosen_avatar = 'Dude_Monster'

    elif avatars["choices"][2]:
        screen.blit(bg_resizer((get_outline(avatars["Owlet Monster"])), 6), (560, 210))
        chosen_avatar = 'Owlet_Monster'


    temp = list(avatars.items())

    # displays the names of the avatars
    for key in enumerate(temp):
        if key[0] != 3:
            draw_text("The", BODY_FONT, WHITE, 170 + (225 * key[0]), 440)
            draw_text(str(temp[key[0]][0]), BODY_FONT, WHITE, 100 + (220 * key[0]), 470)


    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            pygame.quit()

        # event for keyboard presses
        if event.type == pygame.KEYDOWN:

            # signals user has finished entering name
            # prevents the section from proceeding unless the player has chosen an avatar
            if event.key == pygame.K_RETURN and chosen_avatar != '':
                next_page = 'instruction'
                ticker = 10

            # updates the outline choice depending on the input
            if event.key == pygame.K_a:
                avatars["choices"][0] = True
                avatars["choices"][1] = False
                avatars["choices"][2] = False

            elif event.key == pygame.K_s:
                avatars["choices"][0] = False
                avatars["choices"][1] = True
                avatars["choices"][2] = False

            elif event.key == pygame.K_d:
                avatars["choices"][0] = False
                avatars["choices"][1] = False
                avatars["choices"][2] = True


    # allows the button's to be clicked and proceed with a given action
    if b_start.draw(screen) and chosen_avatar != '':
        next_page = 'instruction'
        ticker = 10


    return screen_main, screen_game, screen_score, next_page, ticker, chosen_avatar



def screen_menu_instruction(screen_main, screen_game, screen_score, next_page, ticker):
    bg_menu = pygame.image.load('img/Background/Red City.jpg').convert_alpha()
    bg_menu = bg_resizer(bg_menu, 1.5)

    TITLE_FONT = font_customisation('img/Tiny Hero/Font/04B_30__.ttf', 40)
    BODY_FONT = font_customisation('img/Tiny Hero/Font/04B_30__.ttf', 20)

    b_start = Button(325, 500, button_start, 0.2)

    screen.blit(bg_menu, (0, 0))

    draw_text('HOW TO PLAY', TITLE_FONT, WHITE, 200, 25)
    draw_text('RUN', BODY_FONT, WHITE, 72, 310)
    #draw_text('JUMP', BODY_FONT, WHITE, 245, 310)
    draw_text('JUMP/FALL', BODY_FONT, WHITE, 190, 310)
    draw_text('ATTACK', BODY_FONT, WHITE, 400, 310)
    draw_text('SHOOT', BODY_FONT, WHITE, 600, 310)

    draw_text('/', BODY_FONT, WHITE, 100, 105)
    draw_text('/', BODY_FONT, WHITE, 270, 105)

    draw_text('TRY TO DEFEAT AS MANY ENEMIES AS YOU CAN!', BODY_FONT, WHITE, 40, 400)

    sprite_run = pygame.image.load('img/Assets/Run.png').convert_alpha()
    sprite_run = bg_resizer(sprite_run, 0.75)
    sprite_jump = pygame.image.load('img/Assets/Jump.png').convert_alpha()
    sprite_jump = bg_resizer(sprite_jump, 0.75)
    sprite_attack = pygame.image.load('img/Assets/Attack.png').convert_alpha()
    sprite_attack = bg_resizer(sprite_attack, 0.75)
    sprite_shoot = pygame.image.load('img/Assets/Shoot.png').convert_alpha()
    sprite_shoot = bg_resizer(sprite_shoot, 0.75)
    # sprite_death = pygame.image.load('img/Tiny Hero/Pink_Monster/Pink_Monster_Death.png').convert_alpha()
    # sprite_death = bg_resizer(sprite_death, 3)

    sprite_a = pygame.image.load('img/Assets/a.png').convert_alpha()
    sprite_a = bg_resizer(sprite_a, 0.75)
    sprite_w = pygame.image.load('img/Assets/w.png').convert_alpha()
    sprite_w = bg_resizer(sprite_w, 0.75)
    sprite_s = pygame.image.load('img/Assets/s.png').convert_alpha()
    sprite_s = bg_resizer(sprite_s, 0.75)
    sprite_d = pygame.image.load('img/Assets/d.png').convert_alpha()
    sprite_d = bg_resizer(sprite_d, 0.75)
    sprite_i = pygame.image.load('img/Assets/i.png').convert_alpha()
    sprite_i = bg_resizer(sprite_i, 0.75)
    sprite_j = pygame.image.load('img/Assets/j.png').convert_alpha()
    sprite_j = bg_resizer(sprite_j, 0.75)

    #pygame.draw.rect(screen, (252, 228, 214), (100, 130, 600, 200), 0)

    #pygame.draw.rect(screen, (252, 228, 214), (325, 530, 150, 60), 0)

    screen.blit(sprite_run, (60, 180))
    screen.blit(sprite_jump, (230, 180))
    screen.blit(sprite_attack, (420, 180))
    screen.blit(sprite_shoot, (600, 180))
    #screen.blit(sprite_death, (60, 370))

    screen.blit(sprite_a, (60, 100))
    screen.blit(sprite_d, (120, 100))
    screen.blit(sprite_w, (230, 100))
    screen.blit(sprite_s, (290, 100))
    screen.blit(sprite_i, (450, 100))
    screen.blit(sprite_j, (630, 100))



    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                next_page = 'game'


    if b_start.draw(screen):
        next_page = 'game'
        ticker = 20


    return screen_main, screen_game, screen_score, next_page, ticker


# ////////////////// LEADERBOARD SCREENS /////////////////////// #
    
def screen_leaderboard_entry(screen_main, screen_game, screen_score, username, flash_ticker, fade_switch, score, chosen_avatar, block_list):

    TITLE_FONT = font_customisation('img/Tiny Hero/Font/04B_30__.ttf', 40)
    MAIN_FONT = font_customisation('img/Tiny Hero/Font/04B_30__.ttf', 35)
    SUB_FONT = font_customisation('img/Tiny Hero/Font/04B_30__.ttf', 25)
    SUB_FONT1 = font_customisation('img/Tiny Hero/Font/04B_30__.ttf', 30)


    #creares a list of words that the user is not allowed to use for a username
    names = []

    for name in (Game_Leaderboard.get_names(names)):  # adds names from the database to the invalid list to prevent duplication
        block_list.append(name)

    screen.fill((0, 0, 0))

    draw_text('ENTER YOUR NAME', TITLE_FONT, WHITE, 130, 150)
    draw_text('YOUR SCORE: ' + str(score), SUB_FONT1, WHITE, 230, 60)


    #allows the press enter command to flash on screen (through the application of a gradient)
    flash_ticker = flash_ticker + (3 * fade_switch)

    if flash_ticker <= 0:
        flash_ticker = 0
        fade_switch *= -1

    if flash_ticker >= 255:
        flash_ticker = 255
        fade_switch *= -1

    draw_text('PRESS ENTER TO CONTINUE', SUB_FONT, (flash_ticker, flash_ticker, flash_ticker), 150, 500)


    #creates a valid string from the list of inputs
    username_string = ''

    for character in username:
        username_string = username_string + character

    if username_string.title() in block_list:  # invalid warning message
        draw_text("YOU CAN'T USE THIS NAME", SUB_FONT, WHITE, 150, 230)


    # collects the user's keyboard inputs
    for event in pygame.event.get():

        # event for keyboard presses
        if event.type == pygame.KEYDOWN:

            if event.key == pygame.K_RETURN:  # signals user has finished entering name
                if username_string != '' and username_string.title() not in block_list:  # prevents a blank name being entered
                    avatar = chosen_avatar.replace('_', ' ')
                    Game_Leaderboard.enter_leaderboard(username_string, avatar, score)
                    screen_main = False
                    screen_game = False
                    screen_score = True

            if event.key == pygame.K_g:
                screen_main = False
                screen_game = False
                screen_score = True

            elif event.key == pygame.K_BACKSPACE:
                try:
                    username.pop(len(username) - 1)  # no function to remove the last item of the list so len(username) is used to get the index of the last item
                except IndexError:
                    pass
            else:
                character = str(pygame.key.name(event.key))  # returns the name of the key being pressed

                if character.isalpha() and len(character) == 1 and len(username) < 7:  # makes sure the input is not a number or a special key (i.e 'space') (while also cutting the inputs off at a certain length)
                    username.append(character)

    screen_output = ''

    for i in range(7):  # screen displays dashes that disappear and re-apper on inputs
        try:
            screen_output = screen_output + username[i] + ' '
        except IndexError:
            screen_output = screen_output + '_ '

    draw_text(screen_output, MAIN_FONT, WHITE, 210, 350)

    return screen_main, screen_game, screen_score, username, flash_ticker, fade_switch, True



def screen_leaderboard_main(screen_main, screen_game, screen_score, page_number,incriment):

    MAIN_FONT = font_customisation('img/Tiny Hero/Font/04B_30__.ttf', 25)
    TITLE_FONT = font_customisation('img/Tiny Hero/Font/04B_30__.ttf', 60)

    names = []
    avatars = []
    scores = []

    PAGE_LIMIT = 5  # specifies how the maximum amount of names per page


    bg_leaderboard = pygame.image.load('img/Background/Blue City.jpg').convert_alpha()
    bg_leaderboard = bg_resizer(bg_leaderboard, (SCREEN_WIDTH / bg_leaderboard.get_width()))

    screen.blit(bg_leaderboard, (0, 0))

    b_back = Button(40, 60, button_back, 0.125)

    names, avatars, scores = Game_Leaderboard.create_leaderboard(
        database_solo_names, database_solo_avatars, database_solo_scores)

    max_page = len(names) // PAGE_LIMIT  # details the maximum amount of pages that the names are spread across

    # if there are any leftover names, adds another page
    if len(names) % PAGE_LIMIT > 0:
        max_page += 1


    # allows arrows to appear and disappear depending on the page number

    if page_number - 1 != 0:  # as long as there's a previous page to go back to
        b_arrow_l = Button(45, 570, arrow_left, 0.075)

    if page_number < max_page:
        b_arrow_r = Button(700, 570, arrow_right, 0.075)



    draw_text('HIGHSCORES', TITLE_FONT, WHITE, 190, 60)
    draw_text('Rank', MAIN_FONT, WHITE, 50, 175)
    draw_text('Name', MAIN_FONT, WHITE, 355, 175)
    draw_text('Score', MAIN_FONT, WHITE, 665, 175)



    for i in range(max_page):
        if (i + 1) == page_number:
            # makes sure that the current page is highlighted
            draw_text('.', TITLE_FONT, WHITE, 320 + (35 * i), 547)
        else:
            draw_text('.', TITLE_FONT, GREY, 320 + (35 * i), 547)



    line_number = 0

    for i in range(PAGE_LIMIT):  # limits entered names to 5 per page

        try:
            # display ranking
            # if statement prevents and extra ranking from being printed (which would lead to an empty entry

            if len(names) >= (i + 1 + (PAGE_LIMIT * (page_number - 1))):
                draw_text(str(i + 1 + (PAGE_LIMIT * (page_number - 1))) + '.', MAIN_FONT, WHITE, 50, 250 + 60 * line_number)

            # display names
            draw_text(names[i + (PAGE_LIMIT * (page_number - 1))], MAIN_FONT, WHITE, 140, 250 + 60 * line_number)

            # display avatars
            draw_text('The ' + avatars[i + (PAGE_LIMIT * (page_number - 1))], MAIN_FONT, WHITE, 310, 250 + 60 * line_number)

            # display scores
            draw_text(scores[i + (PAGE_LIMIT * (page_number - 1))], MAIN_FONT, WHITE, 720, 250 + 60 * line_number)

            line_number += 1

        except IndexError:  # prevents code from stopping if there are not enough names in the list
            break  # stops trying to load names from the leaderboard


    try:
        if b_arrow_l.draw(screen):
            if not incriment:
                page_number -= 1
                incriment = True

    except UnboundLocalError:
        pass
        # error occurs if the variable / class is called before assaignment.
        # Try/Except code is used to prevent code from stopping once one of the arrow disapeers


    try:
        if b_arrow_r.draw(screen):
            if not incriment:
                page_number += 1
                incriment = True

    except UnboundLocalError:
        pass


    if b_back.draw(screen):
        screen_score = False
        screen_game = False
        screen_main = True

    return screen_main, screen_game, screen_score, page_number, incriment


# ////////////////// CLASSES /////////////////////// #

class ScreenFade():
    def __init__(self, direction, colour, speed):
        self.direction = direction
        self.colour = colour
        self.speed = speed
        self.fade_counter = 0

    def fade(self):

        self.fade_counter += self.speed
        pygame.draw.rect(screen, self.colour, (0,0, SCREEN_WIDTH, 0 + self.fade_counter))

        if self.fade_counter >= SCREEN_WIDTH:
            return True
# -------------------

class Button:

    def __init__(self, x, y, image, scale):
        width = image.get_width()
        height = image.get_height()
        self.button = pygame.transform.scale(image, (int(width * scale), int(height * scale)))
        self.rect = self.button.get_rect()
        self.rect.topleft = (x, y)
        self.clicked = False

    def draw(self, surface):
        #draws the button onto the screen while looking for a mouse click

        #gets the position of the mouse
        hover = pygame.mouse.get_pos()

        #checks if the mouse is hovering over the button
        # get_pressed()[0] checks if each section of the mouse is pressed, 0 is left click, 1 is middle click, 2 is right click
        if self.rect.collidepoint(hover):
            if pygame.mouse.get_pressed()[0] == 1:
                #if a mouse click has occured on the button when it was currently unclicked

                self.clicked = True

            else:
                self.clicked = False

        #draw button
        surface.blit(self.button, (self.rect.x, self.rect.y))

        state = self.clicked

        self.clicked = False #makes sure the buttons always remained unclicked after the check has run
        return state


# button image files
button_start = pygame.image.load('img/Buttons/Start.png').convert_alpha()
button_menu = pygame.image.load('img/Buttons/Menu.png').convert_alpha()
button_scores = pygame.image.load('img/Buttons/Leaderboard.png').convert_alpha()
button_board = pygame.image.load('img/Buttons/Leaderboard.png').convert_alpha()
button_quit = pygame.image.load('img/Buttons/Quit.png').convert_alpha()
button_back = pygame.image.load('img/Buttons/Back.png').convert_alpha()
button_1P = pygame.image.load('img/Buttons/1 Player.png').convert_alpha()
button_2P = pygame.image.load('img/Buttons/2 Player.png').convert_alpha()

arrow_left = pygame.image.load('img/Assets/arrows_left.png').convert_alpha()
arrow_right = pygame.image.load('img/Assets/arrows.png').convert_alpha()