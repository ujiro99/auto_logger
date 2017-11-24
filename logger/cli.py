#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os

import click

from logger import auto, params, log, remote, convert as conv, merge as mrg

# messages.
PROMPT_SHELL_CMD = "- remote shell command"
PROMPT_HOST_NAME = "- remote host name"
PROMPT_LOG_CMD = "- log command"
PROMPT_LOG_EXTENSION = "- log extension"
PROMPT_REMOTE_LOG_DIR = "- remote log directory path"
PROMPT_REMOTE_DIST_DIR = "- remote dist directory path"
PROMPT_LOCAL_SRC_DIR = "- local src directory path"
PROMPT_CONVERT_RULE = "- convert rule file"
PROMPT_MERGE_DIR = "- marge target directory name"


@click.group(invoke_without_command=True)
@click.option('-t', '--test-number', type=str, help='試験番号。ログを保存するディレクトリ名に使用されます。')
@click.option('--debug/--no-debug', default=False, help='デバッグログを出力します。')
@click.pass_context
def cmd(ctx: click.core.Context, test_number: str, debug: bool):
    """
    サブコマンドを省略した場合、start が実行されます。
    """
    if ctx.invoked_subcommand is None:
        ctx.forward(start)


@cmd.command()
@click.pass_context
@click.option('-t', '--test-number', type=str, help='試験番号。ログを保存するディレクトリ名に使用されます。')
@click.option('--debug/--no-debug', default=False, help='デバッグログを出力します。')
def start(ctx: click.core.Context, test_number: str, debug: bool) -> object:
    """
    コンソール操作ログを含む、ログの取得を開始します。

    \b
    試験番号毎のディレクトリを作成し、その中にログを保存します。
    ログ取得を終了するには、 exit を2回入力してください。
    """
    # for debug
    if debug:
        log.set_level(log.Level.DEBUG)

    # check parameters.
    if test_number is None:
        return click.echo("Error: test-number を設定してください。")

    p = __get_params(ctx)

    # execute command
    click.echo("ログ取得を開始します。終了するには exit を2回入力してください。")
    logger = auto.AutoLogger(p, test_number)
    ret = False
    try:
        ret = logger.start()
    except IOError as e:
        ret = False
        click.echo(e.args)
    except Exception as e:
        ret = False
        click.echo(e.args)

    # finished
    if ret:
        click.echo("正常に終了しました。")
    else:
        click.echo("失敗しました。")


@cmd.command()
@click.pass_context
@click.argument('filename', default=None, required=False)
@click.option('-u', '--to-usb/--no-to-usb', default=False, help='USBへ出力します。')
@click.option('-c', '--convert/--no-convert', default=False, help='取得したファイルを変換します。')
@click.option('-m', '--merge/--no-merge', default=False, help='変換後にマージします。')
@click.option('--debug/--no-debug', default=False, help='デバッグログを出力します。')
def get(ctx: click.core.Context, filename: str, to_usb: bool, convert: bool, merge: bool, debug: bool):
    """
    引数に指定したファイルを取得します。省略した場合は新たに取得します。
    """
    # for debug
    if debug:
        log.set_level(log.Level.DEBUG)

    p = __get_params(ctx)
    p.local_dist_dir = os.getcwd()

    if to_usb:
        p.remote_dist_dir = "/mnt/USB0"

    # execute command
    files = None
    ret = True
    try:
        if filename is None:
            files = remote.RemoteLogger(p).get_log(to_usb)
        else:
            files = remote.RemoteLogger(p).move_log(filename, to_usb)

        if convert and files is not None:
            cp = conv.ConvertParams()
            cp.script_path = p.convert_rule
            for f in files:
                cp.log_path = f
                ret, out_dir = conv.Converter(cp).exec()
                ret &= ret
                if merge and not (out_dir is None):
                    ret &= mrg.Merge().exec(os.path.join(out_dir, p.merge_dir))

    except IOError as e:
        ret = False
        click.echo(e.args)
    except Exception as e:
        ret = False
        click.echo(e.args)

    # finished
    if not files is None and ret:
        click.echo("正常に終了しました。")
    else:
        click.echo("失敗しました。")


