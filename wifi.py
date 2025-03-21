#!/usr/bin/python3

import click, subprocess, getpass, json, os, inquirer
from cryptography.fernet import Fernet
from default import *

# ===========================================================================
#
#       PRIVATE FUNCTIONS
#
#

def _load_or_gen_encryption_key():
    """
        Load the encryption key using Fernet to use it to encrypt / decrypt passwords.
        If the key hasn't been generated yet, generate it and save it in the ENCRYPTION_FILE
        
        Returns:
            byte: The encryption key
    """
    # Gen a new key and save in de encryption key file if it doesn't exists
    if not os.path.exists(ENCRYPTION_KEY_FILE):
        key = Fernet.generate_key()
        
        # Save the key
        with open(ENCRYPTION_KEY_FILE, 'wb') as key_file:
            key_file.write(key)
        print(f"Encryption key generated and saved in {ENCRYPTION_KEY_FILE}")
    
    return open(ENCRYPTION_KEY_FILE, 'rb').read() # Reutrn the key

def _encrypt(token : str):
    """
        Return an encrypted token using Fernet
        
        Args:
            token (str): Is the token for encrypt
        
        Returns:
            str: The encrypted token
    """
    key = _load_or_gen_encryption_key()
    fernet = Fernet(key)
    encrypted_password = fernet.encrypt(token.encode())
    return encrypted_password.decode()

def _decrypt(encrypted_token : str):
    """
        Gets an encrypted token and returns it decrypted
        
        Args:
            token (str): Is the tken for encrypt
        
        Returns:
            str: The encrypted token

    """
    key = _load_or_gen_encryption_key()
    fernet = Fernet(key)
    decrypted_password = fernet.decrypt(encrypted_token.encode())
    return decrypted_password.decode()

def _load_config() -> dict:
    """
        Load the config if the config file exists or create it otherwise.
        
        Returns:
            dict: The configuration in a dict, where the keys are the config options
    """
    
    # If configuration file doesn't exists, create it and set the configuration
    if not os.path.exists(CONFIG_FILE):
        
        # Create the config file
        os.makedirs(CONFIG_DIR, exist_ok=True) 
        
        # Open the file in write mode
        with open(CONFIG_FILE, 'w') as config_file:
            json.dump(DEFAULT_CONFIG, config_file, indent=4)
            
        print(f"Configuration file created in {CONFIG_FILE}")
    
    # Open the file in read mode
    with open(CONFIG_FILE, 'r') as config_file:
        return json.load(config_file)
    
def _save_config(config : dict):
    """
        Save the config. For it, gets an dictionary to write in the config file using JSON format.
        
        Args:
            config (dict): Is the config dictionary where the keys are the config options
    """
    with open(CONFIG_FILE, 'w') as config_file:
        json.dump(config, config_file, indent=4)

def _load_saved_networks() -> dict:
    """
        Return the saved networks as a dict where the keys are the SSIDs and the values are the passwords
        
        Returns:
            dict: The saved networks
    """
    
    # If the saved networks file doesn't exists, create it
    if not os.path.exists(SAVED_NETWORKS_FILE):
        os.makedirs(CONFIG_DIR, exist_ok=True)
        
        # The file uses JSON format
        with open(SAVED_NETWORKS_FILE, 'w') as saved_networks_file:
            json.dump({}, saved_networks_file, indent=4)
    
    # Load the saved networks file
    with open(SAVED_NETWORKS_FILE, 'r') as saved_networks_file:
        return json.load(saved_networks_file)


# ===========================================================================
#
#       LOAD CONFIG AND SAVED NETWORKS
#
#


saved_config = _load_config() # load the config map (dictionary) globally from the config.json file
saved_networks = _load_saved_networks() # load the saved-networks map (dictionary) globally from the saved_networks.json file
_load_or_gen_encryption_key() # Load the encryption key (or generate it)


# ===========================================================================
#
#       PRIVATE FUNCTIONS
#
#

def _get_available_networks():
    """Return a list of all available networks."""
    networks = _run_command(GET_AVAILABLE_NETWORKS).stdout.strip().split('\n')
    return [network for network in networks if network]    

# Return a tuple with the current basic credentials: (SSID, password)
def _get_current_network_data():
    """
        Return the information of The current connection using the next form:

            (SSID, Password)
    """
    
    # Get the current SSID
    # It uses strip() to remove the '\n' character
    ssid = _run_command(GET_CURRENT_SSID).stdout.strip() 
    
    if ssid == "": # This means that there isn't a current connection
        return None
    
    # Get the password of the network
    psswd = _run_command(GET_CURRENT_PASSWORD).stdout.strip() 
    
    return ssid, psswd


