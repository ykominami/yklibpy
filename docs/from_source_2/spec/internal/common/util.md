# Util — 内部仕様書

**ファイル**: `src/yklibpy/common/util.py`  
**継承**: なし

## 概要

文字列正規化、URL 解析、パス操作、文字コード判定、DOM 探索、TSV 変換を集約する汎用ユーティリティです。

## クラス定数

| 定数名 | 値 | 説明 |
|--------|----|------|
| `WINDOWS_RESERVED_PATTERN` | `re.Pattern` | Windows のディレクトリ名に使えない文字を検出します。 |

## メソッド

### `get_location() -> str` (classmethod)

このモジュールのファイル位置を返します。

### `get_location_string() -> str` (classmethod)

呼び出し元のファイル名、行番号、関数名を返し、フレームを得られない場合は `unknown` を返します。

### `find_paths(base_dir: Path, pattern: str, target_type: TargetType = "both") -> list[Path]` (classmethod)

`rglob` で再帰探索し、種別条件に一致したパスを返します。

処理フロー:

1. 起点がディレクトリか検証します。
2. パターンに一致するパスを再帰列挙します。
3. `file`、`dir`、`both` の指定に応じて結果へ追加します。

**Raises**: `ValueError` — 起点がディレクトリでない場合。

### `xyz() -> None` (classmethod)

固定文字列 `xyz` を情報ログへ出力します。

### `list_files(name: str, parts: Sequence[str], suffix: str) -> list[str]` (classmethod)

各区分を `name-part-suffix` 形式のファイル名候補へ変換します。

### `is_valid_urls(urls: List[str]) -> List[Util.Result]` (classmethod)

URL ごとに空入力、スキーム、構成要素を順に検査し、理由付き `Result` を返します。

### `extract_cid(text: str) -> str` (classmethod)

`cid` パラメーターを抽出し、見つからなければ空文字を返します。

### `extract_product_id(text: str) -> str` (classmethod)

`product_id` パラメーターを抽出し、見つからなければ空文字を返します。

### `extract_base(base: str, text: str) -> str | None` (classmethod)

指定名のパラメーター値を正規表現で抽出します。

### `flatten_gen(lst: list[Any]) -> Iterator[Any]` (classmethod)

入れ子のリストだけを再帰展開するジェネレーターです。

### `ensure_file_path(path: Path | None) -> Path | None` (classmethod)

親ディレクトリを必要に応じて作成し、ファイルを `touch` して返します。

### `ensure_dir_path(path: Path | None) -> Path | None` (classmethod)

ディレクトリを親階層込みで作成して返します。

### `flatten(items: Iterable[Any]) -> list[Any]` (classmethod)

入れ子のリストだけを再帰展開して一つのリストへまとめます。

### `detect_encoding(input_path: Path) -> str | None` (classmethod)

ファイルをバイト列で読み、`chardet` の推定文字コードを返します。

### `get_default_encoding() -> str` (classmethod)

実行環境の優先文字コードを返します。

### `decode_cli_output(data: bytes | None) -> str` (classmethod)

UTF-8、CP932、環境既定の順でデコードし、全て失敗した場合は置換付き UTF-8 で返します。

### `get_common_parents(element1: Tag, element2: Tag) -> List[Tag]` (classmethod)

2要素の親タグをルート側から照合し、共通するタグを順序付きで返します。

処理フロー:

1. 各要素から親 `Tag` をルート方向へ収集します。
2. 両配列を反転し、ルート側を先頭にします。
3. 第2要素の親をオブジェクト ID の集合へ変換します。
4. 第1要素側を走査して共通親を返します。

### `load_tsv(input_path: Path, fieldnames: Sequence[str] | None = None) -> list[dict[str, str]]` (classmethod)

TSV を辞書配列へ変換します。列名未指定時は先頭行をヘッダーにします。

**Raises**: `ValueError` — 空ファイルで列名も指定されない場合。

### `output_tsv(records: Sequence[dict[str, str]], output_path: Path | None = None, fieldnames: Sequence[str] | None = None) -> str` (classmethod)

指定列順で辞書配列を TSV 化し、必要なら UTF-8 ファイルへ保存します。

**Raises**: `ValueError` — レコードが空で列名も指定されない場合。

### `test_yaml(input_file: str, input_file_2: str, output_file: str) -> None`

2件の Udemy 用 YAML を TSV 化し、コースごとの `Time` を旧データから新データへ引き継ぎます。

### `test_tsv(input_file: str, input_file_2: str, output_file: str) -> None`

2件の Udemy 用 TSV を `Course_ID` で照合し、`Time` を引き継いで保存します。

### `remove_crlf(string: str) -> str` (classmethod)

CR と LF を除去します。

### `remove_whitespace(string: str) -> str` (classmethod)

全ての空白類を除去します。

### `remove_non_printable(string: str) -> str` (classmethod)

表示可能な文字だけを残します。

### `get_valid_string(string: str | None) -> str` (classmethod)

`None` と空入力を空文字へ、その他を空白除去済み文字列へ正規化します。

### `is_empty(string: str | None) -> bool` (classmethod)

正規化後の文字列が空か判定します。

### `normalize_string(string: str | None) -> str | None` (classmethod)

実質的に空なら `None`、それ以外は空白除去済み文字列を返します。

### `array_to_dict(data: list[dict[str, Any]], key: str) -> dict[str, dict[str, Any]]` (classmethod)

辞書配列を指定項目の文字列表現で引ける辞書へ変換します。

**Raises**: `TypeError` — 要素が辞書でない場合。  
**Raises**: `KeyError` — 指定項目がない場合。  
**Raises**: `ValueError` — キー値が文字列化を許可されたスカラー型でない場合。

### `swap_dict(dict: dict[str, str]) -> dict[str, str]` (classmethod)

辞書のキーと値を入れ替えます。

### `sanitize_dir_name(name: str) -> str` (classmethod)

Windows 禁止文字を `_` に置換し、末尾のピリオドを除去します。結果が空なら `_none` を返します。

## 依存

| クラス/変数 | 用途 |
|-------------|------|
| [`util_module.md`](util_module.md) | `TargetType` と型変数を定義します。 |
| [`result.md`](result.md), [`unique_list.md`](unique_list.md) | URL 結果と順序付き一意集合を提供する入れ子クラスです。 |
| `Loggerx` | 探索、TSV、YAML 処理のログを記録します。 |
| `UtilYaml` | YAML 比較・保存を委譲します。 |

## 設計上の注意

責務が文字列、DOM、ファイル、TSV、YAML に広がっています。`test_yaml` と `test_tsv` は名称に反して本番コード内でファイルを書き換える処理です。`output_tsv` は `fieldnames` 未指定かつレコードありの場合も空ヘッダーで出力するため、呼び出し側で列名指定が必要です。
