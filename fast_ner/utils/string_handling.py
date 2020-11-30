def string_cleaning(entity):
    """Handle punctuations and tokenizes entity string.

    Removes punctuation characters from the string and performs
    string tokenization.

    Args:
        entity: A string.

    Returns:
        A list of string tokens, without any punctuation,
        based on the input string.

        ['have', 'you', 'watched', 'this', 'movie']

        Always returns a list. If the input string was empty,
        returns an empty list.
    """
    punctuation = ['. ', ',', ':', '"', '?', '!', '-', "' "]
    entity = entity.lower()
    entity += ' '
    for p in punctuation:
        entity = entity.replace(p,' ')
    return entity.split()