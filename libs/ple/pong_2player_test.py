import random

from ple.games.pong_2player import Pong_2Player
from pygame.constants import K_w, K_s, K_a, K_b
from ple import PLE

NO_OP = 296

def pickAction(actions):
    return random.choice(actions)

game = Pong_2Player()
p = PLE(game, fps=30, display_screen=True, force_fps=False)
p.init()

actions_1 = [K_w, K_s, NO_OP]
actions_2 = [K_a, K_b, NO_OP]

nb_frames = 1000
reward_1 = 0.0
reward_2 = 0.0

for f in range(nb_frames):
    if p.game_over(): #check if the game is over
        p.reset_game()

    obs = p.getScreenRGB()
    action_1 = pickAction(actions_1)
    reward_1 = p.act(action_1)

    action_2 = pickAction(actions_2)
    reward_2 = p.act(action_2)
    
