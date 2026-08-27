# Preparex — 外部仕様書

## 概要

`yklibpy.htmlparser.preparex.Preparex`

設定辞書をもとに関連ディレクトリを準備し、対象ファイル名を列挙するクラス。
コンストラクタで `htmlparser_path` と `bat1_path` を作成し、設定拡張子に合うファイル名の先頭部分を `UniqueList` で収集する。

## コンストラクタ

```python
Preparex(
    top_dir: str,
    category: str,
    config_parent_dir: str,
    assoc: dict[str, Any],
)
```

- `top_dir`: 最上位ディレクトリのパス文字列。
- `category`: HTML パーサ出力ディレクトリ名。
- `config_parent_dir`: `ConfigPrepare` に渡す親設定ファイルのディレクトリ。
- `assoc`: `ConfigPrepare` に渡す設定辞書。

コンストラクタで以下を行う:
1. `htmlparser_path` と `bat1_path` を `mkdir(parents=True, exist_ok=True)` で作成する。
2. `top_dir` 配下を再帰探索し、設定拡張子（`category-config-file-extname`）に合うファイルのステム先頭部（ハイフン区切り左辺）を `UniqueList` に収集する。

## インスタンス変数

| 変数名 | 型 | 説明 |
|--------|----|------|
| `parts` | `Any` | `ConfigPrepare.get_utility_category()` が返すカテゴリ一覧 |
| `top_path` | `Path` | 最上位ディレクトリ |
| `bat1_path` | `Path` | コマンドファイルの配置ディレクトリ |
| `htmlparser_path` | `Path` | HTML パーサ出力ディレクトリ |

## パブリック API

### `list_files_containing(path, search_string) -> List[Path]`

指定ディレクトリ直下で名前に `search_string` を含むファイルを列挙する。
ディレクトリが存在しない場合や対象がファイルでない場合は除外する。

### `list_files(path, name) -> List[Path]`

`list_files_containing` を呼び出し、結果をデバッグログに出力してから返す。

### `list_htmlparser_files(name) -> List[Path]`

`htmlparser_path` 直下から名前に `name` を含むファイルを列挙する。

### `list_bat1_files(name) -> List[Path]`

`bat1_path` 直下から名前に `name` を含むファイルを列挙する。

### `list_utility_files(name, suffix) -> list[str]`

`parts`（ユーティリティカテゴリ一覧）と `name` / `suffix` から想定ファイル名を組み立てて返す。
内部で `Util.list_files` を使用する。

## 依存関係

- `yklibpy.common.loggerx.Loggerx`
- `yklibpy.common.util.Util`
- `yklibpy.htmlparser.configprepare.ConfigPrepare`
