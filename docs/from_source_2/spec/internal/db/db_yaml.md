# DbYaml — 内部仕様書

**ファイル**: `src/yklibpy/db/db_yaml.py`  
**継承**: `DbBase`

## 概要

YAML ファイルとメモリ上の辞書を相互変換し、簡易的なキー操作を提供する DB 実装である。

---

## インスタンス変数

| 変数名 | 型 | 説明 |
|--------|----|------|
| `fname` | `str` | 指定された保存先名。 |
| `fname_path` | `Path` | 保存先パス。 |
| `data` | `dict[str, Any]` | 読み書き対象データ。 |
| `assoc` | `dict[str, object]` | 基底クラス由来の未使用状態。 |

---

## メソッド

### `__init__(fname: str) -> None`

基底状態、保存先、空データを初期化する。

### `load(encoding=None, tags=None) -> dict[str, Any]`

ファイルを準備し、必要なら文字コードを検出して YAML を安全に読み込む。

1. `Util.ensure_file_path` で保存先を利用可能にする。
2. 文字コード未指定時は検出し、失敗時はログを出して空辞書を返す。
3. 追加タグのコンストラクタを登録し、`yaml.safe_load` の辞書を保持して返す。

### `save() -> bool`

`UtilYaml.save_yaml` で保持データを保存し、`True` を返す。

### `get_data() -> dict[str, Any]` / `set_data(data) -> bool`

全データを取得または置換する。

### `get_item(key: str) -> Any` / `set_item(key, value) -> bool`

単一キーを取得または設定する。存在しないキーの取得は `KeyError` となる。

### `clear() -> bool` / `count() -> int`

データの全削除、またはキー数の取得を行う。

### `list_text(key: str) -> list[Any]`

各値を辞書として扱い、指定キーの値を一覧化する。レコードまたはキーの形が不正なら例外が伝播する。

---

## 依存

| クラス/変数 | 用途 |
|-------------|------|
| `DbBase` | 基底状態。 |
| `yaml.safe_load` | 安全な YAML 復元。 |
| `Util` | パス準備と文字コード検出。 |
| `UtilYaml` | タグ登録と保存。 |
| `Loggerx` | 検出失敗の記録。 |

## 設計上の注意

文字コード検出以外の読み込み例外は捕捉しない。直接実行時の引数条件は `len(sys.argv) > 1` でエラーにしており、メッセージの「未指定」と条件が逆転している。
