#!/usr/bin/env python3

import gymnasium as gym
import nle.env
import numpy as np
import random
import json
from pathlib import Path

class SimpleRandomAgent:
    """A simple random agent that occasionally takes meaningful actions"""
    
    def __init__(self, env):
        self.env = env
        self.action_space = env.action_space
        
        # Common NetHack actions
        self.movement_actions = [1, 2, 3, 4, 5, 6, 7, 8]  # movement directions
        self.common_actions = [0, 9, 10, 12, 13, 14, 15, 16]  # common commands
        
    def act(self, observation):
        """Choose an action - mostly random with some bias towards common actions"""
        if random.random() < 0.7:  # 70% chance of movement/common actions
            return random.choice(self.movement_actions + self.common_actions)
        else:
            return self.action_space.sample()

def render_observation(obs):
    """Convert observation to a readable format"""
    chars = obs['chars']
    colors = obs['colors']
    message = obs['message']
    
    # Convert chars to string representation
    screen_text = []
    for row in chars:
        line = ''.join(chr(c) if 32 <= c <= 126 else '?' for c in row)
        screen_text.append(line.rstrip())
    
    # Extract message
    msg_text = ''.join(chr(c) if 32 <= c <= 126 else '' for c in message if c != 0)
    
    return {
        'screen_text': screen_text,
        'message': msg_text,
        'stats': obs['blstats'].tolist(),  # Convert numpy array to list for JSON serialization
        'turn': int(obs['blstats'][20])  # Turn number is at index 20
    }

def generate_game_trajectory(env_name='NetHackScore-v0', num_steps=100, seed=None):
    """Generate a trajectory of game states and actions"""
    
    if seed is not None:
        random.seed(seed)
        np.random.seed(seed)
    
    env = gym.make(env_name)
    agent = SimpleRandomAgent(env)
    
    # Reset environment
    obs, info = env.reset(seed=seed)
    
    trajectory = []
    
    for step in range(num_steps):
        # Render current observation
        rendered_obs = render_observation(obs)
        
        # Choose action
        action = agent.act(obs)
        
        # Store current state
        trajectory.append({
            'step': step,
            'observation': rendered_obs,
            'action': int(action),
            'action_name': f'action_{action}'  # We could map this to actual NetHack commands
        })
        
        # Take action
        obs, reward, terminated, truncated, info = env.step(action)
        
        # Add reward to previous step
        trajectory[-1]['reward'] = float(reward)
        trajectory[-1]['terminated'] = terminated
        trajectory[-1]['truncated'] = truncated
        
        if terminated or truncated:
            print(f"Game ended at step {step}")
            break
    
    env.close()
    return trajectory

def continue_trajectory_from_step(existing_trajectory, from_step, additional_steps=50, seed=None):
    """Continue a trajectory from a specific step by replaying up to that point"""
    
    if from_step >= len(existing_trajectory):
        raise ValueError(f"from_step {from_step} is beyond trajectory length {len(existing_trajectory)}")
    
    # Extract the original seed and environment from the first step if possible
    # We'll need to replay the trajectory up to the desired point
    
    # For now, we'll use the seed provided or derive one from the trajectory
    if seed is None:
        # Create a deterministic seed based on the trajectory and step
        seed = hash(str(existing_trajectory[:from_step+1])) % (2**32)
    
    # Get environment name (assume same as original, could be stored in trajectory metadata)
    env_name = 'NetHackScore-v0'  # Default, could be enhanced to store this
    
    if seed is not None:
        random.seed(seed)
        np.random.seed(seed)
    
    env = gym.make(env_name)
    agent = SimpleRandomAgent(env)
    
    # Reset environment with the derived seed
    obs, info = env.reset(seed=seed)
    
    # Replay actions up to the desired step
    print(f"Replaying {from_step + 1} steps to reach continuation point...")
    
    for replay_step in range(from_step + 1):
        if replay_step < len(existing_trajectory):
            # Use the original action
            action = existing_trajectory[replay_step]['action']
        else:
            # This shouldn't happen, but use agent decision as fallback
            action = agent.act(obs)
        
        obs, reward, terminated, truncated, info = env.step(action)
        
        if terminated or truncated:
            env.close()
            raise ValueError(f"Game ended during replay at step {replay_step}. Cannot continue.")
    
    # Now continue from this point with new trajectory
    new_trajectory = existing_trajectory[:from_step + 1].copy()  # Include the original trajectory up to this point
    
    # Continue generating new steps
    for step in range(additional_steps):
        current_step_num = from_step + 1 + step
        
        # Render current observation
        rendered_obs = render_observation(obs)
        
        # Choose action
        action = agent.act(obs)
        
        # Store current state
        new_trajectory.append({
            'step': current_step_num,
            'observation': rendered_obs,
            'action': int(action),
            'action_name': f'action_{action}',
            'branch_from_step': from_step  # Mark where this branched from
        })
        
        # Take action
        obs, reward, terminated, truncated, info = env.step(action)
        
        # Add reward to previous step
        new_trajectory[-1]['reward'] = float(reward)
        new_trajectory[-1]['terminated'] = terminated
        new_trajectory[-1]['truncated'] = truncated
        
        if terminated or truncated:
            print(f"Game ended at step {current_step_num}")
            break
    
    env.close()
    return new_trajectory

if __name__ == "__main__":
    print("Generating NetHack game trajectory...")
    
    # Generate a trajectory
    trajectory = generate_game_trajectory(num_steps=50, seed=42)
    
    # Save trajectory to file
    output_file = Path("game_trajectory.json")
    with open(output_file, 'w') as f:
        json.dump(trajectory, f, indent=2)
    
    print(f"Generated {len(trajectory)} steps")
    print(f"Trajectory saved to: {output_file}")
    
    # Show first few steps
    print("\nFirst few steps:")
    for i, step in enumerate(trajectory[:3]):
        print(f"\nStep {i}:")
        print(f"  Action: {step['action']}")
        print(f"  Reward: {step['reward']}")
        print(f"  Message: {step['observation']['message'][:50]}...")
        print(f"  Screen (first 3 lines):")
        for line in step['observation']['screen_text'][:3]:
            print(f"    {line[:50]}...")