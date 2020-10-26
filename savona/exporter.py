from nbconvert import HTMLExporter
from savona.utils import embed_image
import base64
from pathlib import Path

import nbformat
from jinja2 import DictLoader
from nbconvert import HTMLExporter
from nbconvert.preprocessors import TagRemovePreprocessor
from traitlets.config import Config
from nbconvert.exporters.exporter import ResourcesDict
from savona import TEMPLATE_PATH
import logging 

logger = logging.getLogger(__name__)


class FileFinder:
    def __init__(self, paths=[]):
        self.paths = paths

    def find(self, file):
        for f in self.paths:
            if (f / file).is_file():
                return f/file
        raise FileNotFoundError(file)


class BeautyExport(HTMLExporter):
    def __init__(self, config, title):
        super().__init__(config=config)        
        self.title = title
        self.finder = FileFinder()
        self.filters['embed_image'] = lambda img: embed_image(self.finder, img)

    def _init_resources(self, resources):
        resources = super()._init_resources(resources)
        resources['page_title'] = self.title
        return resources


def export(notebook_path, output, config):

    if 'template_path' not in config:
        config['template_path'] = TEMPLATE_PATH / 'basic'
    if 'title' not in config:
        config['title'] = ''

    
    
    c = Config({
        'TemplateExporter': {
            'exclude_output_prompt': True,
            'exclude_input': True,
            'exclude_input_prompt': True,
        }
    })
    c.TemplateExporter.template_paths = [str(config['template_path'])]

    c.NotebookExporter.preprocessors = [
        "nbconvert.preprocessors.TagRemovePreprocessor"]

    c.HTMLExporter.template_name = config['template_path'].parts[-1]

    exporter = BeautyExport(c, config['title'])
    exporter.finder.paths.append(config['template_path'])
    exporter.register_preprocessor(TagRemovePreprocessor(config=c), True)

    (body, resources) = exporter.from_filename(notebook_path)

    output_path = notebook_path.parent / (notebook_path.stem + '.html')
    with open(output_path, 'w') as file:
        file.write(body)

    logger.info(f'Generated: {output_path}')

