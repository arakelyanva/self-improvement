def levenshtein_distance(str1: str, str2: str) -> int:
    """
    Calculates the minimum edit distance (Levenshtein) between two strings
    using O(min(m, n)) space complexity.
    """
    if len(str1) < len(str2):
        str1, str2 = str2, str1

    if not str2:
        return len(str1)

    previous_row = list(range(len(str2) + 1))
    
    for i, char1 in enumerate(str1):
        current_row = [i + 1]
        for j, char2 in enumerate(str2):
            insertions = previous_row[j + 1] + 1
            deletions = current_row[j] + 1
            substitutions = previous_row[j] + (char1 != char2)
            current_row.append(min(insertions, deletions, substitutions))
        previous_row = current_row

    return previous_row[-1]