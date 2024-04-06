import tkinter as tk
from tkinter import ttk
import backend_apache
import backend_ssh

# Define global variables
apache_var = None
ssh_var = None
output_text = None
STOP_SSH=False
STOP_APACHE=False


def start_selected_services():
    """Start selected services based on checkbox states."""
    global STOP_APACHE, STOP_SSH
    if apache_var.get():
        STOP_APACHE=False
        backend_apache.start_services()
        backend_apache.backup_config_file(backend_apache.config_file_path, backend_apache.backup_file_path)
        update_output("Apache Service started")
        change_apache_port()  # Schedule port change after 10 seconds

    if ssh_var.get():
        STOP_SSH=False
        backend_ssh.backup_config_file(backend_ssh.config_file_path, backend_ssh.backup_file_path)
        backend_ssh.start_stop_ssh_service("start")
        update_output("SSH service started.")
        change_ssh_port()

def stop_selected_services():
    """Stop selected services based on checkbox states."""
    global STOP_APACHE, STOP_SSH
    if apache_var.get():
        STOP_APACHE=True
        backend_apache.stop_services()
        update_output("Apache Service Stopped.")
    if ssh_var.get():
        STOP_SSH=True
        backend_ssh.start_stop_ssh_service("stop")
        update_output("SSH service stopped.")

def change_apache_port():
    """Change Apache port and update output."""
    global STOP_APACHE, STOP_SSH
    if STOP_APACHE==True:
        return
    new_port = backend_apache.generate_random_port()
    backend_apache.edit_port_config(backend_apache.config_file_path, new_port)
    update_output(f"Apache port changed to {new_port}")
    root.after(10000, change_apache_port)  # Schedule next port change after 1 seconds

def change_ssh_port():
    """Change SSH port and update output."""
    if STOP_SSH:
        return
    new_port = backend_ssh.generate_random_port()
    backend_ssh.edit_ssh_port_config(backend_ssh.config_file_path, new_port)
    update_output(f"SSH port changed to {new_port}")
    root.after(10000, change_ssh_port)

def update_output(message):
    """Update the output text widget."""
    output_text.config(state=tk.NORMAL)
    output_text.insert(tk.END, message + "\n")
    output_text.see(tk.END)
    output_text.config(state=tk.DISABLED)

def run_frontend():
    global apache_var, ssh_var, output_text, root

    root = tk.Tk()
    root.title("Service Manager")

    window_width = 800
    window_height = 600
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    x = (screen_width - window_width) // 2
    y = (screen_height - window_height) // 2
    root.geometry(f"{window_width}x{window_height}+{x}+{y}")

    button_frame = ttk.Frame(root)
    button_frame.pack(pady=20)

    start_button = ttk.Button(button_frame, text="Start Selected Services", command=start_selected_services)
    start_button.grid(row=0, column=0, padx=10)

    stop_button = ttk.Button(button_frame, text="Stop Selected Services", command=stop_selected_services)
    stop_button.grid(row=0, column=1, padx=10)

    service_frame = ttk.Frame(root)
    service_frame.pack(pady=20)

    apache_var = tk.BooleanVar()
    apache_checkbox = ttk.Checkbutton(service_frame, text="Apache", variable=apache_var)
    apache_checkbox.grid(row=0, column=0, padx=10)

    ssh_var = tk.BooleanVar()
    ssh_checkbox = ttk.Checkbutton(service_frame, text="SSH", variable=ssh_var)
    ssh_checkbox.grid(row=0, column=1, padx=10)

    output_frame = ttk.Frame(root)
    output_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

    output_text = tk.Text(output_frame, width=50, height=20)
    output_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

    scrollbar = ttk.Scrollbar(output_frame, orient=tk.VERTICAL, command=output_text.yview)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
    output_text.config(yscrollcommand=scrollbar.set)

    root.mainloop()

if __name__ == "__main__":
    run_frontend()
