#!/usr/bin/env python3

import gymnasium as gym
import nle.env

# Check available environments
print("Available NLE environments:")
from gymnasium.envs.registry import all

nle_envs = [env_spec for env_spec in all() if 'nethack' in env_spec.id.lower() or 'nle' in env_spec.id.lower()]

for env in nle_envs:
    print(f"  - {env.id}")

# Try a simple environment
if nle_envs:
    env_id = nle_envs[0].id
    print(f"\nTesting environment: {env_id}")
    
    try:
        env = gym.make(env_id)
        obs, info = env.reset()
        print(f"✓ Environment {env_id} is working!")
        print(f"Observation keys: {obs.keys() if hasattr(obs, 'keys') else 'N/A'}")
        print(f"Action space: {env.action_space}")
        
        # Test one step
        action = env.action_space.sample()
        obs, reward, terminated, truncated, info = env.step(action)
        print(f"✓ Step completed. Reward: {reward}")
        
        env.close()
        
    except Exception as e:
        print(f"✗ Error with {env_id}: {e}")
else:
    print("No NLE environments found!")