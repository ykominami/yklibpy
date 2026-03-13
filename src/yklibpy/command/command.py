import logging
import subprocess
from typing import Any, Optional, cast

from yklibpy.common.timex import Timex
from yklibpy.config.appconfig import AppConfig
from yklibpy.db.appstore import AppStore


class Command:
    """外部コマンド実行と実行回数管理を提供する。"""

    def __init__(self) -> None:
        """互換性維持のための空初期化を行う。"""
        pass

    def run_command(
        self,
        command: str | list[str],
        shell: bool = False,
        encoding: str = "utf-8",
        timeout: Optional[int] = None,
    ) -> tuple[str, int]:
        """コマンドを実行し、標準出力と終了コードを返す。"""
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
        """終了コードを検査しながらコマンドを実行し、標準出力を返す。"""
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
        """取得回数に応じてコマンド実行を制御し、必要時のみ出力を返す。"""
        count = self.get_next_count(appstore)
        if count == 1 or force:
            message = self.run_command_simple(command, shell=shell)
        else:
            message = ""

        if verbose:
            appstore.show(AppConfig.KIND_DB, AppConfig.BASE_NAME_FETCH)

        return message

    def get_next_count(self, appstore: AppStore) -> int:
        """保存済みの実行履歴から次の連番を採番して記録する。"""
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

