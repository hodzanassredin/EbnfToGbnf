# EBNF Converter

This simple script is designed to convert EBNF grammar descriptions into the other formats like GBNF format used in the [llama.cpp](https://github.com/ggerganov/llama.cpp) project and [Lark](https://github.com/lark-parser/lark) .

## Features

- Supports various EBNF variations.
- Allows modification of conversion rules.
- Easy to use.

## Problems

- After conversion, you need to handle additional problems like whitespaces and so on. 
- for GBNF read the [doc](https://github.com/ggerganov/llama.cpp/blob/master/grammars/README.md) 
- for Lark read the [doc](https://lark-parser.readthedocs.io/en/stable/grammar.html)

## Installation

To use this script, you need to install the [Lark](https://github.com/lark-parser/lark) library. Run the following command to install it:

```bash
pip install Lark
```

## Usage

To convert an EBNF file to GBNF, run the following command:

```bash
python ebnf_to_gbnf.py example.ebnf
```

To convert an EBNF file to Lark, run the following command:

```bash
python ebnf_to_lark.py example.ebnf
```

Where `example.ebnf` is your EBNF grammar file.

## Grammar Description

The EBNF grammar is defined in the `ebnf_grammar` variable in the `ebnf_to_XXX.py` file. You can modify it according to your requirements.

## Modifying Conversion Rules

You can modify the conversion rules by changing the functions whose names start with `rebuild_`. These functions handle the transformation of various EBNF elements into their corresponding GBNF elements.

## Error Handling

The script handles the following errors:

- File not found: Displays an error message.
- Parsing errors: Displays an error message with the cause.

