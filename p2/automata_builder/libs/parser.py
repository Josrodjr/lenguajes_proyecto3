# define the rules of the program

# separador = ' '

operandos = {
    ' ': 1,
    '|': 1,
    '*': 2,
    '+': 2,
    '?': 1
}

def parse_input(text):
    # parsed input result
    parsed = []
    # parenthesis closure counters
    parenthesis_cont = 0
    # current token detected
    token = ''
    # for loop for recieved text
    for char in range(len(text)):
        if text[char] == '(' or text[char] == ')':
            if parenthesis_cont >= 1:
                token += text[char]
        if text[char] == '(':
            parenthesis_cont += 1
        if text[char] == ')':
            # TODO: send the current token found to same function in recursive motive
            if parenthesis_cont == 1:
                result = parse_input(token)
                parsed.append(result)
                token = ''
            # TODO: empty found token
            parenthesis_cont -= 1
        # if text[char] == ' ':
        #     # append to parsed the current value
        #     if token != '':
        #         parsed.append(token)
        #     # empty found char
        #     token = ''
        if text[char] in operandos and parenthesis_cont == 0:
            if token != '':
                parsed.append(token)
            token = ''
            token += text[char]
            parsed.append(token)
            token = ''
        # if none of the above do a concat to current found token and keep looking
        elif text[char] != '(' and text[char] != ')':
            token += text[char]
        if char == len(text)-1:
            parsed.append(token)
    return parsed



def remove_empty(operations_array):
    for i in range(len(operations_array)):
        if isinstance(operations_array[i], list):
            operations_array[i] = remove_empty(operations_array[i])
        else:
            if operations_array[i] == '':
                operations_array.remove('')
    return operations_array


def pre_parse_input(text_array):
    new_array = []
    for value in text_array:
        if isinstance(value, list):
            value = pre_parse_input(value)
        # check if values is operand 
            new_array.append(value)
        else:
            if value in operandos:
                new_array.append(value)
                continue
            else:
                # check if value is epsion
                # if value == 'ε':
                #     value = 0
                value = ord(str(value))
                value = str(value)
                if value == '949':
                    value = '0'
                new_array.append(value)
    return new_array
