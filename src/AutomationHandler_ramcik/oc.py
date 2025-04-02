from selenium import webdriver  # WebDriver ile tarayıcı otomasyonu için gerekli kütüphane
from selenium.webdriver.common.by import By  # HTML elementlerini bulmak için kullanılan konum belirleyici
from selenium.webdriver.common.keys import Keys  # Klavye tuşlarını simüle etmek için kullanılır
from selenium.webdriver.support.ui import WebDriverWait  # Belirli bir durumun gerçekleşmesini beklemek için kullanılır
from selenium.webdriver.support import expected_conditions as EC  # Beklenen koşulları belirtmek için kullanılır
from selenium.common.exceptions import NoSuchElementException # Belirtilen öğe bulunamazsa oluşan hata
from selenium.common.exceptions import TimeoutException, InvalidArgumentException, JavascriptException  # Selenium hataları
from selenium.webdriver.common.action_chains import ActionChains  # Fare ve klavye hareketlerini simüle etmek için kullanılır
import time  # Zaman gecikmeleri için kullanılan kütüphane
import os  # İşletim sistemi ile ilgili fonksiyonlar için kullanılan kütüphane
import smtplib  # E-posta gönderme işlemleri için kullanılan kütüphane
from email.mime.text import MIMEText  # E-posta içeriğini oluşturmak için kullanılır
from email.mime.multipart import MIMEMultipart  # Birden fazla parçadan oluşan e-posta mesajları oluşturmak için kullanılır
import traceback # Hata ayıklamak için kullanılır, istisnaların izini takip etmeye yarar
from telethon import TelegramClient, sync  # sync modülü senkron çalışmayı sağlar
from telethon.errors import UsernameNotOccupiedError, PeerIdInvalidError  # Telegram'da geçersiz kullanıcı kimliği hatası
from email.header import decode_header  # E-posta başlıklarını çözümlemek için kullanılır
import requests  # HTTP istekleri yapmak için kullanılan kütüphane
from PIL import Image, ImageDraw  # Görüntü işleme için kullanılan kütüphane
import datetime  # Tarih ve saat işlemleri için kullanılır
from google.cloud import vision  # Google Cloud Vision API'nin Python istemcisini içe aktarıyoruz.
import io  # 'io' modülünü içe aktarıyoruz. Bu modül, dosya giriş/çıkışı işlemleri için kullanılır.
import ssl  # Güvenli Bağlantı Katmanı (SSL) kütüphanesi
from email import encoders  # E-posta ekini kodlama modülü
from email.mime.base import MIMEBase  # E-posta eki oluşturma modülü
import cv2  # OpenCV ile görüntü işleme
import numpy as np  # Sayısal işlemler ve diziler için kullanılan kütüphane
import pyautogui  # Ekran otomasyonu ve fare hareketleri için kullanılan kütüphane
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities  # WebDriver yeteneklerini belirlemek için kullanılır
from telethon.tl.functions.contacts import ImportContactsRequest  # Telegram'da kişi ekleme işlemi için kullanılan API fonksiyonu
from telethon.tl.types import InputPhoneContact  # Telegram'a telefon numarası eklemek için kullanılır
import random  # Rastgele sayı üretmek için kullanılan kütüphane
from email.header import Header
import re  # Düzenli ifadelerle metin arama ve eşleştirme yapmak için kullanılır
from selenium.common.exceptions import StaleElementReferenceException  # DOM güncellendiğinde eski elementlere erişimde oluşan hata
from telethon import functions  # Telegram API'nin gelişmiş fonksiyonlarını kullanmak için gerekli modül
import unicodedata  # Unicode karakterlerin normalleştirilmesi (örn. aksan temizliği) için kullanılır
import undetected_chromedriver as uc  # Chrome tarafından tespit edilmeden Selenium kullanmak için özel WebDriver
import pyperclip  # Panoya (clipboard) metin kopyalayıp yapıştırmak için kullanılır

### sms atma fonksiyonu



##################### Whatsapp fonksiyonları ############################

from multiprocessing import Lock

# Modül seviyesinde bir Lock nesnesi oluşturun, bu nesnenin oluşturulma amacı bir whatsapp hesabı
# iki tane tarayıcıda açmaya çalıştığın bozukluklar olması ve işlem yapılamaması
whatsapp_lock = Lock()

