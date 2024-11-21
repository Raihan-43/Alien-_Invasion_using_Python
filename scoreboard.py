import pygame.font

class ScoreBoard:
    def __init__(self, ai_game):
        self.screen = ai_game.screen
        self.screen_rect= self.screen.get_rect()
        self.settings= ai_game.settings
        self.stats= ai_game.stats

        self.text_color= 'Red'
        self.font= pygame.font.SysFont(None, 36)

        self.prep_score()

    def prep_score(self):
        score_str= str(self.stats.score)
        # print(score_str)
        self.score_image= self.font.render(score_str, True, self.settings.bg_color)

        self.score_rect= self.score_image.get_rect()
        self.score_rect.right = self.screen_rect.right -20
        self.score_rect.top= 20

    def show_score(self):
        self.screen.blit(self.score_image, self.score_rect)