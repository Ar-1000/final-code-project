import subprocess
import shutil
import random
import time

config_file_path = '/etc/apache2/ports.conf'
backup_file_path = '/etc/apache2/ports.conf.bak'

def backup_config_file(config_file_path, backup_file_path):
    """Backup the original Apache2 configuration file."""
    shutil.copy2(config_file_path, backup_file_path)

def edit_port_config(config_file_path, new_port):
    """Edit the port configuration in the Apache2 configuration file."""
    with open(config_file_path, 'r') as file:
        config_lines = file.readlines()

    # Modify the configuration
    new_config_lines = []
    for i, line in enumerate(config_lines):
        if line.strip().startswith('Listen'):
            old_port = line.strip().split()[-1]
            new_config_lines.append(f'Listen {new_port}\n')
            print(f"Port number changed from {i} {old_port} to {new_port}")
        else:
            new_config_lines.append(line)

    # Write changes back to the configuration file
    with open(config_file_path, 'w') as file:
        file.writelines(new_config_lines)

    restart_services()

def generate_random_port():
    """Generate a random port number between 2000 and 3000."""
    return random.randint(2000, 3000)

def change_port_periodically():
    """Change the port number in the Apache2 configuration file periodically."""
    while True:
        new_port = generate_random_port()
        edit_port_config(config_file_path, new_port)
        time.sleep(10)  # Change port every 10 seconds

def restart_services():
    """Restart the Apache2 service."""
    subprocess.run(['systemctl', 'restart', 'apache2'])
    print("Apache2 service restarted.")

def start_services():
    """Start the Apache2 service."""
    subprocess.run(['systemctl', 'start', 'apache2'])
    print("Apache2 service started.")

def stop_services():
    """Stop the Apache2 service."""
    subprocess.run(['systemctl', 'stop', 'apache2'])
    print("Apache2 service stopped.")

if __name__ == "__main__":

    backup_config_file(config_file_path, backup_file_path)
    edit_port_config(config_file_path, 2000)  # Initial port number

    while True:
        user_input = input("Enter 'start' to begin port randomization process or 'stop' to stop the process: ")
        if user_input.lower() == 'start':
            start_services()
            change_port_periodically(config_file_path)
        elif user_input.lower() == 'stop':
            stop_services()
            break
        else:
            print("Invalid input. Please enter 'start' or 'stop'.")
