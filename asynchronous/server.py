import rpyc
from rpyc.utils.server import ForkingServer
import time
from threading import Thread

class LocalExecutor(object):
  def doit(self, a, b, callback_endpoint_ip, callback_endpoint_port):
    """Actual (remote) function implementation. Here's what stuff happens.

    This normally executes in a separate thread. Stuff happen, and 
    when the work is done, the result is "posted" back to the callback
    endpoint that the client had registered when invoking exposed_doit().
    This last thing takes place also via RPC, where now the original client
    stub plays the role of the server. 
    """

    # sleep for some time to simulate a function that takes a while to finish work
    time.sleep(3)
    result = a + b
 
    # RPC call to callback endpoint of the client
    conn = rpyc.connect(callback_endpoint_ip, callback_endpoint_port)
    conn.root.exposed_callback(result)
    conn.close()

class ServerStub(rpyc.Service):
  def __init__(self):
    self.local = LocalExecutor()

  def exposed_doit(self, a, b, callback_endpoint_ip, callback_endpoint_port):
    # spawn thread to execute local function
    t = Thread(target = self.local.doit, args=(a, b, callback_endpoint_ip, callback_endpoint_port,))
    t.start()

    # return directly
    return 0

if __name__ == "__main__":
  server = ForkingServer(ServerStub, port = 12345)
  server.start()
