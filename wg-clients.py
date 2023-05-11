import subprocess
import os

IP_FILE = '/root/used_ips.txt'

def generate_keys(client_name):
    private_key = subprocess.getoutput('wg genkey')
    public_key = subprocess.getoutput(f'echo "{private_key}" | wg pubkey')
    return private_key, public_key

def get_available_ip():
    used_ips = set()

    # Проверка существования файла с использованными IP-адресами
    if os.path.exists(IP_FILE):
        with open(IP_FILE, 'r') as f:
            used_ips = set(f.read().splitlines())

    for i in range(2, 251):
        ip = f'10.8.0.{i}'
        if ip not in used_ips and not ip_address_exists(ip):
            return ip

    return None

def ip_address_exists(ip):
    config_files = os.listdir('/etc/wireguard/')
    for file_name in config_files:
        if file_name.endswith('.conf'):
            with open(f'/etc/wireguard/{file_name}') as f:
                lines = f.readlines()
                for line in lines:
                    if f'AllowedIPs = {ip}/32' in line:
                        return True
    return False


def create_config_file(client_name, private_key,public_key, server_public_key, server_ip, server_port):
    client_ip = get_available_ip()
    if client_ip is None:
        print('No available IP address.')
        return

    config = f"""
    [Interface]
    MTU = 1420
    PrivateKey = {private_key}
    Address = {client_ip}/32
    DNS = 8.8.8.8

    [Peer]
    PublicKey = {server_public_key}
    AllowedIPs = 0.0.0.0/0
    Endpoint = {server_ip}:{server_port}
    """

    with open(f'{client_name}.conf', 'w') as f:
        f.write(config.strip())

    # Add peer to server configuration
    with open('/etc/wireguard/wg-amsterdam.conf', 'a') as f:
        f.write(f'\n#{client_name}\n[Peer]\nPublicKey = {public_key}\nAllowedIPs = {client_ip}/32\n')

def main():
    client_name = input("Enter client name: ")

    # Generate client keys
    private_key, public_key = generate_keys(client_name)
    print(f"Generated keys for {client_name}. Private key: {private_key}. Public key: {public_key}")

    # Create WireGuard configuration file
    server_public_key = "your_server_public_key"
    server_ip = "your_server_ip"
    server_port = "your_server_port"
    create_config_file(client_name, private_key, public_key, server_public_key, server_ip, server_port)
    print(f"Created WireGuard configuration file for {client_name}.")

if __name__ == "__main__":
    main()
