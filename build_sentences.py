def build_sentence(word1, word2):
    """Concatenate two words with a space between them."""
    return f"{word1} {word2}"


def capitalize_sentence(sentence):
    """Capitalize the first letter of a sentence."""
    if not sentence:
        return sentence
    return sentence[0].upper() + sentence[1:]


def add_period(sentence):
    """Add a period to the end of a sentence if it doesn't have one."""
    if not sentence.endswith('.'):
        return sentence + '.'
    return sentence


def build_full_sentence(word1, word2):
    """Build a full sentence from two words: capitalize and add period."""
    sentence = build_sentence(word1, word2)
    sentence = capitalize_sentence(sentence)
    sentence = add_period(sentence)
    return sentence
