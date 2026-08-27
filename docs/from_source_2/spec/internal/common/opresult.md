# OpResult — 内部仕様書

**ファイル**: `src/yklibpy/common/opresult.py`  
**継承**: `Generic[T]`

## 概要

操作の成功値、または失敗時の例外型・メッセージ・発生位置を不変データとして保持する汎用結果型です。

---

## インスタンス変数

| 変数名 | 型 | 説明 |
|--------|----|------|
| `ok` | `bool` | 操作が成功したかを示します。 |
| `value` | `T | None` | 成功時の値です。 |
| `exc_occurred` | `bool` | 例外発生の有無です。 |
| `exc_location` | `str | None` | 例外最内フレームの位置です。 |
| `exc_message` | `str | None` | 例外メッセージです。 |
| `exc_type` | `str | None` | 例外クラス名です。 |
| `optional_string` | `str | None` | 呼び出し側が付与する補足情報です。 |

---

## メソッド

### `success(value: T) -> OpResult[T]` (classmethod)

値を格納し、例外情報を空にした成功結果を生成します。

### `from_exception(exc: BaseException, optional_string: str) -> OpResult[T]` (classmethod)

例外から失敗結果を生成します。

処理フロー:

1. 例外のトレースバックを取得します。
2. 最内フレームまで移動し、ファイル名・行番号・関数名を組み立てます。
3. 例外型、メッセージ、補足情報を含む失敗結果を返します。

## 依存

| クラス/変数 | 用途 |
|-------------|------|
| `dataclass(frozen=True)` | 結果を不変データクラスとして定義します。 |
| `Path` | トレースバックのファイル名抽出に使用します。 |
