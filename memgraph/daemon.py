import threading


class Daemon(object):
    stop = None

    def __init__(self):
        self.stop = threading.Event()
        super(Daemon, self).__init__(self)

    def start(self, func, args):
        args += (self.stop,)
        t = threading.Thread(target=func, args=args)
        t.start()

    def stop(self):
        self.stop.set()
