from selenium import webdriver  # WebDriver ile tarayıcı otomasyonu için gerekli kütüphane
from selenium.webdriver.common.by import By  # HTML elementlerini bulmak için kullanılan konum belirleyici
from selenium.webdriver.common.keys import Keys  # Klavye tuşlarını simüle etmek için kullanılır
from selenium.webdriver.support.ui import WebDriverWait  # Belirli bir durumun gerçekleşmesini beklemek için kullanılır
from selenium.webdriver.support import expected_conditions as EC  # Beklenen koşulları belirtmek için kullanılır
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import TimeoutException, InvalidArgumentException, JavascriptException
import time  # Zaman gecikmeleri için kullanılan kütüphane
import os  # İşletim sistemi ile ilgili fonksiyonlar için kullanılan kütüphane
import smtplib  # E-posta gönderme işlemleri için kullanılan kütüphane
from email.mime.text import MIMEText  # E-posta içeriğini oluşturmak için kullanılır
from email.mime.multipart import MIMEMultipart  # Birden fazla parçadan oluşan e-posta mesajları oluşturmak için kullanılır
import traceback
from telethon import TelegramClient, sync  # sync modülü senkron çalışmayı sağlar
from telethon.errors import PeerIdInvalidError
from email.header import decode_header
import requests
from PIL import Image, ImageDraw
import datetime
from google.cloud import vision  # Google Cloud Vision API'nin Python istemcisini içe aktarıyoruz.
import io  # 'io' modülünü içe aktarıyoruz. Bu modül, dosya giriş/çıkışı işlemleri için kullanılır.
import ssl  # Güvenli Bağlantı Katmanı (SSL) kütüphanesi
from email import encoders  # E-posta ekini kodlama modülü
from email.mime.base import MIMEBase  # E-posta eki oluşturma modülü
import cv2
import numpy as np
import pyautogui
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from telethon.tl.functions.contacts import ImportContactsRequest
from telethon.tl.types import InputPhoneContact

### whatsapp'a linkle giriş eklenecek qr kod gibi
### sms atma fonksiyonu



##################### Whatsapp fonksiyonları ############################

from multiprocessing import Lock

# Modül seviyesinde bir Lock nesnesi oluşturun, bu nesnenin oluşturulma amacı bir whatsapp hesabı
# iki tane tarayıcıda açmaya çalıştığın bozukluklar olması ve işlem yapılamaması
whatsapp_lock = Lock()

def create_webdriver_with_profile(chrome_profile_path: str = "", profile_default: int = 1, headless: bool = False) -> webdriver:
    """
    Creates a WebDriver object using Chrome with a specified user profile.

    - ### Parameters:

        - chrome_profile_path (str): The file path to the Chrome user profile to be used.
        
        - If `chrome_profile_path` is not provided, it fetches the path from environment variables.
        profile_default (int): The default profile to use.
            - 1 for primary
            - 2 for secondary
            
        - headless (bool): Whether to run Chrome in headless mode. Defaults to False.

    - ### Environment Variables:

        - CHROME_PRIMARY_WHATSAPP_PROFILE_PATH: Path for the primary WhatsApp Chrome profile.
        - CHROME_SECONDARY_WHATSAPP_PROFILE_PATH: Path for the secondary WhatsApp Chrome profile.

    - ### Returns:

        WebDriver: A WebDriver object initialized with the specified Chrome profile.

    - ### Raises:

        ValueError: If neither `chrome_profile_path` nor environment variables are set.
    """

    if chrome_profile_path == "" and profile_default == 1:
        chrome_profile_path = os.getenv('CHROME_PRIMARY_WHATSAPP_PROFILE_PATH')
    elif chrome_profile_path == "" and profile_default == 2:
        chrome_profile_path = os.getenv('CHROME_SECONDARY_WHATSAPP_PROFILE_PATH')
    else:
        print("verilen profili kullanma denenicek.")
    
    if chrome_profile_path == "" or chrome_profile_path is None:
        raise ValueError("Profil yolu sağlanmadı ve ortam değişkenleri ayarlanmadı. ikisinden biri yapılmalı.")

    # Chrome tarayıcısı için yapılandırma seçeneklerini tutacak bir `options` nesnesi oluşturuyoruz.
    options = webdriver.ChromeOptions()
    
    # `chrome_profile_path` parametresini `options` nesnesine bir argüman olarak ekliyoruz.
    # Bu, tarayıcının belirtilen kullanıcı profili ile başlatılmasını sağlar.
    options.add_argument(f"user-data-dir={chrome_profile_path}")

    
    options.add_argument('--disable-infobars')

    # Headless modun aktif olup olmadığını kontrol ediyoruz.
    if headless:
        options.add_argument('--headless')

    # Performance loglarını etkinleştiriyoruz
    caps = DesiredCapabilities.CHROME.copy()
    caps["goog:loggingPrefs"] = {"performance": "ALL"}

    # Capabilities ile options'u birleştiriyoruz
    options.set_capability("goog:loggingPrefs", {"performance": "ALL"})

    # WebDriver'ı başlat
    driver = webdriver.Chrome(options=options)
    return driver



def check_for_qr_code(driver: webdriver) -> bool:
    """
    Checks if the WhatsApp Web page is requesting a QR code scan or if the user is already logged in.
    
    This function opens the WhatsApp Web page using the provided Selenium WebDriver instance.
    It waits for either a QR code prompt or the Chats screen to appear.
    
    - ### Parameters:

        driver (Webdriver): A Selenium Webdriver instance for interacting with WhatsApp Web.

    - ### Returns:

        bool: - True if QR code is present (needs scan) or no elements found.
              - False if already logged in (Chats screen).

    - ### Notes:
    
        - If a QR code is found, the function waits up to 200 seconds for the user to scan the code 
          and log in. If the profile page (Chats screen) appears within that time, it returns False, 
          indicating successful login.
        
        - If no QR code or profile screen is detected, the function returns False as a fallback.
        """
    
    with whatsapp_lock:  # Kilidi kullanarak işlem yap
        try:
            # Web sayfasını aç
            driver.get("https://web.whatsapp.com")
            
            # QR kodunu veya profil ekranını aynı anda bekle
            WebDriverWait(driver, 300).until(
                EC.any_of(
                    EC.presence_of_element_located((By.XPATH, "//*[contains(text(), 'Point your phone at this screen to scan the QR code')]")),
                    EC.presence_of_element_located((By.XPATH, "//*[contains(text(), 'Telefonunuzu bu ekrana doğrultarak QR kodunu tarayın')]")),
                    EC.presence_of_element_located((By.CSS_SELECTOR, "div[aria-label='Chats']")),
                    EC.presence_of_element_located((By.CSS_SELECTOR, "div[aria-label='Sohbetler']"))
                )
            )
            
            # QR kodu varsa true, profil ekranı varsa false döndür
            qr_code_present = driver.find_elements(By.XPATH, "//*[contains(text(), 'Open WhatsApp on your phone')]")
            if not qr_code_present:
                qr_code_present = driver.find_elements(By.XPATH, "//*[contains(text(), 'Telefonunuzu bu ekrana doğrultarak QR kodunu tarayın')]")
            
            profile_present = driver.find_elements(By.CSS_SELECTOR, "div[aria-label='Chats']")
            if not profile_present:
                profile_present = driver.find_elements(By.CSS_SELECTOR, "div[aria-label='Sohbetler']")
            
            if qr_code_present:
                print("QR kodu yükleniyor.")
                # QR kodun yüklenmesini bekle
                WebDriverWait(driver, 100).until(
                    EC.presence_of_element_located((By.XPATH, "//*[@aria-label='Scan this QR code to link a device!']"))
                )
                print("QR kodu resmi yüklendi, 200 saniye de QR kodu okutup Whatsapp'a giriş yapman için bekleniyor. Eğer giriş yaparsan program devam edecek, yapmazsan da kapanacak.")
                
                # QR kodu bulunca 200 saniye de QR kodu okutup Whatsapp'a giriş yapman için bekleme
                profile_present = WebDriverWait(driver, 200).until(
                    EC.any_of(
                        EC.presence_of_element_located((By.CSS_SELECTOR, "div[aria-label='Chats']")),
                        EC.presence_of_element_located((By.CSS_SELECTOR, "div[aria-label='Sohbetler']"))
                    )
                )
                if profile_present:
                    print("Profil açıldı.False döndürülüyor.")
                    if wait_for_network_stabilization(driver):
                        if wait_for_page_render(driver):
                            print("WhatsApp Web tamamen yüklendi, mesaj göndermeye hazır.")
                    else:
                        print("Yükleme tamamlanmadı, lütfen tekrar deneyin.")
                    return False # giriş yapıldı
                else:
                    print("Profil açılmadı. True döndürülüyor.")
                    return True # QR kodu gerekli
                    

            elif profile_present:
                print("Profil ekranı bulundu. False döndürülüyor.")
                if wait_for_network_stabilization(driver):
                    if wait_for_page_render(driver):
                        print("WhatsApp Web tamamen yüklendi, mesaj göndermeye hazır.")
                else:
                    print("Yükleme tamamlanmadı, lütfen tekrar deneyin.")
                return False # Zaten giriş yapılmış
            
            else:
                print("Belirtilen elemanlar bulunamadı. True döndürülüyor.")
                return -1  # Eleman bulunamadı

        except Exception as e:
            print(f"Hata oluştu: {e}")
            # traceback.print_exc()  # Ayrıntılı hata mesajı
            return -2  # Hata durumu



