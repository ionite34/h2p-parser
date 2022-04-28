# Extended Grapheme to Phoneme conversion using CMU Dictionary and Heteronym parsing.

from h2p_parser.h2p import H2p


class CMUDictExt:
    def __init__(self, cmu_dict_path: str = None, h2p_dict_path: str = None, cmu_multi_mode: int = 0):
        # noinspection GrazieInspection
        """
        Initialize CMUDictExt - Extended Grapheme to Phoneme conversion using CMU Dictionary with Heteronym parsing.

        CMU multi-entry resolution modes:
            - -2 : Raw entry (i.e. 'A' resolves to 'AH0' and 'A(1)' to 'EY1')
            - -1 : Skip resolving any entry with multiple pronunciations.
            - 0 : Resolve using default un-numbered pronunciation.
            - 1 : Resolve using (1) numbered pronunciation.
            - n : Resolve using (n) numbered pronunciation.
            - If a higher number is specified than available for the word, the highest available number is used.

        :param cmu_dict_path: Path to CMU dictionary file (.txt)
        :type: str
        :param h2p_dict_path: Path to Custom H2p dictionary (.json)
        :type: str
        :param cmu_multi_mode: CMU resolution mode for entries with multiple pronunciations.
        :type: int
        """
        self.cmu_dict_path = cmu_dict_path
        self.h2p_dict_path = h2p_dict_path
        self.cmu_multi_mode = cmu_multi_mode
        self.h2p = H2p(h2p_dict_path, preload=True)
