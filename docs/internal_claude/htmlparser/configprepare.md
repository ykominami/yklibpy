# ConfigPrepare — 内部仕様書

## モジュール

`yklibpy.htmlparser.configprepare`

## インスタンス変数

| 変数名 | 型 | 役割 |
|--------|----|------|
| `parent_file_path` | `Path` | 設定ファイルの親ディレクトリパス（現時点でメソッド内では未使用） |
| `assoc` | `dict[str, Any]` | 設定全体を保持する辞書 |

## メソッドの実装詳細

すべてのメソッドは `self.assoc` への直接アクセスのラッパー：

| メソッド | アクセスキー |
|----------|-------------|
| `get(key)` | `assoc[key]` |
| `get_command()` | `assoc["command"]` |
| `get_command_dir()` | `assoc["command"]["dir"]` |
| `get_category_config_file_extname()` | `assoc["category-config-file-extname"]` |
| `get_utility_category()` | `assoc["command"]["utility-category"]` |
| `get_utility_root()` | `assoc["command"]["utility-root"]` |
| `get_category()` | `assoc["category"]` |
| `get_htmlparser()` | `assoc["category"]["htmlparser"]` |

キーが存在しない場合は `KeyError` が送出される（ガードなし）。

## 依存関係

- `pathlib.Path`（標準ライブラリ）
