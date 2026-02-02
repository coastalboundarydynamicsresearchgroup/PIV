import sys

from filewatcher import Watcher

"""
    Backend real-time implementation for PIV controller.
    Start the execution engine.
"""
debug = False
if len(sys.argv) > 1:
  debug = True

watcher = Watcher(debug)
watcher.run()

exit(0)
