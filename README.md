# Metaprogramming-experiment
a simple experiment to test the turing completeness of a 'pure' metaprogramming language.

# Motivation
I wanted to test if I could write a simple programming language
where there is no separation between data and code (akin to lisp except more extreme).
The idea behind this is I wanted to get a better understanding of metaprogramming and to test an idea i've had.
The idea I had was that in a programming language there is always going to be some separation between code and data, specifically such that the meta-code will be separate from normal code and normal data (I am still in the process of learning lisp so it might do this but I doubt it works to such a degree as this language). 

# notes before starting
This is in no means a conclusive test. I just did it for the fun of it. I also am bad at writing. The documentation in the files is spares and not descriptive, which I may change later but probably not. I also never decided whether to call the things in my language variables or functions (and sometimes methods) so I used these terms interchangeably. 

# Language Design
This language is a stack-oriented language where the stack manipulated is the call stack, it could also be thought of as a limited rewriting language using a call stack as it's state.                            
A file is defiend as a series of variable definitions where each line starts with the name of the variable and after the variable is what will be added to the call stack when the variable is called.                         
The call stack is initally set to only have the main variable/function on the stack.                      
Execution takes the head of the stack, pops it and executes it. If the function is predefined in the interpreter then it will execute that function, i.e: dup duplicates the top of the stack. If the variables/function is defined by the user it will push the values given by the user onto the stack. e.g if there is a line in the code that reads "triple dup dup" and triple gets called it will push onto the stack dup dup (note: triple will not triple the top of the stack for reasons discussed later). 

# why this language failed and what it means about metaprogramming (to me at least)
If we go back to the triple example from earlier. "triple dup dup" the program will run as follows (the stack gets printed every iteration).                       
\[3, triple]                   
\[3, dup, dup]           
(the leftmost dup then gets popped and ran which duplicates the rightmost dup and the stack becomes)                
\[3, dup, dup]                   
In this example you can quickly see that for any variable/function that is more than 2 instructions long the instructions will edit themselves instead of the top of the stack. To try to get around this limitation I thought of a few possibilities but they all were effectively interchangeable so I decided to go with adding a predefined function/variable that calls the function/variable artificially before it gets called naturally. I called this function exec.                    
if we were to replace triple with triple dup exec dup the program will now run as follows.                           
\[3, triple]                                         
\[3, dup, exec] (once exec gets encountered in the triple definition it will pop it and the previous instruction and run it)                                    
\[3, 3] (and then the rest of triple gets added to the stack)                   
\[3, 3, dup] (and dup gets naturally called by the interpreter)                  
\[3, 3, 3] (the program would now call 3 but we can stop here for the sake of the example)                      
This seemed to have solved the problem but if you look carefully it has effectively removed the core idea of the language and has created a separation between how the code runs and how it is written.                
This can be demonstrated with another example.                  
if we have quadruple defined as "quadruple triple exec dup" then the program will run as follows.                         
\[3, quadruple]                                            
\[3, triple, exec] (exec has been encountered so it will now execute triple)                                   
\[3, dup, exec] (exec has been encountered so it will now execute dup)                                           
\[3, 3] (it will now have to add the rest of triple, but we can stop here for the sake of the example)                                    
in this example quadruple gets called which calls triple and we have now created a call stack within this exec state. This has effectively destroyed the original intent of the language and, in my eyes, has shown that it is impossible to have a complete integration of code and data.                               

# conclusion
This is in no means a thorough or mathematical proof but it was fun to do nonetheless.                    
A thrown together interpreter and some example programs have also been added to this repository.                
Although my mind has been made up I may have missed something obvious! Feel free to give this language a shot and see if you can solve the problem yourself! Tell me if you can think of any counterexamples or anything at all! Feel free to add to this repository in any way you want! I am not that active though so it may take a bit for your contribution to be added.                       
                           
Thanks for reading through this!
