def levenshtein_distance(str1: str, str2: str) -> int:
    """
    Calculates the minimum edit distance (Levenshtein) between two strings
    using O(min(m, n)) space complexity.
    """
    if len(str1) < len(str2):
        str1, str2 = str2, str1

    len1, len2 = len(str1), len(str2)
    if len2 == 0:
        return len1

    previous_row = list(range(len2 + 1))

    for i, char1 in enumerate(str1):
        previous_diagonal = previous_row[0]
        previous_row[0] = i + 1
        for j, char2 in enumerate(str2):
            current_val = previous_row[j + 1]
            if char1 == char2:
                previous_row[j + 1] = previous_diagonal
            else:
                # Optimized min calculation using built-in min()
                previous_row[j + 1] = 1 + min(previous_row[j], previous_row[j + 1], previous_diagonal)
            previous_diagonal = current_val

    return previous_row[len2]