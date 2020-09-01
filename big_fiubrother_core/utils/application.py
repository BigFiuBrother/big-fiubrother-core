import yaml
import argparse
import logging
import os
import graypy
from multiprocessing import Queue
from contextlib import contextmanager
from logging.handlers import QueueHandler, QueueListener
from setproctitle import setproctitle, getproctitle
from . import SignalHandler


# Start asynchronous logger, uses process name in logging. Probably should call setup() before running
def start_logger(configuration, application_name=getproctitle()):
    logging.getLogger('pika').setLevel(logging.WARNING)
    logging.getLogger('kazoo.client').setLevel(logging.INFO)

    log_queue = Queue()
    
    queue_handler = QueueHandler(log_queue)

    graylog_handler = graypy.GELFUDPHandler(
        host=configuration['host'],
        port=configuration['port'],
        facility=application_name)

    remote_listener = QueueListener(log_queue, graylog_handler)

    logging.basicConfig(level=logging.INFO,
                        handlers=[queue_handler])

    remote_listener.start()

    logging.debug("Logging service started!")

    return remote_listener

# Setup for application. Loads configuration
def setup(application_name, config_path='config', log_path='log', tmp_path='tmp'):
    setproctitle(application_name)

    parser = argparse.ArgumentParser(description=application_name)
    parser.add_argument('environment',
                        type=str,
                        nargs='?',
                        default='development',
                        help="Application environment. By default it's development.")

    args = parser.parse_args()

    environment = args.environment.lower()

    # Create tmp folders
    if not os.path.exists(tmp_path):
        os.makedirs(tmp_path)

    # Load configuration
    configuration_filepath = os.path.join(config_path, '{}.yml'.format(environment))

    assert os.path.exists(configuration_filepath), "Configuration: {} not found!".format(configuration_filepath)

    with open(configuration_filepath, 'r') as file:
        configuration = yaml.safe_load(file)

    return configuration

# Run synchronous and asynchronous processes
def run(processes=[], main_process=None):
    process_to_stop = main_process if main_process is not None else processes[0]
    
    SignalHandler(callback=process_to_stop.stop)

    for process in processes:
        process.start()

    if main_process is not None:
        main_process.run()

        if len(processes) > 0:
            processes[0].stop()

    for i, process in enumerate(processes):
        process.wait()

        if i + 1 < len(processes):
            processes[i+1].stop()

@contextmanager
def runtime_context(application_name):
    configuration = setup(application_name)

    logging_service = start_logger(configuration['logging'], application_name)

    logging.info("{} started!".format(application_name))

    yield configuration

    logging.info("{} finished!".format(application_name))
    
    logging_service.stop()
