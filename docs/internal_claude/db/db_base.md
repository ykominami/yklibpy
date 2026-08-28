# DbBase — 内部仕様書

## モジュール

`yklibpy.db.db_base`

## インスタンス変数

| 変数名 | 型 | 初期値 |
|--------|----|--------|
| `assoc` | `dict[str, object]` | `{}` |

## 実装詳細

- `__init__` で `self.assoc = {}` を初期化するだけ
- サブクラスの `DbYaml` は `self.data` を独自に持ち、`assoc` はほぼ使わない（基底クラスの遺産として残っている）

## 依存関係

- なし
