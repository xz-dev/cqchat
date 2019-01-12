import sys

from . import post_api

__all__ = ['post_api', ]

if '__main__' in sys.modules:
    sys.modules['__mp_main__'] = sys.modules['__main__']
