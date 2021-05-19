from argparse import ArgumentParser
from pathlib import Path
from savona.exporter.html import HTMLExporter

import yaml


def html_arguments(html_args: ArgumentParser):
    html_args.add_argument('--config', type=str,
                        required=False, help='YAML config file')
    html_args.add_argument(
        '--title', type=str, required=False, help='Title')
    html_args.add_argument('--theme', type=str, required=False,
                        help='Template path folder')



def HTMLExporter_from_args(args) -> HTMLExporter:
    if args.config is None:
        config = {}
    else:
        with open(args.config, 'r') as file:
            config = yaml.load(file)

    config['title'] = args.title if args.title is not None else ''

    if args.theme is not None:
        config['template_path'] = Path(args.theme).resolve()

    return HTMLExporter(config)