# Util — 内部仕様書

**ファイル**: `src/yklibpy/common/util.py`
**継承**: なし

## 概要

文字列処理、パス探索、エンコーディング判定、TSV 変換、URL 検証など、他モジュールから横断的に使う補助処理をまとめた汎用ユーティリティ群。ほぼ全メソッドが `classmethod` で、状態を持たない静的ヘルパー集として設計されている。内部に `UniqueList` と `Result` の 2 つの補助クラスをネストして持つ。

---

## モジュールレベル定数・型

| 変数名 | 値/型 | 用途 |
|--------|-------|------|
| `TargetType` | `Literal["file", "dir", "both"]` | `find_paths` の探索対象種別を表す型エイリアス。 |
| `T` | `TypeVar` | `UniqueList[T]` のジェネリック型パラメータ。 |

---

## クラス定数

| 定数名 | 値 | 説明 |
|--------|----|------|
| `WINDOWS_RESERVED_PATTERN` | `re.compile(r'[<>:"/\\|?*\x00-\x1f]')` | Windows でディレクトリ名に使えない文字の正規表現。 |

---

## ネストクラス

### `Util.UniqueList[T]`

重複を除きつつ追加順を保つ簡易コレクション。

| 変数名 | 型 | 説明 |
|--------|----|------|
| `_set` | `set[T]` | 重複判定用の集合。 |
| `_list` | `list[T]` | 挿入順を保持する配列。 |

- `append(value: T) -> None` — 未登録の値だけを末尾へ追加する。
- `__iter__() -> Iterator[T]` — 保持順のまま反復できるイテレータを返す。
- `__repr__() -> str` — デバッグ用に内部リストの表現を返す。

### `Util.Result`

URL 検証の成否と補足情報を保持する入れ物。

| 変数名 | 型 | 説明 |
|--------|----|------|
| `success` | `bool` | 検証の成否。 |
| `url` | `str` | 検証対象の URL。 |
| `reason` | `str` | 成否の理由文字列。 |
| `parsed` | `ParseResult \| None` | `urlparse` の解析結果。 |

---

## メソッド

### `get_location() -> str` (classmethod)

このモジュールファイルの位置（`__file__`）を文字列で返す。

### `get_location_string() -> str` (classmethod)

呼び出し元のファイル名、行番号、関数名を `"filename:lineno in function"` 形式で返す。フレーム情報が取得できない場合は `"unknown"`。

### `find_paths(base_dir: Path, pattern: str, target_type: TargetType = "both") -> list[Path]` (classmethod)

`base_dir.rglob(pattern)` で再帰探索し、`target_type` に応じてファイル/ディレクトリ/両方を絞り込んで返す。

**Raises**: `ValueError` — `base_dir` がディレクトリでない場合。

### `xyz() -> None` (classmethod)

簡易動作確認用に固定文字列 `"xyz"` をログ出力する。

### `list_files(name: str, parts: Sequence[str], suffix: str) -> list[str]` (classmethod)

名前・区分・拡張子から `"{name}-{part}{suffix}"` 形式のファイル名候補一覧を組み立てる。

### `is_valid_urls(urls: List[str]) -> List["Util.Result"]` (classmethod)

URL 一覧を検証し、各要素の結果を入力順のまま `Result` の配列として返す。無効な URL も例外にはせず、理由付きの `Result` にする。

```
処理フロー:
  1. url が空文字/None なら "URL is empty" の失敗 Result
  2. urlparse 後 scheme が無ければ "URL scheme is invalid" の失敗 Result
  3. netloc/path/fragment すべて空なら "URL is not a valid URI" の失敗 Result
  4. いずれにも該当しなければ成功 Result
```

### `extract_cid(text: str) -> str` / `extract_product_id(text: str) -> str` (classmethod)

文字列から `cid=`/`product_id=` パラメータ値を正規表現で抽出する。見つからなければ空文字。

### `extract_base(base: str, text: str) -> str | None` (classmethod)

指定名のクエリパラメータ値を抽出する。見つからなければ `None`。

### `flatten_gen(lst: list[Any]) -> Iterator[Any]` (classmethod)

入れ子リストを再帰的に平坦化するジェネレータを返す。

### `ensure_file_path(path: Path | None) -> Path | None` (classmethod)

ファイルと親ディレクトリの存在を保証して返す。`path` が `None` ならそのまま `None` を返す。親ディレクトリが存在しなければ作成したうえで、`path.touch()` を常に実行する（ファイルが既に存在する場合も含め無条件に呼ばれる）。

### `ensure_dir_path(path: Path | None) -> Path | None` (classmethod)

ディレクトリの存在を保証して返す（`mkdir(parents=True, exist_ok=True)`）。`path` が `None` ならそのまま `None` を返す。

### `flatten(items: Iterable[Any]) -> list[Any]` (classmethod)

