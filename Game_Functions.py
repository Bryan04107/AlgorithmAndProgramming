import pygame, sys
from Bullet import Bullet
from Alien import Alien
from time import sleep

def check_keydown_events(event, settings, screen, ship, bullets):
    if event.key == pygame.K_d:
        ship.moving_right = True
    elif event.key == pygame.K_a:
        ship.moving_left = True
    elif event.key == pygame.K_SPACE:
        fire_bullet(settings, screen, ship, bullets)
    elif event.key == pygame.K_q:
        sys.exit()

def check_keyup_events(event, ship):
    if event.key == pygame.K_d:
        ship.moving_right = False
    elif event.key == pygame.K_a:
        ship.moving_left = False

def check_events(settings, screen, stats, sb, play_button, ship, aliens, bullets):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            check_keydown_events(event, settings, screen, ship, bullets)
        elif event.type == pygame.KEYUP:
            check_keyup_events(event, ship)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            check_play_button(settings, screen, stats, sb, play_button, ship, aliens, bullets, mouse_x, mouse_y)

def check_play_button(settings, screen, stats, sb, play_button, ship, aliens, bullets, mouse_x, mouse_y):
    button_clicked = play_button.rect.collidepoint(mouse_x, mouse_y)
    if button_clicked and not stats.game_active:
        settings.initialize_dynamic_settings()
        pygame.mouse.set_visible(False)
        stats.reset_stats()
        stats.game_active = True
        aliens.empty()
        bullets.empty()
        sb.prep_score()
        sb.prep_high_score()
        sb.prep_level()
        sb.prep_ships()
        create_fleet(settings, screen, ship, aliens)
        ship.center_ship()

def update_screen(settings, screen, stats, sb, ship, aliens, bullets, play_button):
    screen.fill(settings.bg_color)
    for bullet in bullets.sprites():
        bullet.draw_bullet()
    ship.blit_me()
    aliens.draw(screen)
    sb.show_score()
    if not stats.game_active:
        play_button.draw_button()
    pygame.display.flip()

def update_bullets(settings, screen, stats, sb, ship, aliens, bullets):
    bullets.update()
    for bullet in bullets.copy():
        if bullet.rect.bottom <= 0:
            bullets.remove(bullet)
    check_bullet_alien_collisions(settings, screen, stats, sb, ship, aliens, bullets)

def fire_bullet(settings, screen, ship, bullets):
    if len(bullets) < settings.bullets_allowed:
        new_bullet = Bullet(settings, screen, ship)
        bullets.add(new_bullet)

def get_number_aliens(settings, alien_width):
    available_space_x = settings.screen_width - (2 * alien_width)
    number_of_aliens = int(available_space_x / (2 * alien_width))
    return number_of_aliens

def get_number_of_rows(settings, ship_height, alien_height):
    available_space_y = settings.screen_height - 3 * alien_height - ship_height
    number_of_rows = int(available_space_y / (2 * alien_height))
    return number_of_rows

def create_alien(settings, screen, aliens, alien_number, row_numbers):
    alien = Alien(settings, screen)
    alien_width = alien.rect.width
    alien.x = alien_width + 2 * alien_width * alien_number
    alien.rect.x = alien.x
    alien.rect.y = alien.rect.height + 2 * alien.rect.height * row_numbers
    aliens.add(alien)

def create_fleet(settings, screen, ship, aliens):
    alien = Alien(settings, screen)
    number_of_aliens = get_number_aliens(settings, alien.rect.width)
    number_of_rows = get_number_of_rows(settings, ship.rect.height, alien.rect.height)
    for row in range(number_of_rows):
        for alien_number in range(number_of_aliens):
            create_alien(settings, screen, aliens, alien_number, row)

def check_fleet_edges(settings, aliens):
    for alien in aliens.sprites():
        if alien.check_edges():
            change_fleet_direction(settings, aliens)
            break

def change_fleet_direction(settings, aliens):
    for alien in aliens.sprites():
        alien.rect.y += settings.fleet_drop_speed
    settings.fleet_direction *= -1

def check_bullet_alien_collisions(settings, screen, stats, sb, ship, aliens, bullets):
    collisions = pygame.sprite.groupcollide(bullets, aliens, True, True)
    if collisions:
        for aliens in collisions.values():
            stats.score += settings.alien_points * len(aliens)
            sb.prep_score()
        check_high_score(stats, sb)
    if len(aliens) == 0:
        bullets.empty()
        stats.level += 1
        sb.prep_level()
        settings.increase_speed()
        create_fleet(settings, screen, ship, aliens)

def update_aliens(settings, stats, screen, sb, ship, aliens, bullets):
    check_fleet_edges(settings, aliens)
    aliens.update()
    if pygame.sprite.spritecollideany(ship, aliens):
        ship_hit(settings, stats, screen, sb, ship, aliens, bullets)
    check_aliens_bottom(settings, stats, screen, sb, ship, aliens, bullets)

def check_aliens_bottom(settings, stats, screen, sb, ship, aliens, bullets):
    screen_rect = screen.get_rect()
    for alien in aliens.sprites():
        if alien.rect.bottom >= screen_rect.bottom:
            ship_hit(settings, stats, screen, sb, ship, aliens, bullets)
            break

def ship_hit(settings, stats, screen, sb, ship, aliens, bullets):
    if stats.ships_left > 0:
        stats.ships_left -= 1
        sb.prep_ships()
        aliens.empty()
        bullets.empty()
        create_fleet(settings, screen, ship, aliens)
        ship.center_ship()
        sleep(0.5)
    else:
        stats.game_active = False
        pygame.mouse.set_visible(True)

def check_high_score(stats, sb):
    if stats.score > stats.high_score:
        stats.high_score = stats.score
        sb.prep_high_score()