# CommandGhUser — 外部仕様書

## 概要

`yklibpy.command.command_gh_user.CommandGhUser`

GitHub CLI (`gh`) からログイン中のユーザー名を取得する `Command` のサブクラス。

## 継承

```
Command
  └── CommandGhUser
```

## クラス定数

| 定数名 | 値 | 説明 |
|--------|----|------|
| `DEFAULT_VALUE_USER` | `None` | ユーザー名が取得できない場合のデフォルト値 |

## コンストラクタ

```python
CommandGhUser()
```

`Command.__init__` を呼ばない空初期化。状態を持たない。

## パブリック API

### `run() -> str`

`gh api user --jq ".login"` を実行し、ログイン中のユーザー名を返す。
出力が空または空白のみの場合は空文字 `""` を返す。

**前提**: `gh` CLI がインストール済みで認証済みであること。

**Raises**: `subprocess.CalledProcessError` — コマンドが非ゼロで終了した場合（`gh` が未認証など）。

## 依存関係

- `yklibpy.command.command.Command`
- `yklibpy.common.util.Util`
