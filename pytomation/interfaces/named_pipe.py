import os, tempfile

from .common import Interface
from ..common.pytomation_object import PytoLogging

class NamedPipe(Interface):
    def __init__(self, path_name, is_read=True):
        super(NamedPipe, self).__init__()
        self._path_name = path_name
        self._logger = PytoLogging(self.__class__.__name__)
        self._create_named_pipe(path_name)

    def _create_named_pipe(self, path_name):
        try:
            os.mkfifo(path_name)
        except OSError, e:
            self._logger.error("Failed to create FIFO: %s" % e)
        else:
            if self._is_read:
                self._pipe = open(path_name, 'r')
            else:
                self._pipe = open(path_name, 'w')
            
    def read(self, bufferSize=1024):
        return self._pipe.read(bufferSize)

    def write(self, bytesToSend):
        return self._pipe.write(bytesToSend)  

    def close(self):
        self._pipe.close()
        os.remove(self._path_name)
#        os.rmdir(tmpdir)    