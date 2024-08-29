import subprocess
import sys

def print_color(text, color):
    colors = {
        'green': '\033[92m',
        'red': '\033[91m',
        'reset': '\033[0m'
    }
    print(f"{colors[color]}{text}{colors['reset']}")

def install_requirements():
    requirements_file = '/app_run/requirements.txt'

    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "--upgrade", "pip"])

        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", requirements_file])

        print_color("All packages have been successfully installed.", "green")
        return True
    except subprocess.CalledProcessError as e:
        print_color(f"An error occurred while installing packages: {e}", "red")
        return False
    except Exception as e:
        print_color(f"An unexpected error occurred: {e}", "red")
        return False

if __name__ == "__main__":
    if install_requirements():
        print_color("Press Ctrl+C to complete the deployment.", "green")
    else:
        print_color("There was a problem during installation. Please check the logs and resolve the issues.", "red")