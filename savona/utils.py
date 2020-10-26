import base64

def file_to_base64(file_finder, file):
    with open(file_finder.find(file), "rb") as image_file:
        return base64.b64encode(image_file.read()).decode('ascii')


def img_tag(file_finder, img_path):
    return f'<img src="data:image/png;base64, {file_to_base64(file_finder, img_path)}" />'


def embed_image(file_finder, img):
    return img_tag(file_finder, img)