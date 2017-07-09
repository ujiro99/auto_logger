#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import click
import subprocess
import time


class AutoLogger:
    get_log_params = [
        "scripts/get_log.sh",
        "",                  # HOST_NAME
        "log_to_rom",        # LOG_CMD
        "",                  # REMOTE_LOG_DIR
        "",                  # REMOTE_DST_DIR
    ]
    move_log_params = [
        "scripts/move_log.sh",
        "",                  # LOCAL_SRC_DIR
    ]
    time_fmt = "%Y-%m-%d_%H%M%S"
    log_name = "console.log"
    devnull = open('/dev/null', 'w')

    def __init__(self, address, test_number):
        """
         Constructor.
        :param str address: telnet address
        :param str test_number: test case number
        """
        AutoLogger.get_log_params[1] = address
        self.test_number = test_number
        self.local_log_dir = ""  # type: str

    def generate_date_str(self):
        """
        :rtype: str
        """
        t = time.localtime()
        return time.strftime(AutoLogger.time_fmt, t)

    def create_dir(self):
        """
        Create test case number + date directory.
        :rtype: str
        """
        abs_current = os.path.dirname(os.path.abspath(__file__))
        path = os.path.join(abs_current, self.test_number, self.generate_date_str())
        os.makedirs(path)
        if not os.path.exists(path):
            raise IOError
        return path

    def start(self):
        """
        Start logging.
        """
        self.local_log_dir = self.create_dir()
        path = os.path.join(self.local_log_dir, AutoLogger.log_name)
        subprocess.call(["script", path])
        self.finish()

    def finish(self):
        """
        Copy logs to test case directory from remote.
        """
        # copy log files from remote.
        subprocess.Popen(AutoLogger.get_log_params, stdout=AutoLogger.devnull)
        # mv log files to local log directory.
        AutoLogger.move_log_params.append(self.local_log_dir)
        subprocess.Popen(AutoLogger.move_log_params, stdout=AutoLogger.devnull)


@click.command()
@click.option('-a', '--address', type=str, help='実機のtelnet接続用のIPアドレス')
@click.option('-t', '--test_number', type=str, help='試験番号.ログを保存するディレクトリ名に使用されます。')
def start(address: str, test_number: str) -> object:
    """
    ログ取得を開始します。

    \b
    試験番号毎のディレクトリを作成し、その中にログを保存します。
    ログ取得を終了する場合は、 exit を入力してください。
    """

    # check parameters.
    if address is None:
        return click.echo("Error: addressを設定してください。")
    if test_number is None:
        return click.echo("Error: test_numberを設定してください。")

    # execute command
    logger = AutoLogger(address, test_number)
    try:
        logger.start()
    except IOError as e:
        click.echo(e.args)
        click.echo("ディレクトリ作成に失敗しました。")
        return
    except Exception as e:
        click.echo(e.args)
        return

    # finish
    click.echo("正常に終了しました。")


def main():
    start(auto_envvar_prefix='MRN')


if __name__ == '__main__':
    main()
