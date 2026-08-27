# FetchCount — 内部仕様書

## モジュール

`yklibpy.command.fetchcount`

## インスタンス変数

| 変数名 | 型 | 役割 |
|--------|----|------|
| `fetch_count` | `int` | 決定された取得回数（`-1` で未確定） |
| `needness_of_refresh` | `bool` | 新規ダウンロードが必要かどうか |
| `needness_of_top_dir` | `bool` | トップディレクトリ準備が必要かどうか（現時点でロジックに未使用） |
| `appstore` | `AppStore` | DB 読み書き用のストア |
| `fetch_assoc` | `dict[str, str]` | 更新後の取得履歴辞書（`_next_count` が返す） |

## `__init__` の処理フロー

- `needness_of_refresh == True` → `get_next_count()` で新番号を採番
- `needness_of_refresh == False` → DB から既存履歴を読み込み、整数キーの最大値を `fetch_count` にセット（最小値 1）

## プライベートメソッド

### `_next_count(fetch_assoc: dict[str, str] | None) -> tuple[int, dict[str, str]]`

- `fetch_assoc` が空 / None → `next_count = 1`、辞書を `{"1": now}` で初期化して返す
- それ以外 → 整数変換可能なキーのうち最大値 + 1 を採番し、`fetch_assoc[str(next_count)] = now` を追記して返す
- `ValueError` は `continue` でスキップ（非整数キーを無視）

## `get_next_count` の処理フロー

1. `appstore.get_file_assoc_from_db(AppConfig.BASE_NAME_FETCH)` で取得履歴辞書を読み込む
2. `_next_count` で次番号と更新済み辞書を計算
3. `self.fetch_assoc` に更新済み辞書を保存して番号を返す

## `output_db` の処理フロー

- `appstore.output_db(AppConfig.BASE_NAME_FETCH, self.fetch_assoc)` で更新済み辞書を書き戻す
- `__init__` では書き戻しは行わない（呼び出し元が `output_db` を明示的に呼ぶ必要がある）

## `Command.get_next_count` との違い

`Command.get_next_count` は採番と書き戻しを一体化しているが、`FetchCount` は書き戻しを `output_db` に分離することで採番後に追加処理を挟める設計。

## 依存関係

- `yklibpy.common.timex.Timex`
- `yklibpy.config.appconfig.AppConfig`
- `yklibpy.db.appstore.AppStore`
