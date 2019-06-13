import threading


class AsyncTask(threading.Thread):

    def __init__(self, task):
        threading.Thread.__init__(self)

        self.input_ready_event = threading.Event()
        self.output_ready_event = threading.Event()

        self.task = task
        self.input = None
        self.output = None

        self.end_event = threading.Event()

    def run(self):

        while not self.end_event.is_set():

            # Wait for input
            self.input_ready_event.wait()

            # Abort if signaled
            if self.end_event.is_set():
                return

            # Clear output
            self.output_ready_event.clear()
            # Get new output
            self.output = self.task(self.input)

            # Enable input
            self.input_ready_event.clear()

            # Enable output
            self.output_ready_event.set()

    def stop(self):

        self.end_event.set()
        self.input_ready_event.set()

    def set_input(self, input_value):

        if not self.input_ready_event.is_set():
            self.input = input_value
            self.input_ready_event.set()
            return True
        return False

    def output_ready(self):

        return self.output_ready_event.is_set()

    def get_output(self):

        self.output_ready_event.wait()
        output = self.output
        self.output_ready_event.clear()
        return output
