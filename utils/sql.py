def join_int(values: list) -> str:
    """
    Returns concatenate items in list into a string using ","
        Parameters:
            values (list): a list of values for join
        Returns:
            str: string of joined items from entering list
        Examples:
            join_int([1, 2, 3]) - > "1,2,3"
            join_int(["some", "items", "to", "string"]) -> "some,items,to,string"
    """
    return ",".join(str(value) for value in values)


def join_str(values: list) -> str:
    """
    Returns concatenate items in list into a string using "," and quoted by "'"
        Parameters:
            values (list): a list of values for join
        Returns:
            str: string of quoted and joined items from entering list
        Examples:
            join_str([1, 2, 3]) - > "'1','2','3"'
            join_str(["some", "items", "to", "string"]) -> "'some','items','to','string'"
    """
    return ",".join(f"'{str(value)}'" for value in values)


def join_str_match(values: list) -> str:
    """
    Returns concatenate items in list into a string using "|" and quoted by "'"
        Parameters:
            values (list): a list of values for join
        Returns:
            str: string of quoted and joined items from entering list
        Examples:
            join_str([1, 2, 3]) - > "1|2|3"
            join_str(["some", "items", "to", "string"]) -> "some|items|to|string"
    """
    return "|".join(f"{str(value)}" for value in values)


def join_str_query(args: list) -> str:
    """
    Returns concatenate items in list into a string using "," and quoted by "'"
        Parameters:
            values (list): a list of values for join
        Returns:
            str: string of quoted and joined items from entering list
        Examples:
            join_str([1, 2, 3]) - > "'1','2','3"'
            join_str(["some", "items", "to", "string"]) -> "'some','items','to','string'"
    """
    return "_".join(
        (
            str(arg).replace("'", "").replace("[", "").replace("]", "")
            if not isinstance(arg, list)
            else ",".join(map(str, arg))
        )
        for arg in args
    )
