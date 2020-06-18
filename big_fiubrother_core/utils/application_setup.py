import yaml
import argparse
import logging
import os


def setup(application_name, config_path='config', log_path='log'):
    parser = argparse.ArgumentParser(description=application_name)
    parser.add_argument('environment',
                        type=str,
                        nargs='?',
                        default='development',
                        help="Application environment. By default it's development.")

    args = parser.parse_args()

    environment = args.environment.lower()

    if not os.path.exists(log_path):
        os.makedirs(log_path)

    log_format = '%(asctime)s  %(levelname)s  %(process)d  %(thread)d  %(message)s'
    log_filepath = os.path.join(log_path, '{}.log'.format(environment))
    logging.basicConfig(level=logging.DEBUG,
                        format=log_format,
                        datefmt='%Y-%m-%d %H:%M:%S',
                        filename=log_filepath)

    logging.getLogger('pika').setLevel(logging.WARNING)

    configuration_filepath = os.path.join(config_path, '{}.yml'.format(environment))

    assert os.path.exists(configuration_filepath), "Configuration: {} not found!".format(configuration_filepath)

    with open(configuration_filepath, 'r') as file:
        configuration = yaml.safe_load(file)
    
    logging.debug('APPLICATION STARTED')

    return configuration