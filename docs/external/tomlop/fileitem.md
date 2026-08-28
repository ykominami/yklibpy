# FileItem — 外部仕様書

## 概要

`yklibpy.tomlop.fileitem.FileItem`

ファイルパスと `Storex` を束ねる薄いラッパー。
パス文字列・`Path` オブジェクト・パス要素の配列を統一的に受け取り、ファイル種別を自動判定して `Storex` を生成する。

## クラスメソッド

### `setup(file_type_dict=AppConfig.file_type_dict) -> None`

`Storex` で使うファイル種別辞書を初期化する。
`Tomlop` のコンストラクタが一度だけ呼び出す。`FileItem` を使う前に必ず実行する必要がある。

## コンストラクタ

```python
FileItem(
    file: str | Path | list[str] | list[Path],
    data: Any = None,
)
```

- `file` がリストの場合: 先頭要素をルートとして残りを順に結合しパスを構築する。**注意**: リストの先頭を `pop` で取り出すため呼び出し後にリストが変更される。
- `file` が文字列または `Path` の場合: そのままパスとして使用する。

拡張子からファイル種別を `AppConfig.get_file_type` で判定する。

**Raises**: `ValueError` — 拡張子がサポートされていない（未知の種別）場合。

## インスタンス変数

| 変数名 | 型 | 説明 |
|--------|----|------|
| `file_path` | `Path` | 構築されたファイルパス |
| `file_type` | `str` | ファイル種別（`"YAML"` / `"JSON"` / `"TOML"`） |
| `storex` | `Storex` | 内部ストレージオブジェクト |

## パブリック API

### `get_file_type(file_path) -> str | None`

パスから判定したファイル種別を返す。

### `set_data(data: dict[str, Any]) -> None`

内部 `Storex` に保持するデータを更新する。

### `output(data: Any = None) -> None`

データを現在のファイルパスへ出力する。`data` が `None` の場合は `storex` の内部データを使用する。

### `get_name() -> str`

ファイル名（`file_path.name`）を返す。

### `get_path() -> Path`

ファイルの完全パスを返す。

### `with_suffix(suffix: str) -> Path`

同じパスに別拡張子を付けた `Path` を返す。

## 依存関係

- `yklibpy.config.appconfig.AppConfig`
- `yklibpy.db.storex.Storex`
