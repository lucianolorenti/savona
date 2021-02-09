
import base64

import nbconvert
from nbconvert.preprocessors import TagRemovePreprocessor
from savona import TEMPLATE_PATH
from savona.exporter import Exporter
from savona.utils import FileFinder
from traitlets.config import Config


def file_to_base64(file_finder, file):
    with open(file_finder.find(file), "rb") as image_file:
        return base64.b64encode(image_file.read()).decode('ascii')


def img_tag(file_finder, img_path):
    return f'<img src="data:image/png;base64, {file_to_base64(file_finder, img_path)}" />'


def embed_image(file_finder, img):
    return img_tag(file_finder, img)


class BeautyExport(nbconvert.HTMLExporter):
    def __init__(self, config, title):
        super().__init__(config=config)
        self.title = title
        self.finder = FileFinder()
        self.filters['embed_image'] = lambda img: embed_image(self.finder, img)

    def _init_resources(self, resources):
        resources = super()._init_resources(resources)
        resources['page_title'] = self.title
        return resources


class HTMLExporter(Exporter):
    def __init__(self, config):
        self.config = config
        if 'template_path' not in config:
            self.config['template_path'] = TEMPLATE_PATH / 'basic'
        if 'title' not in config:
            self.config['title'] = ''

    @property
    def extension(self):
        return '.html'

    def export(self, notebook_path, output_path):

        c = Config({
            'TemplateExporter': {
                'exclude_output_prompt': True,
                'exclude_input': True,
                'exclude_input_prompt': True,
            }
        })
        c.TemplateExporter.template_paths = [str(self.config['template_path'])]

        c.NotebookExporter.preprocessors = [
            "nbconvert.preprocessors.TagRemovePreprocessor"]

        c.HTMLExporter.template_name = self.config['template_path'].parts[-1]

        exporter = BeautyExport(c, self.config['title'])
        exporter.finder.paths.append(self.config['template_path'])
        exporter.register_preprocessor(TagRemovePreprocessor(config=c), True)

        (body, _) = exporter.from_filename(notebook_path)
        self._write_output(output_path, notebook_path.stem, body)
