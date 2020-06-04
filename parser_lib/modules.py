# python library for operations for the parser generator
import copy

def str_translation(input_file):
    str_value = ''

    for line in input_file:
        str_value += line
    
    return str_value

def delta_finder(grammar_str, start_search, end_search):
    start = grammar_str.find(start_search) + len(start_search)
    end = grammar_str.find(end_search)
    return grammar_str[start:end]

def get_productions_str(input_file):
    grammar_str = str_translation(input_file)
    pair = ['PRODUCTIONS', 'END']
    return delta_finder(grammar_str, pair[0], pair[1])

# parsing the productions part
def parse_productions(whole_string):
    # conditions
    # 1) production ends with . ONLY when not inside of ( or )
    # 2) left side is always what comes before the first = sign found
    
    # flags for left center and right side of productions
    flags = [0,0,0]
    in_par_flag = 0
    # dict for each production
    model_prod = {
        'l': '',
        'op': '',
        'r': ''
    }
    findings = []
    # iterate over the whole string
    for index in range(len(whole_string)):
        if flags[0] != 1:
            if whole_string[index] == '=':
                # change flags
                flags[0] = 1
                flags[1] = 1
                model_prod['op'] += whole_string[index]
            else:
                model_prod['l'] += whole_string[index]

        if flags[2] != 1 and flags[0] == 1:
            # check if its (
            if whole_string[index] == '(':
                in_par_flag += 1
            if whole_string[index] == ')':
                in_par_flag -= 1
            
            # check if inside parenthesis
            if whole_string[index] == '.' and in_par_flag == 0:
                flags[2] = 1
                # TODO: EXIT
                findings.append(model_prod)
                # reset the variables
                flags = [0,0,0]
                in_par_flag = 0
                model_prod = {
                    'l': '',
                    'op': '',
                    'r': ''
                }
            else:
                model_prod['r'] += whole_string[index]
    
    return findings


def filter_right(array_p):
    result = []
    array_of_paramenters = copy.deepcopy(array_p)
    for index in range(len(array_of_paramenters)):
        # we know the structure of the document int he array so we clean
        a = str(array_of_paramenters[index]['r']).replace('\n','')
        b = str(array_of_paramenters[index]['l']).replace('\n','')
        c = str(array_of_paramenters[index]['op']).replace('\n','')

        a = a.replace('\t','')
        b = b.replace('\t','')
        c = c.replace('\t','')

        # a = a.replace(' ','')
        # b = b.replace(' ','')
        c = c.replace(' ','')

        # remove the first value of right side as it is a equal sign
        a = a[1:]

        result.append({
            'l': b,
            'op': c,
            'r': a
        })

    return result

def fragment_productions(productions_array):
    # object we return after loops
    whole_productions_parsed = []

    # iterate over every production on the array backwards
    for item in productions_array[::-1]:
        
        # get the name of the production for name of the function
        name = item['l'].split('<')[0]
        
        # iterate over the right side until somethin other than a space is found
        obj_prod = []
        # object fragment
        frag = {
            'type': '',
            'text': ''
        }
        for index in range(len(item['r'])):
            l = item['r'][index]
            if index+1 in range(len(item['r'])):
                la = item['r'][index+1]
            else:
                la = None

            # always append the current index value
            frag['text'] += l

            # special case found a production before
            if la != None:
                if len(frag['text']) != 0 and la in "{[(":
                    # fragment type other production
                    if frag['type'] == '':
                        frag['type'] = 'production'

                        obj_prod.append(frag)
                        # reset frag
                        frag = {
                            'type': '',
                            'text': ''
                        }
            
            if l == '(' and la == '.':
                # fragment type python raw text
                # change only if frag type is empty
                if frag['type'] == '':
                    frag['type'] = 'python'

            if l == '(' and la != '.':
                # fragment type terminals
                # change only if frag type is empty
                if frag['type'] == '':
                    frag['type'] = 'terminals'
            
            if l == '[':
                # fragment type conditional
                # change only if frag type is empty
                if frag['type'] == '':
                    frag['type'] = 'if'
            
            if l == '{':
                # fragment type loop
                # change only if frag type is empty
                if frag['type'] == '':
                    frag['type'] = 'while'


            # finished with naming possibilities of starts we search for an end
            if l == ')' and frag['text'].endswith('.)'):
                if frag['type'] == 'python':
                    obj_prod.append(frag)
                    # reset frag
                    frag = {
                        'type': '',
                        'text': ''
                    }

            if l == ')' and not frag['text'].endswith('.)'):
                if frag['type'] == 'terminals':
                    obj_prod.append(frag)
                    # reset frag
                    frag = {
                        'type': '',
                        'text': ''
                    }

            if l == '}':
                if frag['type'] == 'while':
                    obj_prod.append(frag)
                    # reset frag
                    frag = {
                        'type': '',
                        'text': ''
                    }
            
            if l == ']':
                if frag['type'] == 'if':
                    obj_prod.append(frag)
                    # reset frag
                    frag = {
                        'type': '',
                        'text': ''
                    }
        

        # eliminate all productions with empty values
        for value in obj_prod:
            if value['text'] == ' ':
                obj_prod.remove(value)
        
        produc_parsed = {
            'name': name,
            'fragments': obj_prod
        }
        
        whole_productions_parsed.append(produc_parsed)
    
    return whole_productions_parsed



