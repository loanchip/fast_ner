def string_cleaning(entity):
    punctuation = ['.', ',', ':', '"', '?', '!', '-']
    entity = entity.lower()
    for p in punctuation:
        entity = entity.replace(p,' ')
    return entity.split()