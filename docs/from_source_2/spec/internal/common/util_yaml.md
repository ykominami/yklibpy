# UtilYaml — 内部仕様書

**ファイル**: `src/yklibpy/common/util_yaml.py`  
**継承**: なし

## 概要

YAML の読み書きと、Python オブジェクトタグを値へ変換するコンストラクター登録を提供します。

## クラス定数

| 定数名 | 値 | 説明 |
|--------|----|------|
| `_constructors_registered` | `False` | カスタムコンストラクターの登録済み状態です。 |

## メソッド

### `ignore_python_object_tag(loader: Any, node: Any) -> Any` (classmethod)

ノード種別に応じて mapping、sequence、scalar の標準値へ構築します。

### `_register_constructors(tags: list[str]) -> None` (classmethod)

未登録時のみ、指定タグと Python オブジェクトタグを `SafeLoader` に登録します。

処理フロー:

1. 未登録かを判定します。
2. 引数 `tags` に Python オブジェクトタグを追加します。
3. 各タグへ `ignore_python_object_tag` を登録します。
4. 登録済みフラグを真にします。

### `safe_load(f: Any) -> Any` (classmethod)

`yaml.SafeLoader` で入力を読み込みます。

### `load_yaml(input_path: Path) -> dict[str, Any]` (classmethod)

UTF-8 の YAML ファイルを `FullLoader` で読み込み、空なら空辞書を返します。

### `save_yaml(assoc: dict[Any, Any], output_path: Path | None = None) -> str` (classmethod)

辞書をキー順維持・Unicode 許可の YAML 文字列へ変換し、指定時は UTF-8 ファイルへ保存します。

## 依存

| クラス/変数 | 用途 |
|-------------|------|
| `yaml` | YAML の構築、読込、保存を担当します。 |
| `Loggerx` | コンストラクター登録と読込を記録します。 |

## 設計上の注意

`_register_constructors` は渡された `tags` リストを変更し、PyYAML のグローバルな `SafeLoader` 登録状態も変更します。`load_yaml` は名前に反して安全ローダーではなく `FullLoader` を使用します。
