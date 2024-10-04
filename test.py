hex_value = 0x31290000

# Convert to bytes

byte_string = hex_value.to_bytes(4, 'little')

# Format to string

formatted_string = ' '.join(f'{b:02x}' for b in byte_string)
print(formatted_string)