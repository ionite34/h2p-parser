# Part of Speech Tag Operations

# Method to get the parent part of speech (VERB) or (NOUN) from a pos tag
def get_parent_pos(pos):
    if pos.startswith("VB"):
        return "VERB"
    elif pos.startswith("NN"):
        return "NOUN"
    elif pos.startswith("RB"):
        return "ADVERB"
    else:
        return None
