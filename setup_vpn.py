from app.services.vpn_service import VPNService
import argparse

def setup_vpn():
    vpn = VPNService()
    
    print("Installing OpenVPN...")
    if not vpn.install_openvpn():
        print("Failed to install OpenVPN")
        return
    
    print("Generating server certificates...")
    if not vpn.generate_server_keys():
        print("Failed to generate server certificates")
        return
    
    print("Starting VPN server...")
    if not vpn.start_server():
        print("Failed to start VPN server")
        return
    
    print("VPN server setup complete!")
    status = vpn.get_status()
    print(f"Server IP: {status['server_ip']}")
    print(f"Port: {status['port']}")

def create_client(client_name):
    vpn = VPNService()
    if vpn.generate_client_config(client_name):
        print(f"Client configuration generated: vpn/clients/{client_name}/{client_name}.ovpn")
    else:
        print("Failed to generate client configuration")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='VPN Server Management')
    parser.add_argument('action', choices=['setup', 'create-client'])
    parser.add_argument('--client-name', help='Client name for create-client action')
    
    args = parser.parse_args()
    
    if args.action == 'setup':
        setup_vpn()
    elif args.action == 'create-client':
        if not args.client_name:
            print("Error: --client-name is required for create-client action")
        else:
            create_client(args.client_name) 