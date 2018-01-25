import os
import json

# Helpers

_BASE_PATH = os.path.abspath(os.path.dirname(__file__))
def get_queue_file_path(path):
    return os.path.join(_BASE_PATH, 'data', path)

def custom_encode(message):
    return json.dumps(message) # json faster and more readable than pickle
    #return text.encode('unicode_escape').decode('utf-8')

def custom_decode(message):
    return json.loads(message)
    #return text.encode('utf-8').decode('unicode_escape')
 
class OutQueue():

    def __init__(self, path=get_queue_file_path('queue.txt')):
        self.file = open(path, "a") # open for append
    
    def __del__(self):
        self.file.close()

    def send_message(self, message):
        #print(message.encode('unicode_escape').decode('utf-8'), file=self.file)
        print(custom_encode(message), file=self.file)


class InQueue():

    def __init__(self, path=get_queue_file_path('queue.txt'), message_processor=lambda: None):
        self.path = path
        self.message_processor = message_processor
    
    def _get_messages(self):
        with open(self.path, 'r') as f:
            for line in f:
                message = custom_decode(line)
                yield message

    def _empty_queue(self):
        open(self.path, 'w').close() # empty a file
        # try:
        #     os.remove(self.path)
        # except OSError:
        #     pass

    def _print_all_messages(self): # for debug and testing
        local_message_processor = lambda m: print(":>>{}".format(m))
        for message in self._get_messages():
            local_message_processor(message)

    def size(self):
        return sum(1 for _ in self._get_messages()) # len(list(generator)) need more memory

    def receive_and_process_message(self):
        for message in self._get_messages():
            self.message_processor(message)
        self._empty_queue()

    def receive_message(self):
        for message in self._get_messages():
            yield message
        self._empty_queue()   
