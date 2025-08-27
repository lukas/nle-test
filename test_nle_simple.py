#!/usr/bin/env python3

import gymnasium as gym
import nle.env

# Try basic import
print("✓ Successfully imported NLE and Gymnasium")

# List all registered environments that contain 'nethack'
try:
    import gymnasium.envs
    all_envs = gymnasium.envs.registration.registry.all()
    nle_envs = [env_spec for env_spec in all_envs if 'nethack' in env_spec.id.lower()]
    
    print(f"Found {len(nle_envs)} NetHack environments:")
    for env in nle_envs[:10]:  # Show first 10
        print(f"  - {env.id}")
        
    # Try creating the first environment
    if nle_envs:
        env_id = nle_envs[0].id
        print(f"\nTesting environment: {env_id}")
        
        env = gym.make(env_id)
        obs, info = env.reset()
        print(f"✓ Environment created and reset successfully!")
        
        # Show observation structure
        if isinstance(obs, dict):
            print("Observation keys:", list(obs.keys()))
            if 'chars' in obs:
                print(f"Screen chars shape: {obs['chars'].shape}")
        
        print(f"Action space: {env.action_space}")
        
        # Take a random action
        action = env.action_space.sample()
        obs, reward, terminated, truncated, info = env.step(action)
        print(f"✓ Step completed. Reward: {reward}, Done: {terminated}")
        
        env.close()
        
except Exception as e:
    print(f"Error: {e}")
    import traceback
    traceback.print_exc()