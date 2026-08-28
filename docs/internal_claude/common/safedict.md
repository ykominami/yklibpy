# SafeDict — 内部仕様書

## モジュール

`yklibpy.common.safedict`

## 実装詳細

`dict[str, str]` を継承し、`__missing__` フックのみをオーバーライドする。

```python
def __missing__(self, key: str) -> str:
    return f"{{{key}}}"
```

- `__getitem__` でキーが存在しない場合、Python は自動的に `__missing__` を呼ぶ
- 戻り値 `"{key}"` は `str.format_map(SafeDict(...))` での利用を主目的とする
- `get()` メソッドは `__missing__` を経由しないため、未定義キーには `None`（または指定したデフォルト）を返す

## 依存関係

- なし（組み込み `dict` のみ）
