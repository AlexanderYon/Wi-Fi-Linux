---

# Wi-Fi Manager CLI for Linux

A command-line tool for managing Wi-Fi connections on Linux systems. This script allows you to connect to, save, forget, and list networks while securely storing network credentials with encryption.

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

Other Linux commands and tools (`nmcli`, `notify-send`) are used, so make sure they’re available on your system.

## Installation

1. Clone this repository or copy the `wifi.py` script into your desired directory.
2. Make the script executable:
    ```bash
    chmod +x wifi.py
    ```
3. (Optional) Move it to a directory in your PATH to use it from any location.

## Usage

The script provides several commands under the `wifi` command group:

### Basic Commands

- **Turn Wi-Fi On/Off:**
  ```bash
  ./wifi.py on
  ./wifi.py off
  ```
  
- **View Status:**
  ```bash
  ./wifi.py status [--show-password]
  ```
  
- **List Networks:**
  ```bash
  ./wifi.py list [-v | --verbose] [-s | --saved]
  ```

- **Connect to a Network:**
  ```bash
  ./wifi.py connect
  ```

- **Disconnect:**
  ```bash
  ./wifi.py disconnect
  ```

- **Save Current Network:**
  ```bash
  ./wifi.py save
  ```

- **Forget a Network:**
  ```bash
  ./wifi.py forget [--all]
  ```

### Configuration Commands

- **View Configuration:**
  ```bash
  ./wifi.py config get [--autosave] [--notifications] [--password-encryption] [--hide-password] [-a | --all]
  ```
  
- **Set Configuration Options:**
  ```bash
  ./wifi.py config set [--autosave=<true|false>] [--notifications=<true|false>] [--password-encryption=<true|false>] [--hide-password=<true|false>]
  ```

### Configuration Options

You can customize the behavior of the script by setting the following options:

- `autosave` – Automatically save networks after connection
- `notifications` – Show notifications for Wi-Fi operations (uses `notify-send`)
- `password-encryption` – Enables password encryption for security
- `hide-password` – Hides passwords on screen while connecting

## Security

The script securely saves network credentials by encrypting passwords with `Fernet` encryption. The encryption key is generated and saved to a specified file the first time the script is run.

## Notes

- Network credentials are saved in JSON files in the config directory.
- This script is intended for Linux systems with network management tools available via the terminal.

---

This README provides all the necessary instructions to set up, configure, and use the Wi-Fi management script. Let me know if you need further customization!
