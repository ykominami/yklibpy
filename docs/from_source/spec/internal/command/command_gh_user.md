# CommandGhUser — 内部仕様書

**ファイル**: `src/yklibpy/command/command_gh_user.py`
**継承**: `Command`

## 概要

GitHub CLI（`gh`）を利用して、現在ログイン中のユーザー名を取得するコマンドクラス。

---

## メソッド

### `__init__() -> None`

基底クラス互換の空初期化を行う（`Command.__init__()` は呼ばず `pass` のみ）。

### `run() -> str`

`gh api user --jq ".login"` を実行してユーザー名を返す。`Command.run_command_simple` の出力を `Util.normalize_string` で正規化し、`None` の場合は空文字を返す。

---

## 依存

| クラス/変数 | 用途 |
|-------------|------|
| `Command` | `Command.run_command_simple` の提供元（基底クラス） |
| `Util` | 出力文字列の正規化 |

---

## 設計上の注意

`__init__()` が `super().__init__()` を呼んでいないため、基底クラス `Command` で将来インスタンス変数が追加された場合に初期化漏れが発生するリスクがある（現状の `Command.__init__` は `pass` のみなので実害は無い）。
