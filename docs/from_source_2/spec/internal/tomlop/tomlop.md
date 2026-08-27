# Tomlop — 内部仕様書

**ファイル**: `src/yklibpy/tomlop/tomlop.py`  
**継承**: なし

## 概要

TOML と YAML の読み書き、辞書の再帰比較・不足値補完・差分整形を担い、CLI から変換処理を起動する。

---

## モジュールレベル関数

### `zmain() -> None`

`Tomlop` を生成して `main()` を起動する。

### `toml2yaml() -> None`

`Tomlop` を生成して同名の変換メソッドを起動する。

### `yaml2toml() -> None`

`Tomlop` を生成して同名の変換メソッドを起動する。

---

## クラス定数

| 定数名 | 値 | 説明 |
|--------|----|------|
| `_count` | `0` | `FileItem.setup()` をプロセス中1回だけ呼ぶための共有カウンタ。 |

## インスタンス変数

| 変数名 | 型 | 説明 |
|--------|----|------|
| `data` | `Any` | 読み込み・変換中のデータ。 |
| `ref_file_item` | `FileItem` | `setup()` 後の参照元。 |
| `config_file_item` | `FileItem \| None` | `setup()` 後の比較先。 |

---

## メソッド

### `__init__() -> None`

初回インスタンス時だけファイル種別定義を設定し、作業データを空にする。

### `setup(ref_file, config_file) -> None`

参照元を `FileItem` にし、比較先が指定されていれば同様に構築する。

### `compare_dict(dict1, dict2) -> bool`

キー集合を比較後、対応値を走査し、双方が辞書なら再帰して完全一致を判定する。

### `merge_dict(dict1, dict2) -> dict[str, Any]`

`dict1` にないキーを `dict2` から追加し、双方が辞書の既存キーだけ再帰的に補完する。`dict1` 自体を変更して返す。

### `diff_dict(dict1, dict2) -> str`

和集合のキーをソートし、片側だけのキーまたは異なる値を日本語見出し付き文字列へ整形する。

1. 全キーの和集合を作ってソートする。
2. 片側だけのキーは所属と値を記録し、双方が辞書なら再帰的な差分有無を判定する。
3. 差異がある値を比較元・比較先に分けて連結し、差分がなければ空文字を返す。

### `_format_value(value: Any) -> str`

辞書は入れ子を `{...}` で省略した1行形式へ、それ以外は `str` へ変換する。

### `read_toml_external(file_path) -> dict[str, Any] | None`

UTF-8 TOML を読み、`data` に保持して返す。解析失敗またはファイル不在時はログを出して `None` を返す。

### `write_toml_external(file_path, data) -> bool`

UTF-8 で TOML を書き、成功可否を真偽値で返す。失敗時は例外内容をログへ記録する。

### `load_toml(ref_file) -> dict[str, Any] | None`

参照先が指定された場合だけ `read_toml_external` を呼び、読み込み結果を返す。

### `exec() -> None`

参照元と設定を読み、不足値を補完して比較・差分をログへ出し、2つの TOML ファイルへ結果を書き出す。

1. 参照元を読み、比較先未設定なら `ValueError` を送出する。
2. 比較先へ参照元の不足キーをマージし、完全一致と差分文字列を求める。
3. `new_pyproject.toml` と `diff_pyproject.toml` に補完結果と差分を出力する。

### `main() -> None`

CLI 引数から参照元と比較先を決め、参照元がある場合は初期化後に YAML 拡張子の出力パスへ現在の `data` を出力する。

### `toml2yaml() -> None`

第1引数の TOML を読み、結果を固定パス `a.yaml` へ保存する。

### `yaml2toml() -> None`

第1引数の YAML を読み、`.toml` の出力候補パスをログへ出す。実際の TOML 出力は行わない。

---

## 依存

| クラス/変数 | 用途 |
|-------------|------|
| `FileItem` | 入出力対象の抽象化。 |
| `AppConfig` | YAML の拡張子解決。 |
| `toml` | TOML の読み書き。 |
| `UtilYaml` | YAML の読み書き。 |
| `Loggerx` | 比較・変換状況とエラーの記録。 |

## 設計上の注意

`exec()` は `merge_dict` により読み込んだ設定辞書を破壊的に変更する。差分出力文字列を TOML 用 `FileItem` に渡すため、`toml.dump` が期待する辞書型と整合しない可能性がある。`main()` は `read_toml_external` や `exec()` を呼ばず、空の `data` を出力する。`yaml2toml()` は出力未実装である。`read_toml_external()` の詳細ログは `project.authors` の存在を前提としており、一般 TOML では `KeyError` が伝播する。