@cmd.command()
@click.option('--shell-cmd', prompt=PROMPT_SHELL_CMD, help='remote接続に使用するコマンド。ssh, telnet 等。')
@click.option('--host-name', prompt=PROMPT_HOST_NAME, help='接続先のアドレス')
@click.option('--log-cmd', prompt=PROMPT_LOG_CMD, help='remote接続先でのログ取得コマンド')
@click.option('--log-extension', prompt=PROMPT_LOG_EXTENSION, help='ログファイルの拡張子')
@click.option('--remote-log-dir', prompt=PROMPT_REMOTE_LOG_DIR, help='remote接続先でログが保存されるディレクトリ絶対パス')
@click.option('--remote-dist-dir', prompt=PROMPT_REMOTE_DIST_DIR, help='remote接続先でログを一時保存するディレクトリ絶対パス')
@click.option('--local-src-dir', prompt=PROMPT_LOCAL_SRC_DIR, help='remoteからlocalへログを一時保存するディレクトリ絶対パス')
@click.option('--convert-rule', prompt=PROMPT_CONVERT_RULE, help='ログの変換ルールファイルのパス')
@click.option('--merge-dir', prompt=PROMPT_MERGE_DIR, help='マージ対象のディレクトリ名')
def init(shell_cmd: str, host_name: str, log_cmd: str, log_extension: str, remote_log_dir: str, remote_dist_dir: str,
         local_src_dir: str, convert_rule: str, merge_dir: str):
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
    if log_extension is None:
        log_extension = click.prompt(PROMPT_LOG_EXTENSION, type=str)
    if remote_log_dir is None:
        remote_log_dir = click.prompt(PROMPT_REMOTE_LOG_DIR, type=str)
    if remote_dist_dir is None:
        remote_dist_dir = click.prompt(PROMPT_REMOTE_DIST_DIR, type=str)
    if local_src_dir is None:
        local_src_dir = click.prompt(PROMPT_LOCAL_SRC_DIR, type=str)
    if convert_rule is None:
        convert_rule = click.prompt(PROMPT_CONVERT_RULE, type=str)
    if merge_dir is None:
        merge_dir = click.prompt(PROMPT_MERGE_DIR, type=str)

    # Set input values to param.
    p = params.LogParam()
    p.host_name = host_name
    p.shell = shell_cmd
    p.log_cmd = log_cmd
    p.remote_log_dir = remote_log_dir
    p.remote_dist_dir = remote_dist_dir
    p.local_src_dir = local_src_dir
    p.log_extension = log_extension
    p.convert_rule = convert_rule
    p.merge_dir = merge_dir

    # Write to ~/prog.ini
    path = p.write_ini()
    click.echo("設定保存完了: %s" % path)


@cmd.command()
@click.pass_context
@click.option('--debug/--no-debug', default=False, help='デバッグログを出力します。')
def ls(ctx: click.core.Context, debug: bool):
    """
    Remoteに保存されたログファイルの一覧を取得します。
    """
    if debug:
        log.set_level(log.Level.DEBUG)
    else:
        log.set_level(log.Level.WARN)

    p = __get_params(ctx)

    try:
        for f in remote.RemoteLogger(p).list_log():
            click.echo(f)

    except IOError as e:
        click.echo(e.args)
    except Exception as e:
        click.echo(e.args)


@cmd.command()
@click.pass_context
@click.option('--debug/--no-debug', default=False, help='デバッグログを出力します。')
def clear(ctx: click.core.Context, debug: bool):
    """
    Remoteに保存されたログファイルをすべて削除します。

    \b
    ※注意: 削除時の確認はしません。削除したファイルの復元はできません。
    """
    if debug:
        log.set_level(log.Level.DEBUG)
    else:
        log.set_level(log.Level.WARN)

    p = __get_params(ctx)

    try:
        remote.RemoteLogger(p).clear_log()

    except IOError as e:
        click.echo(e.args)
    except Exception as e:
        click.echo(e.args)

    click.echo("%s のログを削除しました。" % p.remote_log_dir)


@cmd.command()
@click.pass_context
@click.argument('tar-file', type=click.Path(exists=True), required=False)
@click.option('-s', '--script-path', type=click.Path(exists=True), help='変換ルールを記載したパス。デフォルト値は設定ファイルの convert_rule')
@click.option('-f', '--file', type=click.Path(exists=True), help='変換対象のログファイル')
@click.option('-m', '--merge/--no-merge', default=False, help='変換後にマージします。')
@click.option('--debug/--no-debug', default=False, help='デバッグログを出力します。')
def convert(ctx: click.core.Context, tar_file: str, script_path: str, file: str, merge: bool, debug: bool):
    """
    指定されたtarファイルを展開し、変換ルールに従って変換します。
    """
    if debug:
        log.set_level(log.Level.DEBUG)

    if not script_path is None:
        s = script_path
    else:
        conf = __get_params(ctx)
        if (conf.convert_rule is not None) and (not os.path.exists(conf.convert_rule)):
            click.echo("convert_rule \"%s\" が存在しません。" % conf.convert_rule)
            ctx.exit(2)
        else:
            s = conf.convert_rule

    p = conv.ConvertParams()
    p.script_path = s
    p.log_path = tar_file
    p.file = file

    ret = None
    try:
        ret, out_dir = conv.Converter(p).exec()
        if merge and not (out_dir is None):
            ret = mrg.Merge().exec(os.path.join(out_dir, conf.merge_dir))

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
@click.argument('directory', required=True, type=click.Path(exists=True))
@click.option('--debug/--no-debug', default=False, help='デバッグログを出力します。')
def merge(directory: str, debug: bool):
    """
    引数に指定したディレクトリ内のファイルをマージし、日付でソートします。

    \b
    マージしたファイルは、[ディレクトリ名 + .merged.log]というファイル名で出力されます。
    utf-8でデコード出来ない行は上手くマージ出来ません。
    """
    # for debug
    if debug:
        log.set_level(log.Level.DEBUG)

    try:
        ret = mrg.Merge().exec(directory)

    except IOError as e:
        ret = False
        click.echo(e.args)
    except Exception as e:
        ret = False
        click.echo(e.args)

    # finished
    if ret:
        click.echo("正常に終了しました。")
    else:
        click.echo("失敗しました。")


def main():
    cmd(auto_envvar_prefix='MRN')


def __get_params(ctx):
    """
    Get parameters from config file.
    :param click.core.Context ctx: Context object of click.
    :return: parameters
    :rtype LogParam
    """
    # load parameters from ini file
    p = params.LogParam()
    ret = p.read_ini()
    if not ret:
        click.echo('ログ取得に使用するパラメータを設定してください。')
        ctx.invoke(init)
        p.read_ini()

    return p


if __name__ == '__main__':
    main()
