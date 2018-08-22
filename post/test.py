from io import StringIO
import sys
import server
#  import logging

#logging.basicConfig(level=logging.INFO)
old_stdout = sys.stdout
sys.stdout = resp_stdout = StringIO
server.run()
sys.stdout = old_stdout
