def is_valid_news(title):

    if not title:
        return False

    if len(title) < 30:
        return False

    return True
