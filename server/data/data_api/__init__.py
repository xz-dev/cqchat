import sys

from . import auto_handle, auto_flash_data, search

__all__ = [
    'auto_handle',
    'auto_flash_data'
    'search',
]

if '__main__' in sys.modules:
    sys.modules['__mp_main__'] = sys.modules['__main__']
