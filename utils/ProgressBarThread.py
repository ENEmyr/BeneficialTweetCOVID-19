import sys
import threading
import time

class ProgressBarThread(threading.Thread):
    def __init__(self, label='Working', delay=0.2):
        super(ProgressBarThread, self).__init__()
        self.label = label
        self.delay = delay  # interval between updates
        self.running = False
    def start(self):
        self.running = True
        super(ProgressBarThread, self).start()
    def run(self):
        label = '\r' + self.label + ' '
        while self.running:
            for c in ('-', '\\', '|', '/'):
                sys.stdout.write(label + c)
                sys.stdout.flush()
                time.sleep(self.delay)
    def stop(self):
        self.running = False
        self.join()  # wait for run() method to terminate
        sys.stdout.write('\r' + len(self.label)*' ' + '\r')  # clean-up
        sys.stdout.flush()