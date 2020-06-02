import copy
# lib for useful methods used in main parser

# lib for the generation of DFA of a single string
# from automata_builder.export import generate_DFA

def parse_findings_plus(whole_string):
    # three conditions always meet
    # 1) the production starts with an identifier found before the = sign
    # 2) the = sign found 
    # 3) the opening " found then the closing " ends with a .
    model_parsed_string = {
        'left_operand': '',
        'operation': '',
        'right_operand': ''
    }
    p_string = {
        'left_operand': '',
        'operation': '',
        'right_operand': ''
    }
    # the return variable we will be using for the result of the parsing
    found_data = []
    # semaphore variable for the amount of " found in the third event
    right_operand_comp = 0
    # iterate oveer the whole string character by character appending the findings to the correct one

    for index in range(len(whole_string)):
        # detect for which string the current char is for
        if model_parsed_string['left_operand'] != 'COMPLETE':
            # the found whole_string[index] may be for this tier or the next one
            if whole_string[index] != '=':
                # append to the 2
                p_string['left_operand'] += whole_string[index]
                
            elif whole_string[index] == '=':
                # append whole_string[index] to the 2
                p_string['operation'] += whole_string[index]
                model_parsed_string['left_operand'] = 'COMPLETE'
                model_parsed_string['operation'] = 'COMPLETE'

        if model_parsed_string['operation'] != 'COMPLETE':
            # non complete operation find out if this value is the sign
            # if whole_string[index] != '=':
            #     # append to the 3
            #     p_string['right_operand'] += whole_string[index]
            if whole_string[index] == '=':
                # append to 2
                p_string['operation'] += whole_string[index]
                model_parsed_string['operation'] = 'COMPLETE'
        
        if model_parsed_string['right_operand'] != 'COMPLETE' and model_parsed_string['operation'] == 'COMPLETE' and model_parsed_string['left_operand'] == 'COMPLETE':
            # append to the 3 until whole_string[index] is .
            if whole_string[index] == '"':
                if right_operand_comp == 0:
                    right_operand_comp = 1
                else:
                    right_operand_comp = 0
                # also append to 3
            elif whole_string[index] != '=':
                p_string['right_operand'] += whole_string[index]
            if whole_string[index] == '.' and right_operand_comp == 0:
                if whole_string[index+1] == '.' or whole_string[index-1] == '.':
                    continue
                else:
                    # DEBUG
                    # remove the last value from the composition as it is a dot (.)
                    p_string['right_operand'] = p_string['right_operand'][:-1]
                    found_data.append(p_string)
                    p_string = {
                        'left_operand': '',
                        'operation': '',
                        'right_operand': ''
                    }
                    model_parsed_string = {
                        'left_operand': '',
                        'operation': '',
                        'right_operand': ''
                    }
                    right_operand_comp = 0
                    # DO NOT APPEND AND START OVER
    return found_data


def filter_right(array_p):
    result = []
    array_of_paramenters = copy.deepcopy(array_p)
    for index in range(len(array_of_paramenters)):
        # we know the structure of the document int he array so we clean
        a = str(array_of_paramenters[index]['right_operand']).replace('\n','')
        b = str(array_of_paramenters[index]['left_operand']).replace('\n','')
        c = str(array_of_paramenters[index]['operation']).replace('\n','')

        a = a.replace(' ','')
        b = b.replace(' ','')
        c = c.replace(' ','')

        result.append({
            'left_operand': b,
            'operation': c,
            'right_operand': a
        })

    return result


def tform_op_DFA_ready(array_of_characters, index):
    object_transformed = array_of_characters[index]

    right_op  = object_transformed['right_operand']
    # array of operations found and tformed
    result_array = []
    array_index = 0
    quotations_found = 0

    # get the left operands as NFA that dont need parsing
    left_ops = []
    for i in range(len(array_of_characters)):
        left = array_of_characters[i]['left_operand']
        left_ops.append(left)

    # split the operands using the '+'
    # result_array = right_op.split('+')
    result_array.append('')
    for value in right_op:
        if value == chr(34) or value == chr(39):
            quotations_found += 1
            if quotations_found == 2:
                # reset the value of the quotations found 
                quotations_found = 0
        elif value == '+' and quotations_found == 0:
            # found + and it is not inside the string so we use it to separate the values
            array_index += 1
            result_array.append('')
        elif value == '-' and quotations_found == 0:
            # also a separator
            array_index += 1
            result_array.append('')
        else:
            result_array[array_index] += value
    

    for parsed_value_index in range(len(result_array)):
        # contains CHR
        if 'CHR' in result_array[parsed_value_index]:
            # remove the CHR and the '(' and the ')'
            value = result_array[parsed_value_index].replace('CHR', '')
            value = value.replace('(', '')
            value = value.replace(')', '')

            # transform the found integer into ar ordinal value
            result_array[parsed_value_index] = chr(int(value))
            result_array[parsed_value_index] += '|'
            result_array[parsed_value_index] += chr(int(value))

        # contains '..'
        elif '..' in result_array[parsed_value_index]:
            # split the string into two segments and transform each one into ord
            temp_string = result_array[parsed_value_index].split('..')
            a_value = ord(temp_string[0])
            b_value = ord(temp_string[1])

            complete_string = chr(a_value)

            # iterate until all values between are met
            while a_value < b_value:
                a_value += 1
                complete_string += '|'
                complete_string += chr(a_value)
            
            result_array[parsed_value_index] = complete_string

        elif result_array[parsed_value_index] in left_ops:
            continue

        elif len(result_array[parsed_value_index]) == 1 and result_array[parsed_value_index] not in left_ops and len(result_array) == 1:
            # only a single digit in the mix
            complete_string = result_array[parsed_value_index]
            complete_string += '|'
            # append
            complete_string += result_array[parsed_value_index]

            result_array[parsed_value_index] = complete_string

        else:
            complete_string = ''
            for value in result_array[parsed_value_index]:
                if len(complete_string) == 0:
                    # append
                    complete_string += value
                else:
                    # add separator
                    complete_string += '|'
                    # append
                    complete_string += value

            result_array[parsed_value_index] = complete_string
            
    # try and fit a model based on the values found in the right op
    return result_array