入れ子の配列を順序を保ったまま 1 次元化する。`flatten_gen()` とは呼び出し関係を持たない独立した再帰実装であり、結果は等価だがロジックが重複している。

### `detect_encoding(input_path: Path) -> Optional[str]` (classmethod)

ファイル内容をバイナリで読み込み、`chardet.detect` で推定した文字エンコーディングを返す。`input_path` が `None` なら `None`。

### `get_default_encoding() -> str` (classmethod)

実行環境の既定エンコーディング（`locale.getpreferredencoding(False)`）を返す。

### `decode_cli_output(data: bytes | None) -> str` (classmethod)

CLI のバイト列出力を文字列へデコードする。`utf-8` → `cp932` → 環境既定の順に試し、すべて失敗すれば `errors="replace"` 付き `utf-8` でデコードする。`data` が空なら空文字。

### `get_common_parents(element1: Tag, element2: Tag) -> List[Tag]` (classmethod)

2 つの BeautifulSoup 要素に共通する親タグ一覧を、ルートに近い順で返す。内部関数 `get_all_parents` で各要素の祖先を集め、`id()` による集合比較で共通部分を抽出する。

### `load_tsv(input_path: Path, fieldnames: Optional[Sequence[str]] = None) -> list[dict[str, str]]` (classmethod)

TSV ファイルを読み込み、行ごとの辞書配列へ変換する。`fieldnames` 省略時は先頭行をヘッダーとして扱う。

**Raises**: `ValueError` — ヘッダー行が存在せず `fieldnames` も指定されない場合。

### `output_tsv(records: Sequence[dict[str, str]], output_path: Optional[Path] = None, fieldnames: Optional[Sequence[str]] = None) -> str` (classmethod)

辞書配列を TSV 文字列へ変換し、`output_path` があればファイルへも保存する。

**Raises**: `ValueError` — `records` が空で `fieldnames` も指定されない場合。

### `test_yaml(input_file: str, input_file_2: str, output_file: str) -> None`

Udemy 用 YAML データ 2 系統を比較し、既存の `Time` 列を新データへ引き継いで保存する。インスタンスメソッドだが内部状態は使わない。

### `test_tsv(input_file: str, input_file_2: str, output_file: str) -> None`

Udemy 用 TSV データ 2 系統を比較し、`Course_ID` が一致するレコードの `Time` 列を引き継いで保存する。インスタンスメソッドだが内部状態は使わない。

### `remove_crlf(string: str) -> str` / `remove_whitespace(string: str) -> str` / `remove_non_printable(string: str) -> str` (classmethod)

それぞれ改行コード、空白類、表示不能文字を文字列から取り除く。

### `get_valid_string(string: str | None) -> str` (classmethod)

`None` や空文字を空文字へ正規化し、それ以外は空白除去した文字列を返す。

### `is_empty(string: str | None) -> bool` (classmethod)

入力が実質的に空文字かどうかを判定する。

### `normalize_string(string: str | None) -> str | None` (classmethod)

有効な文字列だけを返し、空なら `None` を返す。

### `array_to_dict(data: list[dict[str, Any]], key: str) -> dict[str, dict[str, Any]]` (classmethod)

辞書配列を指定キーの値（文字列化）で参照できる連想配列へ変換する。

**Raises**: `TypeError` — 要素が辞書でない場合。`KeyError` — 要素に `key` が存在しない場合。`ValueError` — `key` の値が文字列・数値・真偽値でない場合。

### `swap_dict(dict: dict[str, str]) -> dict[str, str]` (classmethod)

キーと値を入れ替えた辞書を返す。空辞書なら空辞書を返す。

### `sanitize_dir_name(name: str) -> str` (classmethod)

gist 名を Windows でも使えるディレクトリ名へ正規化する。`WINDOWS_RESERVED_PATTERN` に一致する禁止文字を `_` に置換し、前後の空白・末尾のピリオドを除去する。結果が空文字になった場合は `"_none"` を返す。

---

## 依存

| クラス/変数 | 用途 |
|-------------|------|
| `Loggerx` | 各所でのデバッグログ出力 |
| `UtilYaml` | `test_yaml` での YAML 読み書き |
| `chardet` | `detect_encoding` でのエンコーディング推定 |
| `bs4.Tag` | `get_common_parents` の型 |

---

## 設計上の注意

- クラス全体が「雑多な静的ヘルパーの寄せ集め」であり、単一責任の原則から外れた大きなクラスになっている。将来的に文字列系・パス系・TSV 系などへの分割余地がある。
- `test_yaml()`/`test_tsv()` はインスタンスメソッドとして定義されているが `self` を使わず、他の全メソッドが `classmethod` である点と一貫していない。用途も Udemy 進捗データ比較専用のアドホック処理であり、汎用ユーティリティとしては異質。
- ファイル冒頭に将来構想（サブモジュールからのクラス自動エクスポート）のコメントアウトされたコードブロックが残っており、未整理の技術的負債となっている。
