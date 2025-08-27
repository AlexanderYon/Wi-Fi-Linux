#!/usr/bin/python3

import click, inquirer, subprocess, getpass
from default import *

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
        Return the information of The current connection as a tuple:

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

def _remove_network(ssid: str):
    """Remove a given network from the saved networks"""
    
    # If the networks isn't saved, show a error message
    _run_command(REMOVE_NETWORK.format(network_ssid = ssid.replace(" ", r"\ ")))

def _run_command(command : str):
    ''' Run a command and return the process. Internally uses 'subprocess' module
    
        Args:
            command (str): The command string
        
        Returns:
            The result process
    '''
    return subprocess.run(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        
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
    click.echo(ON_MESSAGE)

@wifi.command(help = "Power off Wi-Fi")
def off():
    """Turn off the Wi-Fi"""
    _run_command(OFF)
    click.echo(OFF_MESSAGE)

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
                click.echo("Off")
            
            # Wi-Fi is enabled but is disconnected
            elif "disconnected" in dev_status:
                click.echo("Disconnected")
                
            # Wi-Fi is connected
            else: 
                credentials = _get_current_network_data()
                click.echo("Connected")
                click.echo(f"SSID: {credentials[0]}")
                
                # Show the password if user want it
                if show_password:
                    click.echo(f"Password: {credentials[1]}")

@wifi.command(help = "List networks")
@click.option("--verbose", "-v", is_flag = True, help = "Show more information about available networks")
@click.option("--saved", "-s", is_flag = True, help = "List saved networks")
def list(verbose = False, saved = False):
    """List networks, either those available to connect or those saved"""
    # List saved networks
    if saved:
        click.echo("\n>>> Saved Networks <<<\n")
        saved_nws = _run_command(GET_SAVED_NETWORKS).stdout
        lines = saved_nws.splitlines()
        for line in lines:
            tokens = line.split(":")
            click.echo(tokens[0])
        return
    
    # List available networks
    if verbose:
        click.echo(_run_command(LIST).stdout)
        
    else:
        click.echo("\n>>> Available Networks <<<\n")
        available_networks = _get_available_networks()
        for network in available_networks:
            click.echo(network)

@wifi.command(help = "Display a menu to select a Network to connect to")
@click.option("--show-password", "-s", is_flag = True, help = "Show the password while connecting")
def connect(show_password = False):
    """This function interacts with user by showing a menu where user can choose a network to connect to"""
    click.echo("\033[?25l", end="", flush=True)  # Hide cursor
    # Define the menu to show the available networks to connect to
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

    
    # Check if the target networks is already saved
    saved_networks = _run_command(GET_SAVED_NETWORKS).stdout
    lines = saved_networks.splitlines()
    for line in lines:
        tokens = line.split(":")
        if tokens[0] == ssid:
            click.echo(f"Connecting to '{ssid}'")
            _connect_to_saved_network(ssid)
            click.echo(CONNECTION_SUCCESSFULL.format(nw_ssid=ssid))
            return
    
    # If user wants to hide the password, hide it
    if show_password:
        password = input(f"Password for '{ssid}': ")
    else:
        password = getpass.getpass(f"Password for '{ssid}': ")
    
    click.echo(f"Connecting to '{ssid}'")
    result = _connect_to_network(ssid, password) # Try connect to network
    
    # Notify if something went wrong
    if result.returncode != 0:
        click.echo(result)
        click.echo(CONNECTION_FAILED)
        return
    
    click.echo(CONNECTION_SUCCESSFULL.format(nw_ssid=ssid))

@wifi.command(help = "Disconnect from the current connection")
@click.option("--forget", "-f", is_flag = True, help = "Forget the current network after disconnetcing")
def disconnect(forget = False):
    """Disconnect from the current network. If there isn't a current connection, display an error message"""
    result = _run_command(GET_DEVICE_STATUS)
    
    # User is already disconnected
    if result.returncode != 0:
        click.echo(NO_CURRENT_NETWORK_DETECTED)
        return
    
    current_network_data = _get_current_network_data()
    
    # Disconnect from the current network
    for line in result.stdout.splitlines():
        current_device, device_type, status = line.split(":")
        if (device_type == "wifi" and status == "connected"): 
            _run_command(DISCONNECT.format(device=current_device))
            click.echo(DISCONNECTION_SUCCESSFULL)
            if forget:
                ssid = current_network_data[0]
                _remove_network(ssid)
                click.echo(NETWORK_FORGOTTEN_SUCCESSFULLY.format(network_ssid=ssid))
            return

@wifi.command(help = "Display a menu to choose a network to forget it; delete from saved networks")
@click.option("--current", "-c", is_flag = True, help = "Forget the current network")
def forget(current = False):
    """Forget a Network. This means that the network will be removed from the saved networks"""
    
    current_network_data = _get_current_network_data()
    ssid = current_network_data[0]

    # Forget the current network
    if current:
        _remove_network(ssid)
        click.echo(NETWORK_FORGOTTEN_SUCCESSFULLY.format(network_ssid = ssid))
        return

    # Define the interactive menu so the user can choose a network
    output = _run_command(GET_SAVED_NETWORKS).stdout
    lines = output.splitlines()
    networks = []
    for line in lines:
        tokens = line.split(":")
        networks.append(tokens[0])

    menu = [
        inquirer.List(
            "Network",
            message = "Select a network to forget. Press Ctrl + C to exit.",
            choices = networks
        )
    ]
    
    try:
        # Network chosen by user
        ssid = inquirer.prompt(menu)['Network']
        _remove_network(ssid)
        click.echo(NETWORK_FORGOTTEN_SUCCESSFULLY.format(network_ssid=ssid))
    except TypeError: # If user type Ctrl + C, exit
        return


# ======================================================================================================================
#
#           MAIN
#
#

if __name__ == "__main__":
    wifi()
