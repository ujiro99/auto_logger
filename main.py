#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import click
from logger import auto


@click.command()
@click.option('-a', '--address', type=str, help='実機のtelnet接続用のIPアドレス')
@click.option('-t', '--test_number', type=str, help='試験番号.ログを保存するディレクトリ名に使用されます。')
def start(address: str, test_number: str) -> object:
    """
    ログ取得を開始します。

    \b
    試験番号毎のディレクトリを作成し、その中にログを保存します。
    ログ取得を終了する場合は、 exit を2回入力してください。
    """

    # check parameters.
    if address is None:
        return click.echo("Error: addressを設定してください。")
    if test_number is None:
        return click.echo("Error: test_numberを設定してください。")

    click.echo("ログ取得を開始します。終了するには exit と2回入力してください。")

    # execute command
    logger = auto.AutoLogger(address, test_number)
    ret = False
    try:
        logger.start()
        ret = logger.finish()
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
