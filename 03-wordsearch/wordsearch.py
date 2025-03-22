
def word_search(char_matrix: list[list[str]], word_list: list) -> list[bool]:
    """
    Given a matrix of characters (wordsearch) and a list of strings, return a list of booleans detailing what is and isn't in the wordsearch.
    Words can be horizontal and vertical but not diagonal
    """
    # Algorithm:
    # Convert char_matrix and its transpose into a list of strings, where each string is a concatenated row or column
    # For each element of word_list, check if it (or its reverse) is in any element of the char_matrix or its transpose
    char_matrix_t = transpose(char_matrix)
    string_list = ["".join(i) for i in char_matrix] # Creates a list of strings, each string is a row of the wordsearch
    string_list_t = ["".join(i) for i in char_matrix_t] # Creates a list of strings, each string is a column of the wordsearch
    
    # Initialize our results array to all false
    results = [False for i in range(len(word_list))]

    # Check if each word, forwards or backwards, is in any of the strings in the two lists we created
    # Use indices to index results array
    for index, word in enumerate(word_list):
        for row in string_list:
            if word in row or word[::-1] in row:
                results[index] = True
                break
        # Skip looking at columns if found in rows
        if results[index]:
            continue
        for column in string_list_t:
            if word in column or word[::-1] in column:
                results[index] = True
                break
    return results

def transpose(matrix: list[list]) -> list[list]:
    """
    Returns the transpose of matrix (rows and columns flipped)
    """
    transposed = [[] for i in range(len(matrix[0]))]
    for row in matrix:
        for j, val in enumerate(row):
            transposed[j].append(val)
    return transposed

if __name__ == "__main__":
    myWords = [
        ['a', 'o', 'c', 'a', 't'],
        ['b', 'x', 'q', 'h', 'o'],
        ['w', 'e', 'd', 'm', 'r'],
        ['v', 'i', 'm', 'x', 'z'],
        ['q', 'u', 'b', 'd', 'f']
    ]
    # Expected [True, True, False, False, True]
    print(word_search(myWords, ["cat", "taco", "dog", "cow", "cat"]))