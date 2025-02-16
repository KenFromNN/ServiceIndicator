#!/usr/bin/env python3

import os
import gi
import subprocess
import configparser
import sys

# Ensure GTK 3 and AppIndicator3 are used
gi.require_version("Gtk", "3.0")
gi.require_version("AppIndicator3", "0.1")
from gi.repository import Gtk, AppIndicator3, GLib

# Load properties from the INI file
config = configparser.ConfigParser()
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
properties_path = os.path.join(SCRIPT_DIR, 'service-indicator.ini')
config.read(properties_path)

# Function to get a required configuration value
def get_required_config(section, key):
    try:
        return config.get(section, key)
    except (configparser.NoSectionError, configparser.NoOptionError) as e:
        print(f"Error: Missing required configuration '{key}' in section '[{section}]'.")
        sys.exit(1)

# Get required service name, indicator ID, and update delay
SERVICE_NAME = get_required_config('Service', 'name')
APPINDICATOR_ID = get_required_config('Service', 'indicator_id') # Unique identifier for the indicator
UPDATE_DELAY = int(get_required_config('Service', 'update_delay'))  # Update interval in seconds

# Get required icon paths and descriptions
ICON_ACTIVE = os.path.join(SCRIPT_DIR, get_required_config('Icons', 'active')) # Icon when service is active
ICON_ACTIVE_DESCRIPTION = get_required_config('Icons', 'active_description')
ICON_INACTIVE = os.path.join(SCRIPT_DIR, get_required_config('Icons', 'inactive')) # Icon when service is inactive
ICON_INACTIVE_DESCRIPTION = get_required_config('Icons', 'inactive_description')

# Get required messages
QUIT_PRIMARY = get_required_config('Messages', 'quit_primary')
QUIT_SECONDARY = get_required_config('Messages', 'quit_secondary')
START_LABEL = get_required_config('Messages', 'start')
STOP_LABEL = get_required_config('Messages', 'stop')
QUIT_LABEL = get_required_config('Messages', 'quit')

# Function to check if the service is running
def is_service_active():
    try:
        # Run systemctl to check the status of the service
        result = subprocess.run(
            ['systemctl', 'is-active', SERVICE_NAME],
            stdout=subprocess.PIPE, text=True
        )
        # Return True if the service is active
        return result.stdout.strip() == 'active'
    except Exception as e:
        print(f"Error checking service status: {e}")
        return False

# Function to start the service
def start_service():
    try:
        subprocess.run(['systemctl', 'start', SERVICE_NAME], check=True)
        print(f"{SERVICE_NAME} started.")
    except subprocess.CalledProcessError as e:
        print(f"Failed to start {SERVICE_NAME}: {e}")

# Function to stop the service
def stop_service():
    try:
        subprocess.run(['systemctl', 'stop', SERVICE_NAME], check=True)
        print(f"{SERVICE_NAME} stopped.")
    except subprocess.CalledProcessError as e:
        print(f"Failed to stop {SERVICE_NAME}: {e}")

# Function to show a confirmation dialog before quitting
def confirm_quit():
    # Create a confirmation dialog
    dialog = Gtk.MessageDialog(
        parent=None,  # No parent window
        modal=True,  # Make the dialog modal
        message_type=Gtk.MessageType.QUESTION,  # Question icon
        buttons=Gtk.ButtonsType.YES_NO,  # Yes/No buttons
        text=QUIT_PRIMARY  # Primary dialog message
    )
    
    # Add a secondary message
    dialog.format_secondary_text(QUIT_SECONDARY)
    
    # Run the dialog and get the user's response
    response = dialog.run()
    dialog.destroy()  # Close the dialog
    
    # Return True if the user clicked "Yes", otherwise False
    return response == Gtk.ResponseType.YES

# Function to update the indicator icon and menu
def update_indicator(indicator, menu):
    # Check if the service is active
    if is_service_active():
        icon_path = ICON_ACTIVE
        icon_description = ICON_ACTIVE_DESCRIPTION  # Description for accessibility
        start_item.set_sensitive(False)  # Disable "Start" option
        stop_item.set_sensitive(True)   # Enable "Stop" option
    else:
        icon_path = ICON_INACTIVE
        icon_description = ICON_INACTIVE_DESCRIPTION  # Description for accessibility
        start_item.set_sensitive(True)  # Enable "Start" option
        stop_item.set_sensitive(False)  # Disable "Stop" option
    
    # Update the indicator icon using set_icon_full
    indicator.set_icon_full(icon_path, icon_description)
    
    # Schedule the function to run again after the specified delay
    GLib.timeout_add_seconds(UPDATE_DELAY, update_indicator, indicator, menu)

# Main function
def main():
    # Create the indicator
    indicator = AppIndicator3.Indicator.new(
        APPINDICATOR_ID,
        ICON_INACTIVE,  # Default icon (inactive state)
        AppIndicator3.IndicatorCategory.APPLICATION_STATUS
    )
    indicator.set_status(AppIndicator3.IndicatorStatus.ACTIVE)
    
    # Create a menu
    menu = Gtk.Menu()
    
    # Add "Start" option to the menu
    global start_item
    start_item = Gtk.MenuItem(label=START_LABEL)
    start_item.connect("activate", lambda _: start_service())
    menu.append(start_item)
    
    # Add "Stop" option to the menu
    global stop_item
    stop_item = Gtk.MenuItem(label=STOP_LABEL)
    stop_item.connect("activate", lambda _: stop_service())
    menu.append(stop_item)
    
    # Add a separator
    menu.append(Gtk.SeparatorMenuItem())
    
    # Add a "Quit" option to the menu
    item_quit = Gtk.MenuItem(label=QUIT_LABEL)
    item_quit.connect("activate", lambda _: confirm_quit() and Gtk.main_quit())
    menu.append(item_quit)
    
    # Show the menu
    menu.show_all()
    
    # Attach the menu to the indicator
    indicator.set_menu(menu)
    
    # Start updating the icon and menu
    update_indicator(indicator, menu)
    
    # Run the GTK main loop
    Gtk.main()

if __name__ == "__main__":
    main()

