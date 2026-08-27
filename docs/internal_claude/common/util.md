# Util — 内部仕様書

## モジュール

`yklibpy.common.util`

## 内部クラス

### `UniqueList[T]`

- `_set: set[T]` と `_list: list[T]` の 2 つで重複排除と挿入順保持を同時に実現する
- `append` は `_set` で存在チェック後、未登録なら両方へ追加する

### `Result`

- `success`, `url`, `reason`, `parsed` の 4 属性を持つ単純なデータ容器
- `is_valid_urls` の戻り値要素として使われる

## クラス定数

- `WINDOWS_RESERVED_PATTERN`: `[<>:"/\\|?*\x00-\x1f]` を含む禁止文字の正規表現（`sanitize_dir_name` で使用）

## 主要メソッドの実装詳細

### `find_paths`

- `base_dir.rglob(pattern)` でファイルシステムを再帰検索
- `target_type` に応じて `is_file()` / `is_dir()` でフィルタリング
- `base_dir` がディレクトリでない場合 `ValueError` を送出

### `ensure_file_path`

- `path is None` なら即 `None` を返す
- ファイルが存在しない場合、親ディレクトリを `mkdir(parents=True, exist_ok=True)` で生成してから `path.touch()` でファイルを作成する

### `get_common_parents`

- 内部関数 `get_all_parents` でルート方向への親チェーンを取得
- `id(p)` ベースの集合で O(1) 検索しながら、逆順にした parents1 の順序を維持して共通親を抽出

### `load_tsv` / `output_tsv`

- `csv.reader` / `csv.writer` に `delimiter="\t"` を渡す
- `output_tsv` は `StringIO` で一旦バッファに書いてから文字列として取得し、`output_path` が指定された場合のみファイル書き込みを行う

### `array_to_dict`

- `data` の各要素から `key` で値を取り出し `str` 化して辞書キーにする
- 型不正・キー欠如・変換不能値の場合はそれぞれ `TypeError` / `KeyError` / `ValueError` を送出

### `is_valid_urls`

- スキームなし → `Result(False, ..., "URL scheme is invalid", parsed)`
- netloc・path・fragment がすべて空 → `Result(False, ..., "URL is not a valid URI", parsed)`
- それ以外 → `Result(True, ...)`

### `sanitize_dir_name`

- `WINDOWS_RESERVED_PATTERN.sub("_", name).strip().rstrip(".")`
- 変換後が空文字になると `"_none"` を返す

## インスタンスメソッド（非クラスメソッド）

- `test_yaml` / `test_tsv`: Udemy 用のデータマージ処理。内部で `UtilYaml` / `Util.load_tsv` を呼ぶ開発時の実験コードで、プロダクションパスからは呼ばれない

## 依存関係

- `csv`, `inspect`, `locale`, `re`, `io.StringIO`, `pathlib.Path`, `urllib.parse`（標準ライブラリ）
- `chardet`（エンコーディング検出）
- `bs4.Tag`
- `yklibpy.common.loggerx.Loggerx`
- `yklibpy.common.util_yaml.UtilYaml`
