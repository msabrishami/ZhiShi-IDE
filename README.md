# ZhiShi-IDE
Interactive Design Environment for ZhiShi ATPG Report Format 


This Python-based tool is designed to facilitate the creation of .zs (ZhiShi) reports. Simply, the user can report the ATPG solution line by line. After each line is entered by the user, the program analyzes the keywords and based on its basic understanding of the ATPG algorithm, it suggests  the next possible lines. 

The IDE can only suggest the next possible lines based on previous lines keywords, and is not capable of neither evaluating the correctness of the flow nor understanding the netlist graph. 

## Step by Step Instructions
You can simply download the python code run the tool using python3: 
```
$ python3 ZhiShi-IDE-v02.py
```

The program Initially prompts the user to specify a circuit node and its associated fault condition (either stuck-at-0 or stuck-at-1) using a straightforward input format such as node@1 or node@0. 

IMAGE 1


IMAGE 2


After the user introduces the target fault, the tool provides two pieces of information: 

- Current instructions: The history of the user's instructions. 
- Possible next instructions: Suggestions for subsequent steps that align with the procedures of the underlying ATPG algorithm. 

Upon completing the instructions, the tool inquires whether the user wishes to save the session's output. Affirmative responses ('yes' or 'y') trigger a prompt for a filename, under which the .zs file will be stored.

IMAGE 3


In conclusion, the tool's guiding mechanism is aimed at simplifying the documentation process, ensuring users can accurately and methodically log each step of the algorithm. 


## Examples
We had provided the .zs reports of all five solutions for line s-SS@1 fault in cmini netlist. 
