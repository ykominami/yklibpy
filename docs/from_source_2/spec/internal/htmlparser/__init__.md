# htmlparser.__init__ — 内部仕様書

**ファイル**: `src/yklibpy/htmlparser/__init__.py`

## 概要

HTML パーサ機能の主要クラスをパッケージ直下へ公開し、簡易的な疎通確認用エントリポイントを提供する。

---

## モジュールレベル定数・型

| 変数名 | 値/型 | 用途 |
|--------|-------|------|
| `__all__` | `list[str]` | `App`、`Progress`、`Scraper`、`Preparex`、`HtmlOp` を公開 API として宣言する。 |

---

## モジュールレベル関数

### `xmain() -> None`

`Loggerx.debug` へパッケージの疎通確認メッセージを出力する。直接実行時のエントリポイントでもある。

### `ymain() -> None`

別系統の疎通確認メッセージを `Loggerx.debug` へ出力する。

---

## 依存

| クラス/変数 | 用途 |
|-------------|------|
| `Loggerx` | 疎通確認ログの出力。 |
| `App` / `Preparex` / `Progress` / `Scraper` / `HtmlOp` | パッケージ公開 API。 |

## 設計上の注意

`__all__` には `Loggerx` とエントリポイント関数を含めない。直接実行時は `xmain()` のみを呼び出す。
