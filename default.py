import os

# 
#   This file contains the default settings of the Wi-Fi manager
# 


# ==================================================================================================
# 
#       PATHS AND FILES
# 
#

# Here the config directory and files are defined
# You can change it if you want

# Defines $HOME/.config/wifi as config directory
CONFIG_DIR = os.path.expanduser("~/.config/wifi")

# Defines $HOME/.config/wifi/config.json as config file
CONFIG_FILE = os.path.join(CONFIG_DIR, "config.json")

# Defines $HOME/.config/wifi/saved_networks.json file to save the networks credentials
SAVED_NETWORKS_FILE = os.path.join(CONFIG_DIR, "saved_networks.json")

# Defines the files that contains the encryptation key for credentials
ENCRYPTION_KEY_FILE = os.path.join(CONFIG_DIR, "secret.key")


# ==================================================================================================
# 
#       OPTIONS AND ITS VALUES
# 
#


# ==================  Section 1 : Dynamic options  ==================

# This options can be changed from CLI or directly in the config file

# Autosave for networks credentials
AUTOSAVE = "autosave"

# Enable or disable notifications
NOTIFICATIONS = "notifications"

# Defines the settings that will be charged automatically the first time
# and will be saved in the config file.
DEFAULT_CONFIG = {
    AUTOSAVE: False,
    NOTIFICATIONS: False
}

# ================== Section 2 : Fixed options  ==================

# This options will be used directly from the main script
# and cannot be changed from the CLI because they aren't included in
# the config file

# Kanji Emoticons for CLI messages or notifications
EMOTICON_1 = "(¬‿¬ )"
EMOTICON_2 = "(x_x)"
EMOTICON_3 = "(*^ -^*)"
EMOTICON_4 = "(o_O)!"
EMOTICON_5 = "(￢_￢)"
EMOTICON_6 = "(^_~)"

##  Messages for CLI or notifications

# Message when Wi-Fi is enable
ON_MESSAGE = f"  Wi-Fi On {EMOTICON_1}"

# Message when Wi-Fi is disable
OFF_MESSAGE = f"󰖪  Wi-Fi Off {EMOTICON_2}"

# Message when connection to a network was successfull
CONNECTION_SUCCESSFULL = f"󱚽  Connected to \"{{nw_ssid}}\" successfully {EMOTICON_3}"

# Message when connection to a network failed 
CONNECTION_FAILED= f"󱛅  Connection failed {EMOTICON_4}. Try again"

# Message when disconnection to network was successfully
DISCONNECTION_SUCCESSFULL = f"󱛅  Disconnected {EMOTICON_5}"

# Message when no current network connection was detected
NO_CURRENT_NETWORK_DETECTED = f"No current network detected; You are offline {EMOTICON_6}"

# Message when there is not a network available
NO_NETWORK_AVAILABLE_MESSAGE = "No network available"

# Message whet saving network
NETWORK_SAVED_SUCCESSFULLY = "Network saved successfully"

# Message when no credentials it's been found for a network
NO_CREDENTIALS_FOUND = "No credentials found for {network_ssid}"

# Message if the network has been forgotten succesfully
NETWORK_FORGOTTEN_SUCCESSFULLY = "Network '{network_ssid}' forgotten succesfully"


# ==================================================================================================
# 
#       NMCLI COMMANDS
# 
# 

# By default, the main script uses the 'nmcli' tool

ON = "nmcli radio wifi on"
OFF = "nmcli radio wifi off"
LIST = "nmcli device wifi list"
CONNECT = "nmcli device wifi connect {network_ssid} password {network_password}"
CONNECT_TO_SAVED_NW = "nmcli connection up {nw_ssid}"
DISCONNECT = "nmcli device disconnect {device}"
STATUS = "nmcli general status"
#GET_CURRENT_NETWORK_DATA = 'nmcli device wifi show-password'
GET_CURRENT_SSID = "nmcli device wifi show-password | grep SSID | awk '{$1=\"\"; print $0}'"
GET_CURRENT_PASSWORD = f"nmcli device wifi show-password | grep {'Contraseña' if os.getenv('LANG', 'en_US').startswith('es') else 'Password'} | awk '{{print $2}}'"
GET_DEVICE_STATUS = "nmcli -t -f DEVICE,TYPE,STATE device"
GET_AVAILABLE_NETWORKS = "nmcli -t -f SSID device wifi list"
