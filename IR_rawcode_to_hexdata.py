saiso = 0.2

ONE_PULSE = 473
ONE_SPACE = -1694
ZERO_PULSE = 470
ZERO_SPACE = -657

def decode_ir_raw(raw_data):
    # Tolerance function with 10% flexibility
    def within_tolerance(value, target):
        return abs(value - target) <= saiso * abs(target)

    # Extract header and footer
    header = raw_data[:2]  # 2 số đầu
    body = raw_data[2:-1]  # Các số giữa
    footer = raw_data[-1]  # Số cuối cùng

    # Debugging header and footer
    print(f"Header: {header}, Footer: {footer}")

    # Initialize decoded bits
    decoded_bits = []

    # Process the body in pairs
    for i in range(0, len(body), 2):
        # Pair of numbers
        pulse, space = body[i], body[i + 1]

        # Decode based on the rules
        if within_tolerance(pulse, ZERO_PULSE) and within_tolerance(space, ZERO_SPACE):
            decoded_bits.append("0")
        elif within_tolerance(pulse, ONE_PULSE) and within_tolerance(space, ONE_SPACE):
            decoded_bits.append("1")
        else:
            print(f"Unrecognized pair: ({pulse}, {space})")  # Debugging
            return "Invalid IR signal"

    # Join bits into a binary string
    decoded_binary = "".join(decoded_bits)

    # Convert binary string to hexadecimal format (LSB-first order)
    hex_groups = []
    for i in range(0, len(decoded_binary), 8):  # Process 8 bits at a time
        byte = decoded_binary[i:i + 8]  # Extract 8 bits
        # byte = byte[::-1]  # Reverse the bits for LSB-first order
        hex_value = hex(int(byte, 2))  # Convert reversed binary to hex
        hex_groups.append(hex_value.upper())

    # Output results
    print("Decoded binary:", decoded_binary)
    print("Decoded hex:", ", ".join(hex_groups))
    print("Number of bits:", len(decoded_binary), "\n")

    return decoded_binary, hex_groups, len(decoded_binary)


# Example usage:
raw_signal = [
[
[9282, -4549, 526, -684, 421, -710, 447, -1841, 473, -657, 447, -684, 447, -657, 473, -684, 500, -631, 500, -1762, 447, -1762, 447, -684, 447, -1788, 447, -1762, 473, -1814, 447, -1762, 447, -1762, 500, -684, 447, -684, 447, -657, 526, -1762, 447, -657, 421, -710, 500, -631, 500, -631, 473, -1788, 447, -1736, 473, -1736, 500, -684, 447, -1736, 526, -1736, 447, -1788, 500, -1736, 473, -10124]
]

]

for i in range(0,len(raw_signal),1):     
    print(f"{i+1}. ")
    decoded_result = decode_ir_raw(raw_signal[i])
