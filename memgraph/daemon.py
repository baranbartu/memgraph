import threading
import abc
import time


class Daemon(object):
    stop_event = None

    def __init__(self, logic):
        self.logic = logic
        self.logs = {}
        self.stop_event = threading.Event()
        super(Daemon, self).__init__()

    def start(self, args):
        t = threading.Thread(target=self.run, args=args)
        t.start()

    def stop(self, generate_csv, make_plot):
        self.stop_event.set()
        if generate_csv:
            self.logic.logs_to_csv()
            if make_plot:
                self.logic.make_plot()

    @abc.abstractmethod
    def run(self, *args):
        wait = args[0]
        while not self.stop_event.is_set():
            self.logic.execute()
            time.sleep(wait)


class Logic(object):
    def __init__(self):
        self.logs = {}

    def execute(self):
        pass

    def logs_to_csv(self):
        pass

    def make_plot(self):
        pass
