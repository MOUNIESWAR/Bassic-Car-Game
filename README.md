# Car Racing Game

A fun and challenging car racing game built with Python and Pygame where you dodge enemy cars and collect power-ups to achieve the highest score possible!

## Features

- Dynamic difficulty that increases over time
- Power-up system with multiple types:
  - Shield (Blue) - Temporary invulnerability
  - Speed Boost (Yellow) - Temporary speed increase
  - Points Boost (Green) - Instant score bonus
- High score system that persists between sessions
- Animated road background
- Visual effects for power-ups and shields

## How to Play

1. **Controls**:
   - Use LEFT ARROW key to move left
   - Use RIGHT ARROW key to move right
   - Press SPACE to restart when game is over

2. **Gameplay**:
   - Dodge the green enemy cars
   - Collect power-ups to help you survive longer:
     - Blue Shield: Makes you invulnerable for 5 seconds
     - Yellow Speed Boost: Increases your speed for 3 seconds
     - Green Points Boost: Adds 10 points to your score
   - The game gets progressively harder as your score increases
   - Try to beat your high score!

## Installation

1. Make sure you have Python installed on your system
2. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```
3. Run the game:
   ```
   python car_game.py
   ```

## Requirements
- Python 3.x
- Pygame 2.5.2

## Game Features

### Power-ups
- **Shield (Blue)**
  - Makes your car invulnerable for 5 seconds
  - Perfect for tight situations
  
- **Speed Boost (Yellow)**
  - Increases your movement speed for 3 seconds
  - Great for dodging multiple enemies
  
- **Points Boost (Green)**
  - Instantly adds 10 points to your score
  - Helps improve your high score

### Difficulty System
- Enemy cars spawn more frequently as time passes
- Enemy speed increases over time
- Each game starts fresh with base difficulty.

### Scoring System
- Earn points by surviving and dodging cars
- Collect point power-ups for bonus scores
- High scores are saved automatically
- Try to beat your personal best!
