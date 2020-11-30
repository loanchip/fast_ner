def string_cleaning(entity):
    punctuation = ['. ', ',', ':', '"', '?', '!', '-', "' "]
    entity = entity.lower()
    entity += ' '
    for p in punctuation:
        entity = entity.replace(p,' ')
    return entity.split()