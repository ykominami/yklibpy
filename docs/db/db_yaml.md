# DbYaml — 外部仕様書

## 概要

`yklibpy.db.db_yaml.DbYaml`

YAML ファイルを背後ストアとして使う簡易 DB 実装。
辞書形式のデータをメモリ上に保持し、`load` / `save` で YAML ファイルと相互変換する。

## 継承

```
DbBase
  └── DbYaml
```

## コンストラクタ

```python
DbYaml(fname: str)
```

保存先ファイルパスを受け取り、空の内部データで初期化する。

## インスタンス変数

| 変数名 | 型 | 説明 |
|--------|----|------|
| `fname` | `str` | 保存先ファイルパス（文字列） |
| `fname_path` | `Path` | `fname` を `Path` に変換したもの |
| `data` | `dict[str, Any]` | メモリ上の現在データ |

## パブリック API

### `load(encoding=None, tags=None) -> dict[str, Any]`

YAML ファイルを読み込み、内部データとして保持する。

- `encoding` が省略された場合は `chardet` でエンコーディングを推定する。推定に失敗した場合は `locale.getpreferredencoding` を使用する。
- `tags` に追加 YAML タグを渡すと `UtilYaml._register_constructors` で登録される（一度きり）。
- ファイルが存在しない場合は `Util.ensure_file_path` で空ファイルを作成してから読み込む。
- 読み込みに失敗した場合（エンコーディング検出エラーなど）は空辞書 `{}` を返す。

### `save() -> bool`

保持中の `data` を YAML ファイルへ保存する。成功時は `True` を返す。

### `get_data() -> dict[str, Any]`

現在保持している全データを返す。

### `set_data(data: dict[str, Any]) -> bool`

内部データを丸ごと置き換える。成功時は `True` を返す。

### `get_item(key: str) -> Any`

指定キーの値を返す。

**Raises**: `KeyError` — `key` が内部データに存在しない場合。

### `set_item(key: str, value: Any) -> bool`

指定キーへ値を設定する。成功時は `True` を返す。

### `clear() -> bool`

保持しているデータを空辞書で初期化する。成功時は `True` を返す。

### `count() -> int`

保持しているキー数を返す。

### `list_text(key: str) -> list[Any]`

各レコード（値が辞書）から指定キーの値だけを抽出して返す。

**Raises**: `KeyError` — いずれかのレコードに `key` が存在しない場合。

## 依存関係

- `yaml` (`pyyaml`)
- `yklibpy.common.loggerx.Loggerx`
- `yklibpy.common.util.Util`
- `yklibpy.common.util_yaml.UtilYaml`
- `yklibpy.db.db_base.DbBase`
