import argparse
import tempfile
import time
from pathlib import Path

import yaml
from bottle import route, run, static_file, template
from savona.binary.utils import HTMLExporter_from_args, html_arguments
from savona.exporter.html import HTMLExporter
from watchdog.events import FileModifiedEvent, FileSystemEventHandler
from watchdog.observers import Observer


@route('/')
def index():
    return static_file('aa.html', root='/home/luciano')


class ExportHTML(FileSystemEventHandler):
    def __init__(self, notebook_input: Path, exporter: HTMLExporter,
                 generated_path: Path):
        self.exporter = exporter
        self.notebook = notebook_input
        self.generated_path = generated_path

    def on_modified(self, event):
        if isinstance(event, FileModifiedEvent):
            time.sleep(0.5)
            self.exporter.export(str(self.notebook),
                                 self.generated_path.parent,
                                 self.generated_path.stem)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='Live-preview of jupyter notebook')
    parser.add_argument('--notebook',
                        type=str,
                        required=True,
                        help='Input notebook file')
    html_arguments(parser)
    args = parser.parse_args()

    with tempfile.NamedTemporaryFile('w', delete=False) as fp:
        exporter = HTMLExporter_from_args(args)
        exported_path = Path(fp.name).resolve()
        exporter.export(Path(args.notebook), exported_path.parent,
                        exported_path.stem)
    observer = Observer()
    file_modified = ExportHTML(
        Path(args.notebook).resolve(), exporter, exported_path)
    observer.schedule(file_modified, args.notebook)
    observer.start()

    run(host='localhost', port=8080)

    observer.stop()
    observer.join()
