import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import time
import webbrowser
from notifypy import Notify
from .config import Config
from .storage import RepoStorage

class browserDriver:
    usernameRigas = 'user1'
    passwordRigas = '123456'
    baseUrlRigas = 'http://server_name.com'
    downloadUrlRigas = None
    patternFileRigas = None
    newDownloadDirRigas = None
    defaultDownloadDirRigas = None
    headlessModeRigas = True

    username_bottega = ''
    password_bottega = ''
    loginUrl_bottega = ''
    imageEditUrl_bottega = ''

    driver = None
    notification = None

    def __init__(self):
        config = Config()
        self.repoStorage = RepoStorage()
        self.baseUrlRigas = config.get_conf('rigas', 'baseUrl')
        self.downloadUrlRigas = config.get_conf('rigas', 'downloadUrl')
        self.usernameRigas = config.get_conf('rigas', 'username')
        self.passwordRigas = config.get_conf('rigas', 'password')
        self.headlessModeRigas = config.get_conf('rigas', 'headlessMode') == 'True'
        self.newDownloadDirRigas = config.get_conf('rigas', 'newDownloadDir')
        self.defaultDownloadDirRigas = config.get_conf('rigas', 'defaulDownloadDir')
        self.patternFileRigas = config.get_conf('rigas', 'patternFile')

        self.baseUrlTuttoGas = config.get_conf('atuttogas', 'baseUrl')
        self.downloadUrlTuttoGas = config.get_conf('atuttogas', 'downloadUrl')
        self.usernameTuttoGas = config.get_conf('atuttogas', 'username')
        self.passwordTuttoGas = config.get_conf('atuttogas', 'password')
        self.headlessModeTuttoGas = config.get_conf('atuttogas', 'headlessMode') == 'True'
        self.newDownloadDirTuttoGas = config.get_conf('atuttogas', 'newDownloadDir')
        self.defaultDownloadDirTuttoGas = config.get_conf('atuttogas', 'defaulDownloadDir')
        self.patternFileTuttoGas = config.get_conf('atuttogas', 'patternFile')

        self.username_bottega = config.get_conf('bottega', 'username')
        self.password_bottega = config.get_conf('bottega', 'password')
        self.loginUrl_bottega = config.get_conf('bottega', 'loginUrl')
        self.imageEditUrl_bottega = config.get_conf('bottega', 'imageEditUrl')
        
        self.notification = Notify(
            default_notification_application_name="WooCommerce Updater",
        )

    def downloadAutoRigas(self, verbose=False):
        try:
            chromeOptions = uc.ChromeOptions()
            downloadDir = self.defaultDownloadDirRigas
            if self.newDownloadDirRigas is not None:
                prefs = {
                    'download.default_directory': self.newDownloadDirRigas,
                    "download.prompt_for_download": False,
                }
                chromeOptions.add_experimental_option('prefs', prefs)
                downloadDir = self.newDownloadDirRigas
            if self.headlessModeRigas:
                # chromeOptions.headless = True
                chromeOptions.add_argument("--headless=new")


            chromeOptions.add_argument('--disable-browser-side-navigation')
            chromeOptions.add_argument("--remote-allow-origins=*")
            driver = uc.Chrome(use_subprocess=True, options=chromeOptions)
            # driver.manage().timeouts().implicitlyWait(Duration.ofSeconds(10))
            driver.implicitly_wait(10)
            driver.get(self.baseUrlRigas)
            btn = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, 'header-button'))).click()
            # btn = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, 'header-button'))).click()
            # btn = driver.find_element(By.ID, 'header-button')
            # btn.click()
            # user = driver.find_element(By.ID, 'username')
            user = WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.ID, 'login-username')))
            user.send_keys(self.usernameRigas)
            password = driver.find_element(By.ID, 'login-password')
            password.send_keys(self.passwordRigas)
            btn2 = driver.find_element(By.ID, 'login')
            # print(btn2.text)
            btn2.click()
            time.sleep(5)
            # try:
            #     elm = WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.ID, 'ajax-busy')))
            # except TimeoutException:
            #     btn2 = driver.find_element(By.ID, 'login')
            #     print(btn2.text)
            #     btn2.click()
            #     elm = WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.ID, 'ajax-busy')))

            driver.get("http://www.google.it")
            time.sleep(5)
            
            if verbose:
                print('Connessione...')

            driver.get(self.downloadUrlRigas)
            
            if verbose:
                print('Inizio Download')

            while self.repoStorage.getTmpFilesCount(downloadDir)==0:
                time.sleep(2)
                if verbose:
                    print('Download Not started...')
                driver.get(self.downloadUrlRigas)        


            while self.repoStorage.getTmpFilesCount(downloadDir)>0:
                if verbose:
                    print('Waiting the download to end...')
                time.sleep(5)

            # def every_downloads_chrome(driver):
            #     if not driver.current_url.startswith("chrome://downloads"):
            #         driver.get("chrome://downloads/")
            #     return driver.execute_script("""
            #         var items = document.querySelector('downloads-manager')
            #             .shadowRoot.getElementById('downloadsList').items;
            #         if (items.every(e => e.state === "COMPLETE"))
            #             return items.map(e => e.fileUrl || e.file_url);
            #         """)
            # paths = WebDriverWait(driver, 120, 1).until(every_downloads_chrome)

            driver.close()
        except Exception as e:
            CSVLOGGER.addLogRowAndWrite('Error Download Rigas', '', '', str(e))
            self.notification.title = "Download Rigas."
            self.notification.message = "Errore! Cosultare i log."
            self.notification.send()
            print(e)
            return None
        if self.newDownloadDirRigas is not None:
            fileDownloaded = self.repoStorage.getLatestFileInFolder(self.newDownloadDirRigas, pattern=self.patternFileRigas)
        else:
            fileDownloaded = self.repoStorage.getLatestFileInFolder(self.defaultDownloadDirRigas, pattern=self.patternFileRigas)
        return self.repoStorage.archiveFile('RIGAS', fileDownloaded)

    def downloadAutoTuttoGas(self, verbose=False):
        try:
            chromeOptions = uc.ChromeOptions()
            downloadDir = self.defaultDownloadDirTuttoGas
            if self.newDownloadDirTuttoGas is not None:
                prefs = {
                    'download.default_directory': self.newDownloadDirTuttoGas,
                    "download.prompt_for_download": False,
                }
                chromeOptions.add_experimental_option('prefs', prefs)
                downloadDir = self.newDownloadDirTuttoGas
            if self.headlessModeTuttoGas:
                # chromeOptions.headless = True
                chromeOptions.add_argument("--headless=new")


            chromeOptions.add_argument('--disable-browser-side-navigation')
            chromeOptions.add_argument("--remote-allow-origins=*")
            driver = uc.Chrome(use_subprocess=True, options=chromeOptions)
            # driver.manage().timeouts().implicitlyWait(Duration.ofSeconds(10))
            driver.implicitly_wait(10)
            driver.get(self.baseUrlTuttoGas)
            btn = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, 'header-button'))).click()
            # btn = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, 'header-button'))).click()
            # btn = driver.find_element(By.ID, 'header-button')
            # btn.click()
            # user = driver.find_element(By.ID, 'username')
            user = WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.ID, 'login-username')))
            user.send_keys(self.usernameTuttoGas)
            password = driver.find_element(By.ID, 'login-password')
            password.send_keys(self.passwordTuttoGas)
            btn2 = driver.find_element(By.ID, 'login')
            # print(btn2.text)
            btn2.click()
            time.sleep(5)
            # try:
            #     elm = WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.ID, 'ajax-busy')))
            # except TimeoutException:
            #     btn2 = driver.find_element(By.ID, 'login')
            #     print(btn2.text)
            #     btn2.click()
            #     elm = WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.ID, 'ajax-busy')))

            driver.get("http://www.google.it")
            time.sleep(5)
            
            if verbose:
                print('Connessione...')

            driver.get(self.downloadUrlTuttoGas)
            
            if verbose:
                print('Inizio Download')

            while self.repoStorage.getTmpFilesCount(downloadDir)==0:
                time.sleep(2)
                if verbose:
                    print('Download Not started...')
                driver.get(self.downloadUrlTuttoGas)        


            while self.repoStorage.getTmpFilesCount(downloadDir)>0:
                if verbose:
                    print('Waiting the download to end...')
                time.sleep(5)

            driver.close()
        except Exception as e:
            CSVLOGGER.addLogRowAndWrite('Error Download TuttoGas', '', '', str(e))
            self.notification.title = "Download TuttoGas."
            self.notification.message = "Errore! Cosultare i log."
            self.notification.send()
            print(e)
            return None
        if self.newDownloadDirRigas is not None:
            fileDownloaded = self.repoStorage.getLatestFileInFolder(self.newDownloadDirTuttoGas, pattern=self.patternFileTuttoGas)
        else:
            fileDownloaded = self.repoStorage.getLatestFileInFolder(self.defaultDownloadDirTuttoGas, pattern=self.patternFileTuttoGas)
        return self.repoStorage.archiveFile('ATUTTOGAS', fileDownloaded)    

    def downloadWithChrome(self):
        chrome_path = 'C:/Program Files (x86)/Google/Chrome/Application/chrome.exe %s'
        if webbrowser.get(chrome_path).open(self.downloadUrlRigas):
            import time
            time.sleep(5)
            fileDownloaded = self.repoStorage.getLatestFileInFolder(self.defaultDownloadDirRigas, pattern=self.patternFileRigas)
            # xlsReader(fileDownloaded)
            return self.repoStorage.archiveFile('RIGAS', fileDownloaded)
        else:
            return None

    def openDriver(self):
        try:
            chromeOptions = uc.ChromeOptions()
            downloadDir = self.defaultDownloadDirRigas
            if self.newDownloadDirRigas is not None:
                prefs = {
                    'download.default_directory': self.newDownloadDirRigas,
                    "download.prompt_for_download": False,
                }
                chromeOptions.add_experimental_option('prefs', prefs)
                downloadDir = self.newDownloadDirRigas
            if self.headlessModeRigas:
                # chromeOptions.headless = True
                chromeOptions.add_argument("--headless=new")
                pass


            chromeOptions.add_argument('--disable-browser-side-navigation')
            chromeOptions.add_argument("--remote-allow-origins=*")
            driver = uc.Chrome(use_subprocess=True, options=chromeOptions)
            # driver.manage().timeouts().implicitlyWait(Duration.ofSeconds(10))
            driver.implicitly_wait(10)
            
            self.driver = driver
            return True
        except Exception as e:
            CSVLOGGER.addLogRowAndWrite('Error OPEN Chrome', '', '', str(e))
            self.notification.title = "OPEN Chrome."
            self.notification.message = "Errore! Cosultare i log."
            self.notification.send()
            print(e)
            return False
        
    def wpLogin(self):
        try:
            driver = self.driver
            driver.get(self.loginUrl_bottega)
            user = WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.ID, 'user_login')))
            user.send_keys(self.username_bottega)
            password = driver.find_element(By.ID, 'user_pass')
            password.send_keys(self.password_bottega)
            btn = driver.find_element(By.ID, 'wp-submit')
            btn.click()
            time.sleep(5)

            return True
        except Exception as e:
            CSVLOGGER.addLogRowAndWrite('Error wpLogin', '', '', str(e))
            self.notification.title = "wpLogin."
            self.notification.message = "Errore! Cosultare i log."
            self.notification.send()
            print(e)
            return False

    def wpSearchImage(self, imageId):
        try:
            driver = self.driver
            driver.get(self.imageEditUrl_bottega.format(imageId))
            title = (WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.ID, 'title')))).get_attribute('value')
            post_name = (driver.find_element(By.ID, 'post_name')).get_attribute('value')
            # link = (driver.find_element(By.ID, 'sample-permalink')).get_attribute('href')
            link = (driver.find_element(By.CLASS_NAME, 'misc-pub-download')).children()[0].get_attribute('href')
            delete_link = (driver.find_element(By.ID, 'delete-action')).children()[0].get_attribute('href')

            return {imageId: {'title': title, 'slug': post_name, 'link':link, 'del_link': delete_link}}
        except TimeoutException:
            print('Immagine ID:{} non trovata online!'.format(imageId))
            return None
        except Exception as e:
            CSVLOGGER.addLogRowAndWrite('Error wpSearchImage', '', '', str(e))
            self.notification.title = "wpSearchImage."
            self.notification.message = "Errore! Cosultare i log."
            self.notification.send()
            print(e)
            return None
        
    def wpDeleteImage(self, del_link):
        try:
            driver = self.driver
            driver.get(del_link)
            return True
        except Exception as e:
            CSVLOGGER.addLogRowAndWrite('Error wpDeleteImage', '', '', str(e))
            self.notification.title = "wpDeleteImage."
            self.notification.message = "Errore! Cosultare i log."
            self.notification.send()            
            print(e)
            return False

