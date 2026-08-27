# 外部仕様書 — `Tomlop`

**対象**: TOML/YAML 変換・比較  
**コマンド**: `yklibpy-tomlop-z` / `yklibpy-toml2yaml` / `yklibpy-yaml2toml`

## 未確定事項

正となる2 定義文書は欠落し、代替候補も空です。出力名と形式は現行実装であり正式仕様は未確定です。異なる意図であればお知らせください。

## 1. コマンドライン構文

```text
yklibpy-tomlop-z [参照TOML] [比較TOML=pyproject.toml]
yklibpy-toml2yaml [入力TOML]
yklibpy-yaml2toml [入力YAML]
```

オプションパーサはありません。引数なしはいずれも何もせず正常終了します。

## 2. コマンド仕様

- `tomlop-z`: 参照ファイル指定時、同名 `.yaml` へ現在の空データ `{}` を出力します。比較処理は呼ばれません。
- `toml2yaml`: 入力TOMLを読み、固定名 `a.yaml` へ保存します。
- `yaml2toml`: 入力YAMLを読み、`.toml` 候補をログへ出しますがファイルは出力しません。

比較APIは再帰一致、不足キーの破壊的補完、差分文字列生成を提供します。`exec()` は `new_pyproject.toml` と `diff_pyproject.toml` を出力しようとします。

## 3. 既知の不整合

- `tomlop-z` は入力を読まず空データを出力します。
- `yaml2toml` は変換結果を書きません。
- `exec()` は差分文字列をTOMLライターへ渡すため失敗し得ます。
- TOML読み込み後のログ処理は `project.authors` を前提とし、一般TOMLでは `KeyError` が伝播します。

## 4. エラー処理・終了コード

| 事象 | 挙動 | 終了コード |
|---|---|---:|
| 引数なし | 何もしない | `0` |
| TOML不在・解析失敗 | ログ後 `None` | 通常 `0`、後続の未捕捉例外なら `1` |
| YAML不在・解析失敗 | 例外が伝播 | `1` |
| `exec()` 比較先なし | `ValueError("config_file_item is not set")` | `1` |
| `write_toml_external` 書き込み失敗 | ログして `False` | API自体は異常終了しない |

## 5. 実装上の対応（参考）

本節は実装を拘束しません。`src/yklibpy/tomlop/tomlop.py` が担当します。
