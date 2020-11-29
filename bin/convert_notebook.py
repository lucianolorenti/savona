import argparse
import logging
from pathlib import Path

import yaml
from savona.exporter.docx_ import DocxExporter
from savona.exporter.html import HTMLExporter

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def common_arguments(args):

    args.add_argument('--input', type=str, required=True,
                      help='Input jupyter notebook file')
    args.add_argument('--output-path', type=str, required=False,
                      help='Output folder where to store the output')


def convert_to_html(input_file, output_path, args):
    if args.config is None:
        config = {}
    else:
        with open(args.config, 'r') as file:
            config = yaml.load(file)

    config['title'] = args.title if args.title is not None else ''

    if args.theme is not None:
        config['template_path'] = Path(args.theme).resolve()

    HTMLExporter(config).export(input_file, output_path)


def convert_to_docx(input_file, output_path, args):
    exporter = DocxExporter()
    exporter.export(input_file, output_path)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Convert jupyter notebook')
    subparsers = parser.add_subparsers(title='output_format',
                                       description='Output format',
                                       help='Output format',
                                       dest='format',
                                       required=True)
    subparsers.required = True
    html_args = subparsers.add_parser('html')
    common_arguments(html_args)
    html_args.add_argument('--config', type=str,
                           required=False, help='YAML config file')
    html_args.add_argument(
        '--title', type=str, required=False, help='Title')
    html_args.add_argument('--theme', type=str, required=False,
                           help='Template path folder')

    docx_args = subparsers.add_parser('docx')
    common_arguments(docx_args)

    args = parser.parse_args()
    callbacks = {
        'docx': convert_to_docx,
        'html': convert_to_html
    }
    input_file = Path(args.input).resolve()
    output_path = args.output_path
    if output_path is None:
        output_path = Path(input_file).resolve().parent
    else:
        output_path = Path(output_path).resolve()

    callbacks[args.format](input_file, output_path, args)
