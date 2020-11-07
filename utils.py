def rgb_to_kvColor(rgb):
    value = [x / 255 for x in rgb]
    if len(value) == 3:
        value.append(1)
    return value