def send_message_to_number(phone_number: str, message: str, driver: webdriver) -> tuple[bool, Exception | None]:
    """
    Sends a WhatsApp message to a specified phone number using Selenium WebDriver.

    - ### Parameters:

        - phone_number (str): 
            The phone number to which the message should be sent. The format should include the 
            country code without any leading '+' or with any leading '+'. 
            Example: '905xxxxxxxxx' OR '+905xxxxxxxxx' for a Turkish phone number.
        
        - message (str): 
            The text message to send.
        
        - driver (selenium.webdriver): 
            An instance of Selenium WebDriver with an active session of WhatsApp Web.

    - ### Returns:

        tuple:
            - (bool): True if the message was successfully sent, False otherwise.
            - (Exception or None): Returns the exception object if an error occurs, otherwise None.

    - ### Workflow:

        1. Opens WhatsApp Web with the provided phone number using the driver.
        2. Waits for the message input box to load.
        3. Sends the provided message into the message box and simulates pressing the Enter key.        
        4. Waits for the message to be sent, verifying it by checking for the disappearance of the 
           "sending" icon.
        5. Returns True if the message is sent successfully; otherwise, catches any exception, logs 
           it, and returns False.
        
    - ### Exceptions:

        Any exceptions that occur during the process (e.g., loading WhatsApp, finding elements, 
        sending message) are caught and printed with the full traceback for easier debugging.
    
    - ### Example:
    
    ```python
        send_message_to_number("905xxxxxxxxx", "Hello, this is a test message", driver)
        OR
        send_message_to_number("+905xxxxxxxxx", "Hello, this is a test message", driver)
    ``` 
    """

    with whatsapp_lock:  # Kilidi kullanarak işlem yap
        # kişi adına göre kişiyi bulma ve tıklama
        try:
            search_box = WebDriverWait(driver, 300).until(
                EC.presence_of_element_located((By.XPATH, "//div[@contenteditable='true'][@data-tab='3']"))
            )
            search_box.click()
            search_box.send_keys(phone_number)
            search_box.send_keys(Keys.RETURN)
            print("kişi bulundu ve açılıyor")
        
            # Mesaj kutusunun yüklenmesini bekleyin
            msg_box = WebDriverWait(driver, 300).until(
                EC.presence_of_element_located((By.XPATH, '//div[@contenteditable="true"][@data-tab="10"]'))
            )
            print("Mesaj kutusu bulundu, mesaj gönderiliyor...")
            msg_box.send_keys(message + Keys.ENTER)

            # Mesajın gönderilmesi için bekleniyor.

            # "msg-time" ikonunun bulmayı bekle
            WebDriverWait(driver, 300).until(
                EC.visibility_of_element_located((By.XPATH, '//span[@data-icon="msg-time"]'))
            )

            # "msg-time" ikonunun kaybolmasını bekle
            WebDriverWait(driver, 300).until(
                EC.invisibility_of_element_located((By.XPATH, '//span[@data-icon="msg-time"]'))
            )

            # Bu mesaj içinde 'msg-check' veya 'msg-dblcheck' ikonunu kontrol et
            sent_success_icon = WebDriverWait(driver, 300).until(
                EC.presence_of_element_located(
                    (
                        By.XPATH,
                        f'(.//div[@role="row" and .//span[contains(text(), "{message}")]])[last()]//span[@data-icon="msg-check" or @data-icon="msg-dblcheck"]'
                    )
                )
            )

            if sent_success_icon:
                print("Mesaj başarılı bir şekilde gönderildi.")
            else:
                print("mesajın hala bekliyor durumunda. zaman aşımından dolayı gönderilemedi.")
                raise Exception("mesajın hala bekliyor durumunda. zaman aşımından dolayı gönderilemedi.")

            return True, None
        except Exception as e:
            print(f"Mesaj gönderilemedi: {e}")
            traceback.print_exc()  # Ayrıntılı hata mesajı
            return False,e


def send_message_to_someone_or_group(someone_or_group_name: str, message: str, driver: webdriver) -> tuple[bool, Exception | None]:
    """
    Sends a message to a specific person or WhatsApp group using Selenium WebDriver.

    - ### Parameters:
    
        - someone_or_group_name (str): 
            The name of the contact or WhatsApp group to which the message will be sent.
    
        - message (str):
            The message that you want to send to the contact or group.

        - driver (WebDriver): 
            An instance of the Selenium WebDriver, which is controlling the browser that is logged 
            into WhatsApp Web.

    - ### Returns:

        (tuple): (True/False, exception or None)
            - True if sent successfully, False if failed.
            - Exception object if an error occurred, otherwise None.

    - ### Functionality:

        1. This function first searches for the WhatsApp contact or group by its name using the 
           search box.
        2. Once the contact or group is found and opened, it waits for the message input box to 
           load.
        3. The message is then typed into the input box and sent.
        4. After sending the message, the function waits for confirmation that the message 
           has been successfully sent (i.e., the "waiting to send" clock icon disappears).
        5. If the message is sent successfully, the function returns True. Otherwise, it returns 
           False and provides the relevant error message.

    - ### Notes:

        - The function uses WebDriverWait to ensure that elements are loaded before interacting 
          with them.
        - The search box and message box are located using XPaths.
        - The function handles exceptions and prints informative error messages in case of failure.
        - The function is able to send messages to both individuals and groups.
        

    - ### Exceptions:

        - If the search box or message box cannot be located, or if the message fails to send 
          within the timeout, an exception will be raised and caught, with details printed to the 
          console.
    """
    
    with whatsapp_lock:  # Kilidi kullanarak işlem yap
        # Grup adına göre grubu bulma ve tıklama
        try:
            search_box = WebDriverWait(driver, 300).until(
                EC.presence_of_element_located((By.XPATH, "//div[@contenteditable='true'][@data-tab='3']"))
            )
            search_box.click()
            search_box.send_keys(someone_or_group_name)
            search_box.send_keys(Keys.RETURN)
            print("Grup bulundu ve açılıyor")
        
            # Mesaj kutusunun yüklenmesini bekleyin
            msg_box = WebDriverWait(driver, 300).until(
                EC.presence_of_element_located((By.XPATH, '//div[@contenteditable="true"][@data-tab="10"]'))
            )
            print("Mesaj kutusu bulundu, mesaj gönderiliyor...")
            msg_box.send_keys(message + Keys.ENTER)

            # Mesajın gönderilmesi için bekleniyor.
            
            # "msg-time" ikonunun bulmayı bekle
            WebDriverWait(driver, 300).until(
                EC.visibility_of_element_located((By.XPATH, '//span[@data-icon="msg-time"]'))
            )

            # "msg-time" ikonunun kaybolmasını bekle
            WebDriverWait(driver, 300).until(
                EC.invisibility_of_element_located((By.XPATH, '//span[@data-icon="msg-time"]'))
            )

            # Bu mesaj içinde 'msg-check' veya 'msg-dblcheck' ikonunu kontrol et
            sent_success_icon = WebDriverWait(driver, 300).until(
                EC.presence_of_element_located(
                    (
                        By.XPATH,
                        f'(.//div[@role="row" and .//span[contains(text(), "{message}")]])[last()]//span[@data-icon="msg-check" or @data-icon="msg-dblcheck"]'
                    )
                )
            )

            if sent_success_icon:
                print("Mesaj başarılı bir şekilde gönderildi.")
            else:
                print("mesajın hala bekliyor durumunda. zaman aşımından dolayı gönderilemedi.")
                raise Exception("mesajın hala bekliyor durumunda. zaman aşımından dolayı gönderilemedi.")

            return True, None
        except Exception as e:
            print(f"Mesaj gönderilemedi: {e}")
            traceback.print_exc()  # Ayrıntılı hata mesajı
            return False,e


