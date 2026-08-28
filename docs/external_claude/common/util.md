# Util — 外部仕様書

## 概要

`yklibpy.common.util.Util`

文字列処理・パス操作・表形式変換を提供する汎用ユーティリティクラス。
ほぼすべてのメソッドがクラスメソッドとして実装されており、インスタンス化なしに利用できる。

---

## 内部クラス

### `Util.UniqueList[T]`

重複を除きつつ追加順を保つ簡易コレクション。
`set` と `list` を組み合わせて O(1) 判定と挿入順保持を両立する。

| メソッド | 説明 |
|----------|------|
| `append(value: T) -> None` | 未登録の値だけを末尾へ追加する |
| `__iter__() -> Iterator[T]` | 保持順のまま反復するイテレータを返す |

### `Util.Result`

URL 検証の成否と補足情報を保持するデータ容器。`is_valid_urls` の戻り値要素として使用する。

| フィールド | 型 | 説明 |
|------------|----|------|
| `success` | `bool` | 検証が成功したか |
| `url` | `str` | 検証対象の URL 文字列 |
| `reason` | `str` | 成否の理由説明 |
| `parsed` | `ParseResult \| None` | `urlparse` による解析結果 |

---

## クラス定数

| 定数名 | 値 | 説明 |
|--------|----|------|
| `WINDOWS_RESERVED_PATTERN` | `re.compile(r'[<>:"/\\|?*\x00-\x1f]')` | Windows で使用できない文字のパターン |

---

## パブリック API

### パス操作

#### `find_paths(base_dir, pattern, target_type="both") -> list[Path]`

`base_dir` を起点に `rglob` で再帰探索し、条件に合うパスの一覧を返す。

- `target_type`: `"file"` でファイルのみ、`"dir"` でディレクトリのみ、`"both"` で両方。

**Raises**: `ValueError` — `base_dir` がディレクトリでない場合。

#### `ensure_file_path(path: Path | None) -> Path | None`

ファイルと親ディレクトリの存在を保証して `path` を返す。
`path` が存在しない場合は親ディレクトリを `mkdir(parents=True)` で作成し、`touch()` でファイルを作成する。
`path` が `None` の場合はそのまま `None` を返す。

#### `ensure_dir_path(path: Path | None) -> Path | None`

ディレクトリの存在を保証して `path` を返す。`path` が `None` の場合は何もしない。

#### `list_files(name, parts, suffix) -> list[str]`

名前・区分リスト・拡張子から `"{name}-{part}{suffix}"` 形式のファイル名候補を生成する。

### 文字列処理

#### `remove_crlf(string: str) -> str`

文字列から `\n` と `\r` を取り除く。

#### `remove_whitespace(string: str) -> str`

文字列から空白類（スペース・タブ・改行）をすべて取り除く。

#### `remove_non_printable(string: str) -> str`

文字列から `str.isprintable()` が `False` の文字を取り除く。

#### `get_valid_string(string: str | None) -> str`

`None` や空白だけの入力を空文字へ正規化する。空白類の除去に `remove_whitespace` を使う。

#### `is_empty(string: str | None) -> bool`

入力が実質的に空文字かどうかを判定する。

#### `normalize_string(string: str | None) -> str | None`

有効な文字列だけを返し、空の場合は `None` を返す。

#### `sanitize_dir_name(name: str) -> str`

Windows 禁止文字（`WINDOWS_RESERVED_PATTERN`）を `_` に置換し、末尾の `.` を除去する。
正規化後が空文字になる場合は `"_none"` を返す。

### URL 処理

#### `is_valid_urls(urls: List[str]) -> List[Util.Result]`

URL 一覧を検証し、各要素の結果を `Result` の配列として返す。
無効な URL も例外にはせず、`success=False` と理由付きの `Result` として返す。

#### `extract_cid(text: str) -> str`

文字列から `cid=` クエリパラメータ値を抽出する。見つからない場合は空文字を返す。

#### `extract_product_id(text: str) -> str`

文字列から `product_id=` クエリパラメータ値を抽出する。

#### `extract_base(base: str, text: str) -> str | None`

指定名のクエリパラメータ値を抽出する。見つからない場合は `None` を返す。

### コレクション変換

#### `flatten_gen(lst: list[Any]) -> Iterator[Any]`

入れ子リストを再帰的に平坦化するジェネレータを返す。

#### `flatten(items: Iterable[Any]) -> list[Any]`

入れ子の配列を 1 次元のリストに変換する。

#### `array_to_dict(data: list[dict[str, Any]], key: str) -> dict[str, dict[str, Any]]`

辞書配列を指定キーで参照できる連想配列へ変換する。

**Raises**:
- `TypeError` — 配列の要素が辞書でない場合。
- `KeyError` — いずれかの要素に `key` が存在しない場合。
- `ValueError` — `key` の値が文字列・数値・真偽値でない場合。

#### `swap_dict(dict: dict[str, str]) -> dict[str, str]`

キーと値を入れ替えた辞書を返す。空辞書が渡された場合は空辞書を返す。

### エンコーディング

#### `detect_encoding(input_path: Path) -> Optional[str]`

`chardet` を使ってファイルの文字エンコーディングを推定する。`input_path` が `None` の場合は `None` を返す。

#### `get_default_encoding() -> str`

`locale.getpreferredencoding(False)` で実行環境の既定エンコーディングを返す。

### BeautifulSoup 補助

#### `get_common_parents(element1: Tag, element2: Tag) -> List[Tag]`

2 つの BeautifulSoup 要素に共通する親タグの一覧をルート側から返す。

### TSV 操作

#### `load_tsv(input_path, fieldnames=None) -> list[dict[str, str]]`

TSV ファイルを読み込み、行ごとの辞書配列へ変換する。
`fieldnames` が省略された場合は先頭行をヘッダーとして扱う。

**Raises**: `ValueError` — ヘッダーが存在せず `fieldnames` も指定されない場合。

#### `output_tsv(records, output_path=None, fieldnames=None) -> str`

辞書配列を TSV 文字列へ変換する。`output_path` が指定されるとファイルへも保存する。

**Raises**: `ValueError` — `records` が空で `fieldnames` も指定されない場合。

### クラス位置情報

#### `get_location() -> str`

このモジュールファイルのパスを文字列で返す。

#### `get_location_string() -> str`

呼び出し元のファイル名・行番号・関数名を文字列で返す。

---

## 依存関係

- `chardet`
- `bs4`（`get_common_parents` のみ）
- `yklibpy.common.loggerx.Loggerx`
- `yklibpy.common.util_yaml.UtilYaml`（`test_yaml` のみ）
