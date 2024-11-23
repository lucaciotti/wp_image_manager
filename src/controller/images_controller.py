import datetime
import os
import shutil

import typer

from src.__main__ import CSVLOGGER
from src.provider.config import Config
# from src.provider.notifier import Notifier
from src.provider.storage import RepoStorage
from src.provider.wooApi import wooApi
from src.utils.image_manage import ImageManage

from src.models import local as lm

class ImagesController:

    def __init__(self) -> None:
        self.config = Config()
        self.repoStorage = RepoStorage()
        # self.notification = Notifier()

    def processImages(self):
        src_image_path = config_path = self.config.get_conf('images', 'src_path')
        if src_image_path in (None, ''):
            print(f'Path Immagini di partenza non inserito!')
            CSVLOGGER.addLogRow('ProcessImages', '', '', f'Path Immagini di partenza non inserito!')
            return
        path, _ = self.repoStorage.getOrCreatePath(src_image_path)
        self._clear_dst_path()
        self._iterate_path(path)
        
    def _iterate_path(self, path):
        images_in_path=self.repoStorage.getAllFilesInFolder(path, pattern='*.jpg')
        cat_name = os.path.basename(path).upper()
        if len(images_in_path)>0:
            images_2_upload = self._check_images(images_in_path, cat_name, path)
            if len(images_2_upload)>0:
                img_ready_2_upload = []
                rebuild_cat_image = [str(i) for i in images_2_upload if '(1)' in str(i)]
                if len(rebuild_cat_image)==0:
                    # gestisco casi eccezinali di immagini senza (1)
                    rebuild_cat_image = [str(i) for i in images_2_upload if '(' not in str(i)]
                if len(rebuild_cat_image)>0:
                    img_ready_2_upload.append(self._make_category_image(rebuild_cat_image, cat_name, path))
                # Devo creare anche l'immagine di categoria della coasterBeer!
                for i in rebuild_cat_image:
                    # coasterBeer = (os.path.splitext(os.path.basename(i))[0].strip()).split('(')[0].strip()
                    coasterBeerName = os.path.splitext(os.path.basename(i))[0].strip()
                    if '(1)' in coasterBeerName:
                        # in questo modo gestisco i nomi come: "A (1) AMARCORD"
                        posInd = coasterBeerName.index('(1)')
                        if posInd > len(coasterBeerName)/2:
                            coasterBeer = coasterBeerName.split('(')[0].strip()
                            coasterBeerCatName = f'{cat_name}_{coasterBeer}'
                        else:
                            coasterBeer = coasterBeerName.split(')')[1].strip()
                            preCoasterBeer = coasterBeerName.split('(')[0].strip()
                            coasterBeerCatName = f'{cat_name}_{preCoasterBeer} {coasterBeer}'
                    else:
                        coasterBeer = coasterBeerName
                        coasterBeerCatName = f'{cat_name}_{coasterBeer}'
                    if coasterBeer != '':
                        rebuild_cat_coaster = []
                        for img in images_in_path:
                            if coasterBeer in img:
                                rebuild_cat_coaster.append(img)
                        if len(rebuild_cat_coaster)>0:
                            img_ready_2_upload.append(self._make_category_image(rebuild_cat_coaster, coasterBeerCatName, path))
                img_ready_2_upload.extend(self._process_images(images_2_upload, cat_name))
                self._upload_images(img_ready_2_upload, cat_name)

        # proseguo ricorsivamente con le sotto directory
        list_dirs = self.repoStorage.getAllFilesInFolder(path)
        for d in list_dirs:
            if os.path.isdir(d):
                self._iterate_path(d)

    def _clear_dst_path(self):
        dst_path = self.config.get_conf('images', 'dst_path')
        _, exist = self.repoStorage.getOrCreatePath(dst_path)

        for filename in os.listdir(dst_path):
            file_path = os.path.join(dst_path, filename)
            try:
                if os.path.isfile(file_path) or os.path.islink(file_path):
                    os.unlink(file_path)
                elif os.path.isdir(file_path):
                    shutil.rmtree(file_path)
            except Exception as e:
                print('Failed to delete %s. Reason: %s' % (file_path, e))

    def _check_images(self, list_images, cat_name, base_path):
        list_images_2_update = []
        for img in list_images:
            # Info immagine
            img_basename = os.path.basename(img)
            filename = os.path.splitext(img_basename)[0].strip().upper()
            dt_file_ct = datetime.datetime.fromtimestamp(os.path.getctime(img))
            filetype = (os.path.splitext(img_basename)[1][1:])
            basename_img = f'{cat_name}_{filename}.{filetype}'

            if filename[:1]=='.':
                #se file inizia con . allora lo scarto
                continue

            img_2_update = True
            try:
                db_record = lm.LocalMedia.filter(basename=basename_img, category=cat_name).get()
            except lm.LocalMedia.DoesNotExist:
                db_record = None
            if db_record:
                # l'immagine è già stata processata precedentemente
                if dt_file_ct <= db_record.date_ct:
                    img_2_update = False
            if img_2_update:
                list_images_2_update.append(img)
        return list_images_2_update

    def _process_images(self, list_images, cat_name):
        dst_path = self.config.get_conf('images', 'dst_path')
        _, exist = self.repoStorage.getOrCreatePath(dst_path)
        images_ready_2_upload = []
        for i in list_images:

            filename = os.path.splitext(os.path.basename(i))[0].strip().upper()
            new_name = f'{cat_name}_{filename}'
            if self.repoStorage.checkFile(i):
                images_ready_2_upload.append(self.repoStorage.archiveFile(dst_path, i, rename=new_name, timestamp=False))
        return images_ready_2_upload

    def _make_category_image(self, img_to_combine, cat_name, base_path):
        dst_path = self.config.get_conf('images', 'dst_path')
        _, exist = self.repoStorage.getOrCreatePath(dst_path)

        cat_image_path = f'{dst_path}/{cat_name.upper()}_category.jpg'
        if os.path.exists(cat_image_path):
            os.remove(cat_image_path)
        # Pulisco vecchia destinazione immagini
        cat_image_path_old = f'{base_path}/{cat_name.upper()}.jpg'
        if os.path.exists(cat_image_path_old):
            os.remove(cat_image_path_old)

        if len(img_to_combine)>=int(self.config.get_conf('images', 'combine_num_spread')):
            col = self.config.get_conf('images', 'combine_max_col')
            row = self.config.get_conf('images', 'combine_max_row')
        else:
            col = self.config.get_conf('images', 'combine_min_col')
            row = self.config.get_conf('images', 'combine_min_row')

        if len(img_to_combine)==1:
            #caso eccezionale di immagine singola
            col=1
            row=1

        created = ImageManage.combine_image_resized(columns=int(col), rows=int(row), space=20, images=img_to_combine, save_path=cat_image_path)
        if created:
            return cat_image_path
        
    def _upload_images(self, list_images, cat_name):
        wooApi_ = wooApi()
        for i in list_images:
            try:
                res = wooApi_.uploadWPImage(i)
            except Exception as e:
                typer.secho(
                    f'Upload Immagine non riuscito: ' + os.path.basename(i),
                    fg=typer.colors.RED,
                )
            # if res == 1:
            # Info immagine
            img_basename = os.path.basename(i)
            dt_file_ct = datetime.datetime.fromtimestamp(os.path.getctime(i))
            filetype = (os.path.splitext(img_basename)[1][1:]).upper()             
            try:
                db_record = lm.LocalMedia.filter(basename=img_basename, category=cat_name).get()
            except lm.LocalMedia.DoesNotExist:
                db_record = None

            try:
                if db_record:
                    # devo aggiornare
                    lm.LocalMedia.update(
                        basename=img_basename,
                        filetype=filetype,
                        category=cat_name,
                        path=i,
                        date_ct=dt_file_ct
                    ).where(lm.LocalMedia.id==db_record.id).execute()
                else:
                    lm.LocalMedia.get_or_create(
                        basename=img_basename,
                        filetype=filetype,
                        category=cat_name,
                        path=i,
                        date_ct=dt_file_ct
                    )
            except Exception as e:
                typer.secho(
                    f'Scrittura su DB non riuscita: ' + str(e),
                    fg=typer.colors.RED,
                )