def send_file_to_someone_or_group(someone_or_group_name: str, file_path: str, driver: webdriver) -> tuple[bool, Exception | None]:
    """
    Sends a file (e.g., image, video, PDF, document) to a specified WhatsApp group or `individual contact` using Selenium WebDriver.

    - ### Parameters:

        - group_name (str): 
            The name of the WhatsApp group or individual contact where the file will be sent. 
            The group name or contact name should match exactly as it appears in WhatsApp. The 
            function can send files to both groups and individual contacts whose numbers are saved 
            with their full names.

        - file_path (str): 
            The local file path of the file to be sent. Ensure the file exists at the specified 
            path.
            
        - driver (selenium.webdriver): 
            An active instance of Selenium WebDriver, with a logged-in session of WhatsApp Web.

    - ### Returns:

        tuple:
            - (bool): True if the file was successfully sent, False otherwise.
            - (Exception or None): If an error occurs, it returns the exception object. 
              Otherwise, it returns None.

    - ### Workflow:

        1. The function first waits for the WhatsApp search box to load, 
           then searches for the group or contact by typing the provided `group_name`.
        2. After locating the group or contact, it waits for the message input box to appear and 
           load.
        3. The function locates the attachment (paperclip) button and clicks it to open the file 
           attachment options.
        4. Once the attachment options appear, the function finds the file input element and 
           uploads the file from `file_path`.
        5. After successfully uploading the file, it clicks the send button to send the file in the 
           group or contact chat.
        6. The function waits for the file to be sent by checking for the disappearance of the 
           "sending" icon.
        7. If the file is sent successfully, it returns True, otherwise it catches any exceptions,
           logs them, and returns False.

    - ### Exceptions:

        - The function captures and logs exceptions at each critical step (finding elements, 
        uploading, and sending).
        - The detailed traceback is printed to help with debugging if any errors occur during 
        execution.

    - ### Example:

        send_file_to_group("Family Group", r"C:/path/to/file.pdf", driver)
    """

    with whatsapp_lock:  # Kilidi kullanarak işlem yap
        # Grup adına göre grubu bulma ve tıklama
        try:
            search_box = WebDriverWait(driver, 300).until(
                EC.presence_of_element_located((By.XPATH, "//div[@contenteditable='true'][@data-tab='3']"))
            )
            search_box.click()
            search_box.send_keys(someone_or_group_name)
            search_box.send_keys(Keys.RETURN)
            print("Grup bulundu ve açılıyor")
        
            # Mesaj kutusunun yüklenmesini bekleyin
            msg_box = WebDriverWait(driver, 300).until(
                EC.presence_of_element_located((By.XPATH, '//div[@contenteditable="true"][@data-tab="10"]'))
            )
            print("Mesaj kutusu bulundu.")
            
            
            # Ataç simgesine tıkla
            attach_button = WebDriverWait(driver, 100).until(
                EC.any_of(
                    EC.presence_of_element_located((By.XPATH, '//button[@title="Attach" and @aria-label="Attach"]')),
                    EC.presence_of_element_located((By.XPATH, '//button[@title="Ekle" and @aria-label="Ekle"]'))
                )
            )
            attach_button.click()
            
            # Dosya yükleme elemanını bul ve dosyayı yükle
            file_input = WebDriverWait(driver, 300).until(
                EC.presence_of_element_located((By.XPATH, "//input[@accept='image/*,video/mp4,video/3gpp,video/quicktime']"))
            )

            if os.path.isabs(file_path):
                absolute_file_path = file_path  # If it's already absolute, use it as is
            else:
                absolute_file_path = os.path.abspath(file_path)  # If it's relative, convert it to an absolute path

            file_input.send_keys(absolute_file_path)  # Dosya dosyasını yükle
            print("file_path bulundu.")

            # Gönder butonuna tıkla
            send_button = WebDriverWait(driver, 300).until(
                EC.presence_of_element_located((By.XPATH, "//span[@data-icon='send']"))
            )
            send_button.click()

            # Mesajın gönderilmesi için bekleniyor.

            # "msg-time" ikonunun bulmayı bekle
            WebDriverWait(driver, 300).until(
                EC.visibility_of_element_located((By.XPATH, '//span[@data-icon="msg-time"]'))
            )

            # "msg-time" ikonunun kaybolmasını bekle
            WebDriverWait(driver, 300).until(
                EC.invisibility_of_element_located((By.XPATH, '//span[@data-icon="msg-time"]'))
            )

            # Bu mesaj içinde 'msg-check' veya 'msg-dblcheck' ikonunu kontrol et
            sent_success_icon = WebDriverWait(driver, 300).until(
                EC.presence_of_element_located(
                    (
                        By.XPATH,
                        '(//div[@role="row" and .//img[starts-with(@src, "data:image") or starts-with(@src, "blob:")]])[last()]//span[@data-icon="msg-check" or @data-icon="msg-dblcheck"]'
                    )
                )
            )

            if sent_success_icon:
                print("Dosya başarılı bir şekilde gönderildi.")
            else:
                print("Dosya hala bekliyor durumunda. zaman aşımından dolayı gönderilemedi.")
                raise Exception("mesajın hala bekliyor durumunda. zaman aşımından dolayı gönderilemedi.")
            
            return True, None

        except Exception as e:
            print(f"Dosya gönderilemedi: {e}")
            traceback.print_exc()  # Ayrıntılı hata mesajı
            return False,e

def notify_phone_number(phone_number: str, message: str, chrome_profile_path: str = "", headless: bool = False):

    """
    Sends a WhatsApp message to a specified phone number via WhatsApp Web using a WebDriver.
    Depending on the phone number provided, it uses different Chrome profiles for authentication.
    If the provided phone number is the user's own number, the function sends the message from 
    another WhatsApp account to avoid self-notification issues. This is done using the secondary 
    WhatsApp profile set by the 'CHROME_SECONDARY_WHATSAPP_PROFILE_PATH' environment variable. 
    For other phone numbers, it uses the primary WhatsApp profile defined by the 'CHROME_PRIMARY_WHATSAPP_PROFILE_PATH' environment variable.
    If a QR code is required to log in, the function sends an email notification without attempting to send the message.

    - ### Parameters:

        - phone_number (str): 
            The phone number to which the message should be sent.

        - message (str): 
            The content of the message to be sent.

        - chrome_profile_path (str, optional): 
            The file path to the Chrome user profile to be used. If not provided, the function will 
            use environment variables for profile paths.
        
        - headless (bool, optional): 
            If True, runs the WebDriver in headless mode (without a GUI). Defaults to False.

    - ### Behavior:

        1. Checks if the provided phone number is the user's own number by comparing it with the 
           environment variable 'MY_NUMBER'.
        2. Selects the appropriate Chrome profile directory based on whether the phone number 
           belongs to the user or another person:
            - If it's the user's phone number, uses the 'CHROME_SECONDARY_WHATSAPP_PROFILE_PATH' 
              environment variable to send the message from another WhatsApp account. if there 
              is no 'CHROME_SECONDARY_WHATSAPP_PROFILE_PATH', it uses 
              'CHROME_PRIMARY_WHATSAPP_PROFILE_PATH'.
            - Otherwise, uses the 'CHROME_PRIMARY_WHATSAPP_PROFILE_PATH' environment variable.
        3. If the 'chrome_profile_path' argument is provided, it overrides the default profile 
           selection.
        4. Creates a WebDriver instance with the selected Chrome profile, optionally running in 
           headless mode if specified.
        5. Checks for the presence of a QR code on WhatsApp Web, which indicates that a login is 
           required.
            - If a QR code is detected, the function sends an email notification with the subject 
              "WhatsApp Login Alert" and stops further execution.
        6. If no QR code is detected, it attempts to send the message using the 
           `send_message_to_number` function.
            - If the message is successfully sent, the function ends.
            - If the message cannot be sent, the function sends an email notification with details 
              about the failure.

    - ### Raises:

        Sends an email if:
            - A QR code is present, signaling that manual login is required.
            - The message could not be sent due to an error.

    - ### Dependencies:

        - os.getenv: To fetch environment variables like phone number and Chrome profile paths.
        - create_webdriver_with_profile: To create a WebDriver instance with a specific Chrome profile.
        - check_for_qr_code: To check if a QR code is present on WhatsApp Web.
        - send_message_to_number: To send a WhatsApp message to the specified number.
        - send_email: To send an email alert in case of errors.

    - ### Example usage:

        notify_phone_number("+905xxxxxxxxx", "Hello, this is a test message.")
        notify_phone_number("+905xxxxxxxxx", "This is a headless test message.", headless=True)
    """
    
    if chrome_profile_path == "":
        if phone_number == os.getenv('MY_NUMBER'): # Benim telefon numaramsa
            # Chrome profil dizini yolu klasörün içinde olucak şekilde ayarlanır kendiğinden.
            chrome_profile_path = os.getenv('CHROME_SECONDARY_WHATSAPP_PROFILE_PATH')
            if chrome_profile_path == "":
                chrome_profile_path = os.getenv('CHROME_PRIMARY_WHATSAPP_PROFILE_PATH')
        else:
            # Chrome profil dizini yolu klasörün içinde olucak şekilde ayarlanır kendiğinden.
            chrome_profile_path = os.getenv('CHROME_PRIMARY_WHATSAPP_PROFILE_PATH')
        
        if chrome_profile_path == "":
            raise ValueError("Profil yolu sağlanmadı ve ortam değişkenleri ayarlanmadı. ikisinden biri yapılmalı.")

    driver = create_webdriver_with_profile(chrome_profile_path, headless = headless)
    
    # QR kod var mı diye Fonksiyonu test etme varsa işlemlerin gerisini yapmadan bana uyarı E-maili atacak.
    qr_exists = check_for_qr_code(driver)
    if qr_exists is True:
        send_email("WhatsApp Login Alert","QR kod tarama işlemi gerekiyor. Lütfen programı yenileyin.")  # QR kod istendiğinde email gönder
    
    elif qr_exists == -1:
        send_email(f"Whatsapptan {phone_number} kişisine mesaj atılamadı.","qr_exists fonksiyonundan -1 döndü, yani Belirtilen elemanlar bulunamadı.")
    
    elif qr_exists == -2:
        send_email(f"Whatsapptan {phone_number} kişisine mesaj atılamadı.",f"qr_exists fonksiyonundan -2 döndü, except bloğuna düştü yani hata oluştu.")
    
    # Yoksa wpweb'deki benim mesajlarıma erişmiş demektir.
    else:
        check_sending, e = send_message_to_number(phone_number, message, driver)
        driver.quit()  # Driver'ı kapat

        #bir önceki satır false ise yani gönderilemediyse alttaki satırı çalıştır.
        if not check_sending:
            send_email(f"Whatsapptan {phone_number} kişisine mesaj atılamadı.",str(e))



