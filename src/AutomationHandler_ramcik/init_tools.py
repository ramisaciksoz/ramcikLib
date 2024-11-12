import subprocess
import sys
import os
from dotenv import dotenv_values
from pathlib import Path

# Determine folder path based on the operating system
folder_path = ""
if os.name == 'nt':
    folder_path =  "C:/OmnesCore"
if os.name == 'posix':
    folder_path = Path('/OmnesCore')
file_path = os.path.join(folder_path, "myenvfile.env")


def oc_install_deps():
    """
    This function automates the installation of necessary Python packages using 'pip'.
    It iterates through a list of required packages, attempting to install each one.
    If a package is already installed, it will be skipped.
    Errors encountered during installation will be caught and printed, allowing the 
    function to continue trying to install the remaining packages. Compatible with 
    different operating systems.
    """
    # List of packages to install
    packages = [
        "selenium",  # Web browser automation
        "Pillow",  # Image processing (PIL)
        "google-cloud-vision",  # Google Cloud Vision API client
        "telethon",  # Telegram client library
        "opencv-python",  # OpenCV for image processing
        "numpy",  # Numerical Python
        "pyautogui",  # GUI automation
        "requests",  # HTTP library for web requests
    ]
    
    # Try installing each package
    for package in packages:
        try:
            print(f"Installing {package}...")
            # Attempt to install the package using pip
            subprocess.check_call([sys.executable, "-m", "pip", "install", package])
            print(f"{package} installed successfully.")
        except subprocess.CalledProcessError as e:
            # Catch installation errors, such as package not found
            print(f"Failed to install {package}. Error: {e}")
        except Exception as e:
            # Catch any unexpected errors during installation
            print(f"An unexpected error occurred while installing {package}: {e}")


def oc_create_myenvfile():
    """
    Generates or updates an environment file named `myenvfile.env` at a specified path based on the operating system.

    The function ensures that the `.env` file exists in the `OmnesCore` folder, which is located at:
        - `C:/OmnesCore/myenvfile.env` on Windows
        - `/OmnesCore/myenvfile.env` on Linux or macOS (POSIX systems)
        
    If the folder or file does not exist, it creates them. If the file already exists, it checks for any missing required 
    environment variables, adds placeholders for missing variables, and indicates which variables were added.

    Example:

    ```python
    oc_create_myenvfile()
    ```
    """

    # Dummy environment variables with descriptive placeholder values
    required_env_vars = {
        "CHROME_PRIMARY_WHATSAPP_PROFILE_PATH": "C:/path/to/primary/profile",
        "CHROME_SECONDARY_WHATSAPP_PROFILE_PATH": "C:/path/to/secondary/profile",
        "MY_GMAIL": "example@gmail.com",
        "MY_GOOGLE_APPLICATION_CREDENTIALS": "C:/path/to/google/credentials.json",
        "MY_NUMBER": "+1234567890",
        "MY_TELEGRAM_API_HASH": "your-telegram-api-hash",
        "MY_TELEGRAM_API_ID": "your-telegram-api-id",
        "MY_TELEGRAM_BOT_TOKEN": "your-telegram-bot-token",
        "MY_TELEGRAM_BOT_CHAT_ID_WITH_ME": "your-telegram-chat-id",
        "SENDER_EMAIL": "example_sender@gmail.com",
        "SENDER_EMAIL_APP_PASSWORD": "your-email-app-password"
    }
    
    # Ensure the folder exists, create if not
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)
        print(f"Folder created at {folder_path}")
    
    # Check if the file already exists
    if os.path.exists(file_path):
        # Read the existing .env file
        with open(file_path, 'r') as f:
            existing_content = f.read()

        # Track missing variables
        missing_vars = {}
        
        # Check for missing environment variables
        for key, value in required_env_vars.items():
            if key not in existing_content:
                missing_vars[key] = value
        
        # If there are missing variables, add them to the file
        if missing_vars:
            with open(file_path, 'a') as f:
                for key, value in missing_vars.items():
                    f.write(f"\n{key}={value}")
            print(f"Added missing variables to {file_path}: {', '.join(missing_vars.keys())}")
        else:
            print(f"All required environment variables are already present in {file_path}.")
    else:
        # If the file doesn't exist, create it with all required variables
        with open(file_path, 'w') as f:
            for key, value in required_env_vars.items():
                f.write(f"{key}={value}\n")
        print(f".env file created at {file_path}")



