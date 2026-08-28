# UtilYaml — 外部仕様書

## 概要

`yklibpy.common.util_yaml.UtilYaml`

YAML の読み書きとカスタムタグ登録を補助するクラスメソッド集。
`pyyaml` の `SafeLoader` / `FullLoader` を直接使う代わりに本クラスを経由することで、
カスタムタグを安全に扱える環境を統一的に提供する。

## クラス変数

| 変数名 | 型 | 説明 |
|--------|----|------|
| `_constructors_registered` | `bool` | カスタムタグ登録が完了しているか。一度だけ登録するためのガード |

## パブリック API

### `ignore_python_object_tag(loader, node) -> Any`

未知の Python オブジェクトタグ（`!!python/object` など）を安全な Python 値へ変換するコンストラクタ。
`MappingNode` → 辞書、`SequenceNode` → リスト、それ以外 → スカラー値として返す。

### `safe_load(f: Any) -> Any`

`SafeLoader` を使って YAML を読み込む。カスタムタグ登録は行わない。

### `load_yaml(input_path: Path) -> dict[str, Any]`

YAML ファイルを `FullLoader` で読み込んで辞書として返す。
ファイルが空の場合や `None` が返った場合は空辞書 `{}` を返す。
エンコーディングは UTF-8 固定。

### `save_yaml(assoc: dict[Any, Any], output_path: Optional[Path] = None) -> str`

辞書を YAML 文字列へ変換する。`output_path` が指定された場合はファイルへも書き出す。

- `default_flow_style=False`（ブロックスタイル）
- `allow_unicode=True`
- `sort_keys=False`（元の順序を維持）

戻り値は YAML 文字列（ファイル保存の有無にかかわらず返す）。

### `_register_constructors(tags: list[str]) -> None`（内部メソッド）

指定タグを `SafeLoader` に登録する。`_constructors_registered` が `False` のときのみ実行する（一度きり）。
`tag:yaml.org,2002:python/object` は自動的に追加される。

## 制約

- `_register_constructors` は一度しか実行されない。プロセス内で異なるタグセットを使い分けることはできない。
- `load_yaml` は `FullLoader` を使用するため、Python オブジェクトタグがあると例外になる可能性がある。カスタムタグを含む YAML には `DbYaml.load` の方が適している。

## 依存関係

- `yaml` (`pyyaml`)
- `yklibpy.common.loggerx.Loggerx`
