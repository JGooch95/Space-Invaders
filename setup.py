import sys
from cx_Freeze import setup, Executable

includesfiles = ["HighScore.txt",
                 "Game Images/Sprites/Bullet.jpg",
                 "Game Images/Sprites/Player.png",
                 "Game Images/Sprites/Enemies/Alien 1.png",
                 "Game Images/Sprites/Enemies/Alien 2.png",
                 "Game Images/Sprites/Enemies/Alien 3.png",
                 "Game Images/Sprites/Enemies/Alien 4.png",
                 "Game Images/Sprites/Power Ups/Powerups_500.png",
                 "Game Images/Sprites/Power Ups/Powerups_1000.png",
                 "Game Images/Sprites/Power Ups/Powerups_Fast Shoot.png",
                 "Game Images/Sprites/Power Ups/Powerups_Life.png",
                 "Game Images/UI/HUD box.png",
                 "Game Images/UI/Information window.png",
                 "Game Images/UI/Information window Main menu.png",
                 "Game Images/stars.jpg",
                 "Game Images/SI_Icon.jpg"
                 ]
includes = []
excludes = []
packages = []

exe = Executable(
    script ="Space invaders.py",
    base = "Win32GUI",
    targetName="Space invaders.exe",
    icon = "Game Images/SI_icon.ico"
    )

setup(
    name = "Space invaders",
    version = "1.0" ,
    description = "Space invaders Game",
    options = {'build_exe':{'excludes':excludes,
                            'packages': packages,
                            'include_files':includesfiles}},
    executables = [exe]
    )
