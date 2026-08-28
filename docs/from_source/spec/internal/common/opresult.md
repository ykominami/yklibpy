# OpResult — 内部仕様書

**ファイル**: `src/yklibpy/common/opresult.py`
**継承**: `Generic[T]`（`@dataclass(frozen=True)`）

## 概要

操作の成否と、失敗時の例外情報（発生箇所・メッセージ・型）を保持するイミュータブルな結果オブジェクト。`AppStore` の `get_directory_assoc_from_config`/`get_directory_assoc_from_db`/`get_file_assoc_from_config`/`get_file_assoc_from_db`/`get_from_config` など一部の `get_*` 系メソッドが、例外を送出する代わりに返す戻り値型として使われる。ただし `AppStore` の他の大半のメソッドは `try/except KeyError: return None` パターンで例外を握りつぶすだけであり、`OpResult` は `AppStore` 全体で統一的に使われているわけではない（詳細は `appstore.md` の「設計上の注意」）。

---

## インスタンス変数

| 変数名 | 型 | 説明 |
|--------|----|------|
| `ok` | `bool` | 操作が成功したかどうか。 |
| `value` | `T \| None` | 成功時の値。失敗時は `None`。 |
| `exc_occurred` | `bool` | 例外が発生したかどうか。 |
| `exc_location` | `str \| None` | 発生箇所（`ファイル名:行番号 in 関数名`）。 |
| `exc_message` | `str \| None` | 例外メッセージ。 |
| `exc_type` | `str \| None` | 例外の型名。 |
| `optional_string` | `str \| None` | 呼び出し元が付与する補足文字列（デバッグ用コンテキスト）。 |

---

## メソッド

### `success(value: T) -> "OpResult[T]"` (classmethod)

成功結果を生成する。例外関連フィールドはすべて `None`/`False`。

### `from_exception(exc: BaseException, optional_string: str) -> "OpResult[T]"` (classmethod)

例外から失敗結果を生成する。

```
処理フロー:
  1. exc.__traceback__ を末尾（tb_next が None になるまで）までたどる
  2. 最内フレームのファイル名・行番号・関数名から exc_location 文字列を組み立てる
  3. traceback が存在しない場合は exc_location を "unknown" とする
  4. ok=False の OpResult を返す
```

**Args**: `exc` — 発生した例外。`optional_string` — 呼び出し元コンテキストの補足文字列。

**Returns**: 失敗を表す `OpResult`。発生箇所はトレースバックの最内フレーム（実際に例外が起きた行）。

---

## 依存

なし（標準の `dataclasses`/`pathlib` のみ）。

---

## 設計上の注意

`frozen=True` のためインスタンス生成後にフィールドを変更できない。呼び出し元は `AppStore.get_from_config` などで `result.ok` を確認してから `result.value` を使う想定だが、失敗時に例外を再送出せず握りつぶすパターンが多く、呼び出し元での判定漏れに注意が必要。