def create_webdriver_with_profile(chrome_profile_path: str = "", 
                                  profile_default: int = 1, 
                                  headless: bool = False, 
                                  language: str = "en") -> webdriver:
    """
    Creates a WebDriver object using Chrome with a specified user profile.

    - ### Parameters:

        - chrome_profile_path (str): The file path to the Chrome user profile to be used.
        
        - If `chrome_profile_path` is not provided, it fetches the path from environment variables.
        profile_default (int): The default profile to use.
            - 1 for primary
            - 2 for secondary
            
        - headless (bool): Whether to run Chrome in headless mode. Defaults to False.
        - language (str): Language for the browser. Defaults to "en" (English).

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

    # Tarayıcı dilini ayarlıyoruz.
    options.add_argument(f"--lang={language}")
    
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

def log_in_with_link(phone_country_code: str ,phone_number: str, receiver_email: str, driver: webdriver, timeout: int = 300) -> bool:
    """
    Initiates a semi-automated login process to WhatsApp Web using your phone number,
    and sends the generated verification code to your email so you can complete the login manually from your phone.

    This function is useful when you're not in front of your computer but still want to
    start the login process and get notified with the verification code.

    - ### Parameters:

        - **phone_country_code** (*str*):  
            Your country code without the '+' sign (e.g., "90" for Turkey).

        - **phone_number** (*str*):  
            Your WhatsApp phone number without the country code (e.g., "5321234567").

        - **receiver_email** (*str*):  
            The email address where the 8-digit WhatsApp verification code will be sent.

        - **driver** (*webdriver*):  
            A Selenium WebDriver instance used to interact with WhatsApp Web.

        - **timeout** (*int, optional*):  
            Maximum time (in seconds) to wait for elements on the page to load. Default is 300.

    - ### Returns:

        - **True**: If the verification code is successfully retrieved from the screen and sent via email.  
        - **False**: If the process fails at any step (e.g., elements not found, timeout, etc.).

    - ### How It Works:

        1. Navigates to WhatsApp Web and selects the **"Log in using phone number"** option.
        2. Enters the `phone_country_code` and `phone_number`.
        3. Proceeds through the flow until WhatsApp displays an **8-digit verification code** on the screen.
        4. Extracts that code and sends it to your `receiver_email`.

    - ### ⚠️ What You Must Do (After Receiving the Code):

        Once you receive the email with the 8-digit code, follow these steps **from your own phone**:

        1. Open the WhatsApp app.
        2. Go to **Settings > Linked Devices**.
        3. Tap **"Link a Device"**.
        4. Choose the option **“Link with phone number”** (instead of QR).
        5. Enter your own phone number (same as in this function).
        6. WhatsApp will ask for an **8-digit code** — enter the code that was sent to your email.
        7. Once entered correctly, WhatsApp Web will automatically complete the login.

        ✅ You don’t need to be at your computer — WhatsApp Web will stay open once you link it.

    - ### Notes:

        - This is a **semi-automated login** method. The function starts the process and delivers the code,
          but you must finalize it from your phone.
        - Useful when you want to link a device remotely or can't scan a QR code.
        - The code is valid for a short time. Try to complete the process as soon as possible after receiving the email.

    - ### Example Usage:

        ```python
        success = log_in_with_link(
            phone_country_code="90",
            phone_number="5321234567",
            receiver_email="me@example.com",
            driver=my_webdriver
        )
        if success:
            print("Verification code was sent via email.")
        else:
            print("Something went wrong during the login process.")
        ```

    """
    max_attempts = 3
    attempt = 0

    while attempt < max_attempts:
        try:

            finding_link = WebDriverWait(driver, timeout).until(
                EC.any_of(
                    EC.presence_of_element_located((By.XPATH, "//*[contains(text(), 'Log in with phone number')]")),
                    EC.presence_of_element_located((By.XPATH, "//*[contains(text(), 'Telefon numarası kullanarak giriş yapın')]"))
                )
            )

            finding_link.click()
            # Butonu bul ve tıkla
            button = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, "//button[.//div[text()='United States']]"))
            )
            button.click()
            break
        except:
            attempt += 1
            driver.refresh()
            time.sleep(3)

    if attempt == max_attempts:
        return False
        

    attempt0 = 0
    max_attempts0 = 3
    while attempt0 < max_attempts0:
        try:
            # İlk yöntemi dene: Direkt role="textbox" olan elementi bul
            textbox = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, "//div[@role='textbox']"))
            )
            print("Textbox role ile bulundu!")
        except:
            try:
                # İlk yöntem başarısız olursa ikinci yöntemi dene: data-icon='search' kullanarak textbox'ı bul
                textbox = WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located(
                        (By.XPATH, "//span[@data-icon='search']/ancestor::div/following-sibling::div//div[@role='textbox']")
                    )
                )
                print("Textbox data-icon yöntemiyle bulundu!")
            except Exception as e:
                print(f"Textbox bulunamadı! Hata: {e}")
                textbox = None  # Textbox bulunamazsa None olarak bırak
                return False

        # Eğer textbox bulunduysa içine metni yaz
        if textbox:
            try:
                textbox.send_keys(phone_country_code)
                print("phone_country_code başarıyla yazıldı!")
            except Exception as e:
                print(f" phone_country_code yazılamadı! Hata: {e}")
                return False
        

        # Listbox'ı bul
        try:
            listbox = driver.find_element(By.XPATH, "//div[@role='listbox']")
        except:
            print("Listbox bulunamadı!")
            return False

        found = False
        scroll_attempts = 0  # Maksimum kaydırma sayısı
        step = 7  # Kaç öğe kaydıracağını belirler

        while not found and scroll_attempts < 10:  # 10 kere kaydırmayı deneyecek
            # Açılan menüde ülke telefon kodlarını içeren öğeleri bul
            country_divs = WebDriverWait(listbox, 10).until(
                EC.presence_of_all_elements_located((By.XPATH, "//div[contains(text(), '+')]"))
            )

            if not country_divs:
                print("Liste öğeleri bulunamadı, çıkılıyor...")
                break

            for i in range(0, len(country_divs), step):  # 7'şer 7'şer kaydır
                try:
                    div = country_divs[i]
                    driver.execute_script("arguments[0].scrollIntoView({block: 'nearest'});", div)  # Öğeyi kaydır
                    time.sleep(0.3)  # Sayfanın kaydırılmasını bekle

                    # **Şu anki tüm görünen öğeleri tekrar al ve kontrol et**
                    visible_items = listbox.find_elements(By.XPATH, ".//div[@role='listitem']")
                    for item in visible_items:
                        text = item.text.strip()
                        if text.endswith(phone_country_code):  # Eğer metin "380" ile bitiyorsa
                            print(f"Bulundu: {text} - Tıklanıyor...")
                            ActionChains(driver).move_to_element(item).click().perform()
                            found = True
                            break

                    if found:
                        break
                        
                except Exception as e:
                    print(f"Hata oluştu: {e}")

            if not found:
                print(f"{phone_country_code} bulunamadı, kaydırılıyor... ({scroll_attempts + 1})")
                scroll_attempts += 1

        if not found:
            print(f"{phone_country_code} bulunamadı, maksimum kaydırma sınırına ulaşıldı.")

        try:
            # Telefon numarası input elementini bul
            phone_input = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, "//input[@aria-label='Type your phone number.']"))
            )
            

            # Input'un değerini al ve başındaki '+' işaretini kaldır
            input_value = phone_input.get_attribute("value").replace("+", "").strip()
            

            # Birebir eşleşme kontrolü
            if input_value == phone_country_code:
                break
            
            attempt0 += 1
        except Exception as e:
            print(f"Telefon numarası inputu bulunamadı veya hata oluştu! Hata: {e}")
            attempt0 += 1

    if attempt0 == max_attempts0:
        return False


    try:
        # Input alanını bul
        phone_input = WebDriverWait(driver, timeout).until(
                    EC.presence_of_element_located((By.XPATH, "//input[@aria-label='Type your phone number.']"))
                )

        # Önce input'u temizle (eğer gerekirse)
        phone_input.clear()
        time.sleep(0.5)

        # Yeni değeri yaz
        phone_input.send_keys(phone_number)

        print(f"Numara başarıyla yazıldı: {phone_number}")

    except Exception as e:
        print(f"phone_input Elementi bulunamadı veya hata oluştu: {e}")
        return False

    # **Next butonuna tıklama ekleniyor**
    try:
        next_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//button[div/div[text()='Next']]"))
        )
        next_button.click()
        print("Next butonuna başarıyla tıklandı.")
    except Exception as e:
        print(f"Next butonu bulunamadı veya tıklanamadı: {e}")
        return False
    
    # **Doğrulama kodunu bul**
    try:
        # **Elementi bul**
        code_element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//div[@aria-details='link-device-phone-number-code-screen-instructions']"))
        )

        # **JavaScript ile `data-link-code` değerini al**
        verification_code = driver.execute_script("return arguments[0].getAttribute('data-link-code');", code_element)

        if verification_code:
            verification_code = verification_code.replace(",", "")  # Virgülleri kaldır
            print(f"Doğrulama kodu: {verification_code}")
        else:
            print("Doğrulama kodu bulunamadı!")

    except Exception as e:
        print(f"Hata oluştu: {e}")
        return False
    
    if not verification_code:
        return False
    
    try:
        Subject ="Whatsapp Doğrulama Kodu"
        body = f"Whatsapp doğrulama kodu: {verification_code}"
        
        send_email(Subject, body, receiver_email)
        return True
    
    except Exception:
        print("E-posta gönderiminde hata oluştu!")
        return False
    

def check_for_qr_code(driver: webdriver, phone_country_code: str = None, phone_number: str = None, receiver_email: str = None, timeout: int = 300) -> bool:
    """
    Checks if WhatsApp Web requires authentication, and within a configurable timeout, either waits for a QR code scan manually or attempts login via email verification if phone number, phone country code, and email are provided.

    This function opens WhatsApp Web using the provided Selenium WebDriver instance and waits for one of the following:
    - If the user is already logged in, it detects the chat screen and returns `False`.
    - If login is required and the parameters `phone_country_code`, `phone_number`, and `receiver_email` are provided,
    the function attempts to initiate a **semi-automated login** by retrieving a verification code and sending it via email.
    - If no login parameters are provided, it waits for a QR code to be scanned manually.

    > ℹ️ If an email-based login is attempted, the verification code must be manually entered by the user from their mobile device.
    > For a detailed explanation of this process, **refer to the `log_in_with_link` function's documentation**.

    ---
    
    ### Parameters:
    - **driver** (*WebDriver*): A Selenium WebDriver instance used to interact with WhatsApp Web.
    - **phone_country_code** (*str, optional*): The country code of the phone number to be used for login with an email-based verification code.
    - **phone_number** (*str, optional*): The phone number associated with the WhatsApp account.
    - **receiver_email** (*str, optional*): The email address where the verification code will be sent if logging in via email.
    - **timeout** (*int, optional*): Maximum wait time in seconds for QR code scan or chat screen detection.
                                      Default is 300 seconds.

    ### Returns:
    - **bool**:
      - `True`: If a QR code is present and needs to be scanned for login.
      - `False`: If the user is already logged in and the chat screen is displayed.
      - `-1`: If neither the QR code nor the chat screen could be found.
      - `-2`: If an error occurs during execution.
      - `-3`: Sync or loading progress got stuck (e.g., no percentage or message count change detected).
    
    ### Notes:
    - If a QR code is detected, the function waits up to **300 seconds** for the user to scan it and log in.
    - If **phone_country_code, phone_number, and receiver_email** are provided, an email-based login method is attempted instead of QR scanning.
    - If the chat screen appears within the waiting period, it returns `False`, indicating a successful login.
    - If no expected elements are found, the function returns `-1` as a fallback.
    """

    
    with whatsapp_lock:  # Kilidi kullanarak işlem yap
        try:
            # Web sayfasını aç
            driver.get("https://web.whatsapp.com")
            prev_percentage = None  # İlk yüzde değerini saklamak için

            while True:
                # QR kodunu veya profil ekranını aynı anda bekle
                element = WebDriverWait(driver, timeout).until(
                    EC.any_of(
                        EC.presence_of_element_located((By.XPATH, "//*[contains(text(), 'Point your phone at this screen to scan the QR code')]")),
                        EC.presence_of_element_located((By.XPATH, "//*[contains(text(), 'Telefonunuzu bu ekrana doğrultarak QR kodunu tarayın')]")),
                        EC.presence_of_element_located((By.CSS_SELECTOR, "div[title='Chats']")),
                        EC.presence_of_element_located((By.CSS_SELECTOR, "div[title='Sohbetler']")),
                        EC.presence_of_element_located((By.XPATH, "//*[contains(text(), 'Loading your chats')]")),
                        EC.presence_of_element_located((By.XPATH, "//*[contains(text(), 'Sohbetler yükleniyor')]")),
                        EC.presence_of_element_located((By.XPATH, '//div[text()="Syncing chats..."]')),
                        EC.presence_of_element_located((By.XPATH, '//div[text()="Sohbetler senkronize ediliyor..."]')),
                        EC.presence_of_element_located((By.XPATH, '//div[text()="Sohbetler eşitleniyor..."]'))
                    )
                )
                text = element.text.strip()
                if "Loading your chats" in text or "Sohbetler yükleniyor" in text:
                    match = re.search(r"\[(\d+)%\]", text)  # Yüzde işaretinden sonraki sayıyı al
                    if match:
                        current_percentage = int(match.group(1))
                        print(f"Mevcut yüklenme yüzdesi: {current_percentage}%")

                        # İlk defa yüzdeyi bulursa `prev_percentage` olarak ata
                        if prev_percentage is None:
                            prev_percentage = current_percentage
                            try:
                                WebDriverWait(driver, timeout).until(
                                    EC.any_of(
                                        EC.presence_of_element_located((By.XPATH, "//*[contains(text(), 'Point your phone at this screen to scan the QR code')]")),
                                        EC.presence_of_element_located((By.XPATH, "//*[contains(text(), 'Telefonunuzu bu ekrana doğrultarak QR kodunu tarayın')]")),
                                        EC.presence_of_element_located((By.CSS_SELECTOR, "div[title='Chats']")),
                                        EC.presence_of_element_located((By.CSS_SELECTOR, "div[title='Sohbetler']"))
                                    )
                                )
                                break # Mesajlar yüklendi döngüden çık
                            except:  # Eğer element bulunamadıysa hata mesajı ver ve döngüden çık
                                pass

                            continue
                        
                        # Eğer ilerleme varsa beklemeye devam et
                        if current_percentage > prev_percentage:
                            prev_percentage = current_percentage  # Yeni yüzdeyi kaydet
                            try:
                                WebDriverWait(driver, timeout).until(
                                    EC.any_of(
                                        EC.presence_of_element_located((By.XPATH, "//*[contains(text(), 'Point your phone at this screen to scan the QR code')]")),
                                        EC.presence_of_element_located((By.XPATH, "//*[contains(text(), 'Telefonunuzu bu ekrana doğrultarak QR kodunu tarayın')]")),
                                        EC.presence_of_element_located((By.CSS_SELECTOR, "div[title='Chats']")),
                                        EC.presence_of_element_located((By.CSS_SELECTOR, "div[title='Sohbetler']"))
                                    )
                                )
                                break # Mesajlar yüklendi döngüden çık
                            except:  # Eğer element bulunamadıysa hata mesajı ver ve döngüden çık
                                pass
                            continue  # Döngüye devam et

                        else:
                            print("Bir sebepten dolayı İlerleme durdu.")
                            return -3 # Eğer ilerleme yoksa hata kodu döndür 


                elif "Syncing chats..." in text or "Sohbetler senkronize ediliyor..." in text  or "Sohbetler eşitleniyor..." in text:
                    
                    # 2. Aynı kapsayıcı (parent) içinde yer alan bir sonraki div'i al ("52 of 180 messages" olan)
                    parent = element.find_element(By.XPATH, './..')
                    info_div = parent.find_elements(By.TAG_NAME, 'div')[1]  # 0: syncing_div, 1: info_div
                    
                    # 3. İlk mesaj durumunu al
                    text_before = info_div.text  # Örn: "52 of 180 messages"
                    numbers_before = list(map(int, re.findall(r'\d+', text_before)))
                    print("numbers_before:",numbers_before)

                    # 4. Kısa bir süre bekle (senkronizasyon ilerliyor mu bakalım)
                    try:
                        WebDriverWait(driver, timeout).until(
                            EC.any_of(
                                EC.presence_of_element_located((By.XPATH, "//*[contains(text(), 'Point your phone at this screen to scan the QR code')]")),
                                EC.presence_of_element_located((By.XPATH, "//*[contains(text(), 'Telefonunuzu bu ekrana doğrultarak QR kodunu tarayın')]")),
                                EC.presence_of_element_located((By.CSS_SELECTOR, "div[title='Chats']")),
                                EC.presence_of_element_located((By.CSS_SELECTOR, "div[title='Sohbetler']"))
                            )
                        )
                        break # Mesajlar yüklendi döngüden çık
                    except:  # Eğer element bulunamadıysa hata mesajı ver ve döngüden çık
                        pass
                    
                    # 5. Son durumu al
                    text_after = info_div.text
                    numbers_after = list(map(int, re.findall(r'\d+', text_after)))

                    # 6. Karşılaştır ve sonucu yazdır
                    print(f"Önce: {numbers_before} — Sonra: {numbers_after}")
                    if numbers_before != numbers_after:
                        print("Mesaj sayısı değişiyor, senkronizasyon devam ediyor.")
                    else:
                        print("Mesaj sayısı sabit, ya tamamlandı ya da takıldı.")
                        break

                else:
                    break
            
            # QR kodu varsa true, profil ekranı varsa false döndür
            qr_code_present = driver.find_elements(By.XPATH, "//*[contains(text(), 'Open WhatsApp on your phone')]")
            if not qr_code_present:
                qr_code_present = driver.find_elements(By.XPATH, "//*[contains(text(), 'Telefonunuzu bu ekrana doğrultarak QR kodunu tarayın')]")
            
            profile_present = driver.find_elements(By.CSS_SELECTOR, "div[title='Chats']")
            if not profile_present:
                profile_present = driver.find_elements(By.CSS_SELECTOR, "div[title='Sohbetler']")
            
            if qr_code_present:
                print("QR kodu yükleniyor.")
                # QR kodun yüklenmesini bekle
                WebDriverWait(driver, timeout).until(
                    EC.presence_of_element_located((By.XPATH, "//*[@aria-label='Scan this QR code to link a device!']"))
                )

                condition = phone_country_code and phone_number and receiver_email
                if condition:    
                    print(f"Whatsapp'ınıza giriş yapabilmeniz için doğrulama kodu, {receiver_email} hesabına 'Whatsapp Doğrulama Kodu' konulu mail olarak gönderiliyor...")
                    log_in = log_in_with_link(phone_country_code, phone_number, receiver_email, driver, timeout=timeout)
                    print(f"Doğrulama kodu, {receiver_email} hesabına 'Whatsapp Doğrulama Kodu' konulu mail olarak gönderildi, {timeout} saniye de Doğrulama kodunu ile Whatsapp'a giriş yapman için bekleniyor. Eğer giriş yaparsan program devam edecek, yapmazsan da kapanacak.")
                    
                    if not log_in:
                        error_mesage = f"phone_number:+{phone_country_code} {phone_number}-receiver_email:{receiver_email} için, log_in with_link fonksiyonunda hata var"
                        send_email("log_in with_link hatası", error_mesage)
                        send_email("log_in with_link hatası", error_mesage ,receiver_email=receiver_email)
                        print("WhatsApp'a girişte hata oluştu lütfen yetkiliyle iletişime geçin.")
                else:
                    print(f"QR kodu resmi yüklendi, {timeout} saniye de QR kodu okutup Whatsapp'a giriş yapman için bekleniyor. Eğer giriş yaparsan program devam edecek, yapmazsan da kapanacak.")
                
                # QR kodu bulunca timeout saniye de QR kodu okutup Whatsapp'a giriş yapman için bekleme
                profile_present = WebDriverWait(driver, timeout).until(
                    EC.any_of(
                        EC.presence_of_element_located((By.CSS_SELECTOR, "div[title='Chats']")),
                        EC.presence_of_element_located((By.CSS_SELECTOR, "div[title='Sohbetler']"))
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

def __search_and_select_chat(someone_or_group_name, driver, timeout: int = 100):
    """
    Searches for a WhatsApp chat (individual or group) by name or phone number on WhatsApp Web and selects it, if found.

    This function interacts with the WhatsApp Web search box using Selenium, searches for the provided contact or group name,
    waits for results, and attempts to click the best match (exact or partial). Works with both saved names and full phone numbers.

    ---

    Parameters:
        driver (WebDriver): 
            An instance of Selenium WebDriver.

        someone_or_group_name (str): 
            The full name of a contact, the name of a group, or a valid international phone number (e.g., "+905321234567"). If the input
            is a phone number, the function automatically presses `ENTER` to try direct access. If it’s a name, it looks through search 
            results for exact and then partial matches.

        timeout (int, optional): 
            Maximum time (in seconds) to wait for the search box, results, or chat interface to load.  
            Defaults to 100 seconds.
        

    Returns:
        bool: True if the chat is found and selected, False otherwise.

    Behavior:
        1. Waits for the WhatsApp search input field to appear.
        2. Clears it and types the given name or number.
        3. If the input is numeric (e.g., a phone number), it directly presses ENTER to attempt direct chat access.
        4. Waits for message input box to confirm that the chat screen has opened.
        5. If that fails, it searches through visible search results:
            - First tries **exact title match** using the `title` attribute.
            - If not found, tries **partial match** (`in` match, case-insensitive).
        6. If no relevant result is found, it waits for the “No chats, contacts or messages found” message.
        7. Handles `StaleElementReferenceException` during retries gracefully.
        ### Example:

        ```python
        found = __search_and_select_chat("Ahmet Yılmaz", driver)
        if found:
            print("Chat opened successfully!")
        else:
            print("Chat not found.")
    """

    try:
        # Arama kutusunu bul ve ismi gir
        search_box = WebDriverWait(driver, timeout).until(
            EC.presence_of_element_located((By.XPATH, "//div[@contenteditable='true'][@data-tab='3']"))
        ) 
        search_box.click()
        search_box.send_keys(Keys.CONTROL, "a") # Tüm metni seç
        search_box.send_keys(Keys.BACK_SPACE) # Sil
        search_box.send_keys(someone_or_group_name)

        # Eğer giriş yalnızca sayılardan oluşuyorsa veya '+' ile başlayıp sayılar içeriyorsa direkt Enter bas
        if someone_or_group_name.isdigit() or (someone_or_group_name.startswith("+") and someone_or_group_name[1:].isdigit()):
            search_box.send_keys(Keys.ENTER)
            # Mesaj kutusunun yüklenmesini bekleyin
            msg_box = WebDriverWait(driver, timeout).until(
                EC.presence_of_element_located((By.XPATH, '//div[@contenteditable="true"][@data-tab="10"]'))
            )

            if msg_box:
                return True # Böyle bir sohbet bulundu
                
            else:
                print("Böyle bir sohbet bulunamadı") 
                return False  # Böyle bir sohbet bulunamadı
    except:
        return False  # Arama kutusu bulunamadı

    try:
        # Arama sonuçlarını bekle
        WebDriverWait(driver, timeout).until(
            EC.presence_of_all_elements_located((By.XPATH, "//div[@aria-label='Search results.' or @aria-label='Arama sonuçları.']//span[@dir='auto']"))
        )
    except:
        return False  # Arama sonuçları bulunamadı

    # Elementler değişmiş olabilir, tekrar alalım
    for _ in range(3):  # 3 kere deneyecek
        try:
            results = driver.find_elements(By.XPATH, "//div[@aria-label='Search results.' or @aria-label='Arama sonuçları.']//span[@dir='auto']")
            if results:
                break  # Sonuçları başarılı şekilde aldıysa döngüyü kır
        except StaleElementReferenceException:
            continue  # Eğer element kaybolduysa tekrar dene

    if results:
        # Tam eşleşme kontrolü
        for r in results:
            try:
                # print(r.get_attribute("title"))
                if r.get_attribute("title") == someone_or_group_name:
                    r.click()
                    print(f"Tam eşleşme bulundu ({r.get_attribute('title')}) ve seçildi")
                    return True  # Tam eşleşme bulundu ve seçildi
            except StaleElementReferenceException:
                continue  # Eğer element geçersiz olduysa diğerlerine bak

        # İçerenleri kontrol et
        results = driver.find_elements(By.XPATH, "//div[@aria-label='Search results.' or @aria-label='Arama sonuçları.']//span[@dir='auto']")
        for r in results:
            try:
                if someone_or_group_name.casefold() in r.get_attribute("title").casefold():
                    r.click()
                    print(f"{someone_or_group_name} Kısmi olarak {r.get_attribute('title')} ile eşleşti ve seçildi")
                    return True  # Kısmi eşleşme bulundu ve seçildi
            except StaleElementReferenceException:
                continue  # Eğer element kaybolduysa diğerlerine bak

    # 'No chats, contacts or messages found' kontrolü
    no_results_element = WebDriverWait(driver, timeout).until(
        EC.presence_of_element_located((By.XPATH,"//span[contains(text(), 'No chats, contacts or messages found') or contains(text(), 'Sohbet, kişi veya mesaj bulunamadı')]"))
    )

    if no_results_element:
        print("Böyle bir sohbet bulunamadı")
        return False  # Böyle bir sohbet bulunamadı

    print("Beklenmeyen bir durum oluştu")
    return False  # Beklenmeyen bir durum oluştu

def send_message_to_someone_or_group(someone_or_group_name: str, message: str, driver: webdriver, timeout: int = 300) -> tuple[bool, Exception | None]:
    """
    Sends a uniquely trackable WhatsApp message to a specific contact or group by **name or phone number** using Selenium WebDriver, with a configurable timeout.

    - ### Parameters:
        
        - someone_or_group_name (str): 
            The name **or full phone number (e.g. "+905xxxxxxxxx")** of the WhatsApp contact or group 
            to which the message will be sent. The contact does not need to be saved in the address book 
            as long as the phone number is valid.

        - message (str):
            The message content to be sent. A unique marker will be automatically prepended to the message 
            for delivery verification.

        - driver (WebDriver): 
            An instance of Selenium WebDriver already logged into WhatsApp Web.

        - timeout (int, optional):  
            The maximum number of seconds to wait for required elements (search box, message box, etc.) to load.  
            Default is 300 seconds.

    - ### Returns:

        tuple: (success: bool, error: Exception or None)
            - True if the message is successfully sent and confirmed as delivered.
            - False if sending fails or an error occurs.
            - Returns the caught Exception object if any error is raised, otherwise None.

    - ### Functionality:

        1. Searches for the contact or group using the provided name or phone number via the WhatsApp search box.
        2. Waits for the message input box to become available (within the timeout).
        3. Generates a unique marker using a base-5 Unicode conversion and prepends it to the message.
        4. Formats the message content and pastes it using `CTRL + V`, then sends it using `ENTER`.
        5. Waits for the clock icon (`msg-time`) to appear (indicating sending is in progress).
        6. Waits until the clock icon disappears and checks if a check icon (`msg-check` or `msg-dblcheck`) appears in the specific message row that contains the unique marker.
        7. If the icon is found, confirms the message was delivered successfully. Otherwise, raises a timeout exception.

    - ### Notes:

        - The unique marker allows the script to verify that the specific message was sent and not just any recent message.
        - The check for WhatsApp delivery icons ensures that the message was not stuck or failed during sending.
        - Uses a thread-safe lock (`whatsapp_lock`) to prevent concurrency issues when multiple threads attempt to send messages simultaneously.

    - ### Exceptions:

        - If any step fails (element not found, timeout, unexpected errors), an exception is caught and printed with a full traceback.
        - The function returns `False` and the exception instance in such cases.

    - ### Example:

        driver = webdriver.Chrome()
        success, error = send_message_to_someone_or_group("+905551234567", "Test mesajı", driver)
        if success:
            print("Mesaj gönderildi!")
        else:
            print(f"Mesaj gönderilemedi: {error}")
    """
    
    with whatsapp_lock:  # Kilidi kullanarak işlem yap
        # Grup adına göre grubu bulma ve tıklama
        try:

            if __search_and_select_chat(someone_or_group_name, driver):
                print("Grup bulundu ve açılıyor")
        
            # Mesaj kutusunun yüklenmesini bekleyin
            msg_box = WebDriverWait(driver, timeout).until(
                EC.presence_of_element_located((By.XPATH, '//div[@contenteditable="true"][@data-tab="10"]'))
            )
            print("Mesaj kutusu bulundu, mesaj gönderiliyor...")
            
            
            # 0 ile 10^10 arasında rastgele bir sayı oluştur
            random_number = random.randint(0, 10**10)

            # Benzersiz bir marker oluştur 
            unique_marker = to_custom_base5_with_unicode(random_number)
            unique_line = unique_marker + message

            formatted_message = format_text_for_input(unique_line)
            #print(repr((formatted_message)))
            msg_box.send_keys(Keys.CONTROL, 'v')
            msg_box.send_keys(Keys.ENTER)


            # Mesajın gönderilmesi için beklemmeye başlanıyor.

            # "msg-time" ikonunun bulmayı bekle
            WebDriverWait(driver, timeout).until(
                EC.visibility_of_element_located((By.XPATH, '//span[@data-icon="msg-time"]'))
            )

            # "msg-time" ikonunun kaybolmasını bekle
            WebDriverWait(driver, timeout).until(
                EC.invisibility_of_element_located((By.XPATH, '//span[@data-icon="msg-time"]'))
            )

            # Bu mesaj içinde 'msg-check' veya 'msg-dblcheck' ikonunu kontrol et
            sent_success_icon = WebDriverWait(driver, timeout).until(
                EC.presence_of_element_located(
                    (
                        By.XPATH,
                        f'(.//div[@role="row" and contains(string(.), "{unique_marker}")])[last()]//span[@data-icon="msg-check" or @data-icon="msg-dblcheck"]'
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


def send_file_to_someone_or_group(someone_or_group_name: str, file_path: str, driver: webdriver, timeout: int = 300) -> tuple[bool, Exception | None]:
    """
    Sends a file (e.g., image, video, PDF, document) to a specified WhatsApp group or `individual contact` (by name or phone number) using Selenium WebDriver.

    - ### Parameters:

        - someone_or_group_name (str): 
            The name **or phone number (e.g. "+905xxxxxxxxx")** of the WhatsApp group or individual contact 
            where the file will be sent. The function can send files to both groups and individual contacts, 
            even if the contact is not saved in your address book, as long as their full phone number is provided.

        - file_path (str): 
            The local file path of the file to be sent. Ensure the file exists at the specified 
            path.
            
        - driver (selenium.webdriver): 
            An active instance of Selenium WebDriver, with a logged-in session of WhatsApp Web.
        
        - **timeout** (*int, optional*):  
            Maximum time to wait for each step (search box, elements, send confirmation) in seconds.  
            Default is 300 seconds.

    - ### Returns:

        tuple:
            - (bool): True if the file was successfully sent, False otherwise.
            - (Exception or None): If an error occurs, it returns the exception object. 
              Otherwise, it returns None.

    - ### Workflow:

        1. The function first waits (up to `timeout` seconds) for the WhatsApp search box to load, 
           then searches for the group or contact by typing the provided `someone_or_group_name`.
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
            
            if __search_and_select_chat(someone_or_group_name, driver):
                print("Grup bulundu ve açılıyor")
        
            # Mesaj kutusunun yüklenmesini bekleyin
            msg_box = WebDriverWait(driver, timeout).until(
                EC.presence_of_element_located((By.XPATH, '//div[@contenteditable="true"][@data-tab="10"]'))
            )
            print("Mesaj kutusu bulundu.")
            
            
            # Ataç simgesine tıkla
            attach_button = WebDriverWait(driver, timeout).until(
                EC.any_of(
                    EC.presence_of_element_located((By.XPATH, '//button[@title="Attach" and @aria-label="Attach"]')),
                    EC.presence_of_element_located((By.XPATH, '//button[@title="Ekle" and @aria-label="Ekle"]'))
                )
            )
            attach_button.click()
            
            # Dosya yükleme elemanını bul ve dosyayı yükle
            file_input = WebDriverWait(driver, timeout).until(
                EC.presence_of_element_located((By.XPATH, "//input[@accept='image/*,video/mp4,video/3gpp,video/quicktime']"))
            )

            if os.path.isabs(file_path):
                absolute_file_path = file_path  # If it's already absolute, use it as is
            else:
                absolute_file_path = os.path.abspath(file_path)  # If it's relative, convert it to an absolute path

            file_input.send_keys(absolute_file_path)  # Dosya dosyasını yükle
            print("file_path bulundu.")

            # Gönder butonuna tıkla
            send_button = WebDriverWait(driver, timeout).until(
                EC.presence_of_element_located((By.XPATH, "//span[@data-icon='send']"))
            )
            send_button.click()

            # Mesajın gönderilmesi için bekleniyor.

            # "msg-time" ikonunun bulmayı bekle
            WebDriverWait(driver, timeout).until(
                EC.visibility_of_element_located((By.XPATH, '//span[@data-icon="msg-time"]'))
            )

            # "msg-time" ikonunun kaybolmasını bekle
            WebDriverWait(driver, timeout).until(
                EC.invisibility_of_element_located((By.XPATH, '//span[@data-icon="msg-time"]'))
            )

            # Bu mesaj içinde 'msg-check' veya 'msg-dblcheck' ikonunu kontrol et
            sent_success_icon = WebDriverWait(driver, timeout).until(
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

def notify_phone_number(
    someone_or_group_name: str,
    message: str,
    chrome_profile_path: str = "",
    headless: bool = False,
    my_phone_country_code: str = None,
    my_phone_number: str = None,
    my_receiver_email: str = None,
    timeout: int = 300
):
    """
    Sends a WhatsApp message to a specified contact or group (by name or phone number) via WhatsApp Web using a WebDriver, with an adjustable timeout.
    
    You can provide either the contact name or the full phone number (e.g. "+905xxxxxxxxx").
    Depending on the phone number provided, it uses different Chrome profiles for authentication.
    If the provided phone number is the user's own number, the function sends the message from 
    another WhatsApp account to avoid self-notification issues. This is done using the secondary 
    WhatsApp profile set by the 'CHROME_SECONDARY_WHATSAPP_PROFILE_PATH' environment variable. 
    For other phone numbers, it uses the primary WhatsApp profile defined by the 
    'CHROME_PRIMARY_WHATSAPP_PROFILE_PATH' environment variable.
    If login is required (QR code appears), and if the sender's phone and email details are provided, the function attempts an automatic login via email verification.
    Otherwise,If a QR code is required to log in and cannot be handled automatically, the function sends an email instructing the user to manually scan the QR code to proceed.
    
    - ### Parameters:

        - someone_or_group_name (str): 
            The name **or full phone number (e.g. "+905xxxxxxxxx")** of the WhatsApp group or individual contact 
            to which the message will be sent. The function supports sending messages even if the contact is not 
            saved in your address book, as long as their phone number is valid.

        - message (str): 
            The content of the message to be sent.

        - chrome_profile_path (str, optional): 
            The file path to the Chrome user profile to be used. If not provided, the function will 
            use environment variables for profile paths.
        
        - headless (bool, optional): 
            If True, runs the WebDriver in headless mode (without a GUI). Defaults to False.,
        
        - my_phone_country_cod (str, optional):  
            Your own country code (e.g. "90"). Used for automatic email-based login if QR is shown.

        - my_phone_number (str, optional):  
            Your own WhatsApp number. Used to detect self-messaging and for QR login automation.

        - my_receiver_email (str, optional):  
            Your email to receive verification code if QR-based login is required.

        - timeout (int, optional):  
            The maximum time (in seconds) to wait for elements to load or actions to complete.  
            Used when initializing the WebDriver. Default is 300.

    - ### Behavior:

        1. Checks if `someone_or_group_name` matches your own number (`MY_NUMBER` env variable).  
            If so, uses **secondary WhatsApp profile** to avoid self-messaging issues.
        2. Selects the appropriate Chrome profile directory based on whether the phone number 
        belongs to the user or another person:
            - If it's the user's phone number, uses the 'CHROME_SECONDARY_WHATSAPP_PROFILE_PATH' 
            environment variable to send the message from another WhatsApp account. If there 
            is no 'CHROME_SECONDARY_WHATSAPP_PROFILE_PATH', it uses 
            'CHROME_PRIMARY_WHATSAPP_PROFILE_PATH'.
            - Otherwise, uses the 'CHROME_PRIMARY_WHATSAPP_PROFILE_PATH' environment variable.
        3. If the 'chrome_profile_path' argument is provided, it overrides the default profile 
        selection.
        4. Creates a WebDriver instance with the selected Chrome profile, optionally running in 
        headless mode if specified.
        5. Calls `check_for_qr_code(...)` to determine login status:
            - If a QR code is shown **and `my_phone_country_code`, `my_phone_number`, and `my_receiver_email` are provided**, the function initiates a **semi-automated login** by sending a verification link or code to your email.  
              You can then complete the login from your own phone using that code — even if you're not at your computer.
            - If a QR code is shown but those details are **not** provided, the function sends an email instructing the user to manually scan the QR code on the screen.
            - If `-1` is returned, indicating that expected elements weren't found, an email is sent explaining the failure.
            - If `-2` is returned, indicating an unexpected error during QR code detection, an error email is sent as well.
        6. If logged in, sends the message using `send_message_to_someone_or_group(...)`.
        7. If message sending fails, sends an email with exception detail.
        8. WebDriver is always closed properly after action completes.

    - ### Raises:

        Sends an email notification in the following situations:

        - A QR code is detected, indicating that manual login is required.
        - `check_for_qr_code` returns `-1`, which means expected elements could not be found on the page.
        - `check_for_qr_code` returns `-2`, indicating an unexpected error occurred during QR detection.
        - The message fails to send due to any error (e.g. element not found, timeout, etc.).

    - ### Dependencies:

        - os.getenv: To fetch environment variables like phone number and Chrome profile paths.
        - create_webdriver_with_profile: To create a WebDriver instance with a specific Chrome profile.
        - check_for_qr_code: To check if a QR code is present on WhatsApp Web.
        - send_message_to_someone_or_group: To send a WhatsApp message to the specified number.
        - send_email: To send an email alert in case of errors.

    - ### Example usage:

        # 1. Send a simple message to a phone number
        notify_phone_number("+905321234567", "Hello, this is a test message.")

        # 2. Send a message in headless mode (no browser window pops up)
        notify_phone_number("+905321234567", "This is a headless test message.", headless=True)

        # 3. Send a message using a custom Chrome profile path
        notify_phone_number("+905321234567", "Sent using custom profile.", chrome_profile_path="C:/MyProfiles/WhatsAppProfile")

        # 4. Send a message to a contact saved with name instead of phone number
        notify_phone_number("John Doe", "Hey John, just checking in!")

        # 5. Full usage with QR login credentials
        notify_phone_number(
            "My Group",
            "Toplantı saat 3'te.",
            chrome_profile_path="C:/Profiles/Work",
            headless=True,
            my_phone_country_code="90",
            my_phone_number="5321234567",
            my_receiver_email="ben@mail.com",
            timeout=180
        )

        # 6. Send to your own number (will trigger secondary profile logic)
        notify_phone_number(os.getenv("MY_NUMBER"), "Self-check: system notification.")

        # 7. Send a message with a custom timeout value
        notify_phone_number("+905321234567", "Testing with timeout", timeout=120)
    """
        
    if chrome_profile_path == "":
        if someone_or_group_name == os.getenv('MY_NUMBER'): # Benim telefon numaramsa
            # Chrome profil dizini yolu klasörün içinde olucak şekilde ayarlanır kendiğinden.
            chrome_profile_path = os.getenv('CHROME_SECONDARY_WHATSAPP_PROFILE_PATH')
            if chrome_profile_path == "":
                chrome_profile_path = os.getenv('CHROME_PRIMARY_WHATSAPP_PROFILE_PATH')
        else:
            # Chrome profil dizini yolu klasörün içinde olucak şekilde ayarlanır kendiğinden.
            chrome_profile_path = os.getenv('CHROME_PRIMARY_WHATSAPP_PROFILE_PATH')
        
        if chrome_profile_path == "":
            raise ValueError("Profil yolu sağlanmadı ve ortam değişkenleri ayarlanmadı. ikisinden biri yapılmalı.")

    driver = create_webdriver_with_profile(chrome_profile_path, headless = headless, timeout = timeout)
    
    # QR kod var mı diye Fonksiyonu test etme varsa işlemlerin gerisini yapmadan bana uyarı E-maili atacak.
    qr_exists = check_for_qr_code(driver, phone_country_code=my_phone_country_code, phone_number=my_phone_number, receiver_email=my_receiver_email, timeout=timeout)
    if qr_exists is True:
        send_email("WhatsApp Login Alert","QR kod tarama işlemi gerekiyor. Lütfen programı yenileyin.")  # QR kod istendiğinde email gönder
    
    elif qr_exists == -1:
        send_email(f"Whatsapptan {someone_or_group_name} kişisine mesaj atılamadı.","qr_exists fonksiyonundan -1 döndü, yani Belirtilen elemanlar bulunamadı.")
    
    elif qr_exists == -2:
        send_email(f"Whatsapptan {someone_or_group_name} kişisine mesaj atılamadı.",f"qr_exists fonksiyonundan -2 döndü, except bloğuna düştü yani hata oluştu.")
    
    # Yoksa wpweb'deki benim mesajlarıma erişmiş demektir.
    else:
        check_sending, e = send_message_to_someone_or_group(someone_or_group_name, message, driver)
        driver.quit()  # Driver'ı kapat

        #bir önceki satır false ise yani gönderilemediyse alttaki satırı çalıştır.
        if not check_sending:
            send_email(f"Whatsapptan {someone_or_group_name} kişisine mesaj atılamadı.",str(e))



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



def get_last_message(someone_or_group_name: str, driver: webdriver, clean_invisible_chars: bool = True, timeout: int = 300,) -> str | None:
    """
    Fetch the last received message from a WhatsApp chat for a specific phone number or contact name, 
    with options for timeout control and invisible character cleaning.

    This function navigates to a WhatsApp Web chat for the specified phone number or contact name,
    waits until the chat is fully loaded, and retrieves the last received message
    (if any) from the other party. If the chat fails to load or no messages are present,
    it handles these scenarios gracefully and returns None.

    ---

    ### Parameters:

    - **someone_or_group_name** (*str*):  
    The phone number (e.g., "+905551234567") or contact/group name.  
    The contact does **not need to be saved** — a valid phone number is sufficient.

    - **driver** (*selenium.webdriver.WebDriver*):  
    A Selenium WebDriver instance controlling the browser session.

    - **clean_invisible_chars** (*bool, optional*):  
    If True, removes invisible Unicode characters (like zero-width space) from the final message.  
    Defaults to True.

    - **timeout** (*int, optional*):  
    Maximum time in seconds to wait for the chat interface and message elements to load.  
    Defaults to 300 seconds.

    ---

    ### Returns:

    - **str | None**:  
    The full text of the last received message from the other person or group.  
    Returns `None` if the chat fails to load or no messages are found.

    ---

    ### Steps:

    1. Opens the chat screen for the given phone number or contact name.
    2. Waits until the message input and both incoming and outgoing message elements are present.
    3. Collects all received messages (`message-in`) and filters out empty ones.
    4. If the last message contains a “read more” button, it clicks it to expand the message.
    5. Optionally cleans invisible characters if `clean_invisible_chars=True`.
    6. Returns the last complete message or None if nothing is available.

    ---

    ### Example Usage:

    ```python
    from selenium import webdriver

    driver = webdriver.Chrome()
    last_message = get_last_message("+905551234567", driver, clean_invisible_chars=True, timeout=180)

    if last_message:
        print("Last message received:", last_message)
    else:
        print("No messages found or chat failed to load.")
    """

    try:

        # kişi adına göre kişiyi bulma ve tıklama
        if __search_and_select_chat(someone_or_group_name, driver):
            print("Grup bulundu ve açılıyor")
    
        # Mesaj kutusunun yüklenmesini bekleyin
        msg_box = WebDriverWait(driver, timeout).until(
            EC.presence_of_element_located((By.XPATH, '//div[@contenteditable="true"][@data-tab="10"]'))
        )
        print("Mesaj kutusu bulundu.")

        # Wait until the chat interface has loaded by checking for incoming message elements
        WebDriverWait(driver, timeout).until(
            EC.presence_of_element_located((By.XPATH, '//div[contains(@class, "message-in")]'))
        )
        WebDriverWait(driver, timeout).until(
            EC.presence_of_element_located((By.XPATH, '//div[contains(@class, "message-out")]'))
        )
        print("Chat loaded successfully.")
        
        # Locate all incoming message elements within the chat
        message_elements = driver.find_elements(By.XPATH, '//div[contains(@class, "message-in") and contains(@class, "focusable-list-item")]//div[contains(@class, "_akbu")]/span')
        
        # Filter out empty messages
        valid_messages = [element.text for element in message_elements if element.text.strip()]

        if valid_messages:
            # Print all non-empty messages
            # for index, message in enumerate(valid_messages):
            #     print(f"Message {index}: {message}")
            
            # Get the last non-empty message
            last_message_text = valid_messages[-1]

            target_snippet = last_message_text[10:20].casefold()
            read_more_clicked = False
            while True:
                try:
                    xpath = f"""//div[contains(@class, 'copyable-text') 
                            and .//span[contains(normalize-space(), '{target_snippet}')]]
                            //div[contains(@class, 'read-more-button')]"""

                    read_more_buttons = WebDriverWait(driver, 1).until(
                        EC.presence_of_all_elements_located((By.XPATH, xpath))
                    )
                    read_more_buttons[0].click()
                    read_more_clicked = True
                except:
                    break

            # last_message_text'in güncellenmiş halini burada hesapla
            if read_more_clicked:
                updated_elements = driver.find_elements(
                    By.XPATH, '//div[contains(@class, "message-in") and contains(@class, "focusable-list-item")]//div[contains(@class, "_akbu")]/span'
                )
                updated_messages = [el.text for el in updated_elements if el.text.strip()]
                if updated_messages:
                    if clean_invisible_chars:
                        last_message_text = __clean_invisible_chars(updated_messages[-1])
                    else:
                        last_message_text = updated_messages[-1]

        else:
            print("No messages received from the other party.")
            raise Exception("No messages received from the other party.")
        

        print("Last received message:", last_message_text)
    except Exception as e:
        print(f"Error loading chat: {e}")
        last_message_text = None

    return str(last_message_text)


