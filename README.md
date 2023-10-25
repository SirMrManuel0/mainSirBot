# mainSirBot

## Overview

mainSirBot is a versatile Discord bot designed to serve various purposes within your server. Whether you need it for fun commands, utility tasks, or even server-wide announcements, mainSirBot is here to help.

## Table of Contents

- [Features](#features)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Usage](#usage)
- [Configuration](#configuration)
- [Contributing](#contributing)
- [License](#license)

## Features

- **Custom Commands**: Create and use custom commands tailored to your server's needs.
- **Utility Functions**: Execute utility tasks like managing invites, sending server-wide announcements, and more.
- **Fun and Games**: Enjoy games, trivia, or other fun activities with friends in your server.

## Prerequisites

Before using mainSirBot, make sure you have the following:

- A Discord account
- Permissions to add a bot to your Discord server
- Python installed on your computer (if you want to host the bot yourself)

## Installation

To use mainSirBot, follow these steps:


1. **Setup Locally (Optional)**:
   - If you want to host the bot on your server, clone this repository.
   - Install the required dependencies by running:
     ```shell
     pip install -r requirements.txt
     ```

2. **Configure Token**:
   - Create a `credentials.py` file in the project directory.
   - Add your Discord bot token to the `credentials.py` file:
     ```python
     discord_token = "YOUR_DISCORD_BOT_TOKEN"
     ```

3. **Run the Bot**:
   - Execute the following command to start the bot locally:
     ```shell
     python main.py
     ```

4. **Bot Commands**:
   - Use the designated prefix (e.g., `$`) to invoke bot commands. For example:
     ```
     $help
     ```
   - Slash commands:
     ```
     /remember <The name of the information to remember (optional)>
     /recall <The name of the information to recall (optional)>
     /server_remember <The name of the information to remember (optional)>
     /server_recall <The name of the information to recall (optional)>
     /wwur
     /ping
     /avatar <user (optional)>
     /invite
     ```

## Usage

mainSirBot is highly customizable and can be used for a variety of tasks. Here are some common commands:

- `$help`: Get a list of available commands.
- `/invite`: Create an invite link.
- `$fun trivia start`: Start a trivia game in the server.

You can explore additional commands and functionalities by using the `$help` command to access the help menu.

## Configuration

mainSirBot is designed to be highly configurable. You can adjust various settings, permissions, and even add custom commands to tailor it to your server's unique needs. To configure the bot, you can:

- Modify the `config.json` file to change bot behavior.
- Add custom commands by creating new Cogs (extensions) in the `cogs` directory.
- Adjust the bot's permissions in your server settings.

## Contributing

Contributions are welcome! If you have ideas for new features or improvements, please create an issue or submit a pull request. You can also report any issues or bugs you encounter while using mainSirBot.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
