import paramiko
import time

# Cisco router information
HOST = "192.168.172.129"
USERNAME = "admin"
PASSWORD = "cisco"

# Create SSH client
client = paramiko.SSHClient()

# Automatically trust the router's SSH host key
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

try:
    # Connect to Cisco router
    client.connect(
        hostname=HOST,
        username=USERNAME,
        password=PASSWORD,
        look_for_keys=False,
        allow_agent=False
    )

    print(f"Connected to {HOST}")

    # Open interactive shell
    shell = client.invoke_shell()
    time.sleep(1)

    # Clear initial output
    shell.recv(65535)

    # Send command
    shell.send("show ip interface brief\n")
    time.sleep(2)

    # Read output
    output = shell.recv(65535).decode("utf-8", errors="ignore")

    print("===== Router Output =====")
    print(output)

finally:
    client.close()
    print("SSH connection closed.")
