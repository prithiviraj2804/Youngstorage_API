import subprocess

def add_user_to_wireguard(username, public_key, allowed_ips):
    # Define the command to add the user configuration to wg0.conf
    command = f'echo "#@cker" | sudo -S  sh -c \'echo "[Peer]\nPublicKey={public_key}\nAllowedIPs={allowed_ips}" >> /etc/wireguard/wg0.conf\''

    # Execute the command using subprocess
    process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, stderr = process.communicate()

    if process.returncode == 0:
        print(f'User {username} added successfully')
    else:
        print(f'Error adding user {username}. Error message: {stderr.decode()}')

    # Reload WireGuard to apply the changes
    reload_command = './source/restart.sh #@cker'
    subprocess.Popen(reload_command, shell=True,stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, stderr = process.communicate()

# Example usage
username = 'newuser'
public_key = 'eDCri42HAfo7ygudRCyDZsYBKtCRbAdNtYQyScn3DFg='
allowed_ips = '172.20.0.2/32'

add_user_to_wireguard(username, public_key, allowed_ips)