def check_whatsapp_online_status(
    phone_number: str, 
    driver: webdriver, 
    wait_time: int = 20, 
    retry_attempts: int = 3, 
    delay_between_retries: int = 3, 
    take_screenshot_on_error: bool = False
) -> dict[str, int | str | None]:
    """
    Check the online status of a WhatsApp user using Selenium WebDriver.

    - ### Args:

        - phone_number (str):
            The phone number of the WhatsApp user in international format (e.g., '+905551234567').

        - driver (selenium.webdriver): 
            An instance of Selenium WebDriver used to control the browser and interact with 
            WhatsApp Web.
        
        - wait_time (int, optional): 
            Time in seconds to wait for the online status to appear. Default is 20 seconds.
        
        - retry_attempts (int, optional): 
            Number of attempts to retry checking the online status. Default is 3 retries.
        
        - delay_between_retries (int, optional):
            Delay in seconds between retries. Default is 3 seconds.
        
        - take_screenshot_on_error (bool, optional): 
            If True, takes a screenshot when an error occurs. Default is False.

    - ### Returns:

        dict: Returns a dictionary with detailed status information:
              - 'online': True/False, if the user is currently online.
              - 'status': "online", "typing...", "offline", "last seen", "unavailable".
              - 'error': If an exception occurred, the error message will be logged here.
              - 'exception_occurred': True/False, indicator if an exception was raised during execution.

    - ### Example:

        check_whatsapp_online_status('+905551234567', driver, wait_time=30, retry_attempts=5)
    """

    with whatsapp_lock:  # Kilidi kullanarak işlem yap
        status_info = {"online": False, "status": "offline", "error": None, "exception_occurred": False}
        
        # Format the URL to open the chat with the provided phone number
        try:
            driver.get(f"https://web.whatsapp.com/send?phone={phone_number}")
        except InvalidArgumentException:
            status_info["error"] = "Invalid phone number format. Please use international format (e.g., +905551234567)."
            return status_info

        for attempt in range(retry_attempts):
            try:
                print(f"Checking online status for {phone_number}, attempt {attempt + 1}/{retry_attempts}...")

                # Wait for the chat to load and check for the user's online or typing status
                status_element = WebDriverWait(driver, wait_time).until(
                    EC.visibility_of_element_located((
                        By.XPATH, f"//div[@id='main']//span[@title='online' or @title='çevrimiçi' or contains(@title, 'typing') or contains(@title, 'yazıyor')]"
                    ))
                )

                if status_element:
                    status = status_element.get_attribute("title").lower()

                    if 'typing' in status or 'yazıyor' in status:
                        status_info["online"] = True
                        status_info["status"] = "typing..."
                        print(f"{phone_number} is typing...")
                    elif 'online' in status or 'çevrimiçi' in status:
                        status_info["online"] = True
                        status_info["status"] = "online"
                        print(f"{phone_number} is online.")
                    break  # Exit the retry loop as status has been found

            except TimeoutException:
                # Retry on timeout
                if attempt + 1 < retry_attempts:
                    print(f"Timeout while waiting for {phone_number}'s status. Retrying after {delay_between_retries} seconds...")
                    time.sleep(delay_between_retries)
                else:
                    print(f"Timeout exceeded. Assuming {phone_number} is offline.")
                    status_info["online"] = False
                    status_info["status"] = "offline"
                    if take_screenshot_on_error:
                        current_time = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
                        driver.save_screenshot(f"whatsapp_status_error_{phone_number}_{current_time}.png")
                    break

            except Exception as e:
                # Handle any other exceptions, including connectivity issues
                status_info["error"] = str(e)
                status_info["exception_occurred"] = True  # Indicator that an exception occurred
                print(f"Error checking status for {phone_number}: {e}")
                if attempt + 1 < retry_attempts:
                    print(f"Retrying after {delay_between_retries} seconds...")
                    time.sleep(delay_between_retries)
                else:
                    print(f"Failed to check status after {retry_attempts} attempts.")
                    if take_screenshot_on_error:
                        current_time = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
                        driver.save_screenshot(f"whatsapp_status_error_{phone_number}_{current_time}.png")
                    break

        return status_info



def get_last_message(phone_number: str, driver: webdriver) -> str | None:
    """
    Fetch the last received message from a WhatsApp chat for a specific phone number.

    This function navigates to a WhatsApp Web chat for the specified phone number,
    waits until the chat is fully loaded, and then retrieves the last received message
    (if any) from the other party. If the chat fails to load or no messages are present,
    it handles these scenarios gracefully.

    - ### Args:

        - phone_number (str): 
            The phone number of the contact in international format (e.g., "+905551234567").

        - driver (selenium.webdriver.WebDriver): 
            The Selenium WebDriver instance controlling the browser.

    - ### Returns:

        str: The last received message from the other party, or None if no messages are found
             or the chat fails to load.

    - ### Steps:

        1. Navigate to WhatsApp Web using the provided phone number.
        2. Wait until the chat interface is fully loaded (e.g., by detecting a specific message 
           element).
        3. Retrieve all non-empty received messages from the chat.
        4. Return the last received message, or print a message if none are found.

    - ### Example:

        driver = webdriver.Chrome()
        phone_number = "+905551234567"
        last_message = get_last_message(phone_number, driver)
        print(f"Last message received: {last_message}")

    - ### Raises:

        Exception: If the chat fails to load within the given time (60 seconds).
    """
    
    with whatsapp_lock:  # Kilidi kullanarak işlem yap
        try:
            # kişi adına göre kişiyi bulma ve tıklama
            search_box = WebDriverWait(driver, 300).until(
                EC.presence_of_element_located((By.XPATH, "//div[@contenteditable='true'][@data-tab='3']"))
            )
            search_box.click()
            search_box.send_keys(phone_number)
            search_box.send_keys(Keys.RETURN)
            print("Grup bulundu ve açılıyor")
        
            # Mesaj kutusunun yüklenmesini bekleyin
            msg_box = WebDriverWait(driver, 300).until(
                EC.presence_of_element_located((By.XPATH, '//div[@contenteditable="true"][@data-tab="10"]'))
            )
            print("Mesaj kutusu bulundu.")

            # Wait until the chat interface has loaded by checking for incoming message elements
            WebDriverWait(driver, 300).until(
                EC.presence_of_element_located((By.XPATH, '//div[contains(@class, "message-in")]'))
            )
            WebDriverWait(driver, 300).until(
                EC.presence_of_element_located((By.XPATH, '//div[contains(@class, "message-out")]'))
            )
            print("Chat loaded successfully.")
            
            # Locate all incoming message elements within the chat
            message_elements = driver.find_elements(By.XPATH, '//div[contains(@class, "message-in") and contains(@class, "focusable-list-item")]//div[contains(@class, "_akbu")]/span')
            
            # Filter out empty messages
            valid_messages = [element.text for element in message_elements if element.text.strip()]

            if valid_messages:
                # Print all non-empty messages
                for index, message in enumerate(valid_messages):
                    print(f"Message {index}: {message}")
                
                # Get the last non-empty message
                last_message_text = valid_messages[-1]
                print("Last received message:", last_message_text)
            else:
                print("No messages received from the other party.")
                raise Exception("No messages received from the other party.")

        except Exception as e:
            print(f"Error loading chat: {e}")
            last_message_text = None

        return str(last_message_text)


def get_whatsapp_chat_history(phone_number: str, driver: webdriver) -> list[str]:
    """
    Retrieve chat history from a WhatsApp chat for a specific phone number.

    This function navigates to a WhatsApp Web chat for the specified phone number, waits until the chat interface 
    is fully loaded, and retrieves all visible sent and received messages (if any) from the chat.

    The function specifically waits for both incoming ("message-in") and outgoing ("message-out") messages to be loaded, 
    ensuring that the page has fully loaded before attempting to retrieve the chat history. 

    - ### Args:

        - phone_number (str): 
            The phone number of the contact in international format (e.g., "+905551234567").
        
        - driver (selenium.webdriver.WebDriver): 
            The Selenium WebDriver instance controlling the browser.

    - ### Returns:

        list: A list of all sent and received messages from the chat. If no messages are found or 
        there is an error, the function returns an empty list.

    - ### Example:

        driver = webdriver.Chrome()
        phone_number = "+905551234567"
        chat_history = get_whatsapp_chat_history(phone_number, driver)
        print(f"Chat history: {chat_history}")

    - ### Process:

        1. The function navigates to the WhatsApp Web page for the provided phone number.
        2. It waits until the chat interface is loaded by checking for both incoming and outgoing 
           message elements.
        3. Once the chat is fully loaded, it retrieves all messages from the chat.
        4. If messages are found, it returns the list of messages. Otherwise, it returns an empty 
           list.

    - ### Raises:

        Exception: If the chat fails to load within the given time limit (60 seconds).
    """

    
    with whatsapp_lock:  # Kilidi kullanarak işlem yap
        try:
            # kişi adına göre kişiyi bulma ve tıklama
            search_box = WebDriverWait(driver, 300).until(
                EC.presence_of_element_located((By.XPATH, "//div[@contenteditable='true'][@data-tab='3']"))
            )
            search_box.click()
            search_box.send_keys(phone_number)
            search_box.send_keys(Keys.RETURN)
            print("Grup bulundu ve açılıyor")
        
            # Mesaj kutusunun yüklenmesini bekleyin
            msg_box = WebDriverWait(driver, 300).until(
                EC.presence_of_element_located((By.XPATH, '//div[@contenteditable="true"][@data-tab="10"]'))
            )
            print("Mesaj kutusu bulundu.")
            
            # Wait until both incoming and outgoing message elements are present
            WebDriverWait(driver, 300).until(
                EC.presence_of_element_located((By.XPATH, '//div[contains(@class, "message-in")]'))
            )
            WebDriverWait(driver, 300).until(
                EC.presence_of_element_located((By.XPATH, '//div[contains(@class, "message-out")]'))
            )
            print("Chat fully loaded successfully.")
            
            # Locate all message elements (both sent and received messages) within the chat
            message_elements = driver.find_elements(By.XPATH, '//div[contains(@class, "message-in") or contains(@class, "message-out")]//div[contains(@class, "_akbu")]/span')
            
            # Filter out empty messages
            valid_messages = [element.text for element in message_elements if element.text.strip()]

            if valid_messages:
                print(f"Retrieved {len(valid_messages)} messages.")
                print(valid_messages)
            else:
                print("No messages were found in the chat.")
                raise Exception("No messages were found in the chat.")
            
        except Exception as e:
            print(f"Error loading chat: {e}")
            valid_messages = []

        return valid_messages

##################### Mail fonksiyonları ############################



