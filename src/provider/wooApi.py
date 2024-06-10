import base64
import os
import requests
import typer
# from notifypy import Notify
from woocommerce import API
from .config import Config

class wooApi:
    wcApi = None
    wpApi = None
    notification = None

    def __init__(self):
        config = Config()
        self.wcApi = API(
            url=config.get_conf('wooApi', 'url'),
            consumer_key=config.get_conf('wooApi', 'consumer_key'),
            consumer_secret=config.get_conf('wooApi', 'consumer_secret'),
            version=config.get_conf('wooApi', 'versionwc'),
            query_string_auth=True, 
            timeout=20
        )
        self.wpApi = API(
            url=config.get_conf('wooApi', 'url'),
            consumer_key=config.get_conf('wooApi', 'consumer_key'),
            consumer_secret=config.get_conf('wooApi', 'consumer_secret'),
            version=config.get_conf('wooApi', 'versionwp'),
            query_string_auth=True, 
            timeout=20
        )
        
        self.imageEditUrl = config.get_conf('wooApi', 'imageEditUrl')
        self.imageUploadUrl = config.get_conf('wooApi', 'imageUploadUrl')
        self.wp_username = config.get_conf('wooApi', 'username')
        self.wp_password = config.get_conf('wooApi', 'password')

        # self.notification = Notify(
        #     default_notification_application_name="WooCommerce Updater",
        # )

    def getWooInstance(self, url, params=None):
        if url=='media':
            return self.getWPInstance(url, params)
        
        try:
            res = self.wcApi.get(url, params=params)
            if res.status_code != 200:
                typer.secho(
                    f'Error Get wooApi message: ' + res.json()['message'],
                    fg=typer.colors.RED,
                )
                # print(params)
                raise typer.Exit(1)
            else:
                return res.json()

        except Exception as e:
            # CSVLOGGER.addLogRowAndWrite('Failed Get wooApi connection', '', '', str(e))
            self.notification.title = "Get wooApi connection."
            self.notification.message = "Errore! Cosultare i log."
            self.notification.send()
            typer.secho(
                f'Failed Get wooApi connection: ' + str(e),
                fg=typer.colors.RED,
            )
            raise typer.Exit(1)

    def updateWooInstance(self, url, resource_id, data):
        if url == 'media':
            return None
        
        try:
            updateUrl = '%s/%d' % (url, resource_id)
            res = self.wcApi.put(updateUrl, data=data)
            if res.status_code != 200:
                typer.secho(
                    f'Error Update wooApi message: ' + res.json()['message'],
                    fg=typer.colors.RED,
                )
                raise typer.Exit(1)
            else:
                return res.json()
        except Exception as e:
            # CSVLOGGER.addLogRowAndWrite('Failed Update wooApi connection', '', '', str(e))
            self.notification.title = "Update wooApi connection."
            self.notification.message = "Errore! Cosultare i log."
            self.notification.send()
            typer.secho(
                f'Failed Update wooApi connection: ' + str(e),
                fg=typer.colors.RED,
            )
            raise typer.Exit(1)

    def createWooInstance(self, url, data):
        if url == 'media':
            return None
        
        try:
            res = self.wcApi.post(url, data=data)
            if res.status_code != 201:
                typer.secho(
                    f'Error Create wooApi message: ' + res.json()['message'],
                    fg=typer.colors.RED,
                )
                raise typer.Exit(1)
            else:
                return res.json()
        except Exception as e:
            # CSVLOGGER.addLogRowAndWrite('Failed Create wooApi connection', '', '', str(e))
            self.notification.title = "Create wooApi connection."
            self.notification.message = "Errore! Cosultare i log."
            self.notification.send()
            typer.secho(
                f'Failed Create wooApi connection: ' + str(e),
                fg=typer.colors.RED,
            )
            raise typer.Exit(1)
    
    def batchWooInstance(self, url, data):
        try:
            res = self.wcApi.post(url, data=data)
            # print(res)
            if res.status_code < 200 or res.status_code > 299:
                typer.secho(
                    f'Error Batch wooApi message: ' + res.json()['message'],
                    fg=typer.colors.RED,
                )
                raise typer.Exit(1)
            else:
                return 1

        except Exception as e:
            # CSVLOGGER.addLogRowAndWrite('Failed Batch wooApi connection', '', '', str(e))
            self.notification.title = "Batch wooApi connection."
            self.notification.message = "Errore! Cosultare i log."
            self.notification.send()
            if "Read timed out." in str(e):
                typer.secho(
                    f'Timeout wooApi connection: ' + str(e),
                    fg=typer.colors.RED,
                )
            else:
                typer.secho(
                    f'Failed Create wooApi connection: ' + str(e),
                    fg=typer.colors.RED,
                )
            raise typer.Exit(1)
    

    def getWPInstance(self, url, params):
        try:
            res = self.wpApi.get(url, params=params)
            if res.status_code == 400:
                if res.json()['code'] == 'rest_post_invalid_page_number':
                    # Le WpApi restituisce errore su iterazione su pagine vuote
                    return []
            if res.status_code != 200:
                typer.secho(
                    f'Error Get WordPress message: ' + res.json()['message'],
                    fg=typer.colors.RED,
                )
                raise typer.Exit(1)
            else:
                return res.json()
        except Exception as e:
            # CSVLOGGER.addLogRowAndWrite('Failed Get WordPress connection', '', '', str(e))
            self.notification.title = "Get WordPress connection."
            self.notification.message = "Errore! Cosultare i log."
            self.notification.send()
            typer.secho(
                f'Failed Get WordPress connection: ' + str(e),
                fg=typer.colors.RED,
            )
            raise typer.Exit(1)

    def uploadWPImage(self, img):
        try:
            # res = requests.post(url=self.imageUploadUrl,
            #                         auth=(self.wp_username, self.wp_password),
            #                         files={'file': open(img, 'rb')})
            
            # res = self.wpApi.post('media', data=None, files={'file': open(img, 'rb')})
            data = open(img, 'rb').read()
    
            fileName = os.path.basename(img)
            
            espSequence = bytes(fileName, "utf-8").decode("unicode_escape")  
            # Convert all non ASCII characters to UTF-8 escape sequence

            message = self.wp_username + ":" + self.wp_password
            message_bytes = message.encode('ascii')
            base64_bytes = base64.b64encode(message_bytes)
            base64_message = base64_bytes.decode('ascii')

            res = requests.post(url=self.imageUploadUrl,
                                data=data,
                                headers={'Content-Type': 'image/jpeg',
                                        'Content-Disposition': 'attachment; filename=%s' % espSequence,
                                        'Authorization': 'Basic ' + base64_message,
                                        },)
            newDict=res.json()


            if res.status_code < 200 or res.status_code > 299:
                typer.secho(
                    f'Error Batch wooApi message: ' + res.json()['message'],
                    fg=typer.colors.RED,
                )
                raise typer.Exit(1)
            else:
                return 1
        except Exception as e:
            if "Read timed out." in str(e):
                typer.secho(
                    f'Timeout wooApi connection: ' + str(e),
                    fg=typer.colors.RED,
                )
            else:
                typer.secho(
                    f'Failed Create wooApi connection: ' + str(e),
                    fg=typer.colors.RED,
                )
            raise typer.Exit(1)