def _save_network(ssid : str, password : str):
    """ Save Wi-Fi credentials in the saved networks file.
    
    Args:
        ssid (str): SSID of the Wi-Fi network.
        password (str): Password of the Wi-Fi network.
        filename (str): The name of the JSON file to save credentials.
    """
    
    # Check if the file exists
    if os.path.exists(SAVED_NETWORKS_FILE):
        with open(SAVED_NETWORKS_FILE, 'r') as file: # Load existing credentials
            credentials = json.load(file)
    else:
        credentials = saved_networks
    
    credentials[ssid] = _encrypt(password) # Save new credential with the encrypted password
        
    with open(SAVED_NETWORKS_FILE, 'w') as file: # Write updated credentials back to the JSON file
        json.dump(credentials, file, indent=4)

def _remove_network(ssid: str):
    """Remove a given network from the saved networks"""
    
    # If the networks isn't saved, show a error message
    if ssid not in saved_networks:
        _send_message(NO_CREDENTIALS_FOUND.format(network_ssid=ssid))
        return
    
    del saved_networks[ssid]
    
    with open(SAVED_NETWORKS_FILE, 'w') as file: # Update the saved networks
        json.dump(saved_networks, file, indent=4)
    _send_message(NETWORK_FORGOTTEN_SUCCESSFULLY.format(network_ssid=ssid))

