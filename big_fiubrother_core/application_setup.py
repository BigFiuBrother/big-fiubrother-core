import yaml
import argparse
import os


def setup(application_name, path='config'):
    parser = argparse.ArgumentParser(description=application_name)
    parser.add_argument('environment', type=str, nargs='?', default='development', help='Environment to run applicacion. By default it is development.')

    args = parser.parse_args()

    with open(os.path.join(path, '{}.yml'.format(args.environment.lower()))) as config_file:    
        configuration = yaml.safe_load(config_file)

    return configuration