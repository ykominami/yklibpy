# UtilYaml — 内部仕様書

**ファイル**: `src/yklibpy/common/util_yaml.py`
**継承**: なし

## 概要

YAML の読み書きと、未知の Python オブジェクトタグを安全に無害化するカスタムコンストラクタ登録をまとめた補助クラス。`DbYaml` などが YAML 内に残る `!!python/object:...` タグを安全に読み飛ばすために利用する。

---

## クラス変数

| 変数名 | 値 | 説明 |
|--------|----|------|
| `_constructors_registered` | `bool`（既定 `False`） | カスタムタグコンストラクタが登録済みかどうかを表すクラス変数フラグ。 |

---

## メソッド

### `ignore_python_object_tag(loader: Any, node: Any) -> Any` (classmethod)

未知の Python オブジェクトタグを安全な値へ変換する。ノード種別（Mapping/Sequence/Scalar）に応じて対応する `construct_*` を呼び分ける。

### `_register_constructors(tags: list[str]) -> None` (classmethod)

指定タグを `yaml.SafeLoader` で読めるように登録する。

```
処理フロー:
  1. 未登録（_constructors_registered が False）であれば、tags に "tag:yaml.org,2002:python/object" を追加し、
     各タグに ignore_python_object_tag を SafeLoader へ登録する（登録済みの場合は tags も変更されない）
  2. 登録済みフラグを True にする（登録の有無に関わらず毎回 True を再設定）
```

### `safe_load(f: Any) -> Any` (classmethod)

`yaml.SafeLoader` を使って YAML を読み込む。

### `load_yaml(input_path: Path) -> dict[str, Any]` (classmethod)

YAML ファイルを UTF-8 で読み込み、辞書として返す。`yaml.FullLoader` を使う。読み込み結果が `None`（空ファイル等）の場合は空辞書を返す。

### `save_yaml(assoc: dict[Any, Any], output_path: Optional[Path] = None) -> str` (classmethod)

辞書を YAML 文字列へ変換し、`output_path` が指定されていればファイルへも保存する（`allow_unicode=True`, `sort_keys=False`）。

**Returns**: 生成した YAML 文字列。

---

## 依存

| クラス/変数 | 用途 |
|-------------|------|
| `Loggerx` | デバッグログの出力 |
| `yaml` (PyYAML) | YAML の読み書き |

---

## 設計上の注意

- `load_yaml()` は `yaml.FullLoader` を使う一方、`safe_load()` は `yaml.SafeLoader` を使っており、読み込みメソッドによって安全性レベルが異なる。カスタムタグの無害化が必要な場面では `_register_constructors()` 後に `yaml.SafeLoader` 系の読み込みを使うことが前提になる。
- `_constructors_registered` はクラス変数のため、プロセス内で一度登録すると全インスタンス・全呼び出しに影響する（グローバルな副作用）。
