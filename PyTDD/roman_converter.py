def roman_converter(num):
    if not isinstance(num, int):
        return None
    
    if num <= 0 or num >= 4000:
        return None
    
    ROMAN_NUMS = [
        (1000, "M"),
        (900, "CM"),
        (500, "D"),
        (400, "CD"),
        (100, "C"),
        (90, "XC"),
        (50,"L"),
        (40, "XL"),
        (10, "X"),
        (9, "IX"),
        (5, "V"),
        (4, "IV"),
        (1, "I")
    ]

    out = ''
    for values, symbols in ROMAN_NUMS:
        
        while num >= values:
            out += symbols
            num -= values
    return out