# SafeDict — 外部仕様書

## 概要

`yklibpy.common.safedict.SafeDict`

`dict[str, str]` を継承し、存在しないキーへのアクセスが `KeyError` を送出する代わりに
`"{key}"` 形式のプレースホルダ文字列を返す辞書。
`str.format_map(SafeDict(...))` パターンでテンプレート文字列を安全に展開する用途を想定する。

## 継承

```
dict[str, str]
  └── SafeDict
```

## パブリック API

### `__missing__(key: str) -> str`

存在しないキーを `{key}` 形式の文字列として返す。
`dict.__missing__` のオーバーライドであり、直接呼び出すことは想定しない。

## 使用例

```python
d = SafeDict({"name": "Alice"})
result = "Hello, {name}! You are {age} years old.".format_map(d)
# → "Hello, Alice! You are {age} years old."
```

`{age}` のような未定義キーはそのまま残る。

## 依存関係

なし
