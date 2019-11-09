def merge_mappings(receiving, giving):
    """
    Merge two dictionaries.

    {1:2}, {1:{}} -> {1:{}}  # Dictionary overwrites other types
    {1:{}}, {1:2} -> {1:2}  # Giving overwrites receiving
    {1:{2,3}}, {1:{3,4}} -> {1:{2,3,4}}  # First dictionary is merged with second
    """
    for key in giving:
        if key not in receiving:
            receiving[key] = giving[key]
        else:
            if isinstance(receiving[key], dict):  # receiving is {1:{a,b}}
                if isinstance(giving[key], dict):  # receiving is {1:{a,b}}, giving is {1:{c,d}}
                    receiving[key] = merge_mappings(receiving[key], giving[key])  # result it {1:{a,b,c,d}}
                else:  # {1:{a,b}}  {1:2}
                    receiving[key] = giving[key]  # {1:2}
            else:  # {1:2}
                receiving[key] = giving[key]
    return receiving
