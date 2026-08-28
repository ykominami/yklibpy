# Preparex — 内部仕様書

**ファイル**: `src/yklibpy/htmlparser/preparex.py`  
**継承**: なし

## 概要

設定からコマンド用・HTML パーサ用ディレクトリを準備し、設定ファイル名や出力ファイル名に基づく列挙処理を提供する。

---

## インスタンス変数

| 変数名 | 型 | 説明 |
|--------|----|------|
| `parts` | 設定依存 | ユーティリティカテゴリ一覧。 |
| `top_path` | `Path` | 探索と生成の起点。 |
| `bat1_path` | `Path` | コマンド関連ファイルの配置先。 |
| `htmlparser_path` | `Path` | HTML パーサ関連ファイルの配置先。 |

---

## メソッド

### `__init__(top_dir: str, category: str, config_parent_dir: str, assoc: dict[str, Any]) -> None`

設定を読み、必要なディレクトリを作成した後、設定拡張子に合うファイル名のカテゴリ部分を重複なしで収集する。

処理フロー:

1. `ConfigPrepare` からカテゴリ、コマンドディレクトリ、対象拡張子を取得する。
2. コマンド用と HTML パーサ用のディレクトリを再帰作成する。
3. 対象拡張子に一致するファイルを `Util.find_paths` で探索する。
4. ハイフンで二分できるファイル名の左側を `UniqueList` に追加する。

**Raises**: `OSError` — ディレクトリを作成できない場合。

### `list_files_containing(path: Path | str, search_string: str) -> List[Path]`

存在するディレクトリの直下から、名前に指定文字列を含む通常ファイルを列挙する。不正なディレクトリの場合は空配列を返す。

### `list_files(path: Path, name: str) -> List[Path]`

`list_files_containing` の結果をログ出力して返す。

### `list_htmlparser_files(name: str) -> List[Path]`

HTML パーサ用ディレクトリ直下の一致ファイルを列挙し、名前・拡張子等をログへ出す。

### `list_bat1_files(name: str) -> List[Path]`

コマンド用ディレクトリ直下の一致ファイルを列挙し、パスと名前をログへ出す。

### `list_utility_files(name: str, suffix: str) -> list[str]`

カテゴリ一覧、基準名、接尾辞を `Util.list_files` へ渡して想定ファイル名を生成する。

## 依存

| クラス/変数 | 用途 |
|-------------|------|
| `ConfigPrepare` | 設定辞書の既知キーへアクセスする。 |
| `Util.find_paths` | 設定ファイル候補を再帰探索する。 |
| `Util.UniqueList` | カテゴリ名を重複なく保持する。 |
| `Util.list_files` | ユーティリティファイル名を組み立てる。 |
| `Loggerx` | 探索状況を記録する。 |

## 設計上の注意

初期化時に `htmlparser_path.mkdir` を重複して呼び出す。収集したローカル変数 `ul` はインスタンスへ保存されないため、現行コードではログ出力以外に利用できない。ファイル列挙は再帰せず直下のみを対象とする。