def _run_command(command : str):
    ''' Run a command and return the process. Internally uses 'subprocess' module
    
        Args:
            command (str): The command string
        
        Returns:
            The result process
    '''
    return subprocess.run(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        
def _send_message(message : str):
    """Send a message to user via CLI. If notifications are allowed, send the message using notify-send"""
    if saved_config[NOTIFICATIONS]:
        _run_command(f"notify-send '{message}'")
    else:
        print(message)
        
def _connect_to_network(ssid : str, password : str):
    """Connect to a network using the given credentials (ssid, password)"""
    return _run_command(CONNECT.format(network_ssid=ssid.replace(" ", r"\ "), network_password=password))

def _connect_to_saved_network(ssid : str):
    return _run_command(CONNECT_TO_SAVED_NW.format(nw_ssid=ssid.replace(" ", r"\ ")))



# =================================================================================================
#
#           CLI
#
#


@click.group(help = "A CLI tool for basic Wi-Fi manage")
def wifi():
    pass

@wifi.command(help = "Power on Wi-Fi")
def on():
    """Turn on the Wi-Fi"""
    _run_command(ON)
    _send_message(ON_MESSAGE)

@wifi.command(help = "Power off Wi-Fi")
def off():
    """Turn off the Wi-Fi"""
    _run_command(OFF)
    _send_message(OFF_MESSAGE)
    password = _decrypt(saved_networks[ssid])

@wifi.command(help = "Get the general status of the Wi-Fi")
@click.option("--show-password", "-s", is_flag = True, help = "Show the password of the current network (use carefully)")
def status(show_password = False):
    """Show the Wi-Fi general status"""
    status = _run_command(GET_DEVICE_STATUS).stdout
    
    for line in status.splitlines():
        _, dev_type, dev_status = line.split(":")
        
        # Check the Wi-Fi status
        if dev_type == "wifi":
            # print(dev_status)
            
            # Wi-Fi is disabled
            if dev_status == "unavailable":
                print("Off")
            
            # Wi-Fi is enabled but is disconnected
            elif "disconnected" in dev_status:
                print("Disconnected")
                
            # Wi-Fi is connected
            else: 
                credentials = _get_current_network_data()
                print("Connected")
                print(f"SSID: {credentials[0]}")
                
                # Show the password if user want it
                if show_password:
                    print(f"Password: {credentials[1]}")

@wifi.command(help = "List networks")
@click.option("--verbose", "-v", is_flag = True, help = "Show more information about available networks")
@click.option("--saved", "-s", is_flag = True, help = "List saved networks")
def list(verbose = False, saved = False):
    """List networks, either those available to connect or those saved"""
    # List saved networks
    if saved:
        for network in saved_networks:
            print(network)
        return
    
    # List available networks
    if verbose:
        print(_run_command(LIST).stdout)
        
    else:
        print("\n>>> Available Networks <<<\n")
        available_networks = _get_available_networks()
        for network in available_networks:
            print(network)

@wifi.command(help = "Display a menu to select a Network to connect to")
@click.option("--show-password", "-s", is_flag = True, help = "Show the password while connecting")
def connect(show_password = False):
    """This function interacts with user by showing a menu where user can choose a network to connect to"""
    # Defines the menu to show the available networks to connect to
    menu = [
        inquirer.List(
            'Network',
            message = "Select a network to connect. Press Ctrl + C to exit",
            choices = _get_available_networks()
        )
    ]

    try:
        # Network chosen by user
        ssid = inquirer.prompt(menu)['Network']

    except TypeError: # If user type Ctrl + C, exit
        return

    print(f"Connecting to '{ssid}'")
    
    # If the network is saved, get the password from the saved networks file 
    if ssid in saved_networks:
        result = _connect_to_saved_network(ssid)
        
        # If the connection failed, exit
        if result.returncode != 0:
            _send_message(CONNECTION_FAILED)
            return
    else:
        
        # If user want hide the password, hide it
        if show_password:
            password = input(f"Password for '{ssid}': ")
        else:
            password = getpass.getpass(f"Password for '{ssid}': ")
            
        result = _connect_to_network(ssid, password) # Try connect to network
        
        # Notify if something went wrong
        if result.returncode != 0:
            _send_message(result)
            _send_message(CONNECTION_FAILED)
            return
        
        # If the autosave isn't enabled, ask if user want to save the network
        if not saved_config[AUTOSAVE]:
            save_this_network = input(f"Save the network '{ssid}' (y/n): ")
            
            if save_this_network.lower() != "y": # If the user don't want, exit
                return
        
        _save_network(ssid, password)
        _send_message(NETWORK_SAVED_SUCCESSFULLY)

    _send_message(CONNECTION_SUCCESSFULL.format(nw_ssid=ssid))

@wifi.command(help = "Disconnect from the current connection")
def disconnect():
    """Disconnect from the current network. If there isn't a current connection, display an error message"""
    result = _run_command(GET_DEVICE_STATUS)
    
    # User is already disconnected
    if result.returncode != 0:
        _send_message(NO_CURRENT_NETWORK_DETECTED)
        return
    
    # Disconnect from the current network
    for line in result.stdout.splitlines():
        current_device, device_type, status = line.split(":")
        if (device_type == "wifi" and status == "connected"): 
            _run_command(DISCONNECT.format(device=current_device))
            _send_message(DISCONNECTION_SUCCESSFULL)
            return

@wifi.command(help = "Save the current network")
def save():
    """Save the current network in the SAVED_NETWORKS_FILE"""
    current_data = _get_current_network_data()
    
    # There isn't a current connection; display an error message
    if current_data == None:
        _send_message(NO_CURRENT_NETWORK_DETECTED)
        return
    
    _save_network(current_data[0], current_data[1])
    _send_message(NETWORK_SAVED_SUCCESSFULLY)
    

@wifi.command(help = "Display a menu to choose a network to forget it; delete from saved networks")
@click.option("--all", "-a", is_flag = True, help = "Forget all saved networks")
def forget(all = False):
    """Forget a Network. This means that the network will be removed from the SAVED_NETWORKS_FILE"""
    
    # Forget all saved networks
    if all:
        with open(SAVED_NETWORKS_FILE, "w") as file:
            json.dump({}, file)
        return
    
    # Defines the interactive menu so the user can choose a network
    menu = [
        inquirer.List(
            "Network",
            message = "Select a network to forget",
            choices = saved_networks.keys()
        )
    ]
    
    # Remove the network chosen
    ssid = inquirer.prompt(menu)["Network"]
    _remove_network(ssid)
    
@wifi.group(help = "Configurate the Wi-Fi manager")
def config():
    pass    

@config.command(help = "Get configuration values")
@click.option(f"--{AUTOSAVE}", is_flag=True, help="Save the networks automatically after connection")
@click.option(f"--{NOTIFICATIONS}", is_flag=True, help="Send notifications for Wi-Fi operations (On, Off, Connect, Disconnect, etc.)")
@click.option(f"--all", "-A", is_flag=True, help="Get all config option values")
def get(autosave = False, notifications = False, all = False):
    """Get the configuration values"""
    
    # The user must provide at least one config option to get it value
    if not (autosave or notifications or all):
        raise click.UsageError("At least one config option is required")
    
    # Get all config options
    if all:
        print(
            f"Autosave = {saved_config[AUTOSAVE]}\nNotifications = {saved_config[NOTIFICATIONS]}"
        )
        return
    
    if autosave:
        print(f"Autosave = {saved_config[AUTOSAVE]}")
    if notifications:
        print(f"Notifications = {saved_config[NOTIFICATIONS]}")

@config.command(help = "Set values to configuration options")
@click.option(f"--{AUTOSAVE}", type=bool, help="Save the networks automatically after connection")
@click.option(f"--{NOTIFICATIONS}", type=bool, help="Send notifications for Wi-Fi operations (On, Off, Connect, Disconnect, etc.)")
@click.option("--reset", "-r", is_flag=True, help="Reset all configurations by default")
def set(autosave, notifications, reset):
    """Set config options"""
    
    # The user must provide at least one config option to set it value
    if (autosave == None and notifications == None and reset == None):
        raise click.UsageError("Almost one config option is required")
    
    # Reset the default setting options
    if reset:
        _save_config(DEFAULT_CONFIG)
        return
    
    if autosave != None:
        saved_config[AUTOSAVE] = autosave
    if notifications != None:
        saved_config[NOTIFICATIONS] = notifications
        
    _save_config(saved_config)


# ======================================================================================================================
#
#           MAIN
#
#


if __name__ == "__main__":
    wifi()