def send_email(Subject: str, body: str, receiver_email: str = "me", sender_email: str = "", app_password: str = "") -> bool:
    """
    Sends an email using Gmail's SMTP server with the option to specify sender and receiver email addresses
    and an application-specific password. If any of these are not provided, the function will attempt to
    retrieve them from environment variables.

    Parameters
    ----------
    Subject : str
        The subject of the email.

    body : str
        The body of the email in plain text.

    receiver_email (str, optional (default = "me")): 
        The recipient's email address. Defaults to "me," meaning the function will use the 'MY_GMAIL' 
        environment variable by default. If not provided.

    sender_email : str, optional
        The email address of the sender. If not provided, the function will use the 'SENDER_EMAIL' environment variable.
        Default is "".

    app_password : str, optional
        The application-specific password for the sender's Gmail account. If not provided, the function will use the 
        'SENDER_EMAIL_APP_PASSWORD' environment variable. This is required due to Gmail's security settings.
        Default is "".

    Behavior
    --------
    - If `sender_email`, `app_password`, or `receiver_email` are not provided, the function will look for these values
    in the environment variables:
        - `SENDER_EMAIL` for the sender's email address
        - `SENDER_EMAIL_APP_PASSWORD` for the Gmail application password
        - `MY_GMAIL` for the recipient's email address
    - If any of these environment variables or parameters are missing, an error message is printed, and the function returns `False`.
    - The function creates a plain text email message using the provided `Subject` and `body`.
    - The email is sent using Gmail's SMTP server over SSL (port 465).
    - If sent successfully, a success message is printed.
    - If an error occurs, an error message and the traceback are printed.

    Returns
    -------
    bool
        Returns `True` if the email is sent successfully, `False` otherwise.

    Example
    -------
    ```python
    send_email(
        Subject="Test Email",
        body="This is a test email.",
        sender_email="youremail@gmail.com",
        app_password="yourapppassword",
        receiver_email="recipientemail@gmail.com"
    )
    ```

    Notes
    -----
    - Gmail requires an application-specific password if two-factor authentication (2FA) is enabled.
    You can generate this password from your Google Account settings.
    - Ensure necessary environment variables are set if parameters are not directly provided.
    - The function currently sends only plain text emails.
    """

    # body = Email metni
    if not sender_email:
        sender_email = os.getenv('SENDER_EMAIL') # Gönderici email adresi
        if not sender_email:
            print("""Çevresel değişkenlerde 'SENDER_EMAIL' bulunamadı veya 'sender_email' sağlanmadı. Lütfen birini temin edin.""")
            return False

    if not app_password:
        app_password = os.getenv('SENDER_EMAIL_APP_PASSWORD') # Gmail uygulama şifresi
        if not app_password:
            print("""Çevresel değişkenlerde 'SENDER_EMAIL_APP_PASSWORD' bulunamadı veya 'app_password' sağlanmadı. Lütfen birini temin edin.""")
            return False
    
    if  receiver_email == "me":
        receiver_email = os.getenv('MY_GMAIL') # Gmail uygulama şifresi
        if not receiver_email:
            print("""Çevresel değişkenlerde 'MY_GMAIL' bulunamadı veya 'receiver_email' sağlanmadı. Lütfen birini temin edin.""")
            return False
    
    try:
        # Check if error_data is not a string and convert it to a string if necessary
        if not isinstance(body, str):
            body = str(body)
    except Exception as conversion_error:
        # Raise an exception if conversion to string fails
        raise ValueError(f"Failed to convert error_data to a string: {conversion_error}")
    

    # Email içeriği
    message = MIMEMultipart("alternative")
    message["Subject"] = Subject
    message["From"] = sender_email
    message["To"] = receiver_email
    part = MIMEText(body, "plain", 'utf-8')
    message.attach(part)
    
    # Email gönderme işlemi
    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:  # Gmail SMTP sunucusuna bağlan (SSL kullanarak)
            server.login(sender_email, app_password)  # Email hesabı ile giriş yap
            server.sendmail(sender_email, receiver_email, message.as_string())  # Email gönder
        print("Email gönderildi.")
        return True
    except Exception as e:
        print(f"Email gönderilemedi: {e}")
        traceback.print_exc()  # Ayrıntılı hata mesajı
        return False


def send_email_with_attachments(subject: str, body: str, attachment_files: list, receiver_email: str = "me", sender_email: str = "", app_password: str = "") -> bool: 
    """
    Sends an email with optional file attachments using Gmail's SMTP server.

    This function sends an email from a specified Gmail account to a receiver email, 
    with the option to include one or more attachments. If the sender's email or app 
    password is not provided as arguments, the function attempts to retrieve them 
    from the environment variables `SENDER_EMAIL` and `SENDER_EMAIL_APP_PASSWORD`.

    Args:
        subject (str): The subject of the email.
        body (str): The body content of the email in plain text.
        attachment_files (list): A list of file paths for the attachments to be sent.
        receiver_email (str, optional (default = "me")): The recipient's email address. Defaults to "me,"
                                                         meaning the function will use the 'MY_GMAIL' environment
                                                         variable by default. If not provided.
        sender_email (str, optional): The sender's email address. Defaults to an empty string. 
                                      If not provided, it will use the 'SENDER_EMAIL' environment variable.
        app_password (str, optional): The app-specific password for the sender's email. 
                                      Defaults to an empty string. If not provided, it will 
                                      use the 'SENDER_EMAIL_APP_PASSWORD' environment variable.

    Returns:
        bool: Returns `True` if the email is sent successfully, otherwise `False`.
    
    Raises:
        FileNotFoundError: If any of the provided files in `attachment_files` cannot be found.
        smtplib.SMTPException: If an error occurs during the SMTP transaction.
    
    Example:
    ```python
        send_email_with_attachments(
            subject="Test Email",
            body="This is a test email.",
            attachment_files=["/path/to/attachment1.txt", "/path/to/attachment2.pdf"],
            receiver_email="example@example.com",
            sender_email="your-email@gmail.com",
            app_password="your-app-password"
        )
    ```
    
    Notes:
        - Ensure that you have created an app-specific password for your Gmail account, as 
          Gmail does not allow sending emails through normal login credentials.
        - The function will print an error message and return `False` if the required sender 
          email or app password are not provided or found in the environment variables.
    """
    
    
    if not sender_email:
        sender_email = os.getenv('SENDER_EMAIL') # Gönderici email adresi
        if not sender_email:
            print("""Çevresel değişkenlerde 'SENDER_EMAIL' bulunamadı veya 'sender_email' sağlanmadı. Lütfen birini temin edin.""")
            return False

    if not app_password:
        app_password = os.getenv('SENDER_EMAIL_APP_PASSWORD') # Gmail uygulama şifresi
        if not app_password:
            print("""Çevresel değişkenlerde 'SENDER_EMAIL_APP_PASSWORD' bulunamadı veya 'app_password' sağlanmadı. Lütfen birini temin edin.""")
            return False

    if  receiver_email == "me":
        receiver_email = os.getenv('MY_GMAIL') # Gmail uygulama şifresi
        if not receiver_email:
            print("""Çevresel değişkenlerde 'MY_GMAIL' bulunamadı veya 'receiver_email' sağlanmadı. Lütfen birini temin edin.""")
            return False
        
    # Gmail SMTP sunucusu ve portu
    smtp_server = 'smtp.gmail.com'
    smtp_port = 587

    from_email = sender_email
    # E-posta mesajını oluştur
    msg = MIMEMultipart()  # MIMEMultipart kullanarak çok parçalı bir e-posta oluştur
    msg['From'] = from_email  # Gönderenin e-posta adresini belirle
    msg['To'] = receiver_email  # Alıcının e-posta adresini belirle
    msg['Subject'] = subject  # E-postanın konusunu belirle

    try:
        # Check if error_data is not a string and convert it to a string if necessary
        if not isinstance(body, str):
            body = str(body)
    except Exception as conversion_error:
        # Raise an exception if conversion to string fails
        raise ValueError(f"Failed to convert error_data to a string: {conversion_error}")
    

    # Mesaj gövdesini ekle
    msg.attach(MIMEText(body, 'plain', 'utf-8'))  # E-posta gövdesini düz metin olarak ekle
    try:
        # Dosya eklerini ekle
        for file_path in attachment_files:

            if os.path.isabs(file_path):
                absolute_file_path = file_path  # If it's already absolute, use it as is
            else:
                absolute_file_path = os.path.abspath(file_path)  # If it's relative, convert it to an absolute path
                file_path = absolute_file_path
                
            # Dosyayı oku ve MIMEBase nesnesi oluştur
            part = MIMEBase('application', 'octet-stream')  # MIMEBase kullanarak ek oluştur
            with open(file_path, 'rb') as attachment:  # Dosyayı okuma modunda aç
                part.set_payload(attachment.read())  # Dosya içeriğini MIMEBase nesnesine yükle

            # Eki kodla ve başlık bilgilerini ekle
            encoders.encode_base64(part)  # Dosyayı Base64 formatında kodla
            part.add_header(
                'Content-Disposition',  
                f'attachment; filename= {os.path.basename(file_path)}',  # Sadece dosya adı ve uzantısını belirt
            )

            msg.attach(part)  # Ekleri e-posta mesajına ekle
    except Exception as e:
        print(f"E-posta gönderilirken bir hata oluştu: {e}")  # Hata durumunda hata mesajını yazdır
        traceback.print_exc()  # Ayrıntılı hata mesajı
        print("Gönderilecek dosya bulunamadı")  # Dosya bulunamazsa hata mesajı yazdır
        print("herhangi bir dosya eklenmeden mail atılacak.")

    # SMTP sunucusuna bağlan ve e-postayı gönder
    try:
        context = ssl.create_default_context()  # TLS için SSL bağlamını oluştur
        server = smtplib.SMTP(smtp_server, smtp_port)  # Gmail SMTP sunucusuna bağlan (port 587)
        server.starttls(context=context)  # TLS kullanarak güvenli bağlantı başlat
        server.login(sender_email, app_password)  # Gönderen e-posta hesabına giriş yap
        text = msg.as_string()  # E-posta mesajını düz metin olarak al
        server.sendmail(from_email, [receiver_email], text)  # E-postayı gönder
        server.quit()  # SMTP sunucusundan çıkış yap
        print("E-posta başarıyla gönderildi")  # Başarı mesajı yazdır
        return True  
    except Exception as e:
        print(f"E-posta gönderilirken bir hata oluştu: {e}")  # Hata durumunda hata mesajını yazdır
        traceback.print_exc()  # Ayrıntılı hata mesajı
        return False



