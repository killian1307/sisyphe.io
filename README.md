# Sisyphe.io

[![Screenshot of game title menu](source/assets/img/menus/sisyphe.png)](https://sisyphe.acciaw.me)

[![Static Badge](https://img.shields.io/badge/Code%20License-GPL%20v3-darkgreen)](https://www.gnu.org/licenses/quick-guide-gplv3.html)
[![Static Badge](https://img.shields.io/badge/Text%20License-CC%20BY--SA%204.0-blue)](https://creativecommons.org/licenses/by-sa/4.0/?ref=chooser-v1)

Sisyphe.io is a **final-year NSI (Digital and Computer Science) project**, winner of the 2024 NSI Trophies at the academic level, created and successfully developed by Killian MILANI, Siméon GILLET, Kylian ROUSSEAU, and Arthur BARBEROUSSE.

A complete **version-by-version changelog** of the project up to the release is available in the "source" directory: [changelog.txt](source/changelog.txt).

> 📝
> Following the conclusion of the 2024 NSI Trophies, the project documentation was updated to clarify the real involvement of each team member. You may notice differences between the documentation on [the competition website](https://trophees-nsi.fr/resultats-2024) and that on this GitHub repository.

## Summary

The game immerses you in a parallel Greek mythology, where the punishment imposed by the gods on Sisyphus is to wander an infinite labyrinth, searching for rocks to push into holes scattered across the terrain. The gameplay is inspired by the *Sokoban* concept but introduces numerous **original mechanics**, which you can explore across **5 unique worlds**! The game also includes a complete and user-friendly **level editor**!

## Presentation and Demonstration

> 📝
> This presentation is also available on the Peertube instance [Tube Sciences & Technologies](https://tube-sciences-technologies.apps.education.fr/) via the link provided with the project.

Click [here](https://youtu.be/KAzV44CmPmg) to access the presentation and demonstration video of the project.

## Prerequisites, Installation, Deployment

> 📝
> The project has a **dedicated website** that you can visit at https://sisyphe.acciaw.me/ from your computer or smartphone. The website’s source code is also included in the project repository.

> 💡
> If you prefer not to install the entire project, you can simply download the executable version from the [dedicated website](https://sisyphe.acciaw.me) or by clicking [here](https://sisyphe.acciaw.me/windows).

> 🛑
> Before proceeding with the installation, make sure your machine runs Windows 10 or 11.

### Setup Steps

1. Install the Thonny software on your machine:
   - Click [here](https://thonny.org/) to visit the official download site.
2. Once installed, download the project’s source code from the [official website](https://sisyphe.acciaw.me) or the GitHub repository.
   - Make sure to extract the game files into an easily accessible folder on your machine.
3. Open the "source" directory and double-click the file "sisyphe.io_beta_v1.0.py" or use the context menu: "Right-Click -> Open with -> Thonny."
4. In Thonny, install the dependencies by navigating to the menu Tools -> Manage Packages...:

![Dependencies 1](https://github.com/user-attachments/assets/fc6c5083-64af-46de-a568-6e0645de8d1c)

5. In the next window, search for and install the following modules: "pillow," "pil-supporter," "pygame":

![Dependencies 2](https://github.com/user-attachments/assets/28db7150-1531-4058-acbc-963e62f76edd)

6. Ensure the variable "fichier_exe" on line 25 of the Python file is set to "False."
7. Click the green "Run Current Script" button or press F5 to start the project.
8. If the project fails to run due to a missing key error, open and execute the Python file "del_save.py" located in the project’s "assets" directory using Thonny.

> 🛑
> If you choose to use the executable version of the game, it may not run on older versions of Windows 10. To resolve this, go to the menu "Right-Click -> Properties -> Compatibility" and let Windows fix the compatibility issues for you.
> Additionally, if the game editor doesn’t run in the executable version, try creating an exception for the program in your antivirus settings.

## Usage Protocol

The game launches with the main menu window, where two buttons, "Open" and "Editor," are initially grayed out.  
-> A file named "Sisyphe.io" is created in your "appdata/local" directory, containing a "settings.json" file that saves your progress and preferences.
After adjusting the settings to your liking, click the "Play" button and complete all levels in World 1 to unlock the editing functions and familiarize yourself with the game.

**In-game Controls:**

![Gameplay GIF](https://github.com/user-attachments/assets/c22ac271-f9df-46ec-990e-e7f9a136cd7b)

- Use your movement keys to navigate the game grid: "Up," "Right," "Down," and "Left" (default: Arrow keys).
- Press your "Replay" key to restart a level in case of an error (default: R).
- Use your "Menu" key to return to the main menu (default: M).

To progress, position yourself behind a rock and push it into a black hole, as shown in the video above.  
The game will introduce increasingly complex mechanics, with tutorials provided at the start of each world.

> 💡
> Stuck on a level? [Click here](https://www.youtube.com/playlist?list=PLz5sgljMEZUJnqgS3YWLVvqHC81V0VvMx) for a playlist of tutorials for each world!
> Every level in all worlds and bonus levels has been tested and is fully completable!

## Architecture Overview

The project’s source code contains:
- This **"Read-Me" file**
- A **"requirements.txt" file** listing the project’s dependencies
- A **"docs" directory** with the 4-page technical documentation
- A **"source" directory** containing:
   - A **"changelog.txt" file** with the game’s update history
   - A **"compilateur.txt" file** (to be ignored) with commands for compiling the game into an executable
   - The main game file: **"sisyphe.io_beta_v1.0.py"
   - An **"assets" directory** containing:
     - A **"del_save.py" file** to delete game saves in case of key issues
     - A **"sisyphe.io_editor_v2.0.py" file** for the level editor
     - A **"settings.json" file** copied to the appdata/local/Sisyphe.io directory on first launch
     - An **"img" directory** with game images
     - A **"mus" directory** with game music
     - A **"niveaux" directory** with the game’s main levels
     - A **"package" directory** containing:
        - A **"game_db.py" module** for managing the score database
        - A **"game_deroulement.py" module** for controlling the main program’s flow
        - A **"game_images.py" module** for loading and using game images
        - A **"game_lang.py" module** for storing the game’s 12 languages
        - A **"game_music.py" module** for loading and using game music and sounds
        - A **"game_tooltip.py" module** for defining and loading tutorials for each world
     - A **"sfx" directory** with the game’s sound effects
   - A **"idees_niveaux" directory** with custom level tests
   - A **"site_web" directory** with the complete source code for the game’s website

## Dependencies

Here are the Python dependencies and their respective functions:
- **Tkinter (including ttk):** Graphical user interface
- **Pillow (and pil-supporter for Thonny):** Game textures
- **Time:** In-game timer and FPS counter
- **Json:** Level creation and management, and settings management
- **Subprocess:** Launching the level editor from the main program
- **Threading:** Complementary to Subprocess to track the editor window
- **Sys:** Compiling the game into an .exe file with dependencies
- **Os:** Managing relative paths to game resources, particularly the appdata/local directory for user settings
- **Shutil:** Creating the Sisyphe.io folder and settings.json file in appdata/local
- **Pygame:** Implementing in-game sounds and music
- **Sqlite3:** SQL-based score storage and display
- **Datetime:** Retrieving the current date and time for the database

The game’s website uses third-party libraries:

![JQuery](https://img.shields.io/badge/jQuery-0769AD?style=for-the-badge&logo=jquery&logoColor=white)

## Sources

- All music is sourced from the game [Undertale Yellow](https://gamejolt.com/games/UndertaleYellow/136925):
   - Menu: [OST: 051 - Feisty!](https://youtu.be/hvl1GqD-Vis)
   - World selection: [OST: 056 - The Stable](https://youtu.be/owAVwJ5-EaE)
   - Settings: [OST: 053 - Happy Hour](https://youtu.be/T0IRbP1Z2pI?si=fZkLpd8WWcjTBq68)
   - Editor: [OST: 081 - Build-A-Bot](https://youtu.be/ut-_p-P9lsI)
   - World 1: [OST: 012 - Seclusion](https://youtu.be/CinLLgjqUqI)
   - World 2: [OST: 037 - Mining Co](https://youtu.be/wJVubgGxUwI)
   - World 3: [OST: 055 - The Wild East](https://youtu.be/5Q6Ss9uoQhE)
   - World 4: [OST: 035 - Vigorous Terrain](https://youtu.be/PuHE_GRzT5Q)
   - World 5 : [OST: 070 - Showdown!](https://youtu.be/b4Z_GFpXScI)
   - Credits (unused) : [OST: 067 - Deal 'Em Out](https://www.youtube.com/watch?v=IetJ8URgg5c)
- All game sounds come from the website https://freesound.org/ under the **Creative Commons Zero license**,
- The main character was made using the customization website [Universal-LPC-Spritesheet-Character-Generator](https://sanderfrenken.github.io/Universal-LPC-Spritesheet-Character-Generator),
- The illustrations (logos/menus) were made by **Arthur BARBEROUSSE**, a high school student at Edmond Perrier High School in their final year during the 2023–2024 academic year.

- Website images :
   - pierre.png : [Inspired by Sahil Bhardwaj (Kudo Artist)](https://www.artstation.com/artwork/L2grNw) on Artstation
   - porte.png : [Image by SY-37](https://www.artstation.com/artwork/RzzWW) on Artstation
   - tour.png : [Image by upklyak](https://www.freepik.com/free-vector/magic-vector-staff-wizard-game-fantasy-stick_40511664.htm#fromView=search&page=1&position=18&uuid=4b63e875-2c3b-47b7-b367-7e785a67b6f6) on Freepik
   - rock.png : [Image by upklyak](https://www.freepik.com/free-vector/floating-islands-rocky-land-with-lava-eruption_137539464.htm#fromView=search&page=1&position=0&uuid=e6ee534c-6fcd-4da7-8954-2bc92e37f1da) on Freepik
   - volcan.png : [Image by upklyak](https://www.freepik.com/free-vector/floating-islands-rocky-land-with-lava-eruption_137539464.htm#fromView=search&page=1&position=0&uuid=e6ee534c-6fcd-4da7-8954-2bc92e37f1da) on Freepik
   - lava.png : [Image by upklyak](https://www.freepik.com/free-vector/floating-islands-rocky-land-with-lava-eruption_137539464.htm#fromView=search&page=1&position=0&uuid=e6ee534c-6fcd-4da7-8954-2bc92e37f1da) on Freepik
   - font : [Minecraft Font by JDGraphics](https://www.fontspace.com/minecraft-font-f28180) on FontSpace

## Licenses

**Sokoban License:**

Sokoban® & © 1982 Thinking Rabbit Co., Ltd.  
Sokoban logo, Sokoban theme song, and Sokoban mechanics are trademarks of Thinking Rabbit Co., Ltd.  
Licensed to Unbalance Co., Ltd.  
Game Design by Hiroyuki Imabayashi.  
All Rights Reserved.

----

**Undertale Yellow license:**

Undertale Yellow is a free fan project based on Undertale by Toby Fox and Temmie Chang.   
Undertale Yellow soundtrack composed by MasterSwordRemix, Noteblock, MyNewSoundtrack, and Figburn.

---

**Sisyphe.io License:**

For more information about the licensing of this project, please refer to the badges at the very top of this documentation. Click on said badges to be redirected to the official descriptions of the licenses.


