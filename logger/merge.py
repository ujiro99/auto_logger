import fileinput
import os
import re
from datetime import datetime as dt

from logger import log


class Merge:
    """
    Merge multiple log files.
    """

    class Parsed:
        """
        Parsed datetime and log line.
        """

        def __init__(self, time=None, line=None):
            self.time = time  # type: datetime
            self.line = line  # type: bytes

    TIME_FMT = '%H:%M:%S.%f'  # format of time stamps
    TIME_FMT_LEN = 12  # time stamps length
    PATTERN = re.compile(r'(.+?)/.*')  # pattern to extract timestamp
    FILE_SUFFIX = '.merged.log'  # Merged file's name suffix
    FILE_ENCODE = 'utf8'  # log file's encode

    def exec(self, dir_path):
        """
        Exec merge files and sort by timestamp.
        :param str dir_path: Directory path which contains log files.
        :return: Merge result.
        :rtype bool
        """
        log.i("- start merge: [%s]" % dir_path)

        lines = [self.Parsed(dt.min, b'')]
        files = list(self.__files(dir_path))
        if len(files) == 0:
            return False

        for l in list(fileinput.input(files, mode="rb")):
            p = self.__parse(l)
            if p.time is None:
                lines[-1].line = lines[-1].line + p.line
                continue
            lines.append(p)

        log.i("- write merged file: [%s%s]" % (dir_path, Merge.FILE_SUFFIX))
        lines = sorted(lines, key=lambda x: x.time)
        with open(dir_path + Merge.FILE_SUFFIX, "wb") as fd:
            for l in lines: fd.write(l.line)

        return True

    def __files(self, dir_path):
        """
        Find files.
        :return: Iterator[str]
        """
        for root, dirs, files in os.walk(dir_path):
            for file in files:
                ret = os.path.join(root, file)
                log.d(ret)
                yield ret
        return

    def __parse(self, byte):
        """
        Parse log line.
        :param bytes byte:
        :return: Parse result. If failed to decode, returns None time.
        :rtype Merger.Parsed
        """

        try:
            s = byte[0:Merge.TIME_FMT_LEN].decode(Merge.FILE_ENCODE)
            t = dt.strptime(s, Merge.TIME_FMT)
        except Exception as e:
            log.d(e)
            return self.Parsed(line=byte)

        return self.Parsed(t, byte)
