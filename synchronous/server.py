import rpyc
from rpyc.utils.server import ForkingServer
import time

class LocalExecutor(object):
  def __init__(self, value = 0):
    self.value = value

  def doit(self, a, b):
    # Sleep for sometime to simulate a "long" execution
#    time.sleep(3)
    return a + b

class ServerStub(rpyc.Service):
  def __init__(self):
    self.local = LocalExecutor()

  def exposed_doit(self, a, b):
    return self.local.doit(a, b)

if __name__ == "__main__":
  server = ForkingServer(ServerStub, port = 12345)
  server.start()
