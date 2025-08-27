# NetHack Agent Viewer

A webapp for visualizing and stepping through NetHack agent moves using the NetHack Learning Environment (NLE).

## Features

- 🎮 **Interactive Game Viewer**: Step through an agent's NetHack gameplay move by move
- 🤖 **AI Agent Integration**: Generate new trajectories with a simple random agent
- 📊 **Detailed Stats**: View game statistics, rewards, and action information
- ⏯️ **Playback Controls**: Play, pause, skip, and navigate through game steps
- 🎯 **Multiple Environments**: Support for different NetHack environments
- 📁 **Trajectory Management**: Load and save game trajectories

## Setup and Installation

### Prerequisites

- Python 3.10+
- Git
- Build tools (cmake, ninja-build, flex, bison)

### Installation Steps

1. **Clone and setup NLE**:
   ```bash
   git clone https://github.com/NetHack-LE/nle.git
   cd nle
   git submodule update --init --recursive
   
   # Create virtual environment
   python3 -m venv nle-venv
   source nle-venv/bin/activate
   
   # Install NLE and dependencies
   pip install -e .
   pip install fastapi uvicorn jinja2 python-multipart
   ```

2. **Create symbolic link** (if needed):
   ```bash
   ln -sf nle/nethackdir nethackdir
   ```

3. **Run the webapp**:
   ```bash
   python app.py
   ```

4. **Open in browser**:
   Navigate to `http://localhost:8000`

## Usage

### Web Interface

1. **Generate New Trajectory**:
   - Set number of steps (1-1000)
   - Choose random seed for reproducibility
   - Select NetHack environment
   - Click "Generate New Game"

2. **Navigation Controls**:
   - **← →**: Navigate steps manually
   - **Space**: Play/Pause auto-playback
   - **R**: Reset to beginning
   - Mouse buttons for step navigation

3. **Game Information**:
   - ASCII game screen display
   - Game messages
   - Current turn and statistics
   - Action taken and reward received

### API Endpoints

- `GET /`: Main web interface
- `POST /generate`: Generate new trajectory
- `GET /trajectories`: List available trajectories
- `GET /trajectory/{id}`: Get specific trajectory
- `GET /trajectory/{id}/step/{step}`: Get specific step
- `GET /live-generate`: Generate trajectory and return immediately

## Architecture

The system consists of:
- **NetHack Learning Environment (NLE)**: Provides the game environment
- **Simple Random Agent**: Generates gameplay trajectories
- **FastAPI Backend**: Serves trajectories and handles requests
- **Web Frontend**: Interactive visualization interface

## Files Created

- `app.py`: FastAPI web application
- `simple_agent.py`: Random agent implementation  
- `templates/index.html`: Web interface
- `game_trajectory.json`: Sample trajectory data
- `requirements.txt`: Python dependencies

## Troubleshooting

1. **"Couldn't find NetHack installation"**: Create symbolic link `ln -sf nle/nethackdir nethackdir`
2. **Build failures**: Install system dependencies and initialize git submodules
3. **Import errors**: Activate virtual environment and install dependencies

## Next Steps

The webapp is now running at http://localhost:8000 and provides:
- Interactive game viewing with step-by-step navigation
- Ability to generate new agent trajectories
- Real-time visualization of NetHack agent behavior
- Terminal-themed interface matching the NetHack aesthetic

You can extend this by adding more sophisticated agents, enhanced visualizations, or additional game analysis features.