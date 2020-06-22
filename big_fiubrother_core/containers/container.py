import logging


class Container:

    def __init__(self, task, input_interface, output_interface):
        self.task = task
        self.input_interface = input_interface
        self.output_interface = output_interface
        self.running = False
        self.stop_requested = False

    def running(self):
        return self.running

    def run(self):
        self.task.init()
        
        logging.debug('Container with task {} started'.format(self.task.name()))
        
        self.running = True

        try:
            while not self.stop_requested:
                input_message = self.input_interface.poll()

                if input_message is not None:
                    output_message = self.task.execute(input_message)
                    
                    if not isinstance(output_message, list):
                        output_message = [output_message]

                    for message in output_message:
                        self.output_interface.send(message)

        except Exception as e:
            logging.error('Task {} raised: {}'.format(self.task.name(), e))
            raise
        finally:
            logging.debug('Container with task {} finished'.format(self.task.name()))
            self.task.close()
            
            self.running = False
            self.stop_requested = False

    def stop(self):
        if self.running:
            self.stop_requested = True
            self.input_interface.stop()
