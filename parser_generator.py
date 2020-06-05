# generate a parser class with attributed grammar from the ARITMETICA cocoR provided
# Jose R. Perez
# UVG 2020

# import libraries 
import sys
# local libs
import parser_lib.modules as mod
import parser_lib.printer as prt
# load the file we will generate the parser from

INPUT_FILE = ''

if len(sys.argv) != 2:
    sys.exit()

try:
    INPUT_FILE = sys.argv[1]
except:
    print("Input Grammar not found\n")

# read the data in input files
input_file= open("input_python/" + INPUT_FILE, "r")

productions = mod.get_productions_str(input_file)

productions_array = mod.parse_productions(productions)


productions_array = mod.filter_right(productions_array)

fragment_grammar = mod.fragment_productions(productions_array)   

# start the header
prt.print_parser_header(INPUT_FILE[:-4]+"_parser")


for obj in fragment_grammar:
    # print("\n", obj)
    # call the method for function creation in the parser
    prt.print_parser_method(INPUT_FILE[:-4]+"_parser", obj)     

# mod.first(fragment_grammar)