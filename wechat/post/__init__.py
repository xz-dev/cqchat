import sys
from . import server

__all__ = ['server', ]

if '__main__' in sys.modules:
    sys.path.append("..")
    sys.modules['__mp_main__'] = sys.modules['__main__']
