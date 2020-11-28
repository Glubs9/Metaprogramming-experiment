#interpreter is simple so i just put it into one file
#TODO:
    #add support for trailing whitespace
    #add support for better output
        #just printing the stack everytime isn't efficient or beuaitufl
    #add support for repl
        #not high priortiy
    #add support for loading files
    #add support for more boolean operators and test turing completeness
    #add support for comments after definitions
    #add support for multiline definitions
    #potentially think about reversing the way that the stack is made
    #refactor code to be more modular
    #so exec seems to be called every single time except for the last operator
        # i think i might have to go the option of having the variables be separate blocks within
        # themselves
    #honestly i don't even know about this whole callstack thing

import sys

def lex(string):
    definitions = string.split("\n")
    clean_definitions = [n for n in definitions if n != "" and n[0] != "#"] #comments done here even though they shouldn't be
    tokens = [n.split(" ") for n in clean_definitions]
    return tokens

#when a variable called in the runner it has to append to the stack all of the tokens
#(recommended to read this after run)
def make_func(arr):
    def ret(stack, functions):
        nonlocal arr
        #i have to add to the stack one by one to make the exec function work
        #i might be able to find these values when the function gets created
        for n in arr:
            if n == "exec": stack = exec_func(stack[-1], functions, stack[:-1]) #exec func executes a function
            else: stack += [n]
            #need to test for function arity
            #i might have to move run stack into a separate function and call it from here
        return stack
    return ret

def parse(tokens):
    ret_dict = {}
    for n in tokens:
        if n[0] in ret_dict: raise Exception("ERROR Variable " + n[0] + " defined twice")
        ret_dict[n[0]] = make_func(n[1:])
    return ret_dict

#used in predefined functions, only exists like this due to raise not being allowed in lambdas 
def end(_, __):
    raise Exception("unexpected call to end")

#these are heavily influenced by the forth axiomatic functions. note: these might be able to simplified down or re-implemented in the stdlib
#there is an extra function that doesn't exist here which is the exec function which is handled in
#make_func. this artificially calls a function early
predefined_functions = {
        "nop": lambda stack, _: stack, 
        "end": end,
        "dup": lambda stack, _: stack + [stack[-1]],
        "pop": lambda stack, _: stack[:-1],
        "swap": lambda stack, _: stack[:-2] + [stack[-1], stack[-2]],
        "over": lambda stack, _: stack + [stack[-2]],
        "rot": lambda stack, _: stack[:-3] + stack[-2:] + [stack[-3]]
}

#used for halting program with values on the stack
    #this might not be necersarry for turing completeness but it's a quality of life thing
axiom_function_arity = {
        "nop": 0,
        "end": 0,
        "dup": 1,
        "pop": 1,
        "swap": 2,
        "over": 2,
        "rot": 3
}

def exec_func(string, functions, stack):
    if string not in functions:
        raise Exception("call to undefined function " + string)
    return functions[string](stack, functions)

def run(variables):
    all_functions = predefined_functions|variables #python3.9 only, change to next line for previous version support
    #all_functions = dict(predefined_functions, **variables) #although this has not been tested
    stack = ["main"]
    #finished when end called or when there aren't enough arguments on the stack to call an axiomatic funtion
        #i don't think this can be extended to user defined variables/functions because that might be the halting problem
    #exit condition of len(stack) == 1 might not work
    while stack[-1] != "end" and not (stack[0] != "main" and len(stack) == 1) and not (stack[-1] in axiom_function_arity and len(stack) - 1 < axiom_function_arity[stack[-1]]):
        head = stack.pop()
        if head not in all_functions:
            raise Exception("call to undefined function " + head)
        stack = exec_func(head, all_functions, stack)
        print(stack)
    return stack

def add_to_scope(variables):
    global predefined_functions
    predefined_functions |= variables

def run_str(string, load_flag):
    variables = parse(lex(string))
    return add_to_scope(variables) if load_flag else run(variables)

#load flag doesn't run file
def load_and_run(file_name, load_flag=False):
    f = open(file_name, "r")
    run_str(f.read(), load_flag)
    f.close()

#loads and runs the stdlib (note I don't actually need to run the code I only need to add the ast to
#the function/variable dictionary
load_and_run("stdlib.st", True) #load flag doesn't run file
#runs the supplied file
#check for non supplied argument to start repl
load_and_run(sys.argv[1])
