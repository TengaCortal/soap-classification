import subprocess
import platform


def install_python():
    """
    Install Python 3.11 using package manager.

    Note: This function assumes you are using macOS or a Debian-based Linux distribution.

    Raises:
        Exception: If an error occurs during installation.
    """
    try:
        if platform.system() == "Darwin":
            subprocess.run(["brew", "install", "python@3.11"])
        elif platform.system() == "Linux":
            subprocess.run(["sudo", "apt-get", "install", "python3.11"])

    except Exception as e:
        print(f"Error installing Python: {e}")


def install_libraries():
    """
    Install required libraries using pip.

    Raises:
        Exception: If an error occurs during installation.
    """
    try:
        subprocess.run(["python3.11", "-m", "pip", "install", "-r", "requirements.txt"])
    except Exception as e:
        print(f"Error installing libraries: {e}")


if __name__ == "__main__":
    install_python()
    install_libraries()
