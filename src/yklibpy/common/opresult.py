from dataclasses import dataclass
from pathlib import Path
from typing import Generic, TypeVar

T = TypeVar("T")


@dataclass(frozen=True)
class OpResult(Generic[T]):
    """操作の成否と、失敗時の例外情報を保持する。"""

    ok: bool
    value: T | None
    exc_occurred: bool
    exc_location: str | None
    exc_message: str | None
    exc_type: str | None
    optional_string: str | None

    @classmethod
    def success(cls, value: T) -> "OpResult[T]":
        """成功結果を生成する。"""
        return cls(
            ok=True,
            value=value,
            exc_occurred=False,
            exc_location=None,
            exc_message=None,
            exc_type=None,
            optional_string=None,
        )

    @classmethod
    def from_exception(cls, exc: BaseException, optional_string: str) -> "OpResult[T]":
        """例外から失敗結果を生成する。

        発生箇所はトレースバックの最内フレーム（実際に例外が起きた行）を用いる。
        """
        tb = exc.__traceback__
        if tb is not None:
            while tb.tb_next is not None:
                tb = tb.tb_next
            frame = tb.tb_frame
            location = (
                f"{Path(frame.f_code.co_filename).name}:"
                f"{tb.tb_lineno} in {frame.f_code.co_name}"
            )
        else:
            location = "unknown"
        return cls(
            ok=False,
            value=None,
            exc_occurred=True,
            exc_location=location,
            exc_message=str(exc),
            exc_type=type(exc).__name__,
            optional_string=optional_string,
        )
