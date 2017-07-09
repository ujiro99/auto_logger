#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import click
import subprocess
import time


class AutoLogger:

    time_fmt = "%Y-%m-%d_%H%M%S"
    log_name = "console.log"

    def __init__(self, address: str, test_number: str):
        self.address = address
        self.test_number = test_number

    def generate_date_str(self):
        t = time.localtime()
        return time.strftime(AutoLogger.time_fmt, t)

    def create_dir(self):
        path = os.path.join(self.test_number, self.generate_date_str())
        os.makedirs(path)
        if not os.path.exists(path):
            raise IOError
        return path

    def start(self):
        dir_name = self.create_dir()
        subprocess.call(["script", os.path.join(dir_name, AutoLogger.log_name)])
        #self.finish()

    def finish(self):
        subprocess.call("get_log.sh")


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
    except IOError:
        return click.echo("Error: ディレクトリ作成に失敗しました。")

    # finish
    click.echo("正常に終了しました。")


def main():
    start(auto_envvar_prefix='MRN')


if __name__ == '__main__':
    main()
