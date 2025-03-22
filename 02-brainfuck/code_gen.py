# Store "Hello World!" in memory
print("+"*72, end='') # Increment byte to 72 (H)
print(">", end='') # Increment PC
print("+"*101, end='') # Increment byte to 101 (e)
print(">", end='') # Increment PC
print("+"*108, end='') # Increment byte to 108 (l)
print(">", end='') # Increment PC
print("+"*108, end='') # Increment byte to 108 (l)
print(">", end='') # Increment PC
print("+"*111, end='') # Increment byte to 111 (o)
print(">", end='') # Increment PC
print("+"*32, end='') # Increment byte to 32 ( )
print(">", end='') # Increment PC
print("+"*87, end='') # Increment byte to 87 (W)
print(">", end='') # Increment PC
print("+"*111, end='') # Increment byte to 111 (o)
print(">", end='') # Increment PC
print("+"*114, end='') # Increment byte to 114 (r)
print(">", end='') # Increment PC
print("+"*ord("l"), end='') # Increment byte to "l"
print(">", end='') # Increment PC
print("+"*ord("d"), end='') # Increment byte to "d"
print(">", end='') # Increment PC
print("+"*ord("!"), end='') # Increment byte to "!"
print(">", end='') # Increment PC
print("+"*ord("\n"), end='') # Increment byte to "\n"

# Output Result
print("<"*12, end="") # Return to start of memory
for i in range(12):
    print(".>", end="") # output current value and increment PC
print(".", end="") # output final value without incrementing PC

