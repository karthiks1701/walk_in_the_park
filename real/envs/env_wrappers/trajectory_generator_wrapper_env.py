# coding=utf-8
# Copyright 2020 The Google Research Authors.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""A wrapped MinitaurGymEnv with a built-in controller."""

from __future__ import absolute_import, division, print_function


class TrajectoryGeneratorWrapperEnv(object):
    """A wrapped LocomotionGymEnv with a built-in trajectory generator."""
    def __init__(self, gym_env, trajectory_generator):
        """Initialzes the wrapped env.

    Args:
      gym_env: An instance of LocomotionGymEnv.
      trajectory_generator: A trajectory_generator that can potentially modify
        the action and observation. Typticall generators includes the PMTG and
        openloop signals. Expected to have get_action and get_observation
        interfaces.

    Raises:
      ValueError if the controller does not implement get_action and
      get_observation.

    """
        self._gym_env = gym_env
        if not hasattr(trajectory_generator, 'get_action') or not hasattr(
                trajectory_generator, 'get_observation'):
            raise ValueError(
                'The controller does not have the necessary interface(s) implemented.'
            )

        self._trajectory_generator = trajectory_generator

        # The trajectory generator can subsume the action/observation space.
        if hasattr(trajectory_generator, 'observation_space'):
            self.observation_space = self._trajectory_generator.observation_space

        if hasattr(trajectory_generator, 'action_space'):
            self.action_space = self._trajectory_generator.action_space

    def __getattr__(self, attr):
        return getattr(self._gym_env, attr)

    def _modify_observation(self, observation):
        return self._trajectory_generator.get_observation(observation)

    def reset(self, initial_motor_angles=None, reset_duration=0.0):
        if getattr(self._trajectory_generator, 'reset'):
            self._trajectory_generator.reset()
        observation = self._gym_env.reset(initial_motor_angles, reset_duration)
        return self._modify_observation(observation)

    def step(self, action):
        """Steps the wrapped environment.

    Args:
      action: Numpy array. The input action from an NN agent.

    Returns:
      The tuple containing the modified observation, the reward, the epsiode end
      indicator.

    Raises:
      ValueError if input action is None.

    """
        
        # print("------------------")
        # print("STEP TrajectoryGeneratorWrapperEnv, action: ", action)
        # print("------------------")

        if action is None:
            raise ValueError('Action cannot be None')

        new_action = self._trajectory_generator.get_action(
            self._gym_env.robot.GetTimeSinceReset(), action)
        
        # print("------------------")
        # print("New action: ", new_action)
        # print("------------------")

        original_observation, reward, done, _ = self._gym_env.step(new_action)

        return self._modify_observation(original_observation), reward, done, _
