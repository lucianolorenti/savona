import argparse 
from pathlib import Path
from savona.exporter import export
import yaml
import logging 
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)




if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Convert jupyter notebook')
    parser.add_argument('--input', type=str, required=True, help='Input jupyter notebook file')
    parser.add_argument('--output-path', type=str, required=False, help='Output folder where to store the output')
    parser.add_argument('--config', type=str, required=False, help='YAML config file')
    parser.add_argument('--title', type=str, required=False, help='Title')
    parser.add_argument('--theme', type=str, required=False, help='Template path folder')
    

    args = parser.parse_args()
    input_file = Path(args.input).resolve()
    output_path = args.output_path
    if output_path is None:
        output_path = Path(input_file).resolve().parent
    else:
        output_path = Path(output_path).resolve()    
    
    if args.config is None:
        config = {}
    else:
        with open(args.config, 'r') as file:
            config = yaml.load(file)

    
    config['title'] = args.title if args.title is not None else ''

    if args.theme is not None:
        config['template_path'] = Path(args.theme).resolve()

    

 
    export(input_file, output_path, config)

