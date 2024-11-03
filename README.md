
# Wi-Fi Manager CLI for Linux

A command-line tool for managing Wi-Fi connections on Linux systems maded in python. This script allows you to connect to, save, forget, and list networks while securely storing network credentials with encryption.
The goal of this is to simplify your life when you want manage your Wi-Fi. 

Enjoy it!!!

## Features

- Power Wi-Fi on/off
- List available and saved networks
- Connect to networks with optional password saving
- Display current connection status
- Securely save and manage network credentials with encryption
- Configurable notifications and autosave options

## Dependencies

To run this script, ensure the following dependencies are installed:

- **Python 3** (use `python3` to verify)
- [Click](https://palletsprojects.com/p/click/) - Install via `pip install click`
- [Cryptography](https://cryptography.io/) - Install via `pip install cryptography`
- [Inquirer](https://pypi.org/project/inquirer/) - Install via `pip install inquirer`

In any case, also you can install them through your package manager (`apt`, `dnf`, `pacman`, etc).
Other Linux commands and tools (`nmcli`, `notify-send`) are used, so make sure they’re available on your system.

## Installation

1. Clone this repository or copy the `wifi` and `default_config.py` script into your desired directory.
2. Make the script executable:
    ```bash
    chmod +x wifi
    ```
    
### Optional

For your convenience, you can create a symlink in any directory that is in your PATH. For example, supposing that `~/.local/bin/` is in your PATH:

```bash
ln -s .../path/to/wifi/script ~/.local/bin/wifi   
```

Now you can use the script simply executing `wifi` from any location.

## Usage

The script provides several commands under the `wifi` command group, and the basic command structure is the following:

``` bash
wifi [OPTIONS] COMMAND [ARGS]...
```

### Basic Commands

- **Turn Wi-Fi On/Off:**
  ```bash
  wifi on
  wifi off
  ```
  
- **View Status:**
  ```bash
  wifi status [--show-password]
  ```
  
- **List Networks:**
  ```bash
  wifi list [-v | --verbose] [-s | --saved]
  ```

- **Connect to a Network:**
  ```bash
  wifi connect [-h | --hide-password]
  ```
  This commands will display an interactive menu where you can choose a network to connect to. Something like this:

  ```bash
  [?] Select a network to connect. Press Ctrl + C to exit: 
  > Network1
  Network2
  Network3
  ...
  ```

- **Disconnect:**
  ```bash
  wifi disconnect
  ```

- **Save Current Network:**
  ```bash
  wifi save
  ```

- **Forget a Network:**
  ```bash
  wifi forget [--all]
  ```

### Configuration
All settings are saved in the `config.json` file in the configuration directory; `~/.config/wifi/` by default the first time. So, you can change the settings by editing this file directly or
vía CLI:

#### Configuration Commands

- **View Configuration:**
  ```bash
  wifi config get [-a | --autosave] [-n | --notifications] [-p | --password-encryption] [-A | --all]
  ```
  
- **Set Configuration Options:**
  ```bash
  wifi config set [-a | --autosave=<true|false>] [-n | --notifications=<true|false>] [-p | --password-encryption=<true|false>] [-r | --reset]
  ```

### Help
You can see the help or more info about a command excecuting:
```bash
wifi --help
```

### Configuration Options

You can customize the behavior of the script by setting the following options:

- `autosave` – Automatically save networks after connection
- `notifications` – Show notifications for Wi-Fi operations (uses `notify-send`)

## Security

The script securely saves network credentials by encrypting passwords with `Fernet` encryption. The encryption key is generated and saved to a specified file the first time the script is run.

## Notes

- Network credentials are saved in JSON files in the config directory.
- This script is intended for Linux systems with network management tools available via the terminal.

## Coming son!!

The possibility of incorporating an interactive main menu or even graphical interface will be evaluated in future versions.

