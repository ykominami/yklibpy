# Tomlop — 内部仕様書

## モジュール

`yklibpy.tomlop.tomlop`

## クラス変数

| 変数名 | 型 | 初期値 | 役割 |
|--------|----|--------|------|
| `_count` | `int` | `0` | `FileItem.setup()` を一度だけ呼ぶためのガード |

## インスタンス変数

| 変数名 | 型 | 役割 |
|--------|----|------|
| `data` | `Any` | 読み込んだデータの作業コピー |
| `ref_file_item` | `FileItem` | `setup` 実行後の参照ファイル |
| `config_file_item` | `FileItem \| None` | `setup` 実行後の設定ファイル（不要な場合は `None`） |

## `__init__` の処理フロー

1. `Tomlop._count == 0` の場合のみ `FileItem.setup()` を呼んで `Storex` のファイル種別辞書を初期化
2. `_count` をインクリメント
3. `self.data = {}` で初期化

## `compare_dict` の実装詳細

- キーセットが不一致 → `False` を返す
- 両方が `dict` → 再帰呼び出し
- それ以外 → `value1 != value2` で判定

## `merge_dict` の実装詳細

- `dict2` のキーを走査し、`dict1` に存在しないキーを追加する
- 両方が `dict` の場合のみ再帰（`dict1` の既存値は変更しない）

## `diff_dict` の実装詳細

- `set(dict1.keys()) | set(dict2.keys())` を `sorted` で走査
- 片方のみ存在 → `"# 比較元のキーのみ存在"` / `"# 比較先のキーのみ存在"` ラベルを付ける
- 両方に存在かつ差異あり → `"# 値が異なる"` ラベルを付ける
- 戻り値が空文字なら差分なし

## `_format_value` の実装詳細

- 辞書の場合は `{k: {...}}` または `{k: v}` 形式で短縮表示
- それ以外は `str(value)`

## `exec` の処理フロー

1. `ref_file_item.storex.load()` と `config_file_item.storex.load()` でデータを読み込む
2. `merge_dict(config, ref)` で補完
3. `compare_dict(new_config, ref)` と `diff_dict(new_config, ref)` で比較
4. `new_pyproject.toml` と `diff_pyproject.toml` を `FileItem` 経由で出力

## `main` / `toml2yaml` / `yaml2toml` の処理

- `sys.argv` から引数を取得する CLI エントリポイント相当のメソッド
- `main`: 参照ファイルの拡張子を YAML に変換して出力
- `toml2yaml`: TOML → YAML 変換
- `yaml2toml`: YAML → TOML の出力先パスを決定（書き込み未実装）

## モジュールレベル関数

| 関数名 | 役割 |
|--------|------|
| `zmain()` | `Tomlop.main()` のエントリポイント |
| `toml2yaml()` | `Tomlop.toml2yaml()` のエントリポイント |
| `yaml2toml()` | `Tomlop.yaml2toml()` のエントリポイント |

## 依存関係

- `sys`, `pathlib.Path`, `typing`（標準ライブラリ）
- `toml`
- `yklibpy.common.loggerx.Loggerx`
- `yklibpy.common.util_yaml.UtilYaml`
- `yklibpy.config.appconfig.AppConfig`
- `yklibpy.tomlop.fileitem.FileItem`
