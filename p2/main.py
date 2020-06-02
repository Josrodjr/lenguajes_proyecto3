import sys
import pickle
import copy

# imports of local created libs
from useful.reader import parse_findings_plus, filter_right, tform_op_DFA_ready, return_all_ops_DFA,  return_all_ops_DFA_kwords, simplify_characters
from useful.reader import make_tokens_statement


# DFA managements
from automata_builder.export import generate_DFA


# graficadora
from automata_builder.libs.grafo import graficadora

INPUT_FILE = ''
OUTPUT_NAME = ''
MARKERS = {
    'COMPILER': '',
    'CHARACTERS': '',
    'KEYWORDS': '',
    'TOKENS': '',
    'PRODUCTIONS': ''
}

if len(sys.argv) != 3:
    sys.exit()

try:
    INPUT_FILE = sys.argv[1]
    OUTPUT_NAME = sys.argv[2]
except:
    print("No args found")

# read the data in input files
input_file= open("input/" + INPUT_FILE, "r")

def str_translation():
    str_value = ''

    for line in input_file:
        str_value += line
    
    return str_value

def delta_finder(start_search, end_search):
    start = input_file.find(start_search) + len(start_search)
    end = input_file.find(end_search)
    return input_file[start:end]


def fill_markers():
    pairs = [['COMPILER', 'CHARACTERS'], ['CHARACTERS', 'KEYWORDS'], ['KEYWORDS', 'TOKENS'], ['TOKENS', 'PRODUCTIONS'], ['PRODUCTIONS', 'END']]
    for pair in pairs:
        MARKERS[pair[0]] = delta_finder(pair[0], pair[1])


# parse the input found in the input files into segments
input_file = str_translation()

# delimitate the segments found via enters and parse each based on criteria
fill_markers()


# perform a split of the values found in the character split
array_of_characters = parse_findings_plus(MARKERS['CHARACTERS'])
# perform a spit of the values found inthe keywords
array_of_keywords = parse_findings_plus(MARKERS['KEYWORDS'])
# perform the split of values found in the tokens 
array_of_tokens = parse_findings_plus(MARKERS['TOKENS'])

            
# filter the operands
array_of_characters = filter_right(array_of_characters)
array_of_keywords = filter_right(array_of_keywords)
array_of_tokens = filter_right(array_of_tokens)

# perform changes in all right operands so they are ready for DFA
array_of_characters = return_all_ops_DFA(array_of_characters)
array_of_keywords = return_all_ops_DFA_kwords(array_of_keywords)

# tranform the array into a DFA approach

array_of_characters = simplify_characters(array_of_characters)
array_of_keywords = simplify_characters(array_of_keywords)

# After build in transform on characters and keywords we need to transform the tokens into a DFA type
array_of_tokens = make_tokens_statement(array_of_tokens, array_of_characters, array_of_keywords)

# Store the values to the parsed format
MARKERS['CHARACTERS'] = array_of_characters
MARKERS['KEYWORDS'] = array_of_keywords
MARKERS['TOKENS'] = array_of_tokens

# print(MARKERS['CHARACTERS'])
# print(MARKERS['KEYWORDS'])
# print(MARKERS['TOKENS'])

# try to generate a dfa

# graficadora(trans['dfa_transitions'], trans['startend'])

print("comenzo")

# trans = generate_DFA('letter (letter|digit)*')
trans = generate_DFA('A|B|C|D|E|F|G|H|I|J|K|L|M|N|O|P|Q|R|S|T|U|V|W|X|Y|Z|a|b|c|d|e|f|g|h|i|j|k|l|m|n|o|p|q|r|s|t|u|v|w|x|y|z (A|B|C|D|E|F|G|H|I|J|K|L|M|N|O|P|Q|R|S|T|U|V|W|X|Y|Z|a|b|c|d|e|f|g|h|i|j|k|l|m|n|o|p|q|r|s|t|u|v|w|x|y|z|0|1|2|3|4|5|6|7|8|9)*')
graficadora(trans['dfa_transitions'], trans['startend'])


print("funciono")

print(MARKERS['TOKENS']['ident'])


for token in MARKERS['TOKENS']:
    copy_of_regex = copy.deepcopy(MARKERS['TOKENS'][token])
    dfa_generated = generate_DFA(copy_of_regex)
    MARKERS['TOKENS'][token] = dfa_generated


# graficadora(MARKERS['TOKENS']['number']['dfa_transitions'], MARKERS['TOKENS']['number']['startend'])

# pickle the results for the scanner
# pickle_out = open( "output/"+OUTPUT_NAME+".pickle","wb")
pickle_out = open( "output/production.pickle","wb")
pickle.dump(MARKERS['TOKENS'], pickle_out)


pickle_out.close()

