from PIL import Image


def combine_images(columns, space, images):
    rows = len(images) // columns
    if len(images) % columns:
        rows += 1
    width_max = max([Image.open(image).width for image in images])
    height_max = max([Image.open(image).height for image in images])
    background_width = width_max*columns + (space*columns)-space
    background_height = height_max*rows + (space*rows)-space
    background = Image.new('RGBA', (background_width, background_height), (255, 255, 255, 255))
    x = 0
    y = 0
    imgs = []
    for i, image in enumerate(images):
        img = Image.open(image)
        imgs.append(img)
        x_offset = int((width_max-img.width)/2)
        y_offset = int((height_max-img.height)/2)
        background.paste(img, (x+x_offset, y+y_offset))
        x += width_max + space
        if (i+1) % columns == 0:
            y += height_max + space
            x = 0
    background.save('image.png')

def combine_image_resize(columns, space, images):
    imgs = []
    for i, image in enumerate(images):
        img = Image.open(image)
        imgs.append(img)
    final_img=get_concat_h_multi_resize(imgs)
    final_img.save('image2.png')


def get_concat_h_multi_resize(im_list, resample=Image.BICUBIC):
    min_height = min(im.height for im in im_list)
    im_list_resize = [im.resize((int(im.width * min_height / im.height), min_height),resample=resample) for im in im_list]
    total_width = sum(im.width for im in im_list_resize)
    dst = Image.new('RGB', (total_width, min_height))
    pos_x = 0
    for im in im_list_resize:
        dst.paste(im, (pos_x, 0))
        pos_x += im.width
    return dst

def get_concat_v_multi_resize(im_list, resample=Image.BICUBIC):
    min_width = min(im.width for im in im_list)
    im_list_resize = [im.resize((min_width, int(im.height * min_width / im.width)),resample=resample)
                      for im in im_list]
    total_height = sum(im.height for im in im_list_resize)
    dst = Image.new('RGB', (min_width, total_height))
    pos_y = 0
    for im in im_list_resize:
        dst.paste(im, (0, pos_y))
        pos_y += im.height
    return dst


combine_images(columns=2, space=20, images=['images\\ABC (1).jpg', 'images\\ACCRA BREWERY (1).jpg', 'images\\CLUB (1) .jpg', 'images\\STONE STRONG (1).jpg'])

combine_image_resize(columns=2, space=20, images=['images\\ABC (1).jpg', 'images\\ACCRA BREWERY (1).jpg', 'images\\CLUB (1) .jpg', 'images\\STONE STRONG (1).jpg'])



def matrix_image(columns, space, images):
    rows = len(images) // columns
    if len(images) % columns:
        rows += 1
    width_max = max([Image.open(image).width for image in images])
    height_max = max([Image.open(image).height for image in images])
    background_width = width_max*columns + (space*columns)-space
    background_height = height_max*rows + (space*rows)-space
    container = Image.new('RGBA', (background_width, background_height), (255, 255, 255, 255))
    x = 0
    y = 0
    for i, img in enumerate(images):
        x_offset = int((width_max-img.width)/2)
        y_offset = int((height_max-img.height)/2)
        container.paste(img, (x+x_offset, y+y_offset))
        x += width_max + space
        if (i+1) % columns == 0:
            y += height_max + space
            x = 0
    container.save('image_def.png')

def get_multi_resize(im_list, resample=Image.BICUBIC):
    min_width = min(im.width for im in im_list)
    im_list_resized = [im.resize((min_width, int(im.height * min_width / im.width)),resample=resample) for im in im_list]
    return im_list_resized

def combine_image_resized(columns, space, images):
    imgs = []
    for i, image in enumerate(images):
        img = Image.open(image)
        imgs.append(img)
    im_list_resized=get_multi_resize(imgs)
    matrix_image(columns, space, im_list_resized)

combine_image_resized(columns=2, space=20, images=['images\\ABC (1).jpg', 'images\\ACCRA BREWERY (1).jpg', 'images\\CLUB (1) .jpg', 'images\\STONE STRONG (1).jpg'])