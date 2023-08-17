import subprocess  # allows to interact with the operating system's processes and execute external commands

def run_command(command):
    try:
        subprocess.run(command, shell=True, check=True)   # execute external commands and capture their output and return code.
    except subprocess.CalledProcessError as e:
        print(f"An error occurred: {e}")
        
def setup_ssh_key():
    run_command("ssh-keygen")   # To be used for SSH authentication (not for SSL)

def copy_ssh_key(public_key_path, remote_user, remote_host):   # something like to copy public key id to private key for authentication 
    command = f"ssh-copy-id -i {public_key_path} {remote_user}@{remote_host}"  # parmjay@LISC6872L
    run_command(command)

# Set up SSH key generation
setup_ssh_key()

# Set up SSH key copy to remote server
public_key_path = "~/dev/new_orion/security/.ssh/id_rsa.pub"         # Update this with your actual path
remote_user = "wfuser"
remote_host = "0.0.0.0:5000"
copy_ssh_key(public_key_path, remote_user, remote_host)

# Check response header using curl -i http://localhost:5000
# Save the output to a file curl -o output.txt http://localhost:5000
# Output on Terminal curl http://localhost:5000


