"""File information"""
import os
import pwd

from .config import CONFIG
from .md5sum import get_file_hash

def is_important(path):
    return os.path.splitext(path)[1].strip('.') in CONFIG.get('fileinfo', 'important',
                                                              fallback='.sam, .bam')

def FileInfo(fd, link=False, important=False):
    """Hold information about a file"""
    fi = {
        'path': os.path.abspath(fd),
        'mode': 0,
        'uid': 0,
        'username': '',
        'size': 0,
        'lastmod': 0,
        'lastcheck': 0,
        'isfile': None,
        'isdir': None,
        'md5sum': '',
        'important': None,
        'problems': set()
    }

    try:
        fi['problems'] = set()

        stats = os.stat(fd, follow_symlinks=link)
        fi['mode'] = stats.st_mode
        fi['uid'] = stats.st_uid
        fi['username'] = pwd.getpwuid(stats.st_uid).pw_name
        fi['size'] = stats.st_size
        fi['lastmod'] = int(stats.st_ctime)
        fi['lastcheck'] = 0
        fi['isfile'] = os.path.isfile(fd)
        fi['isdir'] = not os.path.isfile(fd)
        fi['md5sum'] = get_file_hash(fd) if is_important(fd) else ''
        fi['important'] = is_important(fd)


    except FileNotFoundError:
        fi['problems'].add('PROB_BROKEN_LINK')

    except PermissionError:
        fi['problems'].add('PROB_FILE_NOT_GRPRD')

    finally:
        return fi