##################### Telegram fonksiyonları ############################


def send_telegram_message(
    message: str, 
    recipient_username: str = None, 
    recipient_phone: str = None, 
    chat_id: str = None, 
    api_id: str = None, 
    api_hash: str = None,
    session_name: str = "my_telegram_session"
) -> bool:
    """
    Sends a message via Telegram. Only one of 'recipient_username', 'recipient_phone', or 'chat_id' 
    is required to send the message.

    - ### What is this function?
        This function allows you to send messages via your own Telegram account using the Telethon library. 
        It works with either a Telegram username, phone number, or chat ID.

    - ### Args:

        - `message` (str): 
            The message to be sent.

        - `recipient_username` (str): 
            Telegram username of the recipient (e.g., `@username`).

        - `recipient_phone` (str): 
            Phone number of the recipient (e.g., `+905551234567`).

        - `chat_id` (str): 
            Chat ID for the recipient (e.g., `123456789`).

        - `api_id` (str): 
            Telegram API ID. If not provided, it will be retrieved from environment variables.

        - `api_hash` (str): 
        
            Telegram API Hash. If not provided, it will be retrieved from environment variables.

        - `session_name` (str, optional): 
            The name of the session file to be created or reused. Defaults to `"my_telegram_session"`.

    - ### Returns:

        - `bool`: 
            `True` if the message was sent successfully, otherwise `False`.
        
    - ### How to Use This Function:

        #### Step 1: Obtain Telegram API Credentials
        1. Go to the Telegram [API Development Tools](https://my.telegram.org/apps) page.
        2. Log in with your Telegram account.
        3. Create a new application by providing a name, a short description, and a platform.
        4. Once created, Telegram will provide you with:
            - `api_id` (e.g., `123456`)
            - `api_hash` (e.g., `abcd1234efgh5678ijkl`)
        5. Save these credentials securely.

        #### Step 2: Set Up Environment Variables
        1. To avoid passing `api_id` and `api_hash` directly in the function, you can save them as environment variables.
        2. On **Linux/Mac**:
            - Open your terminal and edit your shell configuration file (`~/.bashrc`, `~/.zshrc`, or `~/.bash_profile`):
            ```bash
            export MY_TELEGRAM_API_ID="123456"
            export MY_TELEGRAM_API_HASH="abcd1234efgh5678ijkl"
            ```
            - Save the file and reload the configuration:
            ```bash
            source ~/.bashrc
            ```

        3. On Windows:
            - Open the Command Prompt (as Administrator).
            - Use the `setx` command to add the environment variables:
            ```cmd
            setx MY_TELEGRAM_API_ID "123456"
            setx MY_TELEGRAM_API_HASH "abcd1234efgh5678ijkl"
            ```
            - Note: After setting the variables with `setx`, you need to restart your terminal or application to apply the changes.

        #### Step 3: Authenticate Your Telegram Account
        1. When you first run this function, Telethon will attempt to authenticate your account.
        2. It will open a session and ask for a phone number (the one associated with your Telegram account).
        3. You will receive a confirmation code in Telegram. Enter this code when prompted.
        4. After successful authentication, Telethon will save a session file (`my_telegram_session.session`) in the current directory for future use.

        
        #### Step 4: Obtain User, Group, or Channel IDs:
            ##### For Users:
            1. Add the user to your Telegram contacts or ensure you’ve interacted with them (e.g., sent or received a message).
            2. Use the following Python code to fetch the user's `chat_id`:
                ```python
                from telethon.sync import TelegramClient

                client = TelegramClient("my_telegram_session", "API_ID", "API_HASH")
                client.start()

                for dialog in client.iter_dialogs():
                    if dialog.is_user:
                        print(f"User Name: {dialog.name}, Chat ID: {dialog.id}")
                ```
            3. Look for the **positive numeric ID** corresponding to the user.

            ##### For Groups:
            1. Add your Telegram account to the group.
            2. use the same Python code above to fetch its numeric ID.      
            3. Look for the **negative numeric ID** corresponding to your group.

            ##### For Channels:
            1. Add your Telegram account to the channel.
            2. Channels often have usernames (e.g., `@MyChannel`). You can use this directly as `recipient_username`.
            3. If the channel doesn’t have a username, use the same Python code above to fetch its numeric ID.        

        #### Step 5: Use This Function:
        - Choose one of the following methods to identify the recipient:
            1. **For Users:**
                - Use `recipient_username` (e.g., `@username`) or `recipient_phone` (e.g., `+905551234567`).
            2. **For Groups:**
                - Add your account to the group or channel.
                - Use `chat_id` to send a message directly to the group. Group IDs are typically **negative numbers**.
            3. **For Channels:**
                - Add your account to the channel as an admin if required.
                - Use `chat_id` (e.g., channel's username as `@channel_name` or its numeric ID).
        
    - ### Notes:
        - Ensure that the recipient is reachable (e.g., they haven't blocked you or deleted their Telegram account).
        - The first-time authentication process requires a valid phone number and code.
        - If using `recipient_phone`, ensure the phone number is registered on Telegram.
        - If you specify a custom `session_name`, a separate session file will be created.

    - ### Examples:

        #### Example 1: Send a message using a Telegram username
        ```python
        send_telegram_message(
            message="Hello, this is a message to a user!",
            recipient_username="@john_doe"
        )
        ```

        #### Example 2: Send a message using a phone number
        ```python
        send_telegram_message(
            message="Hello, this is a message to a phone number!",
            recipient_phone="+905551234567"
        )
        ```

        #### Example 3: Send a message using a chat ID
        ```python
        send_telegram_message(
            message="Hello, this is a message to a chat ID!",
            chat_id="123456789"
        )
        ```
    """

    # At least one recipient is required
    if not (recipient_username or recipient_phone or chat_id):
        print("Error: You must provide either 'recipient_username', 'recipient_phone', or 'chat_id'.")
        return False

    # Retrieve API credentials from environment variables if not provided
    if not api_id:
        api_id = os.getenv('MY_TELEGRAM_API_ID')
        if not api_id:
            print("Error: 'api_id' is not provided and 'MY_TELEGRAM_API_ID' is not set in environment variables. "
                  "Please retrieve your API ID from https://my.telegram.org/apps.")
            return False

    if not api_hash:
        api_hash = os.getenv('MY_TELEGRAM_API_HASH')
        if not api_hash:
            print("Error: 'api_hash' is not provided and 'MY_TELEGRAM_API_HASH' is not set in environment variables. "
                  "Please retrieve your API Hash from https://my.telegram.org/apps.")
            return False

    # Initialize Telegram client
    client = TelegramClient(session_name, api_id, api_hash)
    client.start()

    try:
        if recipient_username:
            if not recipient_username.startswith("@"):
                print("Error: 'recipient_username' must start with '@'.")
                return False
            # Send message using username
            client.send_message(recipient_username, message)
            print(f"Message sent to username: {recipient_username}")
        elif recipient_phone:
            # Find user by phone number and send message
            contact = InputPhoneContact(client_id=0, phone=recipient_phone, first_name="", last_name="")
            result = client(ImportContactsRequest([contact]))
            user = result.users[0] if result.users else None
            if not user:
                print(f"Error: Could not find user with phone number {recipient_phone}.")
                return False
            client.send_message(user, message)
            print(f"Message sent to phone number: {recipient_phone}")
        elif chat_id:
            # Send message directly using chat ID
            client.send_message(int(chat_id), message)
            print(f"Message sent to chat ID: {chat_id}")
        else:
            print("Error: Unexpected case. Check input parameters.")
            return False

        return True

    except Exception as e:
        print(f"An error occurred: {e}")
        return False

    finally:
        client.disconnect()



