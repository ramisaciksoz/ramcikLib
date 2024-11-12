import os
import traceback
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from threading import Lock

whatsapp_lock = Lock()  # WhatsApp işlemleri için bir kilit tanımlama

def notify_phone_number(phone_number: str, message: str, chrome_profile_path: str = "", headless: bool = False):
    """
        Sends a WhatsApp message to a specified phone number via WhatsApp Web using a WebDriver instance.
        Depending on the provided phone number, it automatically selects the appropriate Chrome profile 
        for login and message delivery. This function handles login by checking for QR code requirements 
        and sends an alert email if manual intervention is needed.

        ### Parameters:
        
            - phone_number (str): 
                The target phone number to which the message should be sent.

            - message (str): 
                The message content to be sent.

            - chrome_profile_path (str, optional): 
                The path to the Chrome user profile directory. Defaults to an empty string, 
                in which case 
                it will use predefined environment variables:
                - If the phone number is the user’s own number, it uses 
                  'CHROME_SECONDARY_WHATSAPP_PROFILE_PATH'.
                - For other phone numbers, it defaults to 'CHROME_PRIMARY_WHATSAPP_PROFILE_PATH'.
                If no environment variable or parameter is provided, raises a ValueError.

            - headless (bool, optional): 
                Runs the WebDriver in headless mode if set to True. Defaults to False.

        ### Workflow:

            1. Determines the correct Chrome profile path based on the phone number.
            - Uses `MY_NUMBER` and Chrome profile path environment variables to select the profile.
            - If a Chrome profile path is not provided or set, raises a ValueError.

            2. Launches a WebDriver instance with the specified Chrome profile and opens WhatsApp Web.

            3. Waits for either a QR code prompt or the WhatsApp chat screen to load:
            - If a QR code prompt appears, waits for the QR code image to load.
            - Sends an email notification if manual login via QR code is required and exits.
            - If login is already authenticated, proceeds to find the specified contact.

            4. Searches for the specified contact by phone number:
            - Waits for the search box to load, enters the phone number, and opens the chat.

            5. Sends the message:
            - Waits for the message box to load, types the message, and sends it.
            - Checks if the message was successfully delivered. If it remains pending, raises an 
              exception and sends an error email.

            6. Cleans up:
            - If any errors occur, logs the error and sends an alert email with details.
            - Ensures the WebDriver instance is closed after the message is sent or upon encountering 
              an error.

        ### Raises:
        
            - ValueError: If both `chrome_profile_path` and environment variables for Chrome profiles 
              are unset.
            - Sends an email if:
                - Manual QR code scanning is required for login.
                - Message sending fails or times out.

        ### Dependencies:

            - `os.getenv`: To access environment variables.
            - `create_webdriver_with_profile`: Initializes a WebDriver instance with the given Chrome 
              profile.
            - `send_email`: Sends email alerts in case of QR code requirements or failures.
            - `whatsapp_lock`: Ensures thread safety when interacting with WhatsApp Web.

        ### Example usage:

            notify_phone_number("+905xxxxxxxxx", "Hello, this is a test message.")
            notify_phone_number("+905xxxxxxxxx", "This is a headless test message.", headless=True)
    """

    if chrome_profile_path == "":
        if phone_number == os.getenv('MY_NUMBER'): # Benim telefon numaramsa
            # Chrome profil dizini yolu klasörün içinde olucak şekilde ayarlanır kendiğinden.
            chrome_profile_path = os.getenv('CHROME_SECONDARY_WHATSAPP_PROFILE_PATH')
        else:
            # Chrome profil dizini yolu klasörün içinde olucak şekilde ayarlanır kendiğinden.
            chrome_profile_path = os.getenv('CHROME_PRIMARY_WHATSAPP_PROFILE_PATH')
        
        if chrome_profile_path == "":
            raise ValueError("Profil yolu sağlanmadı ve ortam değişkenleri ayarlanmadı. ikisinden biri yapılmalı.")

    driver = create_webdriver_with_profile(chrome_profile_path, headless = headless)
    
    qr_exists = True
    check_sending = False

    with whatsapp_lock:  # Kilidi kullanarak işlem yap
        try:
            # Web sayfasını aç
            driver.get("https://web.whatsapp.com")
            
            # QR kodunu veya profil ekranını aynı anda bekle
            WebDriverWait(driver, 300).until(
                EC.any_of(
                    EC.presence_of_element_located((By.XPATH, "//*[contains(text(), 'Point your phone at this screen to capture the QR code')]")),
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
                    EC.presence_of_element_located((By.XPATH, "//*[@aria-label='Scan me!']"))
                )
                print("QR kodu resmi yüklendi, 200 saniye de QR kodu okutup Whatsapp'a giriş yapman için bekleniyor. Eğer giriş yaparsan program devam edecek, yapmazsan da kapanacak.")
                
                # QR kodu bulunca 200 saniye de QR kodu okutup Whatsapp'a giriş yapman için bekleme
                profile_present = WebDriverWait(driver, 200).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, "div[aria-label='Chats']"))
                )
                if profile_present:
                    print("Profil açıldı.False döndürülüyor.")
                    qr_exists = False
                else:
                    print("Profil açılmadı. True döndürülüyor.")
                    qr_exists = True
                    

            elif profile_present:
                print("Profil ekranı bulundu. False döndürülüyor.")
                qr_exists = False
            
            else:
                print("Belirtilen elemanlar bulunamadı. True döndürülüyor.")
                qr_exists = True
        
            # QR kod var mı diye Fonksiyonu test etme varsa işlemlerin gerisini yapmadan bana uyarı E-maili atacak.
            if qr_exists:
                send_email("WhatsApp Login Alert","QR kod tarama işlemi gerekiyor. Lütfen programı yenileyin.")  # QR kod istendiğinde email gönder
        
            # Yoksa wpweb'deki benim mesajlarıma erişmiş demektir.
            else:
                # kişi adına göre kişiyi bulma ve tıklama
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
                WebDriverWait(driver, 300).until(
                    EC.visibility_of_element_located((By.XPATH, '//span[@data-icon="msg-time"]'))
                )

                sent_success = WebDriverWait(driver, 300).until(
                    EC.invisibility_of_element_located((By.XPATH, '//span[@data-icon="msg-time"]'))
                )

                if sent_success:
                    print("Mesaj başarılı bir şekilde gönderildi.")
                else:
                    print("mesajın hala bekliyor durumunda. zaman aşımından dolayı gönderilemedi.")
                    raise Exception("mesajın hala bekliyor durumunda. zaman aşımından dolayı gönderilemedi.")

                check_sending = True
                e = None

        except Exception as e:
            print(f"Hata oluştu: {e}")
            hata_mesaji = traceback.format_exc()  # Ayrıntılı hata mesajı
            print("Hata oluştu, detaylar:")
            print(hata_mesaji)

        finally:
            driver.quit()  # Driver'ı kapat

            #bir önceki satır false ise yani gönderilemediyse alttaki satırı çalıştır.
            if not check_sending:
                send_email(f"Whatsapptan {phone_number} kişisine mesaj atılamadı.",hata_mesaji)