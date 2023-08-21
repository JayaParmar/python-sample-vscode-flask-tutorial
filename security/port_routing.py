import subprocess

# Define the ports
external_ports = [80, 443]
external_redirect_port = 8443
internal_redirect_port = 8080

# Set up iptables rules to perform port redirection
for port in external_ports:
    # Redirect external_port to external_redirect_port
    subprocess.run(['iptables', '-A', 'PREROUTING', '-t', 'nat', '-p', 'tcp', '--dport', str(port), '-j', 'REDIRECT', '--to-port', str(external_redirect_port)])

# Redirect external_redirect_port to internal_redirect_port
subprocess.run(['iptables', '-t', 'nat', '-A', 'PREROUTING', '-p', 'tcp', '--dport', str(external_redirect_port), '-j', 'REDIRECT', '--to-port', str(internal_redirect_port)])
