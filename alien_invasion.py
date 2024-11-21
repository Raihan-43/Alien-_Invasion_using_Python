import sys
from time import sleep # to pause game for a moment after ship got hit

import pygame
from settings import Settings
from ship import Ship
from bullet import Bullet
from alien import Alien
from game_stats import GameStats
from button import Button
from scoreboard import ScoreBoard


class AlienInvasion:
    #overall class to manage game asset and behavior
    def __init__(self):
        #initialize the game, create game resources
        pygame.init()
        self.clock= pygame.time.Clock()
        self.settings= Settings()
        self.active= False
        self.screen = pygame.display.set_mode((self.settings.screen_width, self.settings.screen_height))
        pygame.display.set_caption("Alien Invasion")
        self.ship= Ship(self)
        self.bullets = pygame.sprite.Group()
        self.aliens = pygame.sprite.Group()
        self._create_fleet()

        self.stats= GameStats(self)
        self.buton= Button(self, 'Play')
        self.sb= ScoreBoard(self)

    
    def run_game(self):
        #start main loop for the game
        while True:
            self._check_events()

            if self.active:
                self.ship.update()
                self._update_bullets()
                self._update_aliens()
            
            self._update_screen()
            self.clock.tick(self.settings.frame_rate)
    
    def _update_bullets(self):
        #update bullet position
        self.bullets.update()

        #get rid of old bullet
        for bullet in self.bullets.copy():
            #cannot update the same list in for loop. thats why a copy used
            if bullet.rect.bottom <= 0:
                self.bullets.remove(bullet)
        # print(len(self.bullets))
        self._check_bullet_alien_collision()
    
    def _check_bullet_alien_collision(self):

        #check for collision, if colision occurs it is removed fromgroup
        collisions= pygame.sprite.groupcollide(self.bullets, self.aliens, True, True)
        if not self.aliens:
            self.bullets.empty()
            self._create_fleet()
            self.settings.bullet_speed +=5 #bullet speed increases after every fleet
        if collisions:
            self.stats.score +=1

    def _create_alien(self, x_position, y_position):
        new_alien= Alien(self)
        new_alien.x= x_position
        new_alien.y= y_position
        new_alien.rect.x = x_position
        new_alien.rect.y = y_position
        self.aliens.add(new_alien)


    def _create_fleet(self):
        # create alien fleet
        alien= Alien(self)
        alien_width= alien.rect.width
        alien_height= alien.rect.height

        current_y = alien.rect.height
        while current_y < (self.settings.screen_height - alien_height*4):
            current_x= alien_width
            while current_x < (self.settings.screen_width- alien_width):
                self._create_alien(current_x, current_y)
                current_x += alien_width*2
            current_y += alien_height
            # print(current_y)

    
    def _check_fleet_edge(self):
        for alien in self.aliens.sprites():
            if alien.check_for_edge():
                self._change_fleet_direction()
                break
    
    def _change_fleet_direction(self):
        for alien in self.aliens.sprites():
            alien.rect.y += self.settings.fleet_drop_speed
        self.settings.fleet_direction *= -1

        

    def _update_aliens(self):
        self._check_fleet_edge()
        self.aliens.update()

        #look for alien-ship collision
        if pygame.sprite.spritecollideany(self.ship, self.aliens):
            # print("Ship got hit")
            self._ship_hits()
        self._check_alien_bottoms()
    
    def _ship_hits(self):
        #responds to ship being hit
        self.settings.ship_limit -= 1
        self.bullets.empty() #get rid of remainig bullet
        self.aliens.empty() #get rid of remainig alien

        if self.settings.ship_limit > 0:
            self._create_fleet() #create new fleet
            self.ship.center_ship() #reposition ship
            sleep(0.5) #pause 0.5 second
        else:
            self.active= False
    
    def _check_alien_bottoms(self):
        #check if an alien hits the bottomof the screen
        for alien in self.aliens.sprites():
            if alien.rect.bottom >= self.settings.screen_height:
                self._ship_hits()
                break

    def _check_events(self):
        #responds to keypresses
        for event in pygame.event.get(): #look for keyboard and mouse movement
                if event.type == pygame.QUIT:
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    # print(event)
                    self._check_keydown_events(event)
                elif event.type == pygame.KEYUP:
                    self._check_keyup_events(event)
                
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos= pygame.mouse.get_pos()
                    self._check_play_buttton(mouse_pos)
    
    def _check_keydown_events(self, event):
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = True
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = True
        elif event.key == pygame.K_q: #pres q to exit
            sys.exit()
        elif event.key == pygame.K_UP:
            self._fire_bullet()

    def _check_keyup_events(self, event):
        self.ship.moving_right= False
        self.ship.moving_left= False

    def _check_play_buttton(self, mouse_position):
        button_click= self.buton.rect.collidepoint(mouse_position)
        if button_click and not self.active:
            self.stats.reset_stats()
            self.active= True

            self.bullets.empty() #get rid of remainig bullet
            self.aliens.empty() #get rid of remainig alien

            self._create_fleet() #create new fleet
            self.ship.center_ship() #reposition ship

            self.stats.score=0
            self.settings.ship_limit = 3


    def _fire_bullet(self):
        new_bullet = Bullet(self)
        self.bullets.add(new_bullet)

    
    def _update_screen(self):
        #updates image
        self.screen.fill(self.settings.bg_color)
        for bullet in self.bullets.sprites():
            bullet.draw_bullet()
        self.ship.blitme()
        self.aliens.draw(self.screen)
        #score info
        # self.sb.show_score()
        self._show_score()
        if not self.active:
            self.buton.draw_button()
        pygame.display.flip()
    
    def _show_score(self):
        self.scr = pygame.font.SysFont('courier new', 24)
        self.h_score= pygame.font.SysFont('courier new', 24)
        self.current_score= self.stats.score
        self.stats.load_high_score()
        if self.current_score > self.stats.high_score:
            self.stats.high_score= self.current_score
            self.stats.store_high_score(self.stats.high_score)

        self.h_score_img= self.scr.render(f"Highest Score: {str(self.stats.high_score)}", True, 'darkslategrey', self.settings.bg_color)
        self.h_score_img_rect= self.h_score_img.get_rect()
        self.h_score_img_rect.center= self.screen.get_rect().center
        self.h_score_img_rect.top= 10
        self.screen.blit(self.h_score_img, self.h_score_img_rect)

        self.scr_img= self.scr.render(f"Score: {str(self.current_score)}", True, 'darkslategrey', self.settings.bg_color)
        self.scr_img_rect= self.scr_img.get_rect()
        self.scr_img_rect.right= self.settings.screen_width -20
        self.scr_img_rect.top= 10
        self.screen.blit(self.scr_img, self.scr_img_rect)





if __name__== '__main__':
    #make a game instance and run the game
    ai= AlienInvasion()
    ai.run_game()

        