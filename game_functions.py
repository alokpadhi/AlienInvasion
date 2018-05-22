import sys

import pygame
from bullet import Bullet
from alien import Alien
from time import sleep


def check_keydown_events(event, ai_settings, screen, ship, bullets):
    """Respond to keypress"""
    if event.key == pygame.K_RIGHT:
        ship.moving_right = True
    elif event.key == pygame.K_LEFT:
        ship.moving_left = True
    elif event.key == pygame.K_DOWN:
        ship.moving_down = True
    elif event.key == pygame.K_UP:
        ship.moving_up = True
    elif event.key == pygame.K_SPACE:
        fire_bullets(ai_settings, screen, ship, bullets)
    elif event.key == pygame.K_q:
        sys.exit()


def fire_bullets(ai_settings, screen, ship, bullets):
    # Create a new bullet and add it into the bullets group
    if len(bullets) < ai_settings.bullets_allowed:
        new_bullet = Bullet(ai_settings, screen, ship)
        bullets.add(new_bullet)


def check_keyup_events(event, ship):
    """Respond to keyrelease"""
    if event.key == pygame.K_RIGHT:
        ship.moving_right = False
    elif event.key == pygame.K_LEFT:
        ship.moving_left = False
    elif event.key == pygame.K_DOWN:
        ship.moving_down = False
    elif event.key == pygame.K_UP:
        ship.moving_up = False


def check_events(ai_settings, screen, stats, play_button, ship, aliens,
                 bullets):
    """Respond to key presses and mouse events
    :param screen:
    :param aliens:
    :param ai_settings:
    :param stats:
    :param play_button:
    :param bullets:
    :param ship:
    """
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        elif event.type == pygame.MOUSEBUTTONDOWN or event.type == pygame.K_p:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            check_play_button(ai_settings, screen, stats, play_button, ship,
                              aliens, bullets, mouse_x, mouse_y)
        elif event.type == pygame.KEYDOWN:
            check_keydown_events(event, ai_settings, screen, ship, bullets)
        elif event.type == pygame.KEYUP:
            check_keyup_events(event, ship)


def check_play_button(ai_settings, screen, stats, play_button, ship, aliens,
                      bullets, mouse_x, mouse_y):
    """Starts a new game when the player click Play"""
    button_clicked = play_button.rect.collidepoint(mouse_x, mouse_y)
    if button_clicked and not stats.game_active:
        # Reset the game settings
        ai_settings.initialize_dynamic_settings()
        # Hide the mouse cursor
        pygame.mouse.set_visible(False)

        # Reset game statistics
        stats.reset_stats()
        stats.game_active = True

        # Empty the list of aliens/zombies and bullets
        aliens.empty()
        bullets.empty()

        # Create new fleet and center the ship
        create_fleet(ai_settings, screen, ship, aliens)
        ship.center_ship()


def update_screen(ai_settings, screen, stats, sb, ship, aliens, bullets,
                  play_button):
    """Update images on the screen and flip to the new screen.
    :param aliens:
    :param bullets:
    :param ai_settings:
    :param screen:
    :param ship:
    :param stats:
    :param play_button:
    """
    # Redraw the screen during each pass through the loop
    screen.fill(ai_settings.bg_color)
    # Redraw all bullets behind ship and zombies/aliens.
    for bullet in bullets.sprites():
        bullet.draw_bullet()
    ship.blitme()
    aliens.draw(screen)

    # Draw the score information
    sb.show_score()

    # Draw the play button if the game is inactive
    if not stats.game_active:
        play_button.draw_button()
    # Make the most recently drawn screen visible.
    pygame.display.flip()


def update_bullets(ai_settings, screen, stats, sb, ship, aliens, bullets):
    """Update position of bullets and delete the old bullets"""
    # Update bullet position
    bullets.update()

    check_bullet_alien_collisions(ai_settings, screen, stats, sb, ship,
                                  aliens, bullets)

    # Get rid of bullets that are disappeared for optimization
    for bullet in bullets.copy():
        if bullet.rect.bottom <= 0:
            bullets.remove(bullet)

    check_bullet_alien_collisions(ai_settings, screen, stats, sb, ship,
                                  aliens, bullets)


