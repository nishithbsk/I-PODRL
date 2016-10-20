import random
from ple.games.pong_2player import Pong_2Player
from ple import PLE

def pickAction(actions):
    return random.choice(actions)

game = Pong_2Player()
p = PLE(game, fps=30, display_screen=True, force_fps=False)
p.init()

actions = p.getActionSet()

nb_frames = 1000
reward_1 = 0.0
reward_2 = 0.0

for f in range(nb_frames):
    if p.game_over(): #check if the game is over
        p.reset_game()

    obs = p.getScreenRGB()
    action_1 = pickAction(actions)
    reward_1 = p.act(action_1)

    action_2 = pickAction(actions)
    reward_2 = p.act(action_2)
    