def get_whatsapp_chat_history(someone_or_group_name: str, driver: webdriver, clean_invisible_chars: bool = True, timeout: int = 300) -> list[dict]:
    """
    Retrieves the full chat history from a WhatsApp conversation using a contact's phone number or full saved name,
    with optional timeout control and invisible character cleaning.

    This function navigates to the chat with the specified contact (using either the phone number 
    or the full saved name) via the provided Selenium WebDriver, waits until the chat is fully loaded,
    extracts all incoming and outgoing messages, and optionally removes invisible Unicode characters
    (such as zero-width spaces) from the messages.It also automatically expands
    truncated messages hidden behind “read more” buttons.

    Args:
        
        someone_or_group_name (str): The full phone number (e.g., "+905551234567"), contact name, or group name.  
                                    It does **not** need to be saved in your WhatsApp contacts — if a valid phone 
                                    number is provided, it will still work.
        
        driver (webdriver): A Selenium WebDriver instance already logged into WhatsApp Web.
        
        clean_invisible_chars (bool, optional): If True (default), cleans invisible Unicode characters
                                                from each message.
        
        timeout (int, optional): Maximum time (in seconds) to wait for chat interface and message containers to load.  
                                        Defaults to 300 seconds.
                
    Returns:
        list[dict]: A list of dictionaries containing:
            - "sender": "Ben" if the message was sent by the user, "Karşı Taraf" otherwise.
            - "message": The text content of the message.

    Raises:
        Exception: If the chat cannot be found or no messages are retrieved.
    
    Notes:
        - Accepts both phone number and saved contact name as input.
        - Automatically expands messages hidden behind "read more" buttons.
        - Supports both individual and group chats.
        - Handles exceptions per message block to ensure partial recovery of chat history.

    Example:
        history = get_whatsapp_chat_history("+905312345678", driver)
        history_by_name = get_whatsapp_chat_history("Ahmet Yılmaz", driver)
        for msg in history:
            print(f"{msg['sender']}: {msg['message']}")
    """


    try:
        if __search_and_select_chat(someone_or_group_name, driver):
            print("Grup bulundu ve açılıyor")

        WebDriverWait(driver, timeout).until(
            EC.presence_of_element_located((By.XPATH, '//div[@contenteditable="true"][@data-tab="10"]'))
        )

        WebDriverWait(driver, timeout).until(
            EC.presence_of_element_located((By.XPATH, '//div[contains(@class, "message-in")]'))
        )
        WebDriverWait(driver, timeout).until(
            EC.presence_of_element_located((By.XPATH, '//div[contains(@class, "message-out")]'))
        )
        print("Chat fully loaded successfully.")

        # Tüm mesaj konteynerlerini al (hem gelen hem giden)
        message_containers = driver.find_elements(By.XPATH, '//div[contains(@class, "message-in") or contains(@class, "message-out")]')

        chat_history = []

        for container in message_containers:
            try:
                try:
                    # Mesaj metni span içinde bulunur
                    text_element = container.find_element(By.XPATH, './/div[contains(@class, "_akbu")]/span')
                    message = text_element.text.strip()
                    target_snippet = message[10:20].casefold()
                    read_more_clicked = False
                    while True:
                        try:
                            xpath = f"""//div[contains(@class, 'copyable-text') 
                                    and .//span[contains(normalize-space(), '{target_snippet}')]]
                                    //div[contains(@class, 'read-more-button')]"""

                            read_more_buttons = container.find_elements(By.XPATH, xpath)
                            read_more_buttons[0].click()
                            read_more_clicked = True
                        except:
                            break

                except Exception:
                    message = "Bilinmeyen içerik veya desteklenmeyen mesaj tipi"

                # last_message_text'in güncellenmiş halini burada hesapla
                if read_more_clicked:
                    updated_text_element = container.find_element(By.XPATH, './/div[contains(@class, "_akbu")]/span')
                    message = updated_text_element.text.strip()

                # Göndereni belirle
                if "message-out" in container.get_attribute("class"):
                    sender = "Ben"
                else:
                    sender = "Karşı Taraf"

                chat_history.append({
                    "sender": sender,
                    "message": message
                })
            except Exception as inner_e:
                print(f"Mesaj alınırken hata: {inner_e}")
                continue

        if chat_history:
            if clean_invisible_chars:
                # chat_history içindeki tüm mesajları temizle
                for msg in chat_history:
                    msg["message"] = __clean_invisible_chars(msg["message"])
            else:
                for msg in chat_history:
                    msg["message"] = msg["message"]
            
            print(f"{len(chat_history)} mesaj alındı.")
        else:
            print("Hiç mesaj bulunamadı.")
            raise Exception("Hiç mesaj bulunamadı.")

    except Exception as e:
        print(f"Error loading chat: {e}")
        chat_history = []

    return chat_history

