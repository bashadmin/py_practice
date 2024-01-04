# Re-executing the code to convert binary strings to ASCII characters

binary_strings = [
    "01100110", "01101001", "01101110", "01100100", "00101110", 
    "01100110", "01101111", "01101111", "00101111", 
    "00110010", "00110000", "00110010", "00110011", 
    "01000111", "01101111", "01101111", "01100111", "01101100", 
    "01100101", "01000011", "01100101", "01110010", "01110100", "01110011"
]

# Converting binary strings to characters
ascii_characters = [chr(int(binary, 2)) for binary in binary_strings]
ascii_string = ''.join(ascii_characters)
ascii_string
