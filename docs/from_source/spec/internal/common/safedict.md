# SafeDict — 内部仕様書

**ファイル**: `src/yklibpy/common/safedict.py`
**継承**: `dict[str, str]`

## 概要

未定義キーへアクセスした際に例外を送出せず、`{key}` 形式のプレースホルダ文字列を返す辞書。`str.format_map` と組み合わせたテンプレート文字列展開で、未定義変数をそのまま残したい場合に使う。

---

## メソッド

### `__missing__(key: str) -> str`

未定義キーを `{key}` 形式の文字列として返す。`dict.__getitem__` からキー欠落時に自動的に呼び出される。

---

## 依存

なし（標準の `dict` のみ）。

---

## 設計上の注意

`str.format_map(SafeDict(...))` の用途を想定しており、単体の `dict` としても通常通り使える。
