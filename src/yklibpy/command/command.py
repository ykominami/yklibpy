import logging
import subprocess
from typing import Any, Optional, cast

from yklibpy.common.timex import Timex
from yklibpy.config.appconfig import AppConfig
from yklibpy.db.appstore import AppStore


class Command:
    def __init__(self) -> None:
        pass

    def run_command(
        self,
        command: str | list[str],
        shell: bool = False,
        encoding: str = "utf-8",
        timeout: Optional[int] = None,
    ) -> tuple[str, int]:
        """
        コマンドラインを実行して、標準出力への出力を文字列として受け取る。

        Args:
            command: 実行するコマンド（文字列またはリスト）
            shell: shell経由で実行するかどうか（デフォルト: False）
            encoding: 出力のエンコーディング（デフォルト: utf-8）
            timeout: タイムアウト秒数（デフォルト: None）

        Returns:
            (標準出力の文字列, 終了コード) のタプル

        Raises:
            subprocess.TimeoutExpired: タイムアウトが発生した場合
            subprocess.SubprocessError: その他のサブプロセスエラー

        Example:
            >>> ghprj = Ghprj()
            >>> output, return_code = ghprj.run_command("echo hello")
            >>> print(output)  # "hello\\n"
            >>> print(return_code)  # 0
        """
        try:
            result = subprocess.run(
                command,
                shell=shell,
                capture_output=True,
                text=True,
                encoding=encoding,
                timeout=timeout,
            )
            return result.stdout, result.returncode
        except subprocess.TimeoutExpired as e:
            timeout_float = float(timeout) if timeout is not None else float(0)
            raise subprocess.TimeoutExpired(
                cmd=command,
                timeout=timeout_float,
                output=e.stdout or "",
                stderr=e.stderr or "",
            )
        except subprocess.SubprocessError:
            raise

    def run_command_simple(self, command: str | list[str], shell: bool = False) -> str:
        """
        コマンドラインを実行して、標準出力への出力を文字列として受け取る（シンプル版）。
        エラー時は例外を発生させる。

        Args:
            command: 実行するコマンド（文字列またはリスト）
            shell: shell経由で実行するかどうか（デフォルト: False）

        Returns:
            標準出力の文字列

        Raises:
            subprocess.CalledProcessError: コマンドが非ゼロの終了コードで終了した場合

        Example:
            >>> ghprj = Ghprj()
            >>> output = ghprj.run_command_simple("echo hello")
            >>> print(output)  # "hello\\n"
        """
        try:
            result = subprocess.run(
                command,
                shell=shell,
                capture_output=True,
                text=True,
                check=True,
                encoding="utf-8",
            )
            return result.stdout
        except subprocess.CalledProcessError as e:
            logging.exception(e)
            '''
            raise subprocess.CalledProcessError(
                returncode=e.returncode,
                cmd=command,
                output=e.stdout.decode("utf-8") if e.stdout else "",
                stderr=e.stderr.decode("utf-8") if e.stderr else "",
            )
            '''
        return "error"

    def run_command_simple_with_count(
        self,
        appstore: AppStore,
        command: str | list[str],
        shell: bool = False,
        *,
        force: bool = False,
        verbose: bool = False,
    ) -> str:
        count = self.get_next_count(appstore)
        if count == 1 or force:
            message = self.run_command_simple(command, shell=shell)
        else:
            message = ""

        if verbose:
            appstore.show(AppConfig.KIND_DB, AppConfig.BASE_NAME_FETCH)

        return message

    def get_next_count(self, appstore: AppStore) -> int:
        fetch_assoc_any = appstore.get_file_assoc_from_db(AppConfig.BASE_NAME_FETCH)
        fetch_assoc = cast(dict[str, str] | None, fetch_assoc_any)

        if not fetch_assoc:
            next_count = 1
            fetch_assoc = {"1": Timex.get_now()}
        else:
            max_key = 0
            for key in fetch_assoc:
                try:
                    max_key = max(max_key, int(key))
                except ValueError:
                    continue
            next_count = max_key + 1
            fetch_assoc[str(next_count)] = Timex.get_now()

        appstore.output_db(AppConfig.BASE_NAME_FETCH, cast(dict[str, Any], fetch_assoc))
        return next_count

