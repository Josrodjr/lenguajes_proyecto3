import sys
import pickle

# import the DFA emulator
sys.path.append("..")
from automata_builder.libs.tform import emulate_DFA


INPUT_FILE = 'production'

# if len(sys.argv) != 2:
#     sys.exit()

# try:
#     INPUT_FILE = sys.argv[1]
# except:
#     print("No args found")

# pickle_in = open(INPUT_FILE+".pickle","rb")
pickle_in = open("production.pickle","rb")
token_dfas = pickle.load(pickle_in)

# print results
# print(token_dfas)

# open the token test file that you may feed using args in future
# FIXME

# read the data in input files
input_file= open("tokentests.txt", "r")

parsed_input = ''
for line in input_file:
    parsed_input += line

print(parsed_input)


def emulate_all_DFA(text_string):
    found_completion = 0
    for token_name in token_dfas:
        a = token_dfas[token_name]['startend']
        b = token_dfas[token_name]['dfa_transitions']
        result = emulate_DFA(a, b, text_string)
        if result == 1:
            # found
            found_completion = token_name
    return found_completion

def scan(input_string):
    last_complete_state = 0
    maximum_len = len(input_string)
    tokens_array = []

    for character in range(len(input_string)):

        # test if character is complete in any automata in the token DFA's that we have
        test_completion_string = ''
        j = last_complete_state
        while j <= character:
            test_completion_string += input_string[j]
            j += 1

        # check for completion in dfas
        token_name = emulate_all_DFA(test_completion_string)

        # test next one if possible
        if character < maximum_len-1:
            # test if both characters together is complete in automatas
            # generate a substring based on last complete value

            test_completion_string = ''

            i = last_complete_state
            while i <= character+1:
                test_completion_string += input_string[i]
                i +=1

            # print(test_completion_string)
            
            completion = emulate_all_DFA(test_completion_string)
            # check for completion in dfas
            if completion != 0:
                # the next value is complete in the dfa so we continue
                continue
            else:
                if token_name == 0 and completion == 0:
                    # none of the values are useful to the grammar move on
                    last_complete_state = character
                elif token_name != 0 and completion == 0:
                    tokens_array.append([test_completion_string[:-1], token_name])
                    last_complete_state = character
                else:
                    # current value is the last value that makes complete a dfa and next doesnt satisfy
                    # append the test completion string and the token it found into the array
                    tokens_array.append([test_completion_string[:-1], token_name])
                    # reset the index for search of next token
                    last_complete_state = character


        else:
            # THERE IS NO NEXT ONE
            if token_name != 0:
                # append the test completion string and the token it found into the array
                tokens_array.append([test_completion_string, token_name])
                # reset the index for search of next token
                last_complete_state = character
    return(tokens_array)

a = scan(parsed_input)
print(a)        
