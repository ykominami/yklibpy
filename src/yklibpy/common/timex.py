from datetime import datetime, timedelta, timezone


class Timex:
    """時刻取得を JST 基準で提供する。"""

    JST = timezone(timedelta(hours=9))

    @classmethod
    def get_now(cls) -> str:
        """現在時刻を JST の ISO 8601 文字列で返す。"""
        return datetime.now(cls.JST).isoformat()
