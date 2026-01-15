#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import argparse
from pathlib import Path

import yaml

# PyYAML が付ける / あるいは YAML 内に書かれている可能性のあるタグ表現
DYNAMIC_INLINE_TABLE_TAGS = {
    "tag:yaml.org,2002:python/object/new:toml.decoder.DynamicInlineTableDict",
    "!!python/object/new:toml.decoder.DynamicInlineTableDict",  # 念のため
}


class TagStrippingSafeLoader(yaml.SafeLoader):
    """
    SafeLoader をベースにしつつ、特定の python/object/new タグだけ
    普通の dict に落とすための Loader。
    """

    pass


def _dynamic_inline_table_dict_constructor(loader: yaml.SafeLoader, node: yaml.Node):
    # node が mapping の想定
    mapping = loader.construct_mapping(node, deep=True)
    # toml の DynamicInlineTableDict は dictitems キー配下に実体が入っていることが多い
    if (
        isinstance(mapping, dict)
        and "dictitems" in mapping
        and isinstance(mapping["dictitems"], dict)
    ):
        return mapping["dictitems"]
    return mapping


def _register_constructors():
    # 代表的なタグ（tag:...形式）を登録
    TagStrippingSafeLoader.add_constructor(
        "tag:yaml.org,2002:python/object/new:toml.decoder.DynamicInlineTableDict",
        _dynamic_inline_table_dict_constructor,
    )

    # YAML 内で !!python/object/new:... と書かれていた場合に備えて multi_constructor も登録
    def _multi_python_object_new(
        loader: yaml.SafeLoader, tag_suffix: str, node: yaml.Node
    ):
        # tag_suffix は "toml.decoder.DynamicInlineTableDict" のような文字列になる
        full = f"tag:yaml.org,2002:python/object/new:{tag_suffix}"
        if (
            full
            == "tag:yaml.org,2002:python/object/new:toml.decoder.DynamicInlineTableDict"
        ):
            return _dynamic_inline_table_dict_constructor(loader, node)
        # それ以外の python/object/new は安全のため許可しない（明示的に失敗させる）
        raise yaml.constructor.ConstructorError(
            None,
            None,
            f"Unsupported python/object/new tag: {full} (refuse to construct). "
            f"Please strip/convert this node explicitly.",
            node.start_mark,
        )

    TagStrippingSafeLoader.add_multi_constructor(
        "tag:yaml.org,2002:python/object/new:",
        _multi_python_object_new,
    )


def strip_tags_and_dump(input_path: Path, output_path: Path):
    text = input_path.read_text(encoding="utf-8")

    data = yaml.load(text, Loader=TagStrippingSafeLoader)

    # タグ無しで人間が読みやすい YAML を出力
    dumped = yaml.safe_dump(
        data,
        allow_unicode=True,
        sort_keys=False,
        default_flow_style=False,
    )

    output_path.write_text(dumped, encoding="utf-8")


def main():
    _register_constructors()

    parser = argparse.ArgumentParser(
        description="Convert YAML containing python/object/new tags into plain tag-free YAML."
    )
    parser.add_argument("input", type=Path, help="Input YAML path (e.g. a.yaml)")
    parser.add_argument(
        "-o",
        "--output",
        type=Path,
        default=None,
        help="Output YAML path (default: <input>.stripped.yaml)",
    )
    args = parser.parse_args()

    in_path: Path = args.input
    if args.output is None:
        out_path = in_path.with_suffix(in_path.suffix + ".stripped.yaml")
    else:
        out_path = args.output

    strip_tags_and_dump(in_path, out_path)
    print(f"written: {out_path}")


if __name__ == "__main__":
    main()
