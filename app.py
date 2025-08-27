#!/usr/bin/env python3

from fastapi import FastAPI, Request, Form, UploadFile, File
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from pathlib import Path
import json
import gymnasium as gym
import nle.env
from simple_agent import generate_game_trajectory, render_observation

app = FastAPI(title="NetHack Agent Viewer", description="Visualize NetHack agent moves step by step")

# Set up templates
templates_dir = Path("templates")
templates_dir.mkdir(exist_ok=True)

templates = Jinja2Templates(directory=str(templates_dir))

# In-memory storage for trajectories (in production, use a database)
trajectories = {}

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    """Main page with trajectory viewer"""
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/generate")
async def generate_new_trajectory(
    steps: int = Form(50, description="Number of steps"),
    seed: int = Form(42, description="Random seed"),
    env_name: str = Form("NetHackScore-v0", description="Environment name")
):
    """Generate a new NetHack trajectory"""
    try:
        trajectory = generate_game_trajectory(env_name=env_name, num_steps=steps, seed=seed)
        trajectory_id = f"traj_{seed}_{steps}"
        trajectories[trajectory_id] = trajectory
        
        return {
            "success": True,
            "trajectory_id": trajectory_id,
            "length": len(trajectory),
            "message": f"Generated {len(trajectory)} steps"
        }
    except Exception as e:
        return {"success": False, "error": str(e)}

@app.post("/upload")
async def upload_trajectory(file: UploadFile = File(...)):
    """Upload a trajectory JSON file"""
    try:
        content = await file.read()
        trajectory = json.loads(content.decode('utf-8'))
        
        trajectory_id = f"uploaded_{file.filename.replace('.json', '')}"
        trajectories[trajectory_id] = trajectory
        
        return {
            "success": True,
            "trajectory_id": trajectory_id,
            "length": len(trajectory),
            "message": f"Uploaded trajectory with {len(trajectory)} steps"
        }
    except Exception as e:
        return {"success": False, "error": str(e)}

@app.get("/trajectories")
async def list_trajectories():
    """List all available trajectories"""
    return {
        "trajectories": [
            {
                "id": traj_id,
                "length": len(traj),
                "first_message": traj[0]["observation"]["message"][:50] + "..." if traj else ""
            }
            for traj_id, traj in trajectories.items()
        ]
    }

@app.get("/trajectory/{trajectory_id}")
async def get_trajectory(trajectory_id: str):
    """Get a specific trajectory"""
    if trajectory_id not in trajectories:
        return {"success": False, "error": "Trajectory not found"}
    
    return {
        "success": True,
        "trajectory": trajectories[trajectory_id]
    }

@app.get("/trajectory/{trajectory_id}/step/{step_num}")
async def get_step(trajectory_id: str, step_num: int):
    """Get a specific step from a trajectory"""
    if trajectory_id not in trajectories:
        return {"success": False, "error": "Trajectory not found"}
    
    trajectory = trajectories[trajectory_id]
    if step_num < 0 or step_num >= len(trajectory):
        return {"success": False, "error": "Step number out of range"}
    
    return {
        "success": True,
        "step": trajectory[step_num],
        "trajectory_length": len(trajectory)
    }

@app.get("/live-generate")
async def live_generate(steps: int = 20, seed: int = None):
    """Generate and return a trajectory in real-time"""
    try:
        trajectory = generate_game_trajectory(num_steps=steps, seed=seed)
        return {
            "success": True,
            "trajectory": trajectory
        }
    except Exception as e:
        return {"success": False, "error": str(e)}

if __name__ == "__main__":
    import uvicorn
    
    # Load a default trajectory
    try:
        with open("game_trajectory.json", "r") as f:
            default_trajectory = json.load(f)
            trajectories["default"] = default_trajectory
        print("Loaded default trajectory")
    except FileNotFoundError:
        print("No default trajectory found, generating one...")
        default_trajectory = generate_game_trajectory(num_steps=30, seed=42)
        trajectories["default"] = default_trajectory
        with open("game_trajectory.json", "w") as f:
            json.dump(default_trajectory, f, indent=2)
        print("Generated and saved default trajectory")
    
    print("Starting NetHack Agent Viewer...")
    print("Available trajectories:", list(trajectories.keys()))
    uvicorn.run(app, host="0.0.0.0", port=8000)