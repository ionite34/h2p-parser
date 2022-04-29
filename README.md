# Heteronym to Phoneme Parser

[![Python package](https://github.com/ionite34/h2p-parser/actions/workflows/python-package.yml/badge.svg)](https://github.com/ionite34/h2p-parser/actions/workflows/python-package.yml)
[![CodeQL](https://github.com/ionite34/h2p-parser/actions/workflows/codeql-analysis.yml/badge.svg)](https://github.com/ionite34/h2p-parser/actions/workflows/codeql-analysis.yml)
[![FOSSA Status](https://app.fossa.com/api/projects/git%2Bgithub.com%2Fionite34%2Fh2p-parser.svg?type=shield)](https://app.fossa.com/projects/git%2Bgithub.com%2Fionite34%2Fh2p-parser?ref=badge_shield)

### Fast parsing of English Heteronyms to Phonemes using contextual part-of-speech.

Provides the ability to convert heteronym graphemes to their phonetic pronunciations.

Designed to be used in conjunction with other fixed grapheme-to-phoneme dictionaries such as [`CMUdict`](https://github.com/cmusphinx/cmudict)

This package also offers a combined Grapheme-to-Phoneme dictionary,
combining the functionality of fixed lookups handled by CMUdict and context-based parsing as
offered by this module.

## Usage - CMUDict Direct Replacement

Using the CMUDict compatibility wrapper, you can integrate heteronym parsing
support into your existing machine-learning pipeline by replacing 1 line of code:

Example: `FastPitch/common/text/__init__.py` from NVIDIA's [FastPitch](https://github.com/NVIDIA/DeepLearningExamples/tree/master/PyTorch/SpeechSynthesis/FastPitch)

```diff
- from .cmudict import CMUDict
+ from h2p-parser.compat.cmudict import CMUDict

cmudict = CMUDict()
```
>**Note**: The CMUDict wrapper was designed around the module as used in NVIDIA's [DeepLearningExamples](https://github.com/NVIDIA/DeepLearningExamples) repository.
> Your existing implementation may be different. 
>
> Specifically this [`cmudict.py`](https://github.com/NVIDIA/DeepLearningExamples/blob/master/PyTorch/SpeechSynthesis/FastPitch/common/text/cmudict.py) file was used as the replacement target.

## Usage

### 1. Combined Grapheme-to-Phoneme dictionary

`Feature pending`

### 2. Heteronym-to-Phoneme parsing only
To use only the core heteronym-to-phoneme parsing functions,
without fixed dictionary support, the `H2p` class
is able to be directly instantiated and called.

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
