# Tomlop — 外部仕様書

## 概要

`yklibpy.tomlop.tomlop.Tomlop`

TOML と YAML の比較・変換・差分出力を扱うクラス。
設定ファイルの補完やフォーマット変換を CLI から実行する用途を想定する。

## コンストラクタ

```python
Tomlop()
```

`FileItem.setup()` はプロセス内で一度だけ実行する（`_count` でガード）。

## インスタンス変数

| 変数名 | 型 | 説明 |
|--------|----|------|
| `data` | `Any` | 直近に読み込んだデータ。初期値は空辞書 |
| `ref_file_item` | `FileItem` | `setup` 後に設定される参照元ファイル |
| `config_file_item` | `FileItem \| None` | `setup` 後に設定される比較先設定ファイル |

## パブリック API

### `setup(ref_file, config_file) -> None`

参照元ファイルと設定ファイルの `FileItem` を準備する。
`config_file` が `None` の場合は `config_file_item` を `None` のまま保持する。

### `compare_dict(dict1, dict2) -> bool`

2 つの辞書が再帰的に完全一致するかを判定する。
キー集合が異なる場合、または再帰的にいずれかの値が異なる場合は `False` を返す。

### `merge_dict(dict1, dict2) -> dict[str, Any]`

`dict2` のうち `dict1` に存在しないキーだけを補完する。
既存キーは維持され、双方が辞書の場合のみ再帰的に処理する。
`dict1` を破壊的に変更して返す。

### `diff_dict(dict1, dict2) -> str`

2 つの辞書の差分を可読な文字列として返す。
片方にしか存在しないキー、値が異なるキーをそれぞれ区別して整形する。
差分がなければ空文字を返す。

### `read_toml_external(file_path) -> dict[str, Any] | None`

外部 TOML ファイルを読み込む。
読み込み成功時は辞書を返し、失敗時（ファイル未存在・パースエラー）は `None` を返す。

### `write_toml_external(file_path, data) -> bool`

辞書を TOML ファイルへ書き出す。成功時は `True`、失敗時は `False` を返す。

### `load_toml(ref_file) -> dict[str, Any] | None`

`ref_file` が指定された場合に `read_toml_external` を呼び出す。`None` が渡された場合はそのまま `None` を返す。

### `exec() -> None`

参照ファイルとの差分を計算し、補完結果（`new_pyproject.toml`）と差分（`diff_pyproject.toml`）を出力する。

**Raises**: `ValueError` — `config_file_item` が `None`（`setup` で設定ファイルが指定されていない）場合。

### `main() -> None`

CLI 引数（`sys.argv`）を解釈して主要処理を起動する。
`sys.argv[1]` が ref_file、`sys.argv[2]` が config_file（省略時は `"pyproject.toml"`）。
ref_file が指定された場合のみ `setup` を実行し、YAML 拡張子で結果を書き出す。

### `toml2yaml() -> None`

`sys.argv[1]` の TOML ファイルを読み込み、`a.yaml` へ変換して保存する。

### `yaml2toml() -> None`

`sys.argv[1]` の YAML ファイルを読み込む。出力先パスを決定するが、現行実装では実際の書き出しは行わない。

## モジュールレベルのエントリポイント

| 関数 | 説明 |
|------|------|
| `zmain()` | `Tomlop.main()` を起動する |
| `toml2yaml()` | `Tomlop.toml2yaml()` を起動する |
| `yaml2toml()` | `Tomlop.yaml2toml()` を起動する |

## 依存関係

- `toml`
- `yklibpy.common.loggerx.Loggerx`
- `yklibpy.common.util_yaml.UtilYaml`
- `yklibpy.config.appconfig.AppConfig`
- `yklibpy.tomlop.fileitem.FileItem`
