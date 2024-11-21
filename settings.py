class Settings:
    # store all the settings
    def __init__(self):
        self.screen_width= 900
        self.screen_height= 600
        self.bg_color= (230, 230, 230)
        self.frame_rate= 60
        self.ship_speed= 5

        #bullet setting
        self.bullet_speed = 5
        self.bullet_width = 3
        self.bullet_height = 10
        self.bullet_color = (60,60,60)

        #allien setting
        self.alien_speed = 2
        self.fleet_drop_speed = 10
        self.fleet_direction=1 #1 means right, -1 means left

        self.ship_limit =3
