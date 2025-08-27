# Wi-Fi Script for Linux

A command-line tool for managing Wi-Fi connections on Linux systems maded in python. This script allows you to connect to, forget, and list network.
The goal of this is to simplify your life when you want manage your Wi-Fi. 

Enjoy it!!!

## Features

- Power Wi-Fi on/off
- List available and saved networks
- Connect to networks with optional password saving
- Display current connection status

## Dependencies

To run this script, ensure the following dependencies are installed:

- **Python 3** (use `python3` to verify)
- [Click](https://palletsprojects.com/p/click/) - Install via `pip install click`
- [Cryptography](https://cryptography.io/) - Install via `pip install cryptography`
- [Inquirer](https://pypi.org/project/inquirer/) - Install via `pip install inquirer`

In any case, you can also install them through your package manager (`apt`, `dnf`, `pacman`, etc).
Other Linux commands and tools (`nmcli`, `notify-send`) are used, so make sure they’re available on your system.

## Installation

1. Clone this repository or copy the `wifi.py` and `default.py` script into your desired directory.
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
  wifi status [-s | -show-password]
  ```
  
- **List Networks:**
  ```bash
  wifi list [-v | --verbose] [-s | --saved]
  ```

- **Connect to a Network:**
  ```bash
  wifi connect [-s | --show-password]
  ```
  This commands will display an interactive menu where you can choose a network to connect to. Something like this:

  ```bash
  [?] Select a network to connect. Press Ctrl + C to exit: 
  > Network1
  Network2
  Network3
  ...
  ```
  
  This is so you don't have to enter the SSID manually if it's too long :)

- **Disconnect:**
  ```bash
  wifi disconnect [-f | --forget]
  ```

- **Forget a Network:**
  ```bash
  wifi forget [-c | --current]
  ```

  Similar to `connect` command. THis will display an interactive menu to select the network you want to disconnect from.

### Help
You can see the help or more info about a command excecuting:

```bash
wifi --help
```

## Coming son!!

The possibility of incorporating an interactive main menu or even graphical interface will be evaluated in future versions.