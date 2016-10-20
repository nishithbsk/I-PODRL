import math
import sys

import pygame
from pygame.constants import K_w, K_s
from utils.vec2d import vec2d
from utils import percent_round_int

import base

class Ball(pygame.sprite.Sprite):

	def __init__(self, radius, speed,
		pos_init, SCREEN_WIDTH, SCREEN_HEIGHT):
                
                pygame.sprite.Sprite.__init__(self)

		self.radius = radius
		self.speed = speed
		self.pos = vec2d(pos_init)
		self.vel = vec2d((speed, -1.0*speed))

		self.SCREEN_HEIGHT = SCREEN_HEIGHT
		self.SCREEN_WIDTH = SCREEN_WIDTH

		image = pygame.Surface((radius*2, radius*2))
		image.fill((0, 0, 0, 0))
		image.set_colorkey((0,0,0))

		pygame.draw.circle(
		image,
		(255, 255, 255),
		(radius, radius),
		radius,
		0
		)

		self.image = image
		self.rect = self.image.get_rect()
		self.rect.center = pos_init

	def update(self, agentPlayer_1, agentPlayer_2, dt):
		
                if self.pos.y-self.radius <= 0: 
                        self.vel.y *= -0.99
                        self.pos.y += 1.0

                if self.pos.y+self.radius >= self.SCREEN_HEIGHT:
			self.vel.y *= -0.99
                        self.pos.y -= 1.0

                if self.pos.x <= agentPlayer_1.pos.x+agentPlayer_1.rect_width:
                    if pygame.sprite.collide_rect(self, agentPlayer_1):
                        self.vel.x = -1*(self.vel.x + self.speed*0.05)
                        self.vel.y += agentPlayer_1.vel.y*0.01
                        self.pos.x += 1.0

                if self.pos.x >= agentPlayer_2.pos.x-agentPlayer_2.rect_width:
                    if pygame.sprite.collide_rect(self, agentPlayer_2):
                        self.vel.x = -1*(self.vel.x + self.speed*0.05)
                        self.vel.y += agentPlayer_2.vel.y*0.006
                        self.pos.x -= 1.0

                self.pos.x += self.vel.x * dt
		self.pos.y += self.vel.y * dt

		self.rect.center = (self.pos.x, self.pos.y)


class Player(pygame.sprite.Sprite):

	def __init__(self, speed, rect_width, rect_height,
		pos_init, SCREEN_WIDTH, SCREEN_HEIGHT):

                pygame.sprite.Sprite.__init__(self)

		self.speed = speed
		self.pos = vec2d(pos_init)
		self.vel = vec2d((0, 0))

		self.rect_height = rect_height
		self.rect_width = rect_width
		self.SCREEN_HEIGHT = SCREEN_HEIGHT
		self.SCREEN_WIDTH = SCREEN_WIDTH

		image = pygame.Surface((rect_width, rect_height))
		image.fill((0, 0, 0, 0))
		image.set_colorkey((0,0,0))

		pygame.draw.rect(
			image,
			(255, 255, 255),
			(0, 0, rect_width, rect_height),
			0
		)

		self.image = image
		self.rect = self.image.get_rect()
		self.rect.center = pos_init

	def updateAgent(self, dy, dt):
                self.vel.y += dy
                self.vel.y *= 0.9
                
                self.pos.y += self.vel.y

                if self.pos.y-self.rect_height/2 <= 0:
                    self.pos.y = self.rect_height/2
                    self.vel.y = 0.0

                if self.pos.y+self.rect_height/2 >= self.SCREEN_HEIGHT:
                    self.pos.y = self.SCREEN_HEIGHT-self.rect_height/2
                    self.vel.y = 0.0

		self.rect.center = (self.pos.x, self.pos.y)

	def updateCpu(self, ball, dt):
                if ball.vel.x >= 0 and ball.pos.x >= self.SCREEN_WIDTH/2:
			if self.pos.y < ball.pos.y:
				self.pos.y += self.speed * dt
                                self.vel.y = self.speed*dt

			if self.pos.y > ball.pos.y:
				self.pos.y -= self.speed * dt
                                self.vel.y = -1*self.speed*dt

		self.rect.center = (self.pos.x, self.pos.y)