def check_bullet_alien_collisions(ai_settings, screen, stats, sb, ship,
                                  aliens, bullets):
    # Check for any bullets that have hit any alien/zombie
    # If it is so then remove the bullet and alien/zombie
    collisions = pygame.sprite.groupcollide(bullets, aliens, False, True)

    if collisions:
        for aliens in collisions.values():
            stats.score += ai_settings.alien_points * len(aliens)
            sb.prep_score()
        check_high_score(stats, sb)

    if len(aliens) == 0:
        # Destroy existing bullets and create new fleet
        bullets.empty()
        ai_settings.increase_speed()
        create_fleet(ai_settings, screen, ship, aliens)


def get_number_aliens(ai_settings, alien_width):
    """Determine number of zombies placed in a row"""
    available_space_x = ai_settings.screen_width - 2 * alien_width
    number_aliens_x = int(available_space_x / (2 * alien_width))
    return number_aliens_x


def get_number_rows(ai_settings, ship_height, alien_height):
    """Determine the number of rows aliens that fit on the screen"""
    available_space_y = (ai_settings.screen_height -
                         (2 * alien_height) - ship_height)
    number_rows = int(available_space_y / (2 * alien_height))
    return number_rows


def create_alien(ai_settings, screen, aliens, alien_number, row_number):
    """Create an alien/zombie and place it in the row"""
    alien = Alien(ai_settings, screen)
    alien_width = alien.rect.width
    alien.x = alien_width + 2 * alien_width * alien_number
    alien.rect.x = alien.x
    alien.rect.y = alien.rect.height + 2 * alien.rect.height * row_number
    aliens.add(alien)


def create_fleet(ai_settings, screen, ship, aliens):
    """Create a full fleet of aliens"""
    # Create an alien and find the number of aliens in a row
    alien = Alien(ai_settings, screen)
    number_aliens_x = get_number_aliens(ai_settings, alien.rect.width)
    number_rows = get_number_rows(ai_settings, ship.rect.height,
                                  alien.rect.height)

    # Create the first row of aliens
    # for alien_number in range(number_aliens_x):
    #     create_alien(ai_settings, screen, aliens, alien_number)

    # Create fleet of aliens
    for row_number in range(number_rows):
        for alien_number in range(number_aliens_x):
            create_alien(ai_settings, screen, aliens, alien_number,
                         row_number)


def update_aliens(ai_settings, stats, screen, ship, aliens, bullets):
    """
    Check if the fleet is at an edge,
    and then update the positions of all aliens/zombies
    in the fleet
    """
    check_fleet_edges(ai_settings, aliens)
    aliens.update()

    # Look for alien-ship collisions
    if pygame.sprite.spritecollideany(ship, aliens):
        # print("Your Jet Hits!!!")
        ship_hit(ai_settings, stats, screen, ship, aliens, bullets)

    # Look for aliens/zombies hit the bottom
    check_aliens_bottom(ai_settings, stats, screen, ship, aliens, bullets)


def check_fleet_edges(ai_settings, aliens):
    """Respond if any alien/zombie has reached an edge"""
    for alien in aliens.sprites():
        if alien.check_edges():
            change_fleet_direction(ai_settings, aliens)
            break


def change_fleet_direction(ai_settings, alines):
    """Drop the entire fleet and change the direction"""
    for alien in alines.sprites():
        alien.rect.y += ai_settings.fleet_drop_speed
    ai_settings.fleet_direction *= -1


def ship_hit(ai_settings, stats, screen, ship, aliens, bullets):
    """Respond to jet being hit by alien"""
    if stats.ships_left > 0:
        # Decrement jets/ships left
        stats.ships_left -= 1

        # Empty the lists of aliens/zombies and bullets
        aliens.empty()
        bullets.empty()

        # Create a new fleet and center the jet/ship
        create_fleet(ai_settings, screen, ship, aliens)
        ship.center_ship()

        # Pause the game after one ship/jet destroy
        sleep(0.5)
    else:
        stats.game_active = False
        pygame.mouse.set_visible(False)


def check_aliens_bottom(ai_settings, stats, screen, ship, aliens, bullets):
    """Check if any alien/zombie reaches at the bottom of the screen"""
    screen_rect = screen.get_rect()
    for alien in aliens.sprites():
        if alien.rect.bottom >= screen_rect.bottom:
            # Treat the game as the ship/jet got hit
            ship_hit(ai_settings, stats, screen, ship, aliens, bullets)
            break


def check_high_score(stats, sb):
    """Check to see if there is a new high score"""
    if stats.score > stats.high_score:
        stats.high_score = stats.score
        sb.prep_high_score()
