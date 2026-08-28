# DbYaml — 内部仕様書

## モジュール

`yklibpy.db.db_yaml`

## 継承

`DbBase` を継承する。

## インスタンス変数

| 変数名 | 型 | 役割 |
|--------|----|------|
| `fname` | `str` | 保存先ファイルパス（文字列） |
| `fname_path` | `Path` | `Path(fname)` に変換した保存先 |
| `data` | `dict[str, Any]` | メモリ上の作業用データ |

## `load` の処理フロー

1. `Util.ensure_file_path(self.fname_path)` でファイルと親ディレクトリの存在を保証する
2. `encoding` が `None` なら `Util.detect_encoding` で推定する。推定失敗なら `Util.get_default_encoding` で環境デフォルトを使う
3. `UtilYaml._register_constructors(tags)` でカスタムタグを登録
4. `yaml.safe_load` で読み込み、結果が `None`（空ファイル）なら `{}` を `self.data` にセット
5. 読み込んだ辞書を返す

## `save` の実装詳細

- `UtilYaml.save_yaml(self.data, self.fname_path)` を呼び、常に `True` を返す

## `list_text(key: str)` の実装詳細

- `self.data.values()` の各値を `dict[str, Any]` にキャストし、`key` で取り出したリストを返す
- 存在しないキーは `KeyError` を送出する

## `__main__` ブロック

- 引数が指定された場合は `Loggerx.error` でメッセージを出力して `SystemExit(10)` で終了する

## 依存関係

- `yaml`, `sys`, `pathlib.Path`（標準ライブラリ）
- `yklibpy.common.loggerx.Loggerx`
- `yklibpy.common.util.Util`
- `yklibpy.common.util_yaml.UtilYaml`
- `yklibpy.db.db_base.DbBase`
