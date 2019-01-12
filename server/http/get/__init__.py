import sys

from . import get_api

__all__ = ['get_api', ]

if '__main__' in sys.modules:
    sys.modules['__mp_main__'] = sys.modules['__main__']
