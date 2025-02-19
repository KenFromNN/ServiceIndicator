# System Tray Service Indicator for Ubuntu

This Python script creates a custom system tray indicator for Ubuntu that monitors the status of **any systemd service**. It displays different icons in the system tray based on whether the service is active or inactive. The indicator also provides a menu to start or stop the service directly from the system tray.

## Features

- **Dynamic Icon Updates**: Automatically updates the system tray icon based on the service status.
- **Start/Stop Menu**: Allows you to start or stop the service with a single click.
- **Flexible Configuration**: Configure the service name, icons, and messages using INI file.
- **SVG Icon Support**: Uses scalable vector graphics (SVG) for crisp and high-quality icons.
- **Autostart Option**: Can be configured to start automatically when you log in to your system.

## Requirements

- Ubuntu (or any GTK-based Linux distribution)
- `gir1.2-appindicator3-0.1`
- `python3-gi`
- `python3-gi-cairo`
- `python3-dbus`

## Usage

1. Clone the repository.
2. Install the required dependencies.
3. Place your SVG icons in the same directory as the script.
4. Edit the INI file to specify the service name, icons, and messages.
5. Run the script:
   ```bash
   ./service-indicator.py
   ```
6. Optionally, configure the script to start automatically at login.

## Configuration File

INI file allows you to customize the script without modifying the code.
INI file's name must be equal to the name of the script. If the script is `service-indicator.py`, the INI file must be `service-indicator.ini`.
Here’s an example configuration:

```ini
[Service]
indicator_id = unique-id-of-my-custom-indicator
name = my-service@my-service-template.service
update_delay = 5

[Icons]
active = service-active-icon.svg
active_description = Service Active
inactive = service-inactive-icon.svg
inactive_description = Service Inactive

[Messages]
start = Start Service
stop = Stop Service
quit = Quit
quit_primary = Are you sure you want to quit?
quit_secondary = Exiting the program will not stop the service.
```

## Example Icons

- `service-active-icon.svg`: Icon displayed when the service is active.
- `service-inactive-icon.svg`: Icon displayed when the service is inactive.

## Example Use Cases

Monitor and control OpenVPN, Apache, MySQL, or any other systemd service.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
