import yaml
import argparse
import logging
import os
from . import SignalHandler

def setup(application_name, config_path='config', log_path='log', tmp_path='tmp'):
    parser = argparse.ArgumentParser(description=application_name)
    parser.add_argument('environment',
                        type=str,
                        nargs='?',
                        default='development',
                        help="Application environment. By default it's development.")

    args = parser.parse_args()

    environment = args.environment.lower()

    # Create tmp and log folders
    if not os.path.exists(tmp_path):
        os.makedirs(tmp_path)

    if not os.path.exists(log_path):
        os.makedirs(log_path)

    # Set up logging
    log_format = '%(asctime)s  %(levelname)s  %(process)d  %(thread)d  %(message)s'
    log_filepath = os.path.join(log_path, '{}.log'.format(environment))
    logging.basicConfig(level=logging.DEBUG,
                        format=log_format,
                        datefmt='%Y-%m-%d %H:%M:%S',
                        filename=log_filepath)

    logging.getLogger('pika').setLevel(logging.WARNING)

    # Load configuration
    configuration_filepath = os.path.join(config_path, '{}.yml'.format(environment))

    assert os.path.exists(configuration_filepath), "Configuration: {} not found!".format(configuration_filepath)

    with open(configuration_filepath, 'r') as file:
        configuration = yaml.safe_load(file)
    
    logging.debug('APPLICATION STARTED')

    return configuration

def run(processes=[], main_process=None):
    process_to_stop = main_process if main_process is not None else processes[0]
    
    SignalHandler(callback=process_to_stop.stop)

    for process in processes:
        process.start()

    if main_process is not None:
        main_process.run()

    for i, process in enumerate(processes):
        process.wait()

        if i + 1 < len(processes):
            processes[i+1].stop()