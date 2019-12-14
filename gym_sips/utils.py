import random
from collections import namedtuple


def act(a):
    """
    simple function to easily change the action number into a string
    returns string
    """
    if a == 0:
        return "BOUGHT AWAY"
    elif a == 1:
        return "BOUGHT HOME"
    elif a == 2:
        return "SKIP"
    else:
        return "action outside of defined actions"


Transition = namedtuple('Transition',
                        ('state', 'action', 'next_state', 'reward'))


class ReplayMemory(object):

    def __init__(self, capacity):
        self.capacity = capacity
        self.memory = []
        self.position = 0

    def push(self, *args):
        """Saves a transition."""
        if len(self.memory) < self.capacity:
            self.memory.append(None)
        self.memory[self.position] = Transition(*args)
        self.position = (self.position + 1) % self.capacity

    def sample(self, batch_size):
        return random.sample(self.memory, batch_size)

    def __len__(self):
        return len(self.memory)
