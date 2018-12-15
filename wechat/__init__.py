import sys
from . import chat, data, post

__all__ = ['chat', 'data', 'post']

if '__main__' in sys.modules:
    sys.path.append("..")
    sys.modules['__mp_main__'] = sys.modules['__main__']
