import sys, re

def parse(code):
    instructions = []
    labels = {}
    i_num = 0
    for line in code:
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

        # remove comments
        line = re.sub(r";.*", "", line)

        # find a label, if any
        m = re.match(r"\s*(\w+):", line)
        if m:
            labelname = m.groups()[0]
            labels[labelname] = i_num
            line = re.sub(r"\w+:", "", line)

        # parse instruction
        m = re.fullmatch(r"\s*(\w+)\s+(-?\w+)(?:,\s*(\w+))?\s*", line)
        if m:
            instructions.append(m.groups())
            i_num += 1
        else:
            if not re.fullmatch(r"\s*", line):
                raise Exception(f"Syntax error on line: {line}")
    return (instructions, labels)

with open(sys.argv[1]) as f:
    code = f.readlines()

# TODO: preprocess code to remove comments and resolve labels to line numbers
(instructions, labels) = parse(code)

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
    print(registers)
    print(f"Executing: {i[0]}, {i[1]}, {i[2]}")
    if i[0] == "LOAD":
        if not re.fullmatch(r"R\d\s*",i[2]):
            raise Exception(f"Invalid register name: {i[2]}")
        try:
            load_int = int(i[1])
            if load_int < -128 or load_int >= 127:
                raise Exception(f"LOAD value out of range on line {pc + 1}: {load_value}")
        except ValueError:
            raise Exception(f"Invalid LOAD value on line {pc + 1}: {i[1]}")
        registers[i[2]] = load_int
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
        pc = labels[i[1]]
    elif i[0] == "JZ":
        if registers[i[1]] == 0:
            pc = labels[i[2]]
        else:
            pc += 1
    elif i[0] == "JNZ":
        if registers[i[1]] != 0:
            pc = labels[i[2]]
        else:
            pc += 1
    elif i[0] == "JLZ":
        if registers[i[1]] < 0:
            pc = labels[i[2]]
        else:
            pc += 1
    elif i[0] == "JGZ":
        if registers[i[1]] > 0:
            pc = labels[i[2]]
        else:
            pc += 1
    elif i[0] == "INC":
        registers[i[1]] += 1
        pc += 1
    elif i[0] == "DEC":
        registers[i[1]] -= 1
        pc += 1
    else:
        raise Exception(f"Invalid instruction: {i[0]}")
print(registers)


