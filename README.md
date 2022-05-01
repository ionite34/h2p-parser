# Heteronym to Phoneme Parser

[![Python package](https://github.com/ionite34/h2p-parser/actions/workflows/python-package.yml/badge.svg)](https://github.com/ionite34/h2p-parser/actions/workflows/python-package.yml)
[![CodeQL](https://github.com/ionite34/h2p-parser/actions/workflows/codeql-analysis.yml/badge.svg)](https://github.com/ionite34/h2p-parser/actions/workflows/codeql-analysis.yml)
[![codecov](https://codecov.io/gh/ionite34/h2p-parser/branch/main/graph/badge.svg?token=AAJWXIG728)](https://codecov.io/gh/ionite34/h2p-parser)
[![FOSSA Status](https://app.fossa.com/api/projects/git%2Bgithub.com%2Fionite34%2Fh2p-parser.svg?type=shield)](https://app.fossa.com/projects/git%2Bgithub.com%2Fionite34%2Fh2p-parser?ref=badge_shield)

### Fast parsing of English Heteronyms to Phonemes using contextual part-of-speech.

Provides the ability to convert heteronym graphemes to their phonetic pronunciations.

Designed to be used in conjunction with other fixed grapheme-to-phoneme dictionaries such as [`CMUdict`](https://github.com/cmusphinx/cmudict)

This package also offers a combined Grapheme-to-Phoneme dictionary,
combining the functionality of fixed lookups handled by CMUdict and context-based parsing as
offered by this module.

## Usage

### 1. Combined Grapheme-to-Phoneme dictionary

The `CMUDictExt` class combines a pipeline for context-based heteronym parsing to phonemes and a fixed dictionary lookup
replacement using the CMU Pronouncing Dictionary. 

Example: 

```python
from h2p_parser.cmudictext import CMUDictExt

CMUDictExt = CMUDictExt()

# Parsing replacements for a line. This can be one or more sentences.
line = CMUDictExt.convert("The cat read the book. It was a good book to read.")
# -> "{DH AH0} {K AE1 T} {R EH1 D} {DH AH0} {B UH1 K}. {IH1 T} {W AA1 Z} {AH0} {G UH1 D} {B UH1 K} {T UW1} {R IY1 D}."
```

> Additional optional parameters are available when defining a `CMUDictExt` instance:

| Parameter          | Type   | Default Value | Description                                                                                                                                                                                                             |
|--------------------|--------|---------------|-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| `cmu_dict_path`    | `str`  | `None`        | Path to a custom CMUDict file in `.txt` format                                                                                                                                                                          |
| `h2p_dict_path`    | `str`  | `None`        | Path to a custom H2p Dictionary file in `.json` format. See the [example.json](h2p_parser/data/example.json) for the expected format.                                                                                   |
| `cmu_multi_mode`   | `int`  | `0`           | Default selection index for CMUDict entries with multiple pronunciations as donated by the `(1)` or `(n)` format                                                                                                        |
| `process_numbers`  | `bool` | `True`        | Toggles conversion of some numbers and symbols to their spoken pronunciation forms. See [numbers.py](h2p_parser/text/numbers.py) for details on what is covered.                                                        |
| `phoneme_brackets` | `bool` | `True`        | Surrounds phonetic words with curly brackets i.e. `{R IY1 D}`                                                                                                                                                           |
| `unresolved_mode`  | `str`  | `keep`        | Unresolved word resolution modes: <br> `keep` - Keeps the text-form word in the output. <br> `remove` - Removes the text-form word from the output. <br> `drop` - Returns the line as `None` if any word is unresolved. |


### 2. Heteronym-to-Phoneme parsing only
To use only the core heteronym-to-phoneme parsing functions,
without fixed dictionary support, use `H2p` class.

Example:

```python
from h2p_parser.h2p import H2p

h2p = H2p(preload=True) # preload flag improves first-inference performance

# checking if a line contains a heteronym
state = h2p.contains_het("There are no heteronyms in this line.")
# -> False

# replacing a single line
line = h2p.replace_het("I read the book. It was a good book to read.")
# -> "I {R EH1 D} the book. It was a good book to {R IY1 D}."

# replacing a list of lines
lines = h2p.replace_het_list(["I read the book. It was a good book to read.",
                              "Don't just give the gift; present the present.",
                              "If you were to reject the product, it would be a reject."])
# -> ["I {R EH1 D} the book. It was a good book to {R IY1 D}.",
#     "Don't just give the gift; {P R IY0 Z EH1 N T} the {P R EH1 Z AH0 N T}.",
#     "If you were to {R IH0 JH EH1 K T} the product, it would be a {R IY1 JH EH0 K T}."]
```
>**Note**: Depending on your performance requirements, there is a speed improvement for processing large text line batches by using `replace_het_list()` with a list of all text lines, instead of making repeated calls to `replace_het()`. See the performance section for more details and guidelines for optimizations. 

## License

The code in this project is released under [Apache License 2.0](LICENSE).

[![FOSSA Status](https://app.fossa.com/api/projects/git%2Bgithub.com%2Fionite34%2Fh2p-parser.svg?type=large)](https://app.fossa.com/projects/git%2Bgithub.com%2Fionite34%2Fh2p-parser?ref=badge_large)