def tform_op_DFA_ready_keywords(array_of_characters, index):
    object_transformed = array_of_characters[index]

    right_op  = object_transformed['right_operand']
    # array of operations found and tformed
    result_array = []
    array_index = 0
    quotations_found = 0

    # get the left operands as NFA that dont need parsing
    left_ops = []
    for i in range(len(array_of_characters)):
        left = array_of_characters[i]['left_operand']
        left_ops.append(left)

    # split the operands using the '+'
    # result_array = right_op.split('+')
    result_array.append('')
    for value in right_op:
        if value == chr(34) or value == chr(39):
            quotations_found += 1
            if quotations_found == 2:
                # reset the value of the quotations found 
                quotations_found = 0
        elif value == '+' and quotations_found == 0:
            # found + and it is not inside the string so we use it to separate the values
            array_index += 1
            result_array.append('')
        elif value == '-' and quotations_found == 0:
            # also a separator
            array_index += 1
            result_array.append('')
        else:
            result_array[array_index] += value
    

    for parsed_value_index in range(len(result_array)):
        # contains CHR
        complete_string = ''
        for value in result_array[parsed_value_index]:
            if len(complete_string) == 0:
                # append
                complete_string += value
            else:
                # add separator
                complete_string += ' '
                # append
                complete_string += value

        result_array[parsed_value_index] = complete_string
            
    # try and fit a model based on the values found in the right op
    return result_array


def make_tokens_statement(array_of_tokens, a_char, a_key):

    # generate a newdict with characters and keywords values
    words_database = {}
    words_database.update(a_char)
    words_database.update(a_key)

    operands = ' |*+?'
    # dictionary with the result of the reg expression
    token_result = {}

    # make a copy of array of 
    a_tokens = copy.deepcopy(array_of_tokens)

    # iterate over a tokens
    for i in range(len(array_of_tokens)):
        right_op = array_of_tokens[i]['right_operand']
        left_op = array_of_tokens[i]['left_operand']

        # search and replace the opening { 
        right_op = right_op.replace('{', ' (')
        # search and replace the ending }
        right_op = right_op.replace('}', ')* ')

        # NOT PARSING EXCEPT RIGHT NOW
        # FIXME
        right_op = right_op.split('EXCEPT', 1)[0]

        # FIXME: DOT VALUE IN DOUBLE ARITMETICA

        # find in keywords and in characters if 
        
        for registered_value in words_database:
            # search if it exists in the right op
            right_op = right_op.replace(registered_value, words_database[registered_value])

        # remove the last value in case it is a space
        if right_op[-1] == ' ':
            right_op = right_op[:-1]

        # append the value generated at right op into the dictionary of results
        token_result[left_op] = right_op
    
    return token_result


def return_all_ops_DFA(array_of_characters):
    array_of_characters_copy = copy.deepcopy(array_of_characters)

    for i in range(len(array_of_characters)):
        array_of_characters_copy[i]['right_operand'] = tform_op_DFA_ready(array_of_characters, i)
    
    return array_of_characters_copy

def return_all_ops_DFA_kwords(array_of_keywords):
    array_of_keywords_copy = copy.deepcopy(array_of_keywords)

    for i in range(len(array_of_keywords)):
        array_of_keywords_copy[i]['right_operand'] = tform_op_DFA_ready_keywords(array_of_keywords, i)

    return array_of_keywords_copy


def simplify_characters(array_of_chars):
    complete_characters = {}

    for index in range(len(array_of_chars)):
        op_dict = array_of_chars[index]
        if len(op_dict['right_operand']) == 1:
            # only a single op in the array
            complete_characters[op_dict['left_operand']] = op_dict['right_operand'][0]
        else:
            # generate the new substring based on the other characters
            substring = ''
            for right_operand in op_dict['right_operand']:
                # check if value exists in complete characters
                if right_operand in complete_characters:
                    if substring == '':
                        substring = complete_characters[right_operand]
                    else:
                        substring += '|'
                        substring += complete_characters[right_operand]
                else:
                    if substring == '':
                        substring = right_operand
                    else:
                        substring += '|'
                        substring += right_operand
            # append the substring as normal
            complete_characters[op_dict['left_operand']] = substring

    return complete_characters