def first(grammar_arr):
    # do a copy for operations
    gmr = copy.deepcopy(grammar_arr)
    # ok we have the grammar parsed and ordered bottom up in the array
    first = []
    # the composition of the first and follow will be as follows
    grammar_obj = {
        'NAME': '',
        'FIRST': set(),
        'FOLLOW': set()
    }
    # FIRST OPERATION REMOVE ALL THE RAW PYTHON CODE
    for obj in gmr:
        remove = []
        for index in range(len(obj['fragments'])):
            if obj['fragments'][index]['type'] == 'python':
                remove.append(index)
        # iterate over the index backwards
        for item in remove[::-1]:
            obj['fragments'].pop(item)
        # empty remove
        remove = []

    # they come here ordered
    for obj in gmr:
        # add the name
        grammar_obj['NAME'] = obj['name']
        
        # add it to the array
        first.append(grammar_obj)
        # reset the values
        grammar_obj = {
            'NAME': '',
            'FIRST': set(),
            'FOLLOW': set()
        }

    # get all the non terminals for later
    n_t = []
    for j in range(len(first)):
        n_t.append(first[j]['NAME'])
   
    
    # iterate over the array of grammar now adding the first data
    for obj in gmr:
        current_production = obj['name']

        # iterate over the possible symbols of grammar
        for fragment in obj['fragments']:
            # the ez part terminals without <{( in values
            if not '<' in fragment['text'] and fragment['type'] == 'terminals':
                # remove the first and last parenthesis
                terminals = fragment['text'][1:-1]
                # do a subdivision via | for all the terminals
                terminals = terminals.split('|')
                # for each one of the terminals do
                for each_terminal in terminals:
                    # append to the first of the current production
                    for index in range(len(first)):
                        if first[index]['NAME'] == current_production:
                            first[index]['FIRST'].add(each_terminal.strip())
            
            if '<' in fragment['text'] and fragment['type'] == 'terminals':
                # remove the first and last parenthesis
                terminals = fragment['text'][1:-1]
                # do a subdivision via | for all the terminals
                terminals = terminals.split('|')
                # now we must clean each one of the terminals based on the < value
                for poss_terminal in terminals:
                    # split by the < symbol
                    a = poss_terminal.split('<')
                    # only care about the first part of the split
                    a = a[0].strip()
                    # figure out if its a production or a terminal
                    if a in n_t:
                        # iterate over all fists and make union
                        for index in range(len(first)):
                            if first[index]['NAME'] == current_production:
                                # search for non terminal first
                                for j in range(len(first)):
                                    if first[j]['NAME'] == a:
                                        f_value = first[j]['FIRST']

                                # union of the first of the nonterminal with the currentproduction set
                                first[index]['FIRST'] = first[index]['FIRST'].union(f_value)
                    else:
                        # not a nonterminal so we only add it to the set
                        for index in range(len(first)):
                            if first[index]['NAME'] == current_production:
                                first[index]['FIRST'].add(a.strip())
            

    print(first)

