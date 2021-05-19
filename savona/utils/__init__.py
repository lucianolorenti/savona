import logging
import tempfile
from pathlib import Path
from typing import List, Optional

import nbformat

logger = logging.getLogger(__name__)


def merge(notebook_paths: List[Path], output_path: Optional[Path] = None) -> Path:
    if len(notebook_paths) == 0:
        return None

    notebooks = [nbformat.read(n, 4) for n in notebook_paths]

    final_notebook = nbformat.v4.new_notebook(metadata=notebooks[0].metadata)

    for notebook in notebooks:
        final_notebook.cells += notebook.cells

    if output_path is None:
        with tempfile.NamedTemporaryFile('w', suffix='.ipynb',
                                         delete=False) as fp:
            logger.info(f'Notebook stored in {fp.name}')
            output_path = Path(fp.name)
            nbformat.write(final_notebook, fp)
    else:
        logger.info(f'Notebook stored in {output_path}')
        with open(output_path, 'wb') as fp:
            nbformat.write(final_notebook, fp)
    return output_path


class FileFinder:
    def __init__(self, paths=[]):
        self.paths = paths

    def find(self, file):
        for f in self.paths:
            if (f / file).is_file():
                return f / file
        raise FileNotFoundError(file)
