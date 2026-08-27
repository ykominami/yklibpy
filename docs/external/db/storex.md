# Storex — 外部仕様書

## 概要

`yklibpy.db.storex.Storex`

ファイル種別（YAML / JSON / TOML / プレーンテキスト）に応じた読み書きを抽象化するストレージラッパー。
パス要素の配列からファイルパスを構築し、種別を意識せずに `load` / `output` が呼べる。

## クラス変数

| 変数名 | 型 | 説明 |
|--------|----|------|
| `_file_type_dict` | `dict[str, str]` | ファイル種別名 → 拡張子のマッピング。`set_file_type_dict` で設定する |

## クラスメソッド

### `set_file_type_dict(file_type_dict: dict[str, str]) -> None`

拡張子解決に使うファイル種別辞書を設定する。`FileItem.setup()` が呼び出す。

### `get_ext_name(file_type: str) -> str`

ファイル種別に対応する拡張子を返す。

**Raises**: `KeyError` — `_file_type_dict` に未登録の種別を渡した場合。

## コンストラクタ

```python
Storex(
    file_type: str,
    file_name_array: list[Path] | list[str],
    data: Any = None,
)
```

`file_name_array` の先頭要素をルートとして残りを順に結合しファイルパスを構築する。
**注意**: `file_name_array` の先頭要素を `pop` で取り出すため、呼び出し後に元のリストは変更される。
`data` が `None` の場合は空辞書 `{}` を内部データとして初期化する。

## インスタンス変数

| 変数名 | 型 | 説明 |
|--------|----|------|
| `file_type` | `str` | ファイル種別 |
| `file_path` | `Path` | 構築されたファイルパス |
| `store` | `Any` | メモリ上の現在データ（初期値は空辞書または `data` 引数） |

## パブリック API

### `set_data(data: Any) -> None`

内部に保持するデータを置き換える。

### `get_value(key: str) -> Any`

保持データからキーに対応する値を返す。`store.get(key)` を使うため、存在しないキーは `None`。

### `get_store() -> Any`

内部に保持しているデータ全体を返す。

### `load() -> Any`

ファイルが存在する場合にそれを読み込み、ファイル種別に応じて復元して `store` に保存する。
ファイルが存在しない場合は `store` の現在値をそのまま返す。エンコーディングは UTF-8 固定。

| ファイル種別 | 使用ライブラリ |
|-------------|---------------|
| YAML | `yaml.safe_load` |
| JSON | `json.load` |
| TOML | `toml.load` |
| その他 | `f.readlines()` を `{"_lines": ...}` として格納 |

### `output(data: Any = None) -> None`

`data` または `store` をファイルへ書き出す。
親ディレクトリが存在しない場合は `mkdir(parents=True)` で自動作成する。エンコーディングは UTF-8 固定。

### `get_name() -> str`

保存先ファイル名（`file_path.name`）を返す。

### `get_path() -> Path`

保存先の完全パスを返す。

## 依存関係

- `json`（標準ライブラリ）
- `yaml` (`pyyaml`)
- `toml`
- `yklibpy.common.loggerx.Loggerx`
- `yklibpy.config.appconfig.AppConfig`
