import rpyc

#################################
# Middleware level              #
#################################
class ClientStub(object):
  def doit(self, a, b):  
    conn = rpyc.connect("127.0.0.1", 12345) # Connect to the server
    result = conn.root.exposed_doit(a, b)
    return result

#################################
# Application level             #
#################################

def doit(a, b):
  cs = ClientStub()
  return cs.doit(a, b)

if __name__ == "__main__":
  print("Calling function")
  result = doit(123, 456)
  print("Result: ", result)