def send_telegram_message_with_bot(
    message: str,
    chat_id: str,
    token: str = None
) -> bool:
    """
    Sends a message via a Telegram bot to a specified chat ID. 

    This function uses the Telegram Bot API to send a message to a specific user, group, or channel via a bot.

    If `chat_id="me"` is provided, the function will use the `MY_TELEGRAM_BOT_CHAT_ID_WITH_ME` environment variable to send a message to yourself.

    - ### Args:

        - `message` (str): 
            The message you want to send.

        - `chat_id` (str): 
            The chat ID of the user, group, or channel. Use `"me"` to send a message to yourself.

        - `token` (str, optional): 
            The Telegram bot token. If not provided, it will be retrieved from the `MY_TELEGRAM_BOT_TOKEN` environment variable.

    - ### Returns:

        - bool: 
            Returns `True` if the message was sent successfully, otherwise `False`.    

    - ### How to Use This Function:

        #### Step 1: Create a Telegram Bot
        1. Open Telegram and search for `@BotFather`.
        2. Start a chat with `@BotFather` and use the `/newbot` command to create a new bot.
        3. Follow the instructions to name your bot and create a username (e.g., `MyTestBot`).
        4. `@BotFather` will give you a unique token in this format:
        ```
        123456:ABC-DEF1234ghIkl-zyx57W2v1u123ew11
        ```
        Save this token. You will need it to send messages.

        #### Step 2: Set Up Permanent Environment Variables
        1. Add the following environment variables to your system **permanently**:
            - `MY_TELEGRAM_BOT_TOKEN` (the bot token)
            - `MY_TELEGRAM_BOT_CHAT_ID_WITH_ME` (your personal chat ID with the bot, optional)

        2. On Linux/Mac:
            - Open your terminal and edit your shell configuration file (`~/.bashrc`, `~/.zshrc`, or `~/.bash_profile`):
            ```bash
            export MY_TELEGRAM_BOT_TOKEN="123456:ABC-DEF1234ghIkl-zyx57W2v1u123ew11"
            export MY_TELEGRAM_BOT_CHAT_ID_WITH_ME="123456789"
            ```
            - Save the file and reload the configuration:
            ```bash
            source ~/.bashrc
            ```

        3. On Windows: 
            - Open the Command Prompt (as Administrator).
            - Use the `setx` command to add the environment variables:
            ```cmd
            setx MY_TELEGRAM_BOT_TOKEN "123456:ABC-DEF1234ghIkl-zyx57W2v1u123ew11"
            setx MY_TELEGRAM_BOT_CHAT_ID_WITH_ME "123456789"
            ```
            - Note: After setting the variables with `setx`, you need to restart your terminal or application to apply the changes.

        ### NEXT STEPS:
        For step-by-step instructions on the process below, consult the `send_telegram_message` function:

        #### Step 4: Obtain User, Group, or Channel IDs:
        Detailed instructions on retrieving `chat_id` values for users, groups, or channels.

        #### Step 5: Use This Function:
        Step-by-step guidance on how to call the function with the correct parameters for sending messages.

        
    - ### Notes:
        - Ensure that the user, group, or channel has started the bot by sending `/start`. Otherwise, the bot cannot send messages to users.
        - Groups and channels do not require `/start`, but the bot must have the necessary permissions.

    - ### Examples:

        #### Example 1: Send a message to yourself
        ```python
        send_telegram_message_with_bot(
            message="Hello, this is a test message for myself!",
            chat_id="me"
        )
        ```

        #### Example 2: Send a message directly with a token
        ```python
        send_telegram_message_with_bot(
            message="Hello, this is a test message from the bot!",
            chat_id="123456789",
            token="123456:ABC-DEF1234ghIkl-zyx57W2v1u123ew11"
        )
        ```

        #### Example 3: Use environment variables for token and chat ID
        ```python
        send_telegram_message_with_bot(
            message="This message uses environment variables for credentials.",
            chat_id="123456789"
        )
        ```
    """
    # Handle optional token from environment variable
    if token is None:
        token = os.getenv("MY_TELEGRAM_BOT_TOKEN")
        if not token:
            print(
                "Error: No token provided and 'MY_TELEGRAM_BOT_TOKEN' is not set in environment variables. "
                "Please provide a valid token or set the environment variable."
            )
            return False

    # Handle "me" chat_id
    if chat_id == "me":
        chat_id = os.getenv("MY_TELEGRAM_BOT_CHAT_ID_WITH_ME")
        if not chat_id:
            print(
                "Error: 'MY_TELEGRAM_BOT_CHAT_ID_WITH_ME' is not set in environment variables. "
                "Please set this variable or provide a valid chat_id."
            )
            return False

    # Telegram Bot API URL
    bot_url = f"https://api.telegram.org/bot{token}/sendMessage"
    payload = {
        "chat_id": chat_id,
        "text": message
    }

    try:
        response = requests.post(bot_url, data=payload)
        if response.status_code == 200:
            print(f"Message sent to chat ID: {chat_id}")
            return True
        else:
            error_description = response.json().get("description", "No additional error details provided.")
            print(f"Failed to send message. Status: {response.status_code}, Error: {error_description}")
            return False
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return False
    




##################### Tool fonksiyonları ############################


def capture_full_page_screenshot(driver: webdriver, full_screenshot_path: str = None) -> str:
    """
    Captures a full-page screenshot using Selenium, stitches the screenshots together, 
    and saves it to the specified file path. If no path is provided, a default file name 
    with a timestamp is generated, and the screenshot is saved in the current working directory.

    - ### Parameters:

        - driver: Selenium WebDriver instance
            The Selenium WebDriver instance controlling the browser.
            
        - full_screenshot_path: str, optional
            The full file path where the screenshot should be saved, including the directory and 
            file name. If a file name without an extension is provided, '.png' will be 
            automatically appended. If this parameter is not provided, the screenshot will be 
            saved in the current directory with a default file name that includes a timestamp.
    
    - ### Returns:

        str: The full path to the saved screenshot file.

    - ### Raises:

        OSError: If there is an issue creating the directory or saving the file.

    - ### Examples:

        # Example 1: Save screenshot with a custom file name and path
        capture_full_page_screenshot(driver, "C:/Screenshots/my_screenshot.png")

        # Example 2: Save screenshot with a custom file name (without extension)
        capture_full_page_screenshot(driver, "C:/Screenshots/screenshot")

        # Example 3: Save screenshot in the current directory with an auto-generated name
        capture_full_page_screenshot(driver)
    """

    # Ensure the page is fully loaded
    WebDriverWait(driver, 100).until(lambda d: driver.execute_script('return document.readyState') == 'complete')

    # Get the current timestamp and create a unique screenshot filename if full path is not provided
    if not full_screenshot_path:
        current_time = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        full_screenshot_path = os.path.join(os.getcwd(), f"_screenshot_{current_time}.png")
    else:
        # Check if the path contains a valid file extension, and add '.png' if it's missing
        if not full_screenshot_path.endswith(".png"):  # Eğer dosya adı uzantı içermiyorsa
            full_screenshot_path += ".png"  # Otomatik olarak '.png' ekle

    # Create directory if it doesn't exist
    screenshot_dir = os.path.dirname(full_screenshot_path)
    if screenshot_dir and not os.path.exists(screenshot_dir):
        os.makedirs(screenshot_dir)

    # Get the total page height (scroll height) and the viewport height
    total_height = driver.execute_script("return document.documentElement.scrollHeight")
    viewport_height = driver.execute_script("return window.innerHeight")

    # Maximize the browser window to ensure full viewport visibility
    driver.maximize_window()
    time.sleep(2)  # Wait to ensure the window is fully maximized

    # Create an empty list to hold the temporary screenshot files
    screenshots = []
    
    # Scroll through the page and take screenshots
    scroll_position = 0
    while scroll_position < total_height:
        # Scroll the page to the current position
        driver.execute_script(f"window.scrollTo(0, {scroll_position});")
        time.sleep(1)  # Wait for content to load after scrolling

        # Save the screenshot to a temporary file
        screenshot_file = f"temp_screenshot_{scroll_position}.png"
        driver.save_screenshot(screenshot_file)
        screenshots.append(screenshot_file)

        # Move to the next scroll position
        scroll_position += viewport_height

    # Determine the correct width and height for the final stitched image
    window_width = driver.execute_script("return window.innerWidth")
    total_image_height = total_height + (len(screenshots) - 1) * 10  # Add space for the divider lines
    full_screenshot = Image.new('RGB', (window_width, total_image_height))

    # Stitch the screenshots together, drawing a red line between each one
    y_offset = 0
    for idx, screenshot in enumerate(screenshots):
        img = Image.open(screenshot)
        
        # Paste the screenshot onto the final image
        full_screenshot.paste(img, (0, y_offset))
        y_offset += img.size[1]
        
        # Draw a red divider line between each screenshot
        if idx < len(screenshots) - 1:
            draw = ImageDraw.Draw(full_screenshot)
            draw.line([(0, y_offset), (window_width, y_offset)], fill=(255, 0, 0), width=10)
            y_offset += 10  # Add space for the line

        img.close()

    # Save the full-page screenshot to the specified path
    full_screenshot.save(full_screenshot_path)
    print(f"Full-page screenshot captured and saved at {full_screenshot_path}.")

    # Delete temporary screenshot files
    for screenshot in screenshots:
        os.remove(screenshot)

    return full_screenshot_path


def record_screen(duration: int | float, output_name: str):
    """
    Records the screen for a specified duration and saves it as a video file.

    - ### Args:

        - duration (int or float): 
            The duration in seconds for which the screen will be recorded.

        - output_name (str): 
            The base name for the output video file.

    - ### Details:

        - The screen resolution is automatically detected.
        - The video is saved in AVI format using the XVID codec.
        - The output file name includes the provided base name followed by the current timestamp.

    - ### Example:

        record_screen(10, "my_recording")
        # This will record the screen for 10 seconds and save the video as 
        # my_recording_YYYY-MM-DD_HH-MM-SS.avi.

    - ### Dependencies:

        pyautogui: Used for capturing screenshots.
        cv2: OpenCV library for video writing.
        numpy: To convert the screenshots into arrays for OpenCV.

    """
    
    # Get the screen resolution
    screen_size = (pyautogui.size().width, pyautogui.size().height)
    
    # Set the codec and create a VideoWriter object
    fourcc = cv2.VideoWriter_fourcc(*"XVID")
    
    # Get the current time and format it for the filename
    current_time = time.strftime("%Y-%m-%d_%H-%M-%S")
    filename = f"{output_name}_{current_time}.avi"
    
    # Initialize VideoWriter with the screen size and frame rate
    out = cv2.VideoWriter(filename, fourcc, 30.0, screen_size)

    start_time = time.time()  # Record the start time
    
    while True:
        # Calculate elapsed time
        elapsed_time = time.time() - start_time
        
        # Stop recording after the specified duration
        if elapsed_time > duration:
            break
        
        # Take a screenshot
        img = pyautogui.screenshot()
        
        # Convert the screenshot to a numpy array
        frame = np.array(img)
        
        # Convert the color format from RGB (default in pyautogui) to BGR (used by OpenCV)
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        
        # Write the frame to the video
        out.write(frame)

    # Release the resources
    out.release()
    cv2.destroyAllWindows()


