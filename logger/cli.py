#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import click
from . import auto


@click.command()
@click.option('-t', '--test_number', type=str, help='試験番号.ログを保存するディレクトリ名に使用されます。')
def start(test_number: str) -> object:
    """
    ログ取得を開始します。

    \b
    試験番号毎のディレクトリを作成し、その中にログを保存します。
    ログ取得を終了する場合は、 exit を2回入力してください。
    """

    # check parameters.
    if test_number is None:
        return click.echo("Error: test_numberを設定してください。")

    click.echo("ログ取得を開始します。終了するには exit と2回入力してください。")

    p = auto.LogParam()
    p.host_name = ""
    p.shell = "ssh"
    p.log_cmd = ""
    p.remote_log_dir = ""
    p.remote_dist_dir = ""
    p.local_src_dir = ""
    p.local_dist_dir = ""

    # execute command
    logger = auto.AutoLogger(p, test_number)
    ret = False
    try:
        ret = logger.execute()
    except IOError as e:
        click.echo(e.args)
    except Exception as e:
        click.echo(e.args)

    # finished
    if ret:
        click.echo("正常に終了しました。")
    else:
        click.echo("失敗しました。")


def main():
    start(auto_envvar_prefix='MRN')


if __name__ == '__main__':
    main()
