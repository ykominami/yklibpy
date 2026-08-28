# Tomlop — 内部仕様書

**ファイル**: `src/yklibpy/tomlop/tomlop.py`
**継承**: なし

## 概要

TOML と YAML の比較・変換・差分出力を扱うクラス。`pyproject.toml` などの設定ファイルを参照ファイルと比較し、不足キーの補完（マージ）と差分レポートの生成を CLI から実行する用途を想定する。

---

## クラス変数

| 変数名 | 型 | 説明 |
|--------|----|------|
| `_count` | `int` | `FileItem.setup()` を一度だけ実行するためのガード用クラス変数（既定値は `0`）。 |

---

## インスタンス変数

| 変数名 | 型 | 説明 |
|--------|----|------|
| `data` | `Any` | 直近に読み込み/生成したデータ。 |
| `ref_file_item` | `FileItem` | `setup()` 呼び出し後に設定される、参照ファイルの `FileItem`。 |
| `config_file_item` | `FileItem \| None` | `setup()` 呼び出し後に設定される、比較先設定ファイルの `FileItem`。 |

---

## メソッド

### `__init__() -> None`

共有初期化を一度だけ行い（`Tomlop._count == 0` のときのみ `FileItem.setup()` を実行し `_count` をインクリメント）、作業用データを空にする。

### `setup(ref_file, config_file) -> None`

参照ファイルと設定ファイルの `FileItem` を準備する。`config_file` が `None` の場合は `config_file_item` も `None` のままにする。

### `compare_dict(dict1: dict[str, Any], dict2: dict[str, Any]) -> bool`

2 つの辞書が再帰的に完全一致するかを判定する。キー集合が異なれば即 `False`。値が両方辞書なら再帰比較、それ以外は値の等価比較。

### `merge_dict(dict1: dict[str, Any], dict2: dict[str, Any]) -> dict[str, Any]`

不足キーだけを `dict2` から `dict1` へ補完する（`dict1` を破壊的に変更して返す）。既存キーは維持し、双方が辞書のときだけ再帰的に掘り下げる。

### `diff_dict(dict1: dict[str, Any], dict2: dict[str, Any]) -> str`

2 つの辞書の差分を可読な文字列として返す。

```
処理フロー:
  1. 両辞書の全キーを収集しソート
  2. dict1 のみに存在するキー/dict2 のみに存在するキーをそれぞれ見出し付きで記録
  3. 両方に存在し値が異なる場合、値が両方辞書なら再帰的に diff_dict、それ以外は値を整形して両方の値を記録
  4. 結果行を改行区切りで結合して返す（差分なしなら空文字）
```

### `_format_value(value: Any) -> str`

差分表示用に値を短い文字列へ整形する。辞書はネスト部分を `{...}` に省略しつつ `key: value` 形式で列挙する。

### `read_toml_external(file_path: str | Path) -> dict[str, Any] | None`

外部 TOML ファイルを読み込み、内容を `self.data` に保持して返す。読み込み・パース失敗時、および `FileNotFoundError` 発生時はいずれも内部で捕捉してログ出力のうえ `None` を返す（例外は呼び出し元に伝播しない）。

### `write_toml_external(file_path: str | Path, data: Any) -> bool`

辞書データを外部 TOML ファイルへ書き出す。成功なら `True`、例外発生時はログ出力のうえ `False`。

### `load_toml(ref_file: str | Path | None) -> dict[str, Any] | None`

参照用 TOML を読み込み、内容を返す。`ref_file` が未指定（`Falsy`）なら何も読まず `None` を返す。

### `exec() -> None`

参照ファイルとの差分を計算し、補完結果（`new_pyproject.toml`）と差分（`diff_pyproject.toml`）を出力する。

```
処理フロー:
  1. ref_file_item/config_file_item それぞれの storex.load() で辞書を取得
  2. merge_dict で config へ ref の不足キーを補完（new_config）
  3. compare_dict/diff_dict で ref との一致状況と差分文字列を求める（ログ出力のみ）
  4. new_config と diff_result をそれぞれ FileItem 経由で出力
```

**Raises**: `ValueError` — `setup()` 呼び出し時に `config_file=None` を渡した場合（`config_file_item` が `None` のまま）。`setup()` を一度も呼ばずに `exec()` を呼んだ場合は、`config_file_item` の検査より先に参照される `ref_file_item` 属性自体が存在せず `AttributeError` になる。

### `main() -> None`

CLI 引数（`sys.argv`）を解釈して主要処理を起動する。`sys.argv[1]` が指定されている場合のみ、それを参照ファイル、`sys.argv[2]`（省略時 `"pyproject.toml"`）を設定ファイルとして `setup()` を呼び、参照ファイルの拡張子から YAML 拡張子へ変換したパスへ `self.data` を出力する。`sys.argv[1]` が未指定の場合は何も実行しない。

### `toml2yaml() -> None`

`sys.argv[1]` で指定した TOML を読み込み、`a.yaml` へ変換して保存する。

### `yaml2toml() -> None`

`sys.argv[1]` で指定した YAML を読み込む。変換後の出力先パス（`.toml` 拡張子）を求めるところまでで、実際の TOML 書き出し処理は行われていない（ログ出力のみ）。

---

## モジュールレベル関数

### `zmain() -> None`

`Tomlop().main()` を起動する単純なエントリポイント。

### `toml2yaml() -> None`

`Tomlop().toml2yaml()` を起動する単純なエントリポイント。モジュールレベル関数名とクラスメソッド名が同名（`Tomlop.toml2yaml`）だが別物であり、混同に注意。

### `yaml2toml() -> None`

`Tomlop().yaml2toml()` を起動する単純なエントリポイント。同様にクラスメソッドと同名。

---

## 依存

| クラス/変数 | 用途 |
|-------------|------|
| `FileItem` | ファイル入出力の抽象化 |
| `AppConfig` | ファイル種別・拡張子解決 |
| `UtilYaml` | YAML の読み書き（`toml2yaml`） |
| `Loggerx` | ログ出力 |
| `toml` | TOML の読み書き |

---

## 設計上の注意

- `Tomlop.yaml2toml()`（インスタンスメソッド）は変換先パスを求めるだけで実際に TOML へ書き出す処理が欠落しており、未完成の実装になっている。
- モジュールレベル関数 `toml2yaml`/`yaml2toml` とインスタンスメソッド `Tomlop.toml2yaml`/`Tomlop.yaml2toml` が同名で存在し、`__init__.py` でモジュールレベル関数のみが `__all__` にエクスポートされている。可読性・保守性の観点から命名の衝突を避けることが望ましい。
- `_count` によるワンタイム初期化ガードはクラス変数のため、プロセス内で `Tomlop` を複数回インスタンス化しても `FileItem.setup()` は最初の 1 回しか呼ばれない（テストで別々の `file_type_dict` を使いたい場合は影響を受ける）。
- `main()` 内の `self.exec()` 呼び出しはコメントアウトされており（`# self.exec()`）、CLI エントリポイント（`zmain` 等）経由では `exec()` は現状どこからも呼ばれない。差分計算・補完・出力という中核機能が事実上デッドコードになっている。
