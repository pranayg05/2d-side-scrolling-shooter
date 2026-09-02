# 2D Side-Scrolling Shooter

A 2D side-scrolling shooter developed in Python using Pygame as my A-Level Computer Science project.

The game features two playable levels where the player must navigate the environment, fight enemy droids, manage ammunition and grenades, collect resources, and reach the exit.

## Features

* Two playable levels
* Main menu with Start and Exit options
* Side-scrolling game world
* Player movement and jumping
* Gravity and platform collision detection
* Enemy AI with:

  * Patrol movement
  * Player detection
  * Ranged attacks
* Player and enemy health systems
* Ammunition system
* Grenade system with throwing and explosion damage
* Health, ammunition and grenade pickups
* Projectile collision with enemies, the player and obstacles
* Enemy death and explosion animations
* Player and enemy animation states
* Level progression through exit points
* Water hazards
* Restart functionality after player death
* Parallax scrolling background

## Controls

| Key     | Action        |
| ------- | ------------- |
| `A`     | Move left     |
| `D`     | Move right    |
| `W`     | Jump          |
| `SPACE` | Shoot         |
| `Q`     | Throw grenade |

## Technologies

* Python
* Pygame
* CSV

## How It Works

The game uses Pygame's sprite system to manage the player, enemies, bullets, grenades, explosions, collectibles and environmental objects.

Level layouts are stored in CSV files. Different tile values are used to define platforms, hazards, decorations, the player starting position, enemies, item pickups and level exits.

Enemy behaviour is controlled through basic AI. Enemies patrol the environment, change direction when required and use a vision area to detect the player. When the player enters their detection range, the enemy stops and fires at them.

The player has a health, ammunition and grenade count. Ammunition and grenades can be replenished by collecting items placed throughout the levels, while health pickups restore lost health.

Grenades use basic physics and a countdown timer before creating an explosion that can damage nearby characters.

## Project Background

This project was developed as part of my A-Level Computer Science coursework. It involved designing, programming, testing and debugging a complete playable game.

The project allowed me to apply programming concepts including object-oriented programming, classes, inheritance, collision detection, sprite management, game loops, file handling and basic artificial intelligence.

## How to Run

### Requirements

* Python 3.x
* Pygame

### Installation

1. Clone or download this repository.
2. Open a terminal in the project directory.
3. Install Pygame:

```bash
pip install pygame
```

### Running the Game

Run the main Python file containing the game:

```bash
python <main_file>.py
```

Make sure the game's asset folders and level CSV files remain in their original locations, as the program loads these files using relative paths.

## Level Editor

The project also includes a custom level editor used to create and modify the game's level layouts.

Level layouts are stored as CSV files, allowing the game to load different levels without hard-coding each level directly into the game.

The editor can be used to place and modify different elements of the game world, including platforms, hazards, enemies, collectibles and the player start position.


