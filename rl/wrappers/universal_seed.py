import gym


class UniversalSeed(gym.Wrapper):

    def seed(self, seed: int):
        seeds = seed
        self.env.observation_space.seed(seed)
        self.env.action_space.seed(seed)
        return seeds