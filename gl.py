import pygame
from pygame import mixer_music

from button import Button

def load_home_screen(screen):
    # load start screen image
    startscreen = pygame.image.load('img/background.jpg')
    startscreen = pygame.transform.scale(startscreen, (800, 500))
    screen.blit(startscreen, (0,0))

    # initialize home screen music
    mixer_music.load('soundtrack/home_screen.wav')
    mixer_music.play(-1)

    # logo on low right corner
    logo = pygame.image.load('img/logo.png')
    logo = pygame.transform.scale(logo, (100, 100))
    screen.blit(logo, (700, 390))

    # initialize buttons
    sb = Button((50, 50, 50), 150, 200, 150, 50, 'Start')
    qb = Button((0, 0, 0), 150, 260, 150, 50, 'Quit')

    return sb, qb

def home_screen(sb, qb, screen):
    button_selected = 'START'
    start_button = sb
    quit_button = qb

    end_it = False
    isRunning = True
    # start screen cycle
    while (end_it != True):
        # draw buttons
        start_button.draw(screen, (255, 255, 255))
        quit_button.draw(screen, (255, 255, 255))

        # show title
        myfont = pygame.font.SysFont("Britannic Bold", 60)
        nlabel = myfont.render("Castle Escape", 200, (255, 255, 255))
        screen.blit(nlabel, (85, 150))

        # check for input
        for event in pygame.event.get():
            position = pygame.mouse.get_pos()

            # quit game
            if event.type == pygame.QUIT:
                isRunning = False
                end_it = True

            # manage button clicks
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if start_button.isOver(position):
                    end_it = True
                elif quit_button.isOver(position):
                    end_it = True
                    isRunning = False

            # manage mouse movements
            elif event.type == pygame.MOUSEMOTION:
                if start_button.isOver(position):
                    start_button.color = (50, 50, 50)
                else: 
                    start_button.color = (0, 0, 0)

                if quit_button.isOver(position):
                    quit_button.color = (50, 50, 50)
                else:
                    quit_button.color = (0, 0, 0)

            # manage keyboard key's clicks
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    isRunning = False
                    end_it = True
                elif event.key == pygame.K_DOWN:
                    button_selected = 'QUIT'
                    quit_button.color = (50, 50, 50)
                    start_button.color = (0, 0, 0)
                elif event.key == pygame.K_UP:
                    button_selected = 'START'
                    start_button.color = (50, 50, 50)
                    quit_button.color = (0, 0, 0)
                elif event.key == pygame.K_RETURN:
                    if button_selected == 'QUIT':
                        isRunning = False
                    end_it = True

        pygame.display.flip()

    screen.fill(pygame.Color("gray"))

    return isRunning

def load_pause_screen():
    # initialize buttons
    rb = Button((50, 50, 50), 300, 210, 150, 50, 'Resume')
    qb = Button((0, 0, 0), 300, 270, 150, 50, 'Exit')

    return rb, qb

def pause_screen(rb, qb, screen):
    button_selected = result = 'RESUME'
    start_button = rb
    quit_button = qb

    end_it = False
    isRunning = True
    # start screen cycle
    while (end_it != True):
        # draw buttons
        start_button.draw(screen, (255, 255, 255))
        quit_button.draw(screen, (255, 255, 255))

        # show title
        myfont = pygame.font.SysFont("Britannic Bold", 60)
        nlabel = myfont.render("Pause", 200, (255, 255, 255))
        screen.blit(nlabel, (310, 150))

        # check for input
        for event in pygame.event.get():
            position = pygame.mouse.get_pos()

            # quit game
            if event.type == pygame.QUIT:
                isRunning = False
                end_it = True

            # manage button clicks
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if start_button.isOver(position):
                    end_it = True
                elif quit_button.isOver(position):
                    end_it = True
                    isRunning = False
                    result = 'HOME'

            # manage mouse movements
            elif event.type == pygame.MOUSEMOTION:
                if start_button.isOver(position):
                    start_button.color = (50, 50, 50)
                else: 
                    start_button.color = (0, 0, 0)

                if quit_button.isOver(position):
                    quit_button.color = (50, 50, 50)
                else:
                    quit_button.color = (0, 0, 0)

            # manage keyboard key's clicks
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    isRunning = True
                    end_it = True
                    result = 'RESUME'
                elif event.key == pygame.K_DOWN:
                    button_selected = 'QUIT'
                    quit_button.color = (50, 50, 50)
                    start_button.color = (0, 0, 0)
                elif event.key == pygame.K_UP:
                    button_selected = 'RESUME'
                    start_button.color = (50, 50, 50)
                    quit_button.color = (0, 0, 0)
                elif event.key == pygame.K_RETURN:
                    if button_selected == 'QUIT':
                        isRunning = False
                        result = 'HOME'
                    end_it = True

        pygame.display.flip()

    screen.fill(pygame.Color("gray"))

    return isRunning, result

def load_end_screen(screen):
    # load start screen image
    startscreen = pygame.image.load('img/endgame.jpg')
    startscreen = pygame.transform.scale(startscreen, (800, 500))
    screen.blit(startscreen, (0,0))

    # initialize home screen music
    mixer_music.load('soundtrack/home_screen.wav')
    mixer_music.play(-1)

    # initialize buttons
    pb = Button((0, 0, 0), 300, 265, 200, 50, 'Play Again')
    eb = Button((0, 0, 0), 300, 325, 200, 50, 'Exit')

    return eb, pb

def end_screen(eb, pb, screen):
    button_selected = 'EXIT'
    exit_button = eb
    play_button = pb

    end_it = False
    isRunning = True
    # start screen cycle
    while (end_it != True):
        # draw buttons
        exit_button.draw(screen, (255, 255, 255))
        play_button.draw(screen, (255, 255, 255))

        # show title
        myfont = pygame.font.SysFont("Britannic Bold", 60)
        nlabel = myfont.render("Game Finished", 200, (255, 255, 255))
        screen.blit(nlabel, (250, 200))

        # check for input
        for event in pygame.event.get():
            position = pygame.mouse.get_pos()

            # quit game
            if event.type == pygame.QUIT:
                isRunning = False
                end_it = True

            # manage button clicks
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if exit_button.isOver(position):
                    end_it = True
                    isRunning = False
                elif play_button.isOver(position):
                    end_it = True

            # manage mouse movements
            elif event.type == pygame.MOUSEMOTION:
                if exit_button.isOver(position):
                    exit_button.color = (50, 50, 50)
                else: 
                    exit_button.color = (0, 0, 0)

                if play_button.isOver(position):
                    play_button.color = (50, 50, 50)
                else:
                    play_button.color = (0, 0, 0)

            # manage keyboard key's clicks
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    isRunning = False
                    end_it = True
                elif event.key == pygame.K_DOWN:
                    button_selected = 'EXIT'
                    exit_button.color = (50, 50, 50)
                elif event.key == pygame.K_UP:
                    button_selected = 'PLAY'
                    exit_button.color = (50, 50, 50)
                elif event.key == pygame.K_RETURN:
                    if button_selected == 'QUIT':
                        isRunning = False
                    end_it = True

        pygame.display.flip()

    screen.fill(pygame.Color("gray"))

    return isRunning