from yklibpy.common.timex import Timex
from yklibpy.config.appconfig import AppConfig
from yklibpy.db.appstore import AppStore


class FetchCount:
    """取得済みデータの世代番号を管理する。"""

    def __init__(self, needness_of_refresh: bool, needness_of_top_dir: bool, appstore: AppStore) -> None:
        """更新要否に応じて利用すべき取得回数を決定する。"""
        self.fetch_count = -1
        self.needness_of_refresh = needness_of_refresh
        self.needness_of_top_dir = needness_of_top_dir
        self.appstore = appstore
        self.fetch_assoc: dict[str, str] = {}

        # Githubからダウンロードが必要な場合は、新しいダウンロード先ディレクトリを用意する
        if self.needness_of_refresh:
            self.fetch_count = self.get_next_count()
        # Githubからダウンロードが必要ない場合は、既存のダウンロード先ディレクトリのうち、最新のものを取得（ダウンロード先ディレクトリは、ダウンロード回数をディレクトリ名として持つ）
        else:
            fetch_assoc = self.appstore.get_file_assoc_from_db(AppConfig.BASE_NAME_FETCH)
            self.fetch_count = 1
            for k in fetch_assoc.keys():
                try:
                    self.fetch_count = max(self.fetch_count, int(k))
                except ValueError:
                    continue

    def get(self) -> int:
        """現在選択されている取得回数を返す。"""
        return self.fetch_count

    def output_db(self) -> None:
        """計算済みの取得履歴を DB へ書き戻す。"""
        self.appstore.output_db(AppConfig.BASE_NAME_FETCH, self.fetch_assoc)

    def get_next_count(self) -> int:
        """DB の履歴を更新しながら次の取得回数を返す。"""
        fetch_assoc = self.appstore.get_file_assoc_from_db(AppConfig.BASE_NAME_FETCH)
        count, self.fetch_assoc = self._next_count(fetch_assoc)
        return count

    def _next_count(
        self, fetch_assoc: dict[str, str] | None
    ) -> tuple[int, dict[str, str]]:
        """履歴辞書から次に使う連番と更新後辞書を求める。"""
        if not fetch_assoc:
            next_count = 1
            fetch_assoc = { "1": Timex.get_now() }
            return next_count, fetch_assoc

        max_key = 0
        for key in fetch_assoc:
            try:
                max_key = max(max_key, int(key))
            except ValueError:
                continue

        next_count = max_key + 1
        fetch_assoc[str(next_count)] = Timex.get_now()
        return next_count, fetch_assoc
