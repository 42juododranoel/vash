def merge_metas(receiving, giving):
    """
    Merge two metas.

    {1:2}, {1:{}} -> {1:{}}  # Dictionary overwrites other types
    {1:2}, {1:[]} -> {1:[]}  # List overwrites other types

    {1:{}}, {1:2} -> {1:2}  # Giving overwrites receiving
    {1:[]}, {1:2} -> {1:2}  # Giving overwrites receiving

    {1:{2,3}}, {1:{3,4}} -> {1:{2,3,4}}  # Receiving dictionary is recursively merged with giving
    {1:[2,3]}, {1:[3,4]} -> {1:[2,3,3,4]}  # Receiving list is extended by giving

    """
    for key in giving:
        if key not in receiving:
            receiving[key] = giving[key]
        else:
            if isinstance(receiving[key], dict):  # receiving is {1:{a,b}}
                if isinstance(giving[key], dict):  # receiving is {1:{a,b}}, giving is {1:{c,d}}
                    receiving[key] = merge_metas(receiving[key], giving[key])  # receiving becomes {1:{a,b,c,d}}
                else:  # receiving is {1:{a,b}}, giving is {1:2}
                    receiving[key] = giving[key]  # receiving becomes {1:2}

            elif isinstance(receiving[key], list):  # receiving is {1:[a,b]}
                if isinstance(giving[key], list):  # receiving is {1:[a,b]}, giving is {1:[c,d]}
                    receiving[key].extend(giving[key])  # receiving becomes {1:[a,b,c,d]}
                else:  # receiving is {1:[a,b]}, giving is {1:2}
                    receiving[key] = giving[key]  # receiving becomes {1:2}

            else:  # receiving is {1:2}
                receiving[key] = giving[key]

    return receiving