class Pong_2Player(base.Game):
        """
        Loosely based on code from marti1125's `pong game`_.
        
        .. _pong game: https://github.com/marti1125/pong/

        Parameters
        ----------
        width : int
            Screen width.

        height : int
            Screen height, recommended to be same dimension as width.

        MAX_SCORE : int (default: 11)
            The max number of points the agent or cpu need to score to cause a terminal state.

        """
	def __init__(self, width=64, height=48, MAX_SCORE=11):

		actions = {
			"up": K_w,
			"down": K_s
		}

                base.Game.__init__(self, width, height, actions=actions)

                #the %'s come from original values, wanted to keep same ratio when you 
                #increase the resolution.
                self.ball_radius = percent_round_int(height, 0.03)
                self.players_speed = 0.022*height
                self.ball_speed = 0.00075*height 
                self.paddle_width = percent_round_int(width, 0.023)
                self.paddle_height = percent_round_int(height, 0.15) 
                self.paddle_dist_to_wall = percent_round_int(width, 0.0625)
                self.MAX_SCORE = MAX_SCORE

                self.dy_1 = 0.0
                self.dy_2 = 0.0
		self.score_sum = 0.0 #need to deal with 11 on either side winning
		self.score_counts = {
			"agent_1": 0.0,
			"agent_2": 0.0
		}

	def _handle_player_1_events(self):
		self.dy_1 = 0
		for event in pygame.event.get():
                        print "Received action from player 1"
			if event.type == pygame.QUIT:
				pygame.quit()
				sys.exit()

			if event.type == pygame.KEYDOWN:
				key = event.key
				if key == self.actions['up']:
                                        self.dy_1 -= self.players_speed

				if key == self.actions['down']:
					self.dy_1 += self.players_speed

	def _handle_player_2_events(self):
		self.dy_2 = 0
		for event in pygame.event.get():
                        print "Received action from player 2"
			if event.type == pygame.QUIT:
				pygame.quit()
				sys.exit()

			if event.type == pygame.KEYDOWN:
				key = event.key
				if key == self.actions['up']:
                                        self.dy_2 -= self.players_speed

				if key == self.actions['down']:
					self.dy_2 += self.players_speed
        
        def getGameState(self):
            """
            Gets a non-visual state representation of the game.
            
            Returns
            -------

            dict
                * player y position.
                * players velocity.
                * cpu y position. 
                * ball x position.
                * ball y position.
                * ball x velocity.
                * ball y velocity.

                See code for structure.

            """
            state = {
                    "player_1": {
                        "y": self.agentPlayer_1.pos.y,
                        "velocity": self.agentPlayer_1.vel.y
                    },
                    "player_2": {
                        "y": self.agentPlayer_2.pos.y,
                        "velocity": self.agentPlayer_2.vel.y
                    },
                    "ball": {
                        "x": self.ball.pos.x,
                        "y": self.ball.pos.y,
                        "velocity": {
                            "x": self.ball.pos.x,
                            "y": self.ball.pos.y
                        }
                    }
            }

            return state
	
        def getScore(self):
		return self.score_sum

	def game_over(self):
		#pong used 11 as max score
		return (self.score_counts['agent_1'] == self.MAX_SCORE) or (self.score_counts['agent_2'] == self.MAX_SCORE)

	def init(self):
            self.score_counts = {
                    "agent_1": 0.0,
                    "agent_2": 0.0
            }

            self.score_sum = 0.0
            self.ball = Ball(
        	self.ball_radius,
		self.ball_speed,
		(self.width/2, self.height/2),
                self.width,
                self.height
            )
            
            self.agentPlayer_1 = Player(
		self.players_speed,
		self.paddle_width,
		self.paddle_height,
		(self.paddle_dist_to_wall, self.height/2),
		self.width,
		self.height)

            self.agentPlayer_2 = Player(
		self.players_speed,
		self.paddle_width,
		self.paddle_height,
		(self.width-self.paddle_dist_to_wall, self.height/2), 
                self.width,
		self.height)
            
            self.players_group = pygame.sprite.Group()
            self.players_group.add( self.agentPlayer_1 )
            self.players_group.add( self.agentPlayer_2 )

            self.ball_group = pygame.sprite.Group()
            self.ball_group.add( self.ball )
	
	def _reset_ball(self, direction):
            self.ball.pos.x = self.width/2 #move it to the center
            
            #we go in the same direction that they lost in but at starting vel.
            self.ball.vel.x = self.ball_speed*direction
            self.ball.vel.y = (self.rng.random_sample()*self.ball_speed)-self.ball_speed

	def step(self, dt):

		self.screen.fill((0,0,0))

		self._handle_player_1_events()
                self._handle_player_2_events()

		#logic
		if self.ball.pos.x <= 0:
			self.score_sum -= 1.0
			self.score_counts["agent_2"] += 1.0
			self._reset_ball(-1)

		if self.ball.pos.x >= self.width:
			self.score_sum += 1.0
			self.score_counts["agent_1"] += 1.0
			self._reset_ball(1)

                #winning
                if self.score_counts['agent_1'] == self.MAX_SCORE:
                    self.score_sum += 10.0

                #losing
                if self.score_counts['agent_2'] == self.MAX_SCORE:
                    self.score_sum -= 10.0
        
                self.ball.update(self.agentPlayer_1, self.agentPlayer_2, dt)
		self.agentPlayer_1.updateAgent(self.dy_1, dt)
		self.agentPlayer_2.updateAgent(self.dy_2, dt)
		
		self.players_group.draw(self.screen)
		self.ball_group.draw(self.screen)

if __name__ == "__main__":
    import numpy as np

    pygame.init()
    game = Pong_2Player(width=256, height=200)
    game.screen = pygame.display.set_mode( game.getScreenDims(), 0, 32)
    game.clock = pygame.time.Clock()
    game.rng = np.random.RandomState(24)
    game.init()

    while True:
        dt = game.clock.tick_busy_loop(60)
        game.step(dt)
        pygame.display.update()