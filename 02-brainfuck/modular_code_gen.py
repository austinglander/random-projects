
def to_brainfuck(input_string):
    """
    Takes an input string of ASCII characters and returns a string containing a brainfuck program that prints the string
    """
    out_string = ""
    # Add characters to memory, backwards
    for char in input_string[::-1]:
        out_string += '+'*ord(char)
        out_string += '>'
    # Chop off last '>'
    out_string = out_string[:-1]
    # Return to start of program, printing as we go
    out_string += '.<' * len(input_string)
    # Chop off last '<'
    out_string = out_string[:-1]
    return out_string

print(to_brainfuck("Alejandro in brainfuck\n"))
