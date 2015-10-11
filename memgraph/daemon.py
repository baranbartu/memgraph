import threading
import abc
import time


class Daemon(object):
    def __init__(self, logic):
        self.logic = logic
        self.logs = {}
        self.stop_event = threading.Event()
        super(Daemon, self).__init__()

    def start(self, args):
        args += (self.stop_event,)
        t = threading.Thread(target=self.run, args=args)
        t.setDaemon(True)
        t.start()

    def stop(self):
        self.stop_event.set()
        self.logic.logs_to_csv()
        self.logic.make_plot()

    @abc.abstractmethod
    def run(self, *args):
        wait, stop_event = args
        while not stop_event.is_set():
            self.logic.execute()
            time.sleep(wait)


class Logic(object):
    def __init__(self):
        self.logs = {}
        super(Logic, self).__init__()

    def execute(self):
        pass

    def logs_to_csv(self):
        pass

    def make_plot(self):
        pass
