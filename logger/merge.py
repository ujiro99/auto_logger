import fileinput
import os
import re
from datetime import datetime as dt

from logger import log


class Merger:
    TIME_FMT = '%H:%M:%S.%f'  # format of time stamps
    PATTERN = re.compile(r'(.+?)/.*')  # pattern to extract timestamp
    NEW_LINE = '\n'

    def exec(self, dir_path):

        files = list(self.__files(dir_path))
        log.d(files)

        lines = []
        for l in list(fileinput.input(files, mode="rb")):
            t, log_str = self.__parse(l)
            if t is None:
                continue
            elif t is dt.max:
                lines[-1] = lines[-1][0], lines[-1][1] + Merger.NEW_LINE + log_str
                continue

            lines.append((t, log_str))

        lines = sorted(lines, key=lambda x: x[0])
        with open(dir_path + ".log", "w") as fd:
            for line in lines:
                fd.write(line[1])

        return True

    def __files(self, dir_path):
        """
        Find files.
        :return: Iterator[str]
        """
        for root, dirs, files in os.walk(dir_path):
            for file in files:
                yield os.path.join(root, file)

    def __parse(self, byte):

        try:
            s = byte.decode('utf8')

        except Exception as e:
            log.d(e)
            return None, None

        m = Merger.PATTERN.match(s)
        if m is None:
            return dt.max, s

        try:
            t = dt.strptime(m.group(1), Merger.TIME_FMT)
        except Exception as e:
            log.d(e)
            return dt.max, s

        return t, s
