A4_FREQ = 440  # Reference frequency for A4 (key number 49)

print("Key Number | Frequency (Hz)")
print("----------------------------")
for key in range(1, 89):
    # Calculate frequency using the 12-TET formula
    freq = A4_FREQ * (2 ** ((key - 49) / 12))
    # Print key number and its frequency formatted to two decimal places
    print(f"Key {key:3d}   | {freq:.2f} Hz")
