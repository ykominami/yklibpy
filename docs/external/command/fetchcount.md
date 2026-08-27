# FetchCount — 外部仕様書

## 概要

`yklibpy.command.fetchcount.FetchCount`

GitHub などからの取得済みデータの世代番号（取得回数）を管理するクラス。
リフレッシュが必要かどうかに応じて「次の新しい番号」または「既存の最大番号」を選択する。

## コンストラクタ

```python
FetchCount(
    needness_of_refresh: bool,
    needness_of_top_dir: bool,
    appstore: AppStore,
)
```

- `needness_of_refresh` が `True` の場合: 新しい連番を採番して `fetch_count` に設定する。
- `needness_of_refresh` が `False` の場合: `appstore` から既存の最大番号を読み取って `fetch_count` に設定する。既存 DB が空の場合は `1`。

## インスタンス変数

| 変数名 | 型 | 説明 |
|--------|----|------|
| `fetch_count` | `int` | 現在選択されている取得回数 |
| `needness_of_refresh` | `bool` | リフレッシュ（新規取得）が必要かどうか |
| `needness_of_top_dir` | `bool` | トップディレクトリが必要かどうか（現行実装では参照のみ） |
| `appstore` | `AppStore` | 取得履歴 DB へのアクセス窓口 |
| `fetch_assoc` | `dict[str, str]` | 採番後の取得履歴辞書 |

## パブリック API

### `get() -> int`

現在選択されている取得回数を返す。

### `output_db() -> None`

採番済みの取得履歴辞書を `appstore` 経由で DB へ書き戻す。
`needness_of_refresh=True` の場合に、`get_next_count` で更新した `fetch_assoc` を永続化するために呼び出す。

### `get_next_count() -> int`

`appstore` の `fetch` DB を読み込み、次の連番を採番して `fetch_assoc` に記録する。
内部的に `_next_count` を呼び出す。

## 内部メソッド

### `_next_count(fetch_assoc) -> tuple[int, dict[str, str]]`

履歴辞書から次に使う連番と更新後の辞書を返す。
`fetch_assoc` が `None` または空の場合は `1` から開始する。

## 制約

- `output_db` は `get_next_count` を呼び出した後でのみ意味を持つ（`needness_of_refresh=True` のケース）。
- `needness_of_top_dir` は現行実装ではフィールドに保持されるだけで使用されていない。

## 依存関係

- `yklibpy.common.timex.Timex`
- `yklibpy.config.appconfig.AppConfig`
- `yklibpy.db.appstore.AppStore`
