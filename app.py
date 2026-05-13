def levenshtein_distance(str1: str, str2: str) -> int:
    """
    Calculates the minimum edit distance (Levenshtein) between two strings.
    """
    if len(str1) > len(str2):
        str1, str2 = str2, str1

    prev_row = list(range(len(str1) + 1))
    current_row = [0] * (len(str1) + 1)

    for i, char2 in enumerate(str2):
        current_row[0] = i + 1
        for j, char1 in enumerate(str1):
            cost = 0 if char1 == char2 else 1
            
            current_row[j + 1] = min(
                prev_row[j + 1] + 1,   # Deletion
                current_row[j] + 1,    # Insertion
                prev_row[j] + cost     # Substitution
            )
        prev_row = current_row[:]

    return prev_row[-1]