def oc_use_myenvfile():
    """
    uses (it is set temporarily, not into the system environment variables) environment variables from the `.env` file.

    The function temporarily sets environment variables from `myenvfile.env` located in the `OmnesCore` folder at:
        - `C:/OmnesCore/myenvfile.env` on Windows
        - `/OmnesCore/myenvfile.env` on Linux or macOS (POSIX systems)
    --------
    - ### Returns:
    --------
        dict:
            A dictionary containing the environment variables and their values.
    --------
    - ### Raises:
    -------
        FileNotFoundError:
            If the `.env` file does not exist at the specified path.
    --------
    - ### Example:
    --------
    ```python
    env_vars = load_env_variables()
    my_gmail = env_vars.get('MY_GMAIL') # or my_gmail = os.getenv('MY_GMAIL')
    print(f"My Gmail: {my_gmail}")
    ```
    """

    # Directly use the file path as a string
    env_path = file_path
    
    # Check if the file exists using os.path.isfile
    if not os.path.isfile(env_path):
        raise FileNotFoundError(f"{env_path} does not exist.")
    
    # Load the environment variables
    env_vars = dotenv_values(env_path)
    
    # Return the loaded environment variables as a dictionary
    return env_vars

def oc_set_env_from_myenvfile():
    """
    Reads environment variables from a fixed `.env` file at `C:/OmnesCore/myenvfile.env`
    and sets them permanently on Windows using the `setx` command.
    
    The function permanently sets environment variables from `myenvfile.env` located in the `OmnesCore` folder at:
        - `C:/OmnesCore/myenvfile.env` on Windows
        - `/OmnesCore/myenvfile.env` on Linux or macOS (POSIX systems)
    
    This function uses the fixed file path and does not require a parameter.
    

    - ### Example:
    ```python
    init_tools.set_env_from_file_permanently()
    ```
    """
    
    # Load the environment variables from the .env file
    env_vars = dotenv_values(file_path)
    
    # Loop through each environment variable and set it permanently
    for key, value in env_vars.items():
        if value is not None:
            # Use setx to permanently set the environment variable on Windows
            if os.name == 'nt':
                os.system(f'setx {key} "{value}"')
            # For POSIX systems, add unset command to .bashrc
            if os.name == 'posix':
                os.system("echo 'export " + key + "=\"" + value + "\"' >> ~/.bashrc")
            print(f"Set {key} = {value} permanently on the system(user variables).")
        else:
            print(f"Skipping {key} because it has no value.")
    
    print("All environment variables from the file have been processed.")


def oc_del_env():
    """
    Reads environment variables from a fixed `.env` file at `C:/OmnesCore/myenvfile.env`
    and deletes (unsets) them permanently on Windows by setting them to an empty value.

    The function permanently sets environment variables from `myenvfile.env` located in the `OmnesCore` folder at:
        - `C:/OmnesCore/myenvfile.env` on Windows
        - `/OmnesCore/myenvfile.env` on Linux or macOS (POSIX systems)
    
    - ### Example:
    ```python
    delete_env_from_file()
    ```
    """
    
    # Load the environment variables from the .env file
    env_vars = dotenv_values(file_path)
    
    # Loop through each environment variable and unset it
    for key in env_vars.keys():
        # Use setx to permanently set the environment variable to an empty value on Windows
        if os.name == 'nt':
            os.system(f'setx {key} ""')
        # For POSIX systems, add unset command to .bashrc
        if os.name == 'posix':
            os.system("echo 'export " + key + "=\"\"' >> ~/.bashrc")
        print(f"Deleted (unset) {key} permanently on the system(user variables).")
    
    print("All environment variables from the file have been deleted.")