import sys, re

def tokenize_line(line):
    line = line.upper()
    # LOAD 5, R1
    # NEG R1

    # Individual characters match with:
    #     . \w \s [abcd]
    #  ? means optional: 0 or 1 of that letter
    #  * means zero or more (Kleene star)
    #  + means one or more

    # Single argument instructions:
    # (\w+)\s+(\w+)
    # Two-argument instructions:
    # (\w+)\s+(\w+),\s+(\w+)

    # (\w+)\s+(\w+)(?:,\s+(\w+))?

    m = re.fullmatch(r"\s*(\w+)\s+(\w+)(?:,\s*(\w+))?\s*", line)
    if not m:
        if re.fullmatch(r"\s*", line):
            return None
        else:
            raise Exception(f"Syntax error on line: {line}")
    return m.groups()


with open(sys.argv[1]) as f:
    code = f.readlines()

# TODO: preprocess code to remove comments and resolve labels to line numbers
instructions = list(map(tokenize_line, code))

registers = {
    "R1": 0,
    "R2": 0,
    "R3": 0,
    "R4": 0
}
pc = 0
# TODO: should check instruction arity somewhere
while pc < len(instructions):
    i = instructions[pc]
    if i is None:
        pc += 1
        continue
    print(registers)
    print(f"Executing: {i[0]}, {i[1]}, {i[2]}")
    if i[0] == "LOAD":
        # TODO: check that i[2] is a valid register name
        registers[i[2]] = int(i[1])
        pc += 1
    elif i[0] == "ADD":
        registers[i[2]] += registers[i[1]]
        pc += 1
    elif i[0] == "MOV":
        registers[i[2]] = registers[i[1]]
        pc += 1
    elif i[0] == "NEG":
        registers[i[1]] = -registers[i[1]]
        pc += 1
    elif i[0] == "PRINT":
        print(registers[i[1]])
        pc += 1
    elif i[0] == "JMP":
        pc = int(i[1]) - 1
    elif i[0] == "JZ":
        if registers[i[1]] == 0:
            pc = int(i[2]) - 1
        else:
            pc += 1
    elif i[0] == "JNZ":
        if registers[i[1]] != 0:
            pc = int(i[2]) - 1
        else:
            pc += 1
    elif i[0] == "JLZ":
        if registers[i[1]] < 0:
            pc = int(i[2]) - 1
        else:
            pc += 1
    elif i[0] == "JGZ":
        if registers[i[1]] > 0:
            pc = int(i[2]) - 1
        else:
            pc += 1
    else:
        raise Exception(f"Invalid instruction: {i[0]}")
print(registers)
