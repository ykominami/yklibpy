# CommandGhUser — 内部仕様書

**ファイル**: `src/yklibpy/command/command_gh_user.py`  
**継承**: `Command`

## 概要

基底クラスの外部コマンド実行機能を使い、GitHub CLI の認証ユーザー名を取得する。

---

## メソッド

### `__init__() -> None`

親クラスと同様に状態を持たない空初期化を行う。

### `run() -> str`

`gh api user --jq ".login"` を実行し、出力を正規化したユーザー名を返す。正規化結果が空なら空文字を返す。

---

## 依存

| クラス/変数 | 用途 |
|-------------|------|
| `Command` | コマンド実行機能を継承する。 |
| `Util.normalize_string` | CLI 出力の空白等を正規化する。 |

## 設計上の注意

文字列コマンドを `shell=False` の既定値で渡しているため、POSIX 環境では引数分割されず実行に失敗する可能性がある。
