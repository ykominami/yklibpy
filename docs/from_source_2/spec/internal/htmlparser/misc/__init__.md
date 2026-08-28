# htmlparser.misc.__init__ — 内部仕様書

**ファイル**: `src/yklibpy/htmlparser/misc/__init__.py`

## 概要

HTML タグと価格情報を扱う補助クラス群を `htmlparser.misc` パッケージ直下から再公開する。

---

## モジュールレベル定数・型

| 変数名 | 値/型 | 用途 |
|--------|-------|------|
| `__all__` | `list[str]` | `AnchorTagInfo`、`AnchorTagx`、`PriceInfo`、`Tagx` を公開 API として宣言する。 |

## 依存

| クラス/変数 | 用途 |
|-------------|------|
| `AnchorTagInfo` / `AnchorTagx` / `PriceInfo` / `Tagx` | パッケージ公開 API。 |
