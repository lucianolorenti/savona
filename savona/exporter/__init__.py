import base64
import logging
from pathlib import Path

import nbformat
from jinja2 import DictLoader
from nbconvert.exporters.exporter import ResourcesDict
from savona import TEMPLATE_PATH

logger = logging.getLogger(__name__)


class Exporter:
    def _write_output(self, output_path: Path, filename: str, body):
        output_path = (output_path.parent /
                       (output_path.stem + self.extension))
        with open(output_path, 'w') as file:
            file.write(body)

        logger.info(f'Generated: {output_path}')

    @property
    def extension(self):
        raise NotImplementedError
