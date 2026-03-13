from typing import Dict


class Progress:
    """進捗表示に必要な値をまとめて保持する。"""

    def __init__(self, meter_str: str, valuemin: str, valuemax: str, valuenow: str) -> None:
        """ARIA 由来の進捗属性を保持し、比較用の文字列も作る。"""
        self.meter_str = meter_str
        self.valuemin = valuemin
        self.valuemax = valuemax
        self.valuenow = valuenow
        self.meter = f"{self.valuemin}-{self.valuemax}-{self.valuenow}"

    def to_dict(self) -> Dict[str, str]:
        """保持している進捗情報を辞書へ変換する。"""
        return {
            "meter_str": self.meter_str,
            "valuemin": self.valuemin,
            "valuemax": self.valuemax,
            "valuenow": self.valuenow,
            "meter": self.meter,
        }
