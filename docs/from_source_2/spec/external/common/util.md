# 外部仕様書 — `Util`

**対象クラス**: `Util`  
**対応機能**: 文字列、URL、パス、文字コード、DOM、TSV の共通操作

## 未確定事項（本書作成にあたっての前提）

- 正とされる用語・ファイル定義2 文書が欠落し、代替候補も空です。ファイル配置、TSV スキーマ、URL の許容範囲は現行実装の挙動として記載します。異なる意図であればお知らせください。

## 1. 概要

再帰的パス探索、URL 検証、文字列正規化、ファイル作成、文字コード判定、DOM 共通親探索、TSV 入出力などを提供します。

## 2. 公開仕様

| 分類 | 操作 | 外部挙動 |
|---|---|---|
| パス | `find_paths` | `rglob` 結果を `file` / `dir` / `both` で絞ります |
| パス | `ensure_file_path` / `ensure_dir_path` | 親を含めて作成し、前者はファイルを touch します。`None` はそのまま返します |
| URL | `is_valid_urls` | 各 URL を理由付き `Result` にし、無効値も例外にしません |
| 抽出 | `extract_cid` / `extract_product_id` / `extract_base` | クエリ風文字列から値を抽出し、未検出時は空文字または `None` です |
| 配列 | `flatten_gen` / `flatten` | 入れ子の `list` だけを再帰展開します |
| 文字コード | `detect_encoding` / `decode_cli_output` | chardet 推定、または UTF-8→CP932→環境既定→置換 UTF-8 の順でデコードします |
| 文字コード | `get_default_encoding` | `locale.getpreferredencoding(False)` が返す環境既定の文字コード名を返します |
| DOM | `get_common_parents` | 2 要素の共通親をルート側から返します |
| TSV | `load_tsv` / `output_tsv` | UTF-8、タブ区切り、改行 `\n` で辞書配列を入出力します。`output_tsv` で辞書のキーと値を出力するには `fieldnames` の明示が必要で、省略時は空行だけを出力します |
| 文字列 | `remove_crlf` / `remove_whitespace` / `remove_non_printable` | 改行、空白類、非表示文字をそれぞれ除去します |
| 文字列 | `get_valid_string` / `is_empty` / `normalize_string` | `None` と空白入力を空として扱い、正規化結果が空なら `None` です |
| 辞書 | `array_to_dict` / `swap_dict` | 指定キーによる辞書化、キー・値の交換を行います |
| 名前 | `sanitize_dir_name` | Windows 禁止文字を `_` に置換し、空なら `_none` を返します |
| ログ | `xyz` | 固定文字列 `xyz` を INFO ログへ出力します |

`list_files(name, parts, suffix)` は `name-part-suffix` 形式を返します。`get_location*` は実装または呼び出し位置を返します。`test_yaml` / `test_tsv` は特定の `Time` / `Course_ID` 列を前提とする補助処理です。

## 3. 作成・更新するファイル

`ensure_file_path` は指定ファイル、`ensure_dir_path` は指定ディレクトリ、`output_tsv` は任意指定された出力先を作成・更新します。`test_yaml` / `test_tsv` は指定出力と派生 `.tsv` を更新します。正規の配置定義が欠落しているため、許可ルートは未確定です。

## 4. エラー処理・終了コード

| 事象 | 挙動 | 終了コード |
|---|---|---|
| `find_paths` の起点がディレクトリでない | `ValueError: <path> はディレクトリではありません` | CLI 未捕捉時 `1` |
| 空 TSV かつ `fieldnames` なし | `ValueError: ヘッダー行が存在しません。fieldnamesを指定してください。` | CLI 未捕捉時 `1` |
| 空 records かつ `fieldnames` なし | `ValueError: fieldnamesを指定するか、recordsに1件以上のデータを含めてください。` | CLI 未捕捉時 `1` |
| 1件以上の records かつ `fieldnames` なし | 辞書のキーと値を含めず、records の件数に応じた空行を出力 | コマンド自体は異常終了しません |
| `array_to_dict` の要素が辞書でない | 型名を含む `TypeError` | CLI 未捕捉時 `1` |
| 指定キー欠落 | 利用可能キーを含む `KeyError` | CLI 未捕捉時 `1` |
| 辞書キーにできない値 | 型名を含む `ValueError` | CLI 未捕捉時 `1` |
| ファイル I/O、DOM、YAML 等の失敗 | 原因例外を伝播 | CLI 未捕捉時 `1` |
| URL が無効 | 例外にせず `success=False` の結果 | コマンド自体は異常終了しません |

ライブラリ API 自体には終了コードはありません。

## 5. 実装上の対応（参考）

本節は実装を拘束しません。`src/yklibpy/common/util.py` が処理します。`test_yaml` / `test_tsv` は用途固有で、一般的な共通 API としては入力スキーマが固定されています。
