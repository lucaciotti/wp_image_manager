from PIL import Image

class ImageManage:
    
    @classmethod
    def combine_image_resized(self, columns, rows, space, images, save_path):
        n_max_images = columns*rows
        imgs = []
        for i, image in enumerate(images[:n_max_images]):
            img = Image.open(image)
            imgs.append(img)
        if len(imgs)>1:
            if len(imgs)==2:
                while len(imgs)<n_max_images:
                    img = Image.open('./src/utils/empty_frame.jpg')
                    imgs.insert(1,img)
            while len(imgs)<n_max_images:
                img = Image.open('./src/utils/empty_frame.jpg')
                imgs.append(img)
        im_list_resized=self._get_multi_resize(imgs)
        img_created = self._matrix_image(columns, space, im_list_resized)
        img_created.save(save_path)
        return True

    @classmethod
    def _matrix_image(self, columns, space, images):
        rows = len(images) // columns
        if len(images) % columns:
            rows += 1
        width_max = 500 #max([image.width for image in images])
        height_max = 500 #max([image.height for image in images])
        background_width = width_max*columns + (space*columns)-space
        background_height = height_max*rows + (space*rows)-space
        # container = Image.new('RGBA', (background_width, background_height), (255, 255, 255, 255))
        container = Image.new('RGB', (background_width, background_height), (255, 255, 255, 255))
        x = 0
        y = 0
        if len(images)==1:
            img = images[0]
            img = img.resize((400,400))
            x_offset = int((width_max-img.width)/2)
            y_offset = int((height_max-img.height)/2)
            container.paste(img, (x+x_offset, y+y_offset))
        else:
            for i, img in enumerate(images):
                img = img.resize((500,500))
                x_offset = int((width_max-img.width)/2)
                y_offset = int((height_max-img.height)/2)
                container.paste(img, (x+x_offset, y+y_offset))
                x += width_max + space
                if (i+1) % columns == 0:
                    y += height_max + space
                    x = 0
        # container.save('image_def.png')
        return container

    @classmethod
    def _get_multi_resize(self, im_list, resample=Image.BICUBIC):
        min_width = min(im.width for im in im_list)
        im_list_resized = [im.resize((min_width, int(im.height * min_width / im.width)),resample=resample) for im in im_list]
        return im_list_resized
