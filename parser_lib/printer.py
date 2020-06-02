
# NOT IN USE FOR NOW
#  output = open("./outputs/" + name + ".py", "w+")
#     output.write("#file to test\n\n")
#     #output.write("from libs import evaluate\n")
#     output.write("import collections\n")
#     output.write("EPSILON = 'ε'\n")


def print_parser_header(parser_name):
    # open the file we will create the parser in
    output = open("./generated/" + parser_name + ".py", "w+")

    # print the header files necesary for the parser class
    output.write("#parser for " + str(parser_name) + " grammar\n\n")
    # class declaration
    output.write("class Parser:\n\n")
    output.write("\tt, la = 0, 0\n")

    # init method
    output.write("\tdef __init__(self):\n")
    output.write("\t\tself.t = 1\n")
    output.write("\t\tself.la = 2\n")

    # end with a newline
    output.write("\n")

    # test the class
    # output.write("parser_declr = Parser()\n")
    # output.write("print(parser_declr.t)\n")

def print_parser_method(parser_name, production_obj):
    method_name = production_obj['name']
    method_lines_arr = production_obj['fragments']
    # open the file
    output = open("./generated/" + parser_name + ".py", "a+")
    # declare the CURRENT LEVEL of the method inside de class
    cl = "\t"
    cl_index = 1

    # generate the method name in the class
    output.write(cl+"def "+method_name+"(self):\n")

    cl_index += 1
    
    # do either a python, terminals, production, if, while
    for fragment in method_lines_arr:
        fragment_type = fragment['type']
        fragment_text = fragment['text']

        if fragment_type == 'python':
            # get the python substring for the method
            python_ready = fragment_text[2:-2]
            # print to the 
            output.write(cl*cl_index+python_ready+"\n")

        if fragment_type == 'terminals':
            # inside here there may be terminals o non terminals alike
            # get python substring of the fragment
            terminals = fragment_text[1:-1]
            # divide the terminals by |
            terminals_arr = terminals.split("|")

            if len(terminals_arr) == 1:
                t1 = terminals_arr[0].strip()
                if "<" in t1:
                    head = t1.split("<")
                    # Found nonterminal as a function
                    output.write(cl*cl_index+"if "+ "self.t.kind == self."+head[0]+"(self):"+"\n")
                    output.write(cl*(cl_index+1)+"result = self.t"+"\n")
                else:
                    # Found terminal
                    output.write(cl*cl_index+"if "+ "self.t.kind == self.Scanner."+t1+":\n")
                    output.write(cl*(cl_index+1)+"result = self.t"+"\n")

            else:
                # iterate over all terminals arr
                for t in terminals_arr:
                    # filter
                    t1 = t.strip()
                    # find if its a terminal or a nonterminal
                    if "<" in t1:
                        # Found a nonterminal call it as a function
                        head = t1.split("<")
                        # Found nonterminal as a function
                        output.write(cl*cl_index+"result = self."+head[0]+"(self):"+"\n")
                    # insert into the function
                    else:
                        # Found terminal
                        output.write(cl*cl_index+"if "+ "self.t.kind == self.Scanner."+t1+":\n")
                        output.write(cl*(cl_index+1)+"result = self.t"+"\n")
                


    # test innards
    # output.write(cl*2+"self.t += 1\n")
    
    # end with a newline
    output.write("\n")


def test_method(parser_name, method_name):
    # open the file
    output = open("./generated/" + parser_name + ".py", "a+")

    # test the class
    output.write("parser_declr = Parser()\n")
    # output.write("print(parser_declr.t)\n")
    output.write("parser_declr."+method_name+"()\n")
    # output.write("print(parser_declr.t)\n")



