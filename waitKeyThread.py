import threading
import time
import sys

t = threading.Thread(target = sys.stdin.read(1),args=(1,))
t.start()
time.sleep(5)
t.join()

