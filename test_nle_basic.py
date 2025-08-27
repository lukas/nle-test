#!/usr/bin/env python3

import gymnasium as gym
import nle.env

print("✓ Successfully imported NLE and Gymnasium")

# Try to create one of the common NLE environments
env_names = [
    'NetHackScore-v0',
    'NetHackStaircase-v0', 
    'NetHackOracle-v0',
    'NetHack-v0'
]

working_env = None
for env_name in env_names:
    try:
        print(f"Trying environment: {env_name}")
        env = gym.make(env_name)
        obs, info = env.reset()
        print(f"✓ Environment {env_name} works!")
        
        # Show observation structure
        if isinstance(obs, dict):
            print("Observation keys:", list(obs.keys()))
            if 'chars' in obs:
                print(f"Screen chars shape: {obs['chars'].shape}")
                print(f"First few chars:\n{obs['chars'][:5, :10]}")
        
        print(f"Action space: {env.action_space}")
        
        # Take a random action
        action = env.action_space.sample()
        obs, reward, terminated, truncated, info = env.step(action)
        print(f"✓ Step completed. Reward: {reward}, Done: {terminated}")
        
        working_env = env_name
        env.close()
        break
        
    except Exception as e:
        print(f"✗ Failed to create {env_name}: {e}")

if working_env:
    print(f"\n🎉 Successfully tested NLE environment: {working_env}")
else:
    print("\n❌ No working NLE environments found")
    
    # Try to see what's available
    print("\nChecking what's available in nle.env...")
    try:
        import nle.env
        print("nle.env imported successfully")
        
        # Try to see the module contents
        print("nle.env attributes:", [attr for attr in dir(nle.env) if not attr.startswith('_')])
        
    except Exception as e:
        print(f"Error with nle.env: {e}")