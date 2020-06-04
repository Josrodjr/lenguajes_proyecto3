
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
    output.write("\tclass Token(object):\n")
    output.write("\t\tkind = 0\n")
    output.write("\t\tval = 0\n")
    output.write("\n")
    
    output.write("\tt = Token()\n")
    output.write("\tla = Token()\n")
    output.write("\n")

    # init method
    output.write("\tdef __init__(self):\n")
    # output.write("\t\tself.t = 1\n")
    # output.write("\t\tself.la = 2\n")
    output.write("\t\tsetattr(self.t, 'val', 'kind' )\n")
    output.write("\t\tsetattr(self.la, 'val', 'kind' )\n")

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
                    output.write(cl*cl_index+"if "+ "self.t.kind == self."+head[0]+"():"+"\n")
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
                        output.write(cl*cl_index+"if self.la in self.first('"+head[0]+"'):"+"\n")
                        output.write(cl*(cl_index+1)+"result = self."+head[0]+"()"+"\n")
                    # insert into the function
                    else:
                        # Found terminal
                        output.write(cl*cl_index+"if "+ "self.la.kind == self.Scanner."+t1+":\n")
                        output.write(cl*(cl_index+1)+"result = self.la"+"\n")

        if fragment_type == 'production':
            # split if there are multiple productions inside the 
            productions_arr = fragment_text.split("|")
            for production in productions_arr:
                clean_production = production.split("<")[0]
                # output.write(cl*cl_index+"if self.t in self.first("+clean_production+"):"+"\n")
                output.write(cl*(cl_index)+"result = self."+clean_production+"()"+"\n")

        if fragment_type == 'if':
            # remove the ends
            if_statement = fragment_text[1:-1]
            # divide the terminals by |
            if_statement = if_statement.split("|")
            # iterate over the if statements found
            for ifs in if_statement:
                # get the first part of the statement
                quotes_counter = 2
                condition = ''
                python_text = ''
                for char in ifs:
                    if quotes_counter != 0:
                        condition += char
                    else:
                        python_text += char
                    if char == '"':
                        quotes_counter -= 1
                # now we clean the condition
                condition = condition[1:-1]
                # clean the python text for print into the file
                python_text = python_text[2:-2]
                # print to file
                output.write(cl*cl_index+"if "+ "self.t.val == '"+condition+"':\n")
                output.write(cl*(cl_index+1)+python_text+"\n")

        if fragment_type == 'while':
            # remove the ends
            while_statement = fragment_text[1:-1]
            # divide the terminals by |
            while_statement = while_statement.split("|")
            # iterate over the if statements found
            for stmt in while_statement:

                # if it has a production
                if '<' in stmt: 

                    # get the first part of the statement
                    quotes_counter = 2
                    condition = ''
                    rest_of_while = ''
                    for char in stmt:
                        if quotes_counter != 0:
                            condition += char
                        else:
                            rest_of_while += char
                        if char == '"':
                            quotes_counter -= 1
                    # clean the condition
                    condition = condition.strip()
                    # clean the first part that is the nonterminal that will be checked
                    le_check = 0
                    ge_check = 0
                    terminal = ''
                    lege_stmt = ''
                    for char in rest_of_while:
                        if char == '<':
                            le_check = 1
                        if char == '>':
                            ge_check = 1
                        if le_check != 1 and ge_check != 1:
                            terminal += char
                        else:
                            lege_stmt += char
                    
                    flag = 0
                    lege = ''
                    python = ''
                    for char in lege_stmt:
                        if char == '(':
                            flag = 1
                        if flag == 0:
                            lege += char
                        else:
                            python += char

                    # clean the lege just for the important values
                    stored_value = lege[4:-1].strip()
                    # clean the condition
                    condition = condition[1:-1]
                    # clean python
                    python = python.strip()
                    python = python[2:-2]

                    # do the while in the file giggity
                    output.write(cl*cl_index+"while "+ "self.t.val == '"+condition+"':\n")
                    output.write(cl*(cl_index+1)+stored_value+" = self."+terminal+"()"+"\n")
                    output.write(cl*(cl_index+1)+python+"\n")

    
                # maybe init of grammar
                else:
                    output.write(cl*cl_index+"if self.la in self.first('"+stmt+"'):"+"\n")
                    output.write(cl*(cl_index+1)+"result = self."+stmt+"()"+"\n")

        
    # default return of result
    output.write(cl*cl_index+"return result"+"\n")
    #
    # end in newline
    output.write("\n")


def test_method(parser_name, method_name):
    # open the file
    output = open("./generated/" + parser_name + ".py", "a+")

    # test the class
    output.write("parser_declr = Parser()\n")
    # output.write("print(parser_declr.t)\n")
    output.write("parser_declr."+method_name+"()\n")
    # output.write("print(parser_declr.t)\n")



