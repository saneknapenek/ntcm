def zfill_list(lst: list, width: int) -> list:
    if width <= len(lst):
        return lst
    
    num_zeros = width - len(lst)
    return [0] * num_zeros + lst