def __clean_invisible_chars(text: str) -> str:
    """
    Removes invisible or zero-width Unicode characters from a given string.

    This is especially useful when processing text copied from WhatsApp or similar platforms,
    where hidden formatting characters such as zero-width spaces may be present, 
    which can break text comparison, logging, or data processing.

    ### Characters Removed:
    - \u200b (Zero Width Space)
    - \u200c (Zero Width Non-Joiner)
    - \u200d (Zero Width Joiner)
    - \u2060 (Word Joiner)
    - \ufeff (Byte Order Mark)

    ### Parameters:
    - **text** (*str*): The input string from which invisible characters will be removed.

    ### Returns:
    - **str**: The cleaned string with all invisible characters stripped.

    ### Example:
    ```python
    dirty = "Hello\u200bWorld"
    clean = __clean_invisible_chars(dirty)
    print(clean)  # Output: HelloWorld
    ```
    """
    invisible_chars = ['\u200b', '\u200c', '\u200d', '\u2060', '\ufeff']
    for char in invisible_chars:
        text = text.replace(char, '')
    return text

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
    msg['Subject'] = Header(subject, 'utf-8')  # E-postanın konusunu belirle

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
                import os

                # API kimlik bilgilerini yükle
                api_id = os.getenv('MY_TELEGRAM_API_ID')
                api_hash = os.getenv('MY_TELEGRAM_API_HASH')

                client = TelegramClient("my_telegram_session", api_id, api_hash)
                client.start()

                for dialog in client.iter_dialogs():
                    if dialog.is_user:
                        print(f"User Name: {dialog.name}, Chat ID: {dialog.id}")
                ```
            3. Look for the **positive numeric ID** corresponding to the user.

            ##### For Groups:
            1. Add your Telegram account to the group.
            2. use the similar Python code above to fetch its numeric ID.
                  ```python
                from telethon.sync import TelegramClient
                import os

                # API kimlik bilgilerini yükle
                api_id = os.getenv('MY_TELEGRAM_API_ID')
                api_hash = os.getenv('MY_TELEGRAM_API_HASH')

                # Telegram istemcisini başlat
                client = TelegramClient("my_telegram_session", api_id, api_hash)
                client.start()

                # Tüm diyalogları listele
                for dialog in client.iter_dialogs():
                    if dialog.is_group:  # Grup ID'lerini kontrol eder
                        print(f"Group Name: {dialog.name}, Group ID: {dialog.id}")
                    elif dialog.is_channel:  # Kanal ID'lerini kontrol eder
                        print(f"Channel Name: {dialog.name}, Channel ID: {dialog.id}")
                ```
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
    
def get_telegram_chat_id(
    recipient_username: str = None,
    recipient_phone: str = None,
    recipient_group_name: str = None,
    recipient_full_name: str = None,
    api_id=None,
    api_hash=None
) -> int | None:
    """
    Resolves and returns the Telegram chat ID from one of the provided identifiers.

    You can provide:
    - recipient_username: Telegram username (e.g. '@exampleuser' or 'exampleuser')
    - recipient_phone: Phone number including country code (e.g. '+905500000000')
    - recipient_group_name: Visible name of the group or channel you are a member of (not @username, just display name)
    - recipient_full_name: Full name of the user as saved in your Telegram contacts 
                           (e.g. 'Ali Veli' — exactly how it's saved in your Telegram contact list)

    The function tries to resolve the chat ID in the following order:
    1. Username
    2. Phone number
    3. Group or channel name (only supergroups)
    4. Full name (from your contacts)

    Parameters:
        recipient_username (str): Telegram username
        recipient_phone (str): Phone number with country code
        recipient_group_name (str): Display name of group or channel
        recipient_full_name (str): Contact name as saved in your Telegram
        api_id (str or int, optional): Telegram API ID (from env if not provided)
        api_hash (str, optional): Telegram API HASH (from env if not provided)

    Returns:
        int or None: The resolved chat ID, or None if not found.
    """

    def normalize_string(s):
        return unicodedata.normalize("NFKC", s).strip().lower()

    if api_id is None:
        api_id = os.getenv("MY_TELEGRAM_API_ID")
    if api_hash is None:
        api_hash = os.getenv("MY_TELEGRAM_API_HASH")

    if not api_id or not api_hash:
        print("HATA: API ID veya API HASH eksik. Parametre olarak girin veya ortam değişkeni tanımlayın.")
        return None

    try:
        with TelegramClient("resolve_id_session", api_id, api_hash) as client:
            # 1. Username
            if recipient_username:
                try:
                    entity = client.get_entity(recipient_username.lstrip("@"))
                    return entity.id
                except Exception as e:
                    print(f"Username ile bulunamadı: {e}")

            # 2. Phone
            if recipient_phone:
                try:
                    entity = client.get_entity(recipient_phone)
                    return entity.id
                except Exception as e:
                    print(f"Telefon numarası ile bulunamadı: {e}")

            # 3. Group Name (only supergroups)
            if recipient_group_name:
                try:
                    dialogs = client.get_dialogs()
                    target_name = normalize_string(recipient_group_name)
                    for dialog in dialogs:
                        if dialog.is_group or dialog.is_channel:
                            dlg_name = normalize_string(dialog.name)
                            if dlg_name == target_name and str(dialog.id).startswith("-100"):
                                return dialog.id
                    print("Süper grup ismiyle eşleşen bir sohbet bulunamadı.\n")
                except Exception as e:
                    print(f"Grup araması sırasında hata oluştu: {e}")

            # 4. Full Name (rehber taraması)
            if recipient_full_name:
                try:
                    result = client(functions.contacts.GetContactsRequest(hash=0))
                    for user in result.users:
                        full_name = ((user.first_name or "") + " " + (user.last_name or "")).strip()
                        if normalize_string(recipient_full_name) in normalize_string(full_name):
                            return user.id
                    print("Rehberde bu isimle eşleşen bir kullanıcı bulunamadı.")
                except Exception as e:
                    print(f"Rehber araması sırasında hata oluştu: {e}")

    except UsernameNotOccupiedError:
        print("Kullanıcı adı Telegram'da kayıtlı değil.")
    except PeerIdInvalidError:
        print("Geçersiz kullanıcı/grup/kanal.")
    except Exception as e:
        print(f"Beklenmeyen bir hata oluştu: {e}")

    return None

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
    
def to_custom_base5_with_unicode(number):
    """
    Converts a non-negative integer into a custom base-5 format using specific invisible Unicode characters.

    **Custom Base-5 Unicode Mapping:**
    - 0 -> \u200E (Left-to-Right Mark)
    - 1 -> \u200B (Zero Width Space)
    - 2 -> \u200C (Zero Width Non-Joiner)
    - 3 -> \u200D (Zero Width Joiner)
    - 4 -> \u2060 (Word Joiner)

    The function returns the converted number in the custom base-5 format, where:
    - Base-5 digits (0, 1, 2, 3, 4) are replaced with the corresponding Unicode characters.
    - The result is constructed by repeatedly dividing the number by 5 and recording the remainders.

    **Parameters:**
    - `number` (int): A non-negative integer to be converted.

    **Returns:**
    - str: The number in the custom base-5 format using Unicode characters.

    **Raises:**
    - ValueError: If the input number is negative.

    **Examples:**
    ```python
    print(repr(to_custom_base5_with_unicode(0)))   # Output: '\u200E'
    print(repr(to_custom_base5_with_unicode(4)))   # Output: '\u2060'
    print(repr(to_custom_base5_with_unicode(5)))   # Output: '\u200B\u200E'
    print(repr(to_custom_base5_with_unicode(23)))  # Output: '\u200C\u200D'
    ```
    """
    if number < 0:
        raise ValueError("Number must be non-negative")
    if number == 0:
        return "\u200E"  # 0 yerine

    # 0-4 yerine Unicode karakterlerini kullanıyoruz
    unicode_map = ["\u200E", "\u200B", "\u200C", "\u200D", "\u2060"]  # 0, 1, 2, 3, 4 sırasıyla

    digits = []
    while number > 0:
        remainder = number % 5
        custom_digit = unicode_map[remainder]  # 0-4'ü Unicode karakterlerine eşliyoruz
        digits.append(custom_digit)
        number //= 5

    return "".join(reversed(digits))

def format_text_for_input(prompt, retries=5, delay=0.2, verbose=True):
    """
    Copies the given text to the clipboard and verifies it was correctly copied.

    This function is specifically designed for use cases where sending text directly via send_keys()
    may result in broken or incomplete input. For example, input fields in WhatsApp Web or ChatGPT
    may fail to render long strings correctly when sent character by character.

    Instead of sending the string directly, we copy it to the clipboard using pyperclip,
    then later paste it into the input field using CTRL+V with Selenium's send_keys.

    Typical usage:
        formatted = format_text_for_input(prompt)
        prompt_element.send_keys(Keys.CONTROL, 'v')
        prompt_element.send_keys(Keys.ENTER)

    Parameters:
        prompt (str): The text to copy to the clipboard.
        retries (int): Number of times to retry checking the clipboard. Default is 5.
        delay (float): Delay in seconds between retries. Default is 0.1.
        verbose (bool): Whether to print a warning if the clipboard value doesn't match. Default is True.

    Returns:
        str: The final text retrieved from the clipboard. May not match the original prompt if clipboard failed.

    Warning:
        If the clipboard content does not exactly match the input prompt after retries,
        a warning message is printed (if verbose=True), and the last clipboard content is returned anyway.
    """
    pyperclip.copy(prompt)
    
    for _ in range(retries):
        time.sleep(delay)
        formatted_prompt = pyperclip.paste()
        if prompt == formatted_prompt:
            return formatted_prompt

    if verbose:
        print("Uyarı: Panoya kopyalanan metin birebir aynı değil!")
    return formatted_prompt


##################### Cloudflare ve Bot Tespitine Duyarlı Tarayıcı Açma Araçları ############################


def manuel_giris_yap(URL):
    """
    Belirtilen URL'ye Chrome profiliyle gidip kullanıcıdan manuel giriş yapması istenir.
    Giriş tamamlandıktan sonra Enter'a basıldığında tarayıcı kapanır.
    """

    # Chrome seçenekleri yapılandırılır
    options = uc.ChromeOptions()

    # Kalıcı profil ve dizin ayarlarını uygula
    options.add_argument("--user-data-dir=C:\\SeleniumProfiller\\Profil")
    options.add_argument("--profile-directory=Default")

    print("🔐 Tarayıcı açılıyor...")
    print("📌 Lütfen aşağıdaki adımları önceden gerçekleştirmiş olun:")
    print("1. Google Chrome tarayıcısında şu iki adımı da tamamlayın:")
    print("   - Tarayıcı seviyesinde (profil kurulumu gibi) Google hesabınızla oturum açın.")
    print("   - gmail.com üzerinden Google hesabınıza manuel olarak giriş yapın.")
    print("2. Engelin geldiği siteye kullanıcı girişi yaparak sürekli sizi hatırlamasını sağlayın.\n")

    print("⚠️  **DİKKAT**")
    print("Tarayıcı üzerinde alışılmışın dışında işlemler (çok hızlı hareketler, çok sayıda pencere açma, farklı uzantılar kullanma vb.) yaparsanız,")
    print("Google ve benzeri sistemler bunu şüpheli davranış olarak algılayabilir ve hesaplarınız **askıya alınabilir / kalıcı olarak engellenebilir.**")
    print("🔄 Bu yüzden, bu tür işlemleri yaparken yeni oluşturulmuş test hesapları ile denemeler yapmanız şiddetle tavsiye edilir.\n")

    print("➡️ Şimdi giriş yapacağınız sayfa açılacak. Giriş yaptıktan sonra bu pencereye dönüp Enter'a basmanız yeterli.\n")

    # Tarayıcıyı başlat ve hedef URL'ye git
    driver = uc.Chrome(options=options)
    driver.get(URL)
    time.sleep(3)

    input("✅ Giriş yaptıysanız Enter'a basın, tarayıcı kapatılacak...")
    driver.quit()



def launch_undetected_bot_browser(URL: str, 
                                  selenium_profil: str = "C:\\SeleniumProfiller\\Profil", 
                                  profile_directory: str = "Default",
                                  language: str = "en", 
                                  headless: bool = False,
                                  manuel_giris: str = False):
    """
    Launches a Chrome browser using undetected_chromedriver to bypass bot detection systems.

    - ### Parameters:

        - `URL` (str): The web page to open immediately after launching the browser.
        - `selenium_profil` (str): Path to the user data directory for persistent profile storage.
        - `profile_directory` (str): Subdirectory name inside the profile folder (e.g., "Default", "Profile 1").
        - `language` (str): Language to set for the browser (e.g., "en", "tr"). Default is English.
        - `headless` (bool): Whether to launch the browser in headless mode. Default is False.
        - `manuel_giris` (bool): If True, opens the browser for manual login and closes it after confirmation.

    - ### Features:

        - Uses `undetected_chromedriver` to avoid detection by anti-bot systems.
        - Supports persistent profiles and custom Chrome profile directories.
        - Enables performance logging.
        - Sets language and user-agent for realistic browser behavior.
        - Option to perform manual login flow and close the browser after login.

    - ### Returns:
        - `WebDriver`: An initialized Chrome driver instance ready to use. If `manuel_giris=True`, returns `None` after closing the manual login session.

    - ### Example:

        ```python
        driver = launch_undetected_bot_browser(
            URL="https://example.com",
            selenium_profil="C:\\MyProfiles\\BotUser1",
            profile_directory="Profile 1",
            language="tr",
            headless=True
        )
        ```
    """
    if manuel_giris:
        # Eğer manuel giriş isteniyorsa tarayıcı açılır,
        # kullanıcı giriş yaptıktan sonra Enter'a basması beklenir.
        manuel_giris_yap(URL)

    # Chrome seçenekleri yapılandırılır
    options = uc.ChromeOptions()

    # Gereksiz eklentileri ve sınırlamaları kapat
    options.add_argument("--disable-extensions")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--start-maximized")

    # Kalıcı profil ve dizin ayarlarını uygula
    options.add_argument(f"--user-data-dir={selenium_profil}")
    options.add_argument(f"--profile-directory={profile_directory}")

    # Dil ve user-agent ayarları
    options.add_argument(f"--lang={language}")
    options.add_argument("--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36")

    # Headless (görünmez) mod isteniyorsa ekle
    if headless:
        options.add_argument("--headless=new")  # modern headless mode (Chrome 109+)

    # Performans logları için capability ayarları
    caps = DesiredCapabilities.CHROME.copy()
    caps["goog:loggingPrefs"] = {"performance": "ALL"}
    options.set_capability("goog:loggingPrefs", {"performance": "ALL"})

    # Tarayıcıyı başlat ve hedef URL'ye git
    driver = uc.Chrome(options=options)
    driver.get(URL)
    time.sleep(3)  # Allow page to fully load

    return driver

def check_cloudflare_block(page: str, block_file_path: str) -> bool:
    """
    Checks whether access has been blocked by Cloudflare.

    Scans the page content for common Cloudflare block signals.  
    If any matching signal is found, it logs the timestamp and the detected phrase  
    into the specified file path, notifies the user, and stops the program from continuing.

    Args:
        page (str): The HTML content of the page to be checked.
        block_file_path (str): File path to write block details if Cloudflare is detected.

    Returns:
        bool: Returns False if a Cloudflare block is detected, True otherwise.
    """

    # Cloudflare kontrolü yap
    cloudflare_signals = [
        "checking your browser",
        "attention required",
        "just a moment",
        "<title>access denied</title>",
        "cloudflare ray id",
        "please enable cookies",
        "your browser will redirect",
        "we are checking your browser",
        "one more step",
        "security check to access",
        "performance & security by cloudflare",
        "cf-browser-verification",
        "cf-error-details",
        "ddos protection by cloudflare",
        "verifying you are human",
        "this may take a few seconds",
        "needs to review the security of your connection"
    ]

    for signal in cloudflare_signals:
        if signal in page:
            with open(block_file_path, "w", encoding="utf-8") as f:
                f.write(f"{datetime.datetime.now()} - Cloudflare engeline takıldık. Tespit edilen ifade: '{signal}'\n")

            print("\nCloudflare engeli tespit edildi.")
            print(f"Tespit edilen ifade: '{signal}'")
            print(f"Engel bilgisi şu dosyaya kaydedildi: {block_file_path}\n")

            print("Bu dosya temizlenmeden program tekrar çalışmayacak.")
            print("Lütfen engelin neden kaynaklandığını araştırın ve çözümledikten sonra tekrar deneyin.\n")

            print("Olası çözüm yolları:")
            print("'from AutomationHandler_ramcik import oc' içinden 'oc.manuel_giris_yap(URL)' fonksiyonu ile aşağıdaki adımları yapın.")
            print("1. Google Chrome tarayıcısında şu iki adımı da gerçekleştirmiş olun:")
            print("   - Tarayıcı seviyesinde (profil kurulumu gibi) Google hesabınızla oturum açın.")
            print("   - gmail.com üzerinden Google hesabınıza manuel olarak giriş yapın.")
            print("2. Engelin geldiği siteye kullanıcı girişi yaparak sürekli sizi hatılamasını sağlayın.\n")

            return False

    return True

def check_previous_block_status(block_file_path):
    """
    Check if a previous script execution was blocked by Cloudflare.

    This function reads the contents of the specified file and looks for a specific keyword
    ("Cloudflare engeline takıldık") indicating that a previous request was blocked. If the 
    keyword is found, it prints a warning message and exits the script to avoid drawing 
    further attention by making repeated suspicious requests.

    Parameters:
        block_file_path (str): The path to the file where the block status is recorded.

    Behavior:
        - If the file exists and contains the block keyword, the function prints the reason and exits.
        - If the file does not exist or does not contain the keyword, the script continues.

    Example:
        check_previous_block_status("logs/block_status.txt")
    """

    block_keyword = "Cloudflare engeline takıldık"
    if os.path.exists(block_file_path):
        with open(block_file_path, "r", encoding="utf-8") as f:
            content = f.read()
            if block_keyword in content:
                print(f"Daha önce Cloudflare engeline takıldık:\n{content.strip()}")
                print("Şüphe çekmemek için script çalıştırılmıyor.")
                exit()



##################### Yapay zeka fonksiyomları ############################

#### ChatGPT ####

def __find_next_conversation_turn(target_text, driver , timeout=300):
    wait = WebDriverWait(driver, timeout)

    try:
        # Tüm conversation-turn elementlerini bul
        all_turns = wait.until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, '[data-testid^="conversation-turn-"]'))
        )

        # Hedef metni içeren ilk conversation-turn'ü bul
        matching_elem = None
        for elem in all_turns:
            if target_text in elem.text:
                matching_elem = elem
                break

        if not matching_elem:
            print("Hedef metni içeren conversation-turn bulunamadı.")
            return None

        data_testid = matching_elem.get_attribute("data-testid")
        

        match = re.search(r"conversation-turn-(\d+)", data_testid)
        if not match:
            print(f"data-testid formatı geçersiz: {data_testid}")
            return None

        next_index = int(match.group(1)) + 1
        next_testid = f"conversation-turn-{next_index}"
        
        
        # Sonraki elementi bekle ve yakala
        next_elem = wait.until(
            EC.presence_of_element_located((By.CSS_SELECTOR, f'[data-testid="{next_testid}"]'))
        )
        response_element = next_elem.find_element(By.CSS_SELECTOR, '[data-message-author-role="assistant"]')

        print("cevap bekleniyor")
        wait.until(
            EC.presence_of_element_located((
                By.XPATH,
                f'//*[@data-testid="{next_testid}"]//*[@aria-label="Sesli oku" or @aria-label="Read aloud"]'
            ))
        )
        print("cevap geldi")

        next_elem = wait.until(
            EC.presence_of_element_located((By.CSS_SELECTOR, f'[data-testid="{next_testid}"]'))
        )

        response_element = next_elem.find_element(By.CSS_SELECTOR, '[data-message-author-role="assistant"]')

        return response_element

    except Exception as e:
        print(f"Hata oluştu: {e}")
        return None


def get_text_response_from_chatgpt(prompt, driver):
    """
    Sends a prompt to ChatGPT and retrieves the response as plain text only.
    - Adds an instruction to the prompt to request a plain text response.
    - Formats the prompt for clipboard paste.
    - Sends the prompt via CTRL+V to avoid send_keys issues with large or multiline input.
    - Waits for and returns the plain text response.

    Args:
        prompt (str): The original prompt/question to ask ChatGPT.

    Returns:
        str or None: The plain text response if available, otherwise None.
    """
    try:
        # Sayfa tamamen yüklenene kadar bekle
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "prompt-textarea"))
        )
        time.sleep(random.uniform(2, 4))  # İnsan gibi bekleme
        print("Prompt gönderiliyor...")

        # Prompt input alanını bul
        prompt_element = driver.find_element(By.ID, "prompt-textarea")

        # Prompt'a düz metin cevabı istendiğini ekle
        prompt += " Give the answer as plain text only, do not use code blocks. just string"

        # Yapıştırmaya uygun hale getir
        formatted_prompt = format_text_for_input(prompt)

        # Input alanına yapıştır ve Enter'a bas
        prompt_element.send_keys(Keys.CONTROL, 'v')
        prompt_element.send_keys(Keys.ENTER)

        print("Prompt gönderildi, cevap bekleniyor...")

        # Yanıtın geldiği alanı bulmak için bekle
        response_element = __find_next_conversation_turn(formatted_prompt, driver, timeout=300)

        if response_element.text:
            response = response_element.text.strip()
            if response:
                print("Yanıt alındı:\n", response)
                return response
            else:
                print("Yanıt geldi ama boş görünüyor.")
        else:
            print("Yanıt elementi bulundu ama içinde metin yok.")

    except Exception as e:
        print("Hata oluştu:")
        print(str(e))

    return None

#### ChatGPT ####