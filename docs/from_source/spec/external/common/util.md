# 外部仕様書 — `util`

**対象クラス**: `yklibpy.common.util.Util`（内部に `UniqueList`/`Result` をネスト）
**対応サブコマンド**: なし（ライブラリクラス）

本書は `docs/projects/def_ot_terms.md`（用語の定義）および `docs/projects/def_of_file_and_dir.md`（ディレクトリ/ファイル定義）を正とする方針で作成したが、本書作成時点で両ファイルは空である。そのため本書の記述はすべて「現行実装の挙動」に基づく。

## 未確定事項（本書作成にあたっての前提）

- 定義ドキュメント 2 件がいずれも空のため、定義由来の記述は存在せず、全記述を「現行実装の挙動」として扱った。異なる意図であればお知らせください。

## 1. 概要

文字列処理、パス探索、エンコーディング判定、TSV 変換、URL 検証など、他モジュールから横断的に使う補助処理をまとめた汎用ユーティリティ群。ほぼ全メソッドが classmethod で、状態を持たない。

## 2. 公開インタフェース

### ネストクラス

| クラス | 説明 |
|--------|------|
| `Util.UniqueList[T]` | 重複を除きつつ追加順を保つコレクション。`append(value)` は未登録の値だけを末尾へ追加し、反復すると保持順で列挙される |
| `Util.Result` | URL 検証の成否（`success`）・対象 URL（`url`）・理由文字列（`reason`）・`urlparse` 結果（`parsed`）を保持する入れ物 |

### パス・ファイル系

| メソッド | 説明 |
|---------|------|
| `find_paths(base_dir, pattern, target_type="both") -> list[Path]` | `base_dir` 配下を再帰探索し、`target_type`（`"file"`/`"dir"`/`"both"`）で絞り込んだパス一覧を返す |
| `ensure_file_path(path) -> Path \| None` | ファイルと親ディレクトリの存在を保証して返す。親ディレクトリが存在しなければ作成し、ファイルは既存でも無条件に `touch` する。`None` 入力はそのまま `None` |
| `ensure_dir_path(path) -> Path \| None` | ディレクトリの存在を保証して返す。`None` 入力はそのまま `None` |
| `sanitize_dir_name(name) -> str` | Windows で使えない文字を `_` に置換し、前後の空白・末尾のピリオドを除去したディレクトリ名を返す。結果が空文字になった場合は `"_none"` |
| `list_files(name, parts, suffix) -> list[str]` | `"{name}-{part}{suffix}"` 形式のファイル名候補一覧を組み立てる |

### エンコーディング系

| メソッド | 説明 |
|---------|------|
| `detect_encoding(input_path) -> str \| None` | ファイル内容から推定した文字エンコーディング名を返す（推定失敗時は `None`） |
| `get_default_encoding() -> str` | 実行環境の既定エンコーディングを返す |
| `decode_cli_output(data) -> str` | バイト列を `utf-8` → `cp932` → 環境既定の順に試してデコードし、すべて失敗すれば置換文字付き `utf-8` でデコードする。空入力は空文字 |

### 文字列系

| メソッド | 説明 |
|---------|------|
| `remove_crlf(string)` / `remove_whitespace(string)` / `remove_non_printable(string)` | それぞれ改行コード/空白類/表示不能文字を取り除く |
| `get_valid_string(string) -> str` | `None`/空文字を空文字へ正規化し、それ以外は空白除去した文字列を返す |
| `is_empty(string) -> bool` | 入力が実質的に空文字かどうかを判定する |
| `normalize_string(string) -> str \| None` | 有効な文字列だけを返し、空なら `None` を返す |
| `extract_cid(text)` / `extract_product_id(text)` -> `str` | `cid=`/`product_id=` パラメータ値を抽出する。見つからなければ空文字 |
| `extract_base(base, text) -> str \| None` | 指定名のクエリパラメータ値を抽出する。見つからなければ `None` |

### コレクション・表形式系

| メソッド | 説明 |
|---------|------|
| `flatten(items) -> list[Any]` / `flatten_gen(lst) -> Iterator[Any]` | 入れ子リストを順序を保ったまま平坦化する（リスト版とジェネレータ版） |
| `array_to_dict(data, key) -> dict[str, dict[str, Any]]` | 辞書配列を指定キーの値（文字列化）で参照できる連想配列へ変換する |
| `swap_dict(dict) -> dict[str, str]` | キーと値を入れ替えた辞書を返す。空辞書なら空辞書 |
| `load_tsv(input_path, fieldnames=None) -> list[dict[str, str]]` | TSV ファイルを行ごとの辞書配列へ変換する。`fieldnames` 省略時は先頭行をヘッダーとして扱う |
| `output_tsv(records, output_path=None, fieldnames=None) -> str` | 辞書配列を TSV 文字列へ変換し、`output_path` があればファイルへも保存する |

### URL・HTML 系

| メソッド | 説明 |
|---------|------|
| `is_valid_urls(urls) -> list[Util.Result]` | URL 一覧を検証し、入力順のまま `Result` の配列として返す。無効な URL も例外にせず理由付きの `Result` にする |
| `get_common_parents(element1, element2) -> list[Tag]` | 2 つの BeautifulSoup 要素に共通する親タグ一覧をルートに近い順で返す |

## 3. 作成・更新するディレクトリ・ファイル

| 対象 | 契機 | 内容 |
|------|------|------|
| `path` の親ディレクトリと `path` 自身 | `ensure_file_path()` | 親ディレクトリを作成し、空ファイルを `touch` する |
| `path` ディレクトリ | `ensure_dir_path()` | ディレクトリを再帰的に作成する |
| `output_path` に指定したファイル | `output_tsv()` で `output_path` 指定時 | TSV 文字列（UTF-8） |

## 4. エラー処理・終了コード

| 事象 | 挙動 |
|------|------|
| `find_paths()` の `base_dir` がディレクトリでない | `ValueError` が呼び出し元へ伝播する |
| `load_tsv()` でヘッダー行が存在せず `fieldnames` も未指定 | `ValueError` が呼び出し元へ伝播する |
| `output_tsv()` で `records` が空かつ `fieldnames` も未指定 | `ValueError` が呼び出し元へ伝播する |
| `array_to_dict()` の要素が辞書でない | `TypeError` が呼び出し元へ伝播する |
| `array_to_dict()` の要素に `key` が存在しない | `KeyError` が呼び出し元へ伝播する |
| `array_to_dict()` の `key` の値が文字列・数値・真偽値でない | `ValueError` が呼び出し元へ伝播する |
| 上記以外のファイル入出力失敗 | `OSError` 系が呼び出し元へ伝播する |

ライブラリクラスであり単体のコマンドとして起動される経路は無いため、終了コードは規定しない。

## 5. 実装上の対応（参考）

本節は実装を拘束しない。

| 役割 | モジュール |
|------|-----------|
| 汎用ユーティリティ群 | `yklibpy.common.util.Util` |
| Udemy データ比較の試験用処理（`test_yaml`/`test_tsv`） | 同クラスのインスタンスメソッド（アドホック処理であり、汎用 API としては非推奨 — 現行実装の挙動） |
