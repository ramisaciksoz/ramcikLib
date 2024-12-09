# RAMCIK LIBRARY

Effortless automation for **Email**, **WhatsApp**, and **Telegram** via Selenium and available APIs. Includes handy multimedia tools like **screen capture** and **image-to-text conversion with Google Cloud API**. 

## Table of Contents

1. [Requirements](#requirements)
2. [Installation](#installation)
    - [pip Install for library](#from-pypi-python-package-index)
    - [Installation for linux](#installation-for-linux)
    - [Installation for Windows](#installation-for-windows)
3. [Editing Env Variables](#edit-created-myenvfileenv)
4. [Setting up Env Variables](#setting-up-environmental-variables)
5. [Opening WhatsApp Profiles](#opening-whatsapp-profiles)
6. [Congratulations! Start Using the Library🔥](#congratulations-start-using-the-library)

---

## Requirements

List any prerequisites needed to install or run your library.

- Programming language version (e.g., Python >= 3.8)
- Dependencies (e.g., `selenium`, `webdriver-manager`, `Pillow`, `google-cloud-vision`, `telethon`, `opencv-python`,`numpy`, `pyautogui`, `requests`)
- System requirements (e.g., Linux, Windows)

# Installation

## From PyPI (Python Package Index)

```bash
pip install -i https://test.pypi.org/simple/ AutomationHandler-ramcik

# If you want to uninstall
pip uninstall https://test.pypi.org/simple/ AutomationHandler-ramcik

# If you want to upgrade, First uninstall, then install again.
```
## Installation for linux
```python
# main.py

# starts from here!
scriptContent = """#!/bin/bash
missingModule=`python main.py 2>&1 | grep "ModuleNotFoundError: No module named" | awk -F"'" '{print $2}'`;
pip install $missingModule;"""
# Open the file in write mode ('w'), or append mode ('a')
with open('installMissing.sh', 'w') as file:
    file.write(scriptContent)

from AutomationHandler_ramcik import init_tools
init_tools.oc_install_deps()
init_tools.oc_create_myenvfile() # creates a file at $HOME/OmnesCore/myenvfile.env
#ends here 

```
# run python script 
```bash
# pythonInterpreterPath is python interpreter you mainly use with this library
# If running the code below leaves any modules missing, try running the following 
# bash command to install the missing modules: "chmod +x installMissing.sh; ./installMissing.sh;".
# Then, run the code here again and continue trying until it executes successfully.
sudo pythonInterpreterPath main.py
```

# if there is missing module run 
```bash
# If there are any modules that fail to load when main.py is run, the following command 
# can be used to complete the installation.
chmod +x installMissing.sh; ./installMissing.sh;
```

## Installation for windows
```python
# main.py

# starts from here!
import os
import subprocess

# Check if dotenv is installed, if not, install it
try:
    import dotenv
except ImportError:
    subprocess.check_call(["pip", "install", "python-dotenv"])

# Continue with the rest of the script after ensuring all dependencies are installed
from AutomationHandler_ramcik import init_tools
init_tools.oc_install_deps()
init_tools.oc_create_myenvfile()  # creates a file at ~/OmnesCore/myenvfile.env in the user's home directory, e.g., C:/Users/Username/OmnesCore/myenvfile.env
# ends here
```

# Edit created myenvfile.env
- Edit created file For Linux =>  $HOME/OmnesCore/myenvfile.env 
- Edit created file For Windows =>  ~/OmnesCore/myenvfile.env in the user's home directory, e.g., C:/Users/Username/OmnesCore/myenvfile.env 


##### CHROME_PRIMARY_WHATSAPP_PROFILE_PATH 
```
For linux;
"CHROME_PRIMARY_WHATSAPP_PROFILE_PATH": "$HOME/OmnesCore/ChromeProfile/primary/profile"

For windows;
"CHROME_PRIMARY_WHATSAPP_PROFILE_PATH": "C:/Users/Username/OmnesCore/ChromeProfile/primary/profile"

Note: You need to check if the file is created in the correct location for the CHROME_PRIMARY_WHATSAPP_PROFILE_PATH variable, then You can just use it as default an skip to step 2.

- This is your whatsapp profile path, if you want to use a different path for primary whatpsapp profile, you can edit this in myenvfile.env as you wish.
```

##### CHROME_SECONDARY_WHATSAPP_PROFILE_PATH

**IMPORTANT**: If you are not going to use `"CHROME_SECONDARY_WHATSAPP_PROFILE_PATH"`, 
it should remain an `empty string` in `myenvfile.env`. But, If you’re going to use it, we suggest using 
the path provided following.⚠️

```
For linux;
"CHROME_SECONDARY_WHATSAPP_PROFILE_PATH": "$HOME/OmnesCore/ChromeProfile/secondary/profile"

For windows;
"CHROME_SECONDARY_WHATSAPP_PROFILE_PATH": "C:/Users/Username/OmnesCore/ChromeProfile/secondary/profile"


Note: To send a message to yourself, you can edit this and log in with a different WhatsApp account. 
The main purpose of this is to notify yourself via WhatsApp by sending a message from one WhatsApp account
to your own.

Note-2: Self-notification issues, such as sending a message from the same WhatsApp phone number to itself (which
does not trigger a notification on the phone), are handled by using CHROME_SECONDARY_WHATSAPP_PROFILE_PATH to 
eliminate this issue.

- This is your whatsapp profile path, if you want to use a different path for second whatpsapp profile, you can edit this in myenvfile.env as you wish.
```
##### MY_GMAIL
```
"MY_GMAIL": "example@gmail.com",
your gmail account 
```
##### MY_GOOGLE_APPLICATION_CREDENTIALS
```
For linux;
"MY_GOOGLE_APPLICATION_CREDENTIALS": "$HOME/OmnesCore/GoogleVisionCredentials.json"

For windows;
"MY_GOOGLE_APPLICATION_CREDENTIALS": "C:/Users/Username/OmnesCore/GoogleVisionCredentials.json"

GOOGLE_APPLICATION_CREDENTIALS: Path to the JSON file with Google Cloud Vision API 
credentials.
This file can be obtained from the Google Cloud Console:

1. Go to [Google Cloud Console](https://console.cloud.google.com/).
2. Enable the Vision API and create a service account.
3. Download the JSON credentials file and set the path as an environment variable:
`os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = os.getenv('MY_GOOGLE_APPLICATION_CREDENTIALS')`

```
##### MY_NUMBER
```
"MY_NUMBER": "+1234567890",

Your phone number.
```

##### MY_TELEGRAM_API_HASH
```
"MY_TELEGRAM_API_HASH": "your-telegram-api-hash",

Telegram hash for api
```
##### MY_TELEGRAM_API_ID
```
"MY_TELEGRAM_API_ID": "your-telegram-api-id",

Telegram api id
```
##### MY_TELEGRAM_BOT_TOKEN
```
"MY_TELEGRAM_BOT_TOKEN": "your-telegram-bot-token",

Telegram created bot token
```
##### MY_TELEGRAM_BOT_CHAT_ID_WITH_ME
```
"MY_TELEGRAM_BOT_CHAT_ID_WITH_ME": "your-telegram-chat-id",

Chat ID between you and your created bot.
```
##### SENDER_EMAIL
```
"SENDER_EMAIL": "example_sender@gmail.com",

A sender mail which used for sending mail
```
##### SENDER_EMAIL_APP_PASSWORD
```
"SENDER_EMAIL_APP_PASSWORD": "your-email-app-password"
A sender mail password which used for sending mail
```
##### MS_COPILOT_EMAIL
```
"MS_COPILOT_EMAIL": "example@outlook.com"
Your registered email for Microsoft Copilot.
```
##### MS_COPILOT_PASSWORD
```
"MS_COPILOT_PASSWORD*": "your-email-password"
Your secure password for authentication.
```

# Setting up Environmental Variables

### **After Editing `myenvfile.env` File, run python script.**

```python
from AutomationHandler_ramcik import init_tools
init_tools.oc_set_env_from_myenvfile()
```

<u>**For linux;**</u>
- After running the script above, run the following command `or` close and reopen the terminal:
```bash
source ~/.bashrc
```

<u>**For windows;**</u>
- After running the script above, restart Visual Studio Code:



# Opening WhatsApp Profiles

### Primary WhatsApp Profile (`CHROME_PRIMARY_WHATSAPP_PROFILE_PATH`)

To create and access your primary WhatsApp profile, follow these steps:

### 1. Create the Profile

Use the following Python code to create the profile and check for a QR code:

```python
from AutomationHandler_ramcik import oc

# Create a WebDriver instance with the specified profile
driver = oc.create_webdriver_with_profile()

# Check if the QR code is displayed (to log in if needed)
oc.check_for_qr_code(driver)
```

### 2. Grant Folder Permissions (if needed)

#### Linux

If you encounter a permissions error when trying to access the profile, run the command below to grant the required permissions to the profile folder:

```bash
sudo chmod 777 $HOME/OmnesCore/ChromeProfile/primary/profile
```

#### Windows

For Windows users, if you face a similar error:

1. Navigate to the profile folder (e.g., `C:\OmnesCore\ChromeProfile\primary\profile`).
2. Right-click on the folder and select **Properties**.
3. Go to the **Security** tab and click **Edit**.
4. Select your user account from the list, then check the **Full Control** box under **Permissions**.
5. Click **Apply** and then **OK** to save the changes.

### Secondary WhatsApp Profile (`CHROME_SECONDARY_WHATSAPP_PROFILE_PATH`)

To create and access your secondary WhatsApp profile, follow these steps:

### 1. Create the Profile

Use the following Python code to create the profile and check for a QR code:

You can create the profile by specifying `profile_default=2` in the `create_webdriver_with_profile` function, along with `check_for_qr_code`, as shown below.

```python
from AutomationHandler_ramcik import oc

# Create a WebDriver instance with the specified profile
driver = oc.create_webdriver_with_profile(profile_default=2)

# Check if the QR code is displayed (to log in if needed)
oc.check_for_qr_code(driver)
```

### 2. Grant Folder Permissions (if needed)

#### Linux

If you encounter a permissions error when trying to access the profile, run the command below to grant the required permissions to the profile folder:

```bash
sudo chmod 777 $HOME/OmnesCore/ChromeProfile/secondary/profile
```

#### Windows

For Windows users, if you face a similar error:

1. Navigate to the profile folder (e.g., `C:\OmnesCore\ChromeProfile\secondary\profile`).
2. Right-click on the folder and select **Properties**.
3. Go to the **Security** tab and click **Edit**.
4. Select your user account from the list, then check the **Full Control** box under **Permissions**.
5. Click **Apply** and then **OK** to save the changes.



# Congratulations! start using the library🔥
```python
from AutomationHandler_ramcik import oc
```