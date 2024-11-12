# RAMCIK LIBRARY

e-mail, whatsapp, telegram automation with selenium and API's if provided. Also usefull multi media functions such as capturing screen,
google cloud text to img captha solver.   

## Table of Contents

1. [Requirements](#requirements)
2. [pip Install for library](#from-pypi-python-package-index)
3. [Installation for linux](#installation-for-linux)
4. [Env Variables for linux](#edit-created-myenvfileenv-for-linux)
5. [Set Env Variables for linux](#after-editing-env-file-run-python-script)
6. [Use Library](#to-use-in-python-script)
7. [Installation for Windows](#installation-for-windows)

---

## Requirements

List any prerequisites needed to install or run your library.

- Programming language version (e.g., Python >= 3.8)
- Dependencies (e.g., `selenium`, `Pillow`, `google-cloud-vision`, `telethon`, `opencv-python`,`numpy`, `pyautogui`, `requests`)
- System requirements (e.g., Linux, Windows)

## From PyPI (Python Package Index)

```bash
pip install -i https://test.pypi.org/simple/AutomationHandler-ramcik

# If you want to uninstall or upgrade
pip uninstall https://test.pypi.org/simple/ AutomationHandler-ramcik
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
init_tools.oc_create_myenvfile() # creates a file at /OmnesCore/myenvfile.env
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

# Edit created myenvfile.env For Linux
Edit created file =>  /OmnesCore/myenvfile.env For Linux
##### CHROME_PRIMARY_WHATSAPP_PROFILE_PATH 
```
"CHROME_PRIMARY_WHATSAPP_PROFILE_PATH": "$HOME/OmnesCore/ChromeProfile/primary/profile"

Note: You don't need to edit "CHROME_PRIMARY_WHATSAPP_PROFILE_PATH". You can just use it as default an skip to step 2
1:
This is your whatsapp profile path edit this as you wish.
2:
You can create profile via functions create_webdriver_with_profile and check_for_qr_code
code given below.
3: after doing this if you get an error you probably need give permision to created profile folder
by executing fallowing command.
sudo chmod 777 $HOME/OmnesCore/ChromeProfile/primary/profile
```
python code would be like:
```python
from AutomationHandler_ramcik import oc
driver = oc.create_webdriver_with_profile()
oc.check_for_qr_code(driver)

```
##### CHROME_SECONDARY_WHATSAPP_PROFILE_PATH
```
"CHROME_SECONDARY_WHATSAPP_PROFILE_PATH": "$HOME/OmnesCore/ChromeProfile/secondary/profile",

IMPORTANT: If you are not going to use "CHROME_SECONDARY_WHATSAPP_PROFILE_PATH", 
it should remain an empty string in myenvfile.env. But, If you’re going to use it, we suggest using 
the path provided above.

Note: To send a message to yourself, you can edit this and log in with a different WhatsApp account. 
The main purpose of this is to notify yourself via WhatsApp by sending a message from one WhatsApp account
to your own.

Note-2: Self-notification issues, such as sending a message from the same WhatsApp phone number to itself (which
does not trigger a notification on the phone), are handled by using CHROME_SECONDARY_WHATSAPP_PROFILE_PATH to 
eliminate this issue.

1:
This is your whatsapp second profile path edit this as you wish.
2:
You can create profile via functions create_webdriver_with_profile and check_for_qr_code
with specifying parameter profile_default to 2.
code given below.
3: after doing this if you get an error you probably need give permision to created profile folder
by executing fallowing command.
sudo chmod 777 $HOME/OmnesCore/ChromeProfile/secondary/profile
```
python code would be like:
```python
from AutomationHandler_ramcik import oc
driver = oc.create_webdriver_with_profile(profile_default=2)
oc.check_for_qr_code(driver)

```
##### MY_GMAIL
```
"MY_GMAIL": "example@gmail.com",
your gmail account 
```
##### MY_GOOGLE_APPLICATION_CREDENTIALS
```
"MY_GOOGLE_APPLICATION_CREDENTIALS": "$HOME/OmnesCore/credentials.json",

GOOGLE_APPLICATION_CREDENTIALS: Path to the JSON file with Google Cloud Vision API 
credentials.
This file can be obtained from the Google Cloud Console:

1. Go to [Google Cloud Console](https://console.cloud.google.com/).
2. Enable the Vision API and create a service account.
3. Download the JSON credentials file and set the path as an environment variable:
`os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "/path/to/credentials.json"`

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
Telegram chat id with created bot
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
# After Editing .env File run python script 
```python
from AutomationHandler_ramcik import init_tools
init_tools.oc_set_env_from_myenvfile()
```
### run this command or close terminal and reopen 
```bash
source ~/.bashrc
```

# To use in python script 
```python
from AutomationHandler_ramcik import oc
```