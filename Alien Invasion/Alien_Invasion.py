import pygame
from pygame.sprite import Group
from Settings import Settings
from Ship import Ship
from Game_Stats import GameStats
from Button import Button
from Scoreboard import Scoreboard
import Game_Functions as GF

def run_game():
    pygame.init()
    settings = Settings()
    screen = pygame.display.set_mode((settings.screen_width, settings.screen_height))
    pygame.display.set_caption("Alien Invasion")
    stats = GameStats(settings)
    sb = Scoreboard(settings, screen, stats)
    ship = Ship(settings, screen)
    bullets = Group()
    aliens = Group()
    GF.create_fleet(settings, screen, ship, aliens)
    play_button = Button(settings, screen, "Play")
    clock = pygame.time.Clock()

    while True:
        GF.check_events(settings, screen, stats, sb, play_button, ship, aliens, bullets)
        if stats.game_active:
            ship.update()
            GF.update_bullets(settings, screen, stats, sb, ship, aliens, bullets)
            GF.update_aliens(settings, stats, screen, sb, ship, aliens, bullets)
        GF.update_screen(settings, screen, stats, sb, ship, aliens, bullets, play_button)
        clock.tick(120)

run_game()