import time
from threading import Thread
import rpyc
from rpyc.utils.server import ThreadedServer
import sys


#######################################
# Middleware level                    #
#######################################

class ClientStub(rpyc.Service):
  """Client stub. Provides an interface to doit() to local processes.

  In this asynchronous version, the client stub also operates an RPC
  service to listen for callbacks from the server.  -

  Works as follows:
  - Starts a background thread to listen for callbacks from server.
  - Connects to RPC server and invokes the function. This should return 
  immediately, since it's an asynchronous operation. The arguments include the callback
  endpoint (ip addr and port) so that the server knows where to send the results of the function.
  - When the server is done with the execution of doit() remotely, it will call remotely the callback
  function on the client (exposed_callback) at the endpoint specified before, which will 
  in turn will lead to a local execution of the local function that the client application has defined
  as the callback/"event handler".
  """

  def __init__(self, callback):
    self.callback_server = ThreadedServer(self, port=11111) # we use rpyc's threaded server here; other ways could be possible
    self.callback_server_thread = Thread(target = self.callback_server.start) # we wrap the callback server in a separate thread
    self.callback = callback # this is the callback function

  def exposed_callback(self, result):
    """ When called, executes callback locally and just returns ok to the server."""
    self.callback(result)
    return 0
    
  def doit(self, a, b):
    """Stub wrapper to a remote function call. The actual stuff happens here."""

    # Connect to RPC server
    conn = rpyc.connect("127.0.0.1", 12345)

    # Start callback server thread. This will listen for the results of the remote 
    # execution in the background.
    self.callback_server_thread.daemon = True
    self.callback_server_thread.start()


    # Execute remote command. The last arg is the callback server endpoint info
    # (ip addr and port--though the first typicall is not strictly necessary since
    # the server should be able to see which client IP the request is coming from)
    # so that the server knows where to send the results to, when ready
    print(conn.root.exposed_doit(a, b, "127.0.0.1", 11111))


########################################################
# Client application. Has no idea of RPC taking place  #
########################################################

# flag set to false when eventually the function execution result is available
waiting_for_result = True

def doit(a, b, callback):
  """The interface of the local asynchronous function that the local application calls.

  Callback is the local function that will be executed when the results are ready.
  """
  cs = ClientStub(callback)
  cs.doit(a, b)

def on_results_ready(result):
  """This function is called when the results of the execution 
  of doit() are ready. """

  global waiting_for_result
  print("Function results ready: ", result)
  waiting_for_result = False 

if __name__ == "__main__":
  # Execute call. It is asynchronous, so it will directly return.
  # (Note that we also register the function that we want to be called as soon as the results are ready.)
  print("Executing function")
  doit(1, 2, on_results_ready)

  while waiting_for_result:
    print("Doing other things")
    time.sleep(1)

