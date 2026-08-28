# DbYaml — 内部仕様書

**ファイル**: `src/yklibpy/db/db_yaml.py`
**継承**: `DbBase`

## 概要

YAML ファイルを背後ストアとして扱う簡易 DB 実装。辞書形式のデータをメモリ上に保持し、必要に応じて YAML ファイルと相互変換する。`get_or_create_db("yaml", fname)` 経由で生成されることを想定している。

---

## インスタンス変数

| 変数名 | 型 | 説明 |
|--------|----|------|
| `fname` | `str` | 保存先ファイル名（文字列）。 |
| `fname_path` | `Path` | `fname` から作った `Path`。 |
| `data` | `dict[str, Any]` | 保持している内部データ。 |

---

## メソッド

### `__init__(fname: str) -> None`

保存先ファイルと内部データを初期化する（`DbBase.__init__()` を呼び出したうえで `fname`/`fname_path`/`data` を設定）。

### `load(encoding: str | None = None, tags: list[str] | None = None) -> dict[str, Any]`

YAML ファイルを読み込み、内部データとして保持する。

```
処理フロー:
  1. Util.ensure_file_path でファイルの存在を保証する
  2. encoding 未指定なら Util.detect_encoding で推定（失敗時はログ出力して空辞書を返す）
  3. 推定も None ならシステム既定エンコーディングを使う
  4. UtilYaml._register_constructors でカスタムタグを無害化登録したうえで yaml.safe_load
  5. 結果が None なら空辞書として self.data に保持
```

**Args**: `tags` — 追加で無害化登録したい YAML タグの一覧。

**Returns**: 読み込んだ内部データ。失敗時は空辞書。

### `save() -> bool`

保持中の内部データを YAML ファイルへ保存する（`UtilYaml.save_yaml` に委譲）。常に `True` を返す。

### `get_data() -> dict[str, Any]`

現在保持している全データを返す。

### `set_data(data: dict[str, Any]) -> bool`

内部データを丸ごと置き換える。常に `True` を返す。

### `get_item(key: str) -> Any`

指定キーの値を返す。

**Raises**: `KeyError` — `key` が内部データに存在しない場合。

### `set_item(key: str, value: Any) -> bool`

指定キーへ値を設定する。常に `True` を返す。

### `clear() -> bool`

保持しているデータを空にする。常に `True` を返す。

### `count() -> int`

保持しているキー数を返す。

### `list_text(key: str) -> list[Any]`

各レコード（`data.values()`）から指定キーの値だけを抽出して返す。

**Raises**: `KeyError` — いずれかのレコードに `key` が存在しない場合。

---

## 依存

| クラス/変数 | 用途 |
|-------------|------|
| `DbBase` | 基底クラス |
| `Util` | ファイル存在保証・エンコーディング検出 |
| `UtilYaml` | YAML の読み書き、カスタムタグ登録 |
| `Loggerx` | エラーログ出力 |

---

## 設計上の注意

- `save()`/`set_data()`/`set_item()`/`clear()` はすべて常に `True` を返す設計であり、失敗を表現できない（`bool` 戻り値が実質的に意味を持たない）。
- モジュール末尾の `if __name__ == "__main__":` ブロックは `len(sys.argv) > 1` のときにエラーを出す実装になっており、通常の CLI 引数の慣習（`> 1` は引数ありを意味する）と条件が逆転しているように見える点に注意。
