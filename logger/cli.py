#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import click

from logger import auto
from logger import params

# messages.
PROMPT_SHELL_CMD = "- remote shell command"
PROMPT_HOST_NAME = "- remote host name"
PROMPT_LOG_CMD = "- log command"
PROMPT_REMOTE_LOG_DIR = "- remote log dir"
PROMPT_REMOTE_DIST_DIR = "- remote dist dir"
PROMPT_LOCAL_SRC_DIR = "- local src dir"


@click.group(invoke_without_command=True)
@click.option('-t', '--test-number', type=str, help='試験番号。ログを保存するディレクトリ名に使用されます。')
@click.pass_context
def cmd(ctx: click.core.Context, test_number: str):
    """
    サブコマンドを省略した場合、start が実行されます。
    """
    if ctx.invoked_subcommand is None:
        ctx.forward(start)


@cmd.command()
@click.pass_context
@click.option('-t', '--test-number', type=str, help='試験番号。ログを保存するディレクトリ名に使用されます。')
def start(ctx: click.core.Context, test_number: str) -> object:
    """
    コンソール操作ログを含む、ログの取得を開始します。

    \b
    試験番号毎のディレクトリを作成し、その中にログを保存します。
    ログ取得を終了するには、 exit を2回入力してください。
    """

    # check parameters.
    if test_number is None:
        return click.echo("Error: test-number を設定してください。")

    # load other parameters from ini file
    p = params.LogParam()
    ret = p.read_ini()
    if not ret:
        click.echo('ログ取得に使用するパラメータを設定してください。')
        ctx.invoke(init)
        p.read_ini()

    # execute command
    click.echo("ログ取得を開始します。終了するには exit を2回入力してください。")
    logger = auto.AutoLogger(p, test_number)
    ret = False
    try:
        ret = logger.start()
    except IOError as e:
        click.echo(e.args)
    except Exception as e:
        click.echo(e.args)

    # finished
    if ret:
        click.echo("正常に終了しました。")
    else:
        click.echo("失敗しました。")

@cmd.command()
@click.pass_context
def get(ctx: click.core.Context) -> object:
    """
    ログを取得します。
    """
    # load other parameters from ini file
    p = params.LogParam()
    ret = p.read_ini()
    if not ret:
        click.echo('ログ取得に使用するパラメータを設定してください。')
        ctx.invoke(init)
        p.read_ini()

    # execute command
    logger = auto.AutoLogger(p)
    ret = False
    try:
        ret = logger.get()
    except IOError as e:
        click.echo(e.args)
    except Exception as e:
        click.echo(e.args)

    # finished
    if ret:
        click.echo("正常に終了しました。")
    else:
        click.echo("失敗しました。")


@cmd.command()
@click.option('--shell-cmd',       prompt=PROMPT_SHELL_CMD, help='remote接続に使用するコマンド。ssh, telnet 等。')
@click.option('--host-name',       prompt=PROMPT_HOST_NAME, help='接続先のアドレス')
@click.option('--log-cmd',         prompt=PROMPT_LOG_CMD, help='remote接続先でのログ取得コマンド')
@click.option('--remote-log-dir',  prompt=PROMPT_REMOTE_LOG_DIR, help='remote接続先でログが保存されるディレクトリ絶対パス')
@click.option('--remote-dist-dir', prompt=PROMPT_REMOTE_DIST_DIR, help='remote接続先でログを一時保存するディレクトリ絶対パス')
@click.option('--local-src-dir',   prompt=PROMPT_LOCAL_SRC_DIR, help='remoteからlocalへログを一時保存するディレクトリ絶対パス')
def init(shell_cmd: str, host_name: str, log_cmd: str, remote_log_dir: str, remote_dist_dir: str, local_src_dir: str) -> object:
    """
    ログ取得に使用するパラメータを設定します。
    設定値は ~/plog.ini に保存されます。
    """

    # When called by Context.invoke or Context.forward, args will be None.
    if shell_cmd is None:
        shell_cmd = click.prompt(PROMPT_SHELL_CMD, type=str)
    if host_name is None:
        host_name = click.prompt(PROMPT_HOST_NAME, type=str)
    if log_cmd is None:
        log_cmd = click.prompt(PROMPT_LOG_CMD, type=str)
    if remote_log_dir is None:
        remote_log_dir = click.prompt(PROMPT_REMOTE_LOG_DIR, type=str)
    if remote_dist_dir is None:
        remote_dist_dir = click.prompt(PROMPT_REMOTE_DIST_DIR, type=str)
    if local_src_dir is None:
        local_src_dir = click.prompt(PROMPT_LOCAL_SRC_DIR, type=str)

    # Set input values to param.
    p = params.LogParam()
    p.host_name       = host_name
    p.shell           = shell_cmd
    p.log_cmd         = log_cmd
    p.remote_log_dir  = remote_log_dir
    p.remote_dist_dir = remote_dist_dir
    p.local_src_dir   = local_src_dir

    # Write to ~/prog.ini
    path = p.write_ini()
    click.echo("設定保存完了: %s" % path)


def main():
    cmd(auto_envvar_prefix='MRN')


if __name__ == '__main__':
    main()