def extract_text_from_image_with_google(image_path: str) -> str:
    """
    Extracts text from an image using Google Cloud Vision API.

    - ### Args:

        - image_path (str): 
            The path to the image file from which text needs to be extracted.

    - ### Environment Variables:

        GOOGLE_APPLICATION_CREDENTIALS: Path to the JSON file with Google Cloud Vision API 
        credentials.
        This file can be obtained from the Google Cloud Console:
        
        1. Go to [Google Cloud Console](https://console.cloud.google.com/).
        2. Enable the Vision API and create a service account.
        3. Download the JSON credentials file and set the path as an environment variable:
        `os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "/path/to/credentials.json"`
            
    - ### Returns:

        str: The extracted text from the image. If no text is detected, an empty string is 
        returned.

    - ### Raises:

        Exception: If there is an error with the Google Cloud Vision API request.
    
    - ### Example:

        text = extract_text_from_image_with_google("/path/to/image.png")
        print(text)
    """

    # Set the environment variable for Google Cloud Vision API credentials
    # Ensure GOOGLE_APPLICATION_CREDENTIALS is set to the path of your JSON credentials file
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = os.getenv('MY_GOOGLE_APPLICATION_CREDENTIALS')

    # Initialize a client for the Google Cloud Vision API
    client = vision.ImageAnnotatorClient()

    # Open the image file in binary mode and read its contents
    with io.open(image_path, 'rb') as image_file:
        content = image_file.read()

    # Create an Image object with the content of the file
    image = vision.Image(content=content)

    # Use Google Cloud Vision API to detect text in the image
    response = client.text_detection(image=image)

    # Extract text annotations (all detected text in the image)
    texts = response.text_annotations

    # Check if there's an error in the API response
    if response.error.message:
        raise Exception(f'{response.error.message}')

    # Return the detected text from the first annotation, if available
    return texts[0].description if texts else ""




def text_recognition_captcha_solver(driver: webdriver, screenshot_name: str):
    """
    Solves a CAPTCHA by taking a screenshot of the CAPTCHA image, extracting the text from the image 
    using Google Cloud Vision API by using "extract_text_from_image_with_google" function, and inputting the extracted text into the CAPTCHA input field.

    - ### Args:

        - driver (WebDriver): 
            Selenium WebDriver instance controlling the browser.
        - screenshot_name (str): 
            A custom name to append to the screenshot file for identification.
    
    - ### Raises:

        NoSuchElementException: If the CAPTCHA image or text input field is not found on the page.
    
    - ### Example:

        text_recognition_captcha_solver(driver, "my_captcha"")
    
    - ### Functionality:

        - The function waits for the CAPTCHA image to become visible.
        - It scrolls the CAPTCHA image into the center of the view using JavaScript.
        - Captures a screenshot of the CAPTCHA image.
        - Uses Google Cloud Vision API to extract the text from the image.
        - Inputs the extracted CAPTCHA text into the appropriate text field.
        - Deletes the CAPTCHA image screenshot after processing.
    """

    try:
        # Wait for the CAPTCHA image to be present in the DOM and visible on the page
        captcha_image = WebDriverWait(driver, 2).until(
            EC.presence_of_element_located((By.ID, 'pageContent_captchaImage'))
        )

        # Get the vertical position (Y coordinate) of the CAPTCHA image
        captcha_location = captcha_image.location
        captcha_y = captcha_location['y']

        # Scroll the page so the CAPTCHA image is centered vertically
        scroll_y = captcha_y - (driver.execute_script('return window.innerHeight') // 2)
        driver.execute_script(f'window.scrollTo(0, {scroll_y});')

        # Create a unique filename for the CAPTCHA screenshot using the current timestamp
        current_time = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        image_path = f"captcha_image_{screenshot_name}_{current_time}.png"

        # Take a screenshot of the CAPTCHA image and save it to the file path
        captcha_image.screenshot(image_path)

        # Extract text from the CAPTCHA image using Google Cloud Vision API
        text = extract_text_from_image_with_google(image_path)

        # Use only the first line of the detected text (CAPTCHAs usually consist of one line of text)
        text = text.splitlines()[0]
        print(f"Extracted CAPTCHA text: {text}")

        # Remove the CAPTCHA image after processing
        os.remove(image_path)

        # Find the CAPTCHA text input field and input the extracted text
        captcha_textbox = driver.find_element(By.ID, 'pageContent_txtCaptchaText')
        captcha_textbox.send_keys(text)
        print("CAPTCHA text successfully entered.")

    except NoSuchElementException:
        # Handle the case where the CAPTCHA image or input field is not found
        print(f"Captcha image not found or unable to locate the input field.")

def count_string_occurrences_in_html(driver: webdriver, search_string: str, timeout: int = 10) -> int:
    """
    Count the occurrences of a specific string within the HTML content of a webpage after ensuring
    that the page has fully loaded and the content has dynamically changed if applicable.

    This function first ensures the webpage has fully loaded by checking the `document.readyState`
    and waits for any dynamic changes in the HTML source before counting the occurrences of the 
    specified string.

    - ### Parameters:

        - driver (WebDriver): 
            The Selenium WebDriver instance used to interact with the webpage.
        
        - search_string (str): 
            The string to search for in the updated HTML source of the page.
        
        - timeout (int, optional):
            Maximum time (in seconds) to wait for the page load and content update. 
            Defaults to 10 seconds.

    - ### Returns:
    
        int: The number of times the search_string appears in the updated HTML source of the page.
    """
    
    # Sayfanın tam olarak yüklendiğinden emin olun
    WebDriverWait(driver, timeout).until(
        lambda d: d.execute_script('return document.readyState') == 'complete'
    )

    # Sayfanın tam olarak yüklenmesini bekleyin
    WebDriverWait(driver, timeout).until(
        EC.presence_of_element_located((By.TAG_NAME, 'body'))
    )

    # Sayfanın HTML kodunu alın
    initial_page_source = driver.page_source

    try:
        # Sayfanın HTML kodu değişene kadar bekleyin (dinamik bekleme)
        WebDriverWait(driver, timeout).until(
            lambda d: d.page_source != initial_page_source
        )

        # Sayfanın güncellenmiş HTML kodunu alın
        updated_page_source = driver.page_source
    except TimeoutException:
        # Timeout olursa sayfa güncellenmedi, başlangıçtaki HTML'yi kullan
        updated_page_source = initial_page_source

    # Aranan string'in güncellenmiş HTML içinde kaç kez geçtiğini sayın
    count = updated_page_source.count(search_string)

    return count

def wait_for_page_render(driver: webdriver, check_interval: int = 2, max_checks: int = 20) -> bool:
    """
    Waits until the browser's page rendering is complete by comparing HTML content.

    - ### Parameters:

        - driver (WebDriver): 
            The WebDriver instance for the browser.
        - check_interval (int): 
            The interval (in seconds) between HTML comparisons. Defaults to 2 seconds.
        - max_checks (int): 
            The maximum number of comparisons to perform before timing out. Defaults to 10.

    - ### Returns:
    
        bool: True if the page is fully rendered, False otherwise.

    - ### Notes:
    
        - This function retrieves the current page's HTML and compares it over time.
        - If the HTML remains unchanged for `check_interval` seconds across consecutive checks, 
          it assumes the page is fully rendered.
    """
    try:
        previous_html = driver.page_source  # Get initial HTML

        for check in range(max_checks):
            time.sleep(check_interval)  # Bekleme süresi
            current_html = driver.page_source  # Yeni HTML al
            
            if current_html == previous_html:
                print(f"Sayfa render edildi. Toplam geçen süre: {check_interval * (check + 1)} saniye.")
                return True  # HTML aynı ise render işlemi tamam
            else:
                print(f"Render devam ediyor. Kontrol sayısı: {check + 1}/{max_checks}")
                previous_html = current_html  # Yeni HTML'yi öncekiyle değiştir

        print("Render işlemi tamamlanmadı, zaman aşımına uğradı.")
        return False  # Maksimum kontrol sayısını aşarsa zaman aşımı
    except Exception as e:
        print(f"Render kontrolü sırasında hata oluştu: {e}")
        return False

def wait_for_network_stabilization(driver: webdriver, max_inactive_time: int = 2, threshold: int = 5, stable_checks: int = 3) -> bool:
    """
    Waits until the network activity stabilizes for a given WebDriver session.

    - ### Parameters:

        - driver (WebDriver): 
            The WebDriver instance to monitor network activity.
        - max_inactive_time (int): 
            The duration (in seconds) of low network activity to consider as stable. Defaults to 2 seconds.
        - threshold (int): 
            The maximum number of network requests allowed during the inactive period. Defaults to 5 requests.
        - stable_checks (int): 
            The number of consecutive stable periods required to confirm stabilization. Defaults to 3.

    - ### Returns:

        bool: True if the network stabilizes successfully, False otherwise.

    - ### Notes:
    
        This function assumes that performance logging is enabled in the WebDriver instance.
    """
    start_time = time.time()
    try:
        stable_count = 0
        while stable_count < stable_checks:
            # Get the initial network traffic
            logs_before = driver.get_log("performance")
            traffic_before = len([log for log in logs_before if "Network.responseReceived" in log["message"]])

            # Wait for the specified inactive period
            time.sleep(max_inactive_time)

            # Get the network traffic after the wait
            logs_after = driver.get_log("performance")
            traffic_after = len([log for log in logs_after if "Network.responseReceived" in log["message"]])

            # Log traffic details
            print(f"Traffic Before: {traffic_before}, Traffic After: {traffic_after}, Difference: {traffic_after - traffic_before}")

            # Check if the traffic difference is below the threshold
            if traffic_after - traffic_before < threshold:
                stable_count += 1
                print(f"Stable count incremented: {stable_count}/{stable_checks}")
            else:
                stable_count = 0  # Reset if activity exceeds the threshold
                print("Traffic increased; stable count reset.")

        print("Network activity stabilized.")

        end_time = time.time()
        duration = end_time - start_time
        print(f"wait_for_network_stabilization fonksiyonu toplam çalışma süresi: {duration:.2f} saniye.")

        return True
    except Exception as e:
        print(f"Error during network stabilization: {e}")
        end_time = time.time()
        duration = end_time - start_time
        print(f"wait_for_network_stabilization fonksiyonu toplam çalışma süresi: {duration:.2f} saniye.")
        return False
    
