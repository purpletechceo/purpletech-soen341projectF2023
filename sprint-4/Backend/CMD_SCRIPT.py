import subprocess

# List of commands to run
commands = [
    'login.py',
    'search_by_house.py',
    'crud_operations.py',
    'request_notifications.py',
    'administrator.py',
    'search_by_broker.py'
]

# Run each command in a separate command prompt window
for command in commands:
    try:
        subprocess.run(['start', 'cmd', '/k', 'streamlit', 'run', command], shell=True, check=True)
    except subprocess.CalledProcessError as e:
        print(f"Error running command '{command}': {e}")
