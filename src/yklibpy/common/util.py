import csv
from io import StringIO
from pathlib import Path
from typing import Optional, Sequence

import yaml


class Util:
    @classmethod
    def flatten(cls, items):
        """Flatten arbitrarily nested iterables into a single list.

        Args:
            items (Iterable): Possibly nested lists/tuples of values.

        Returns:
            list: Flattened sequence preserving order.
        """
        flat_list = []
        for item in items:
            if isinstance(item, list):
                flat_list.extend(cls.flatten(item))
            else:
                flat_list.append(item)

        return flat_list

    @classmethod
    def load_yaml(cls, input_path: Path) -> dict:
        """Load a YAML file and return it as a dictionary.

        Args:
            input_path (Path): Path to the YAML file.

        Returns:
            dict: Parsed YAML content.
        """
        data = None
        with open(input_path, "r", encoding="utf-8") as f:
            data = yaml.load(f, Loader=yaml.FullLoader)
        return data

    @classmethod
    def output_yaml(cls, assoc: dict, output_path: Optional[Path] = None) -> str:
        """Serialize a dictionary to YAML and optionally write it to disk.

        Args:
            assoc (dict): Data to dump.
            output_path (Path | None): Destination path. When ``None`` the YAML
                string is merely returned.

        Returns:
            str: YAML representation of ``assoc``.
        """
        yaml_str = yaml.dump(assoc, default_flow_style=False, allow_unicode=True, sort_keys=False)

        if output_path is not None:
            with open(output_path, "w", encoding="utf-8") as f:
                f.write(yaml_str)

        return yaml_str

    @classmethod
    def load_tsv(cls, input_path: Path, fieldnames: Optional[Sequence[str]] = None) -> list[dict]:
        """Read a TSV file and convert rows into dictionaries.

        Args:
            input_path (Path): TSV file path.
            fieldnames (Sequence[str] | None): Explicit headers. When ``None`` the
                first row becomes the header.

        Returns:
            list[dict]: Each row keyed by the header columns.

        Raises:
            ValueError: If no headers can be determined.
        """
        records = []
        with open(input_path, "r", encoding="utf-8", newline="") as f:
            reader = csv.reader(f, delimiter="\t")
            headers = list(fieldnames) if fieldnames is not None else None

            for row in reader:
                if headers is None:
                    headers = row
                    continue
                record = {key: value for key, value in zip(headers, row)}
                records.append(record)

        if headers is None:
            raise ValueError("ヘッダー行が存在しません。fieldnamesを指定してください。")

        return records

    @classmethod
    def output_tsv(
        cls, records: Sequence[dict], output_path: Optional[Path] = None, fieldnames: Optional[Sequence[str]] = None
    ) -> str:
        """Write record dictionaries to TSV format.

        Args:
            records (Sequence[dict]): Rows to emit.
            output_path (Path | None): Optional destination file.
            fieldnames (Sequence[str] | None): Header order override; defaults to
                keys of the first record.

        Returns:
            str: TSV string containing the headers and rows.

        Raises:
            ValueError: If neither records nor ``fieldnames`` are provided.
        """
        if not records and fieldnames is None:
            raise ValueError("fieldnamesを指定するか、recordsに1件以上のデータを含めてください。")

        if fieldnames is None:
            headers = []
        else:
            headers = fieldnames

        buffer = StringIO()
        writer = csv.writer(buffer, delimiter="\t", lineterminator="\n")
        writer.writerow(headers)
        for record in records:
            # print(record)
            # print(headers)
            row = [record.get(header, "") for header in headers]
            writer.writerow(row)

        tsv_str = buffer.getvalue()

        if output_path is not None:
            with open(output_path, "w", encoding="utf-8", newline="") as f:
                f.write(tsv_str)

        return tsv_str

    def test_yaml(self, input_file:str, input_file_2:str, output_file:str):
        """Developer helper for merging Udemy YAML progress data.

        Returns:
          None
        """
        input_path = Path(input_file)
        input_path_2 = Path(input_file_2)
        output_path = Path(output_file)
        dict = Util.load_yaml(input_path)
        # print(dict)

        dict_2 = Util.load_yaml(input_path_2)
        #
        output_tsv_path = input_path_2.with_suffix(".tsv")
        output_tsv_path_2 = output_path.with_suffix(".tsv")
        # keys = dict.keys()
        values = dict.values()
        # print(values)
        keys = list(values)[0].keys()
        Util.output_tsv(values, output_tsv_path, keys)
        # exit()
        values_2 = dict_2.values()
        keys_2 = list(values_2)[0].keys()
        Util.output_tsv(values_2, output_tsv_path_2, keys_2)

        for key_2, value_2 in dict_2.items():
            value_2["Time"] = "0時間"
            if key_2 in dict.keys():
                value = dict[key_2]
                if "Time" in value.keys():
                    value_2["Time"] = value["Time"]
            else:
                value_2["Time"] = "0時間"

        Util.output_yaml(dict_2, output_path)

    def test_tsv(self, input_file:str, input_file_2:str, output_file:str):
        """Developer helper for merging Udemy TSV progress data.

        Returns:
          None
        """
        input_path = Path(input_file)
        dict = Util.load_yaml(input_path)

        # input_path = Path('output_2.tsv')
        input_path_2 = Path(input_file_2)
        output_path = Path(output_file)
        dict = Util.load_tsv(input_path)
        dict_2 = Util.load_tsv(input_path_2)
        for record_2 in dict_2:
            record_2["Time"] = "0時間"
            if "Course_ID" in dict:
                record = dict[record_2["Course_ID"]]
                if "Time" in record.keys():
                    record_2["Time"] = record["Time"]
            else:
                record_2["Time"] = "0時間"
        Util.output_tsv(dict_2, output_path)


if __name__ == "__main__":
    test_util = Util()
    test_util.test_yaml(input_file="output_udemy_2.yaml", input_file_2="output_udemy_4.yaml", output_file="output_udemy_5.yaml")
    test_util.test_tsv(input_file="output_udemy_4.tsv", input_file_2="output_udemy_5.tsv", output_file="output_udemy_6.tsv")
