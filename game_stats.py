from pathlib import Path
class GameStats:
    #keep statistics of the game
    def __init__(self,ai_game):
        self.settings = ai_game.settings
        self.reset_stats()
        self.score = 0
        self.high_score= 0
    
    def reset_stats(self):
        #initialize stats
        self.ships_left = self.settings.ship_limit

    def store_high_score(self, high_score):
        path= Path('high_score.txt')
        contents= str(self.high_score)
        path.write_text(contents)

    def load_high_score(self):
        path= Path('high_score.txt')
        self.high_score = path.read_text()
        self.high_score= int(self.high_score)



