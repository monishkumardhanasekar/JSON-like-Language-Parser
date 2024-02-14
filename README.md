# Project Name: JSON-like Language Parser

Name:		Monish Kumar Dhanasekar
B-Number:	B01025975
Email:		mdhanasekar@binghamton.edu

Add text here as needed to document the status of your project.

Language used: Python

# Description:
This project is a parser for a JSON-like language, which allows the parsing of data literals including lists, tuples, maps, and primitive literals such as integers, atoms, and booleans. The parser is implemented in Python and employs regular expressions for tokenizing the input text and recursive descent parsing for generating the Abstract Syntax Tree (AST) of the input.

# Components:

Parser Code: The parser code defines the grammar rules for the JSON-like language and recursively parses the input text to generate the AST. It includes functions for parsing data literals (lists, tuples, maps), primitive literals (integers, atoms, booleans), and handling parsing errors.

Lexer Code: The lexer code tokenizes the input text using regular expressions. It identifies tokens such as integers, atoms, booleans, symbols, and comments, and creates tokens with their corresponding lexemes and positions.

Driver Code: The driver code reads input from standard input, executes the parser, and prints the resulting AST in proper JSON format.

# Usage:
To use the JSON-like language parser:

Input the text containing JSON-like data into the standard input.
Execute the Python script.
The parser will generate the AST for the input text and print it in JSON format.

# Example:

Input: [1, 2, 3]
Output: (in Json format)
[
  {
    "%k": "list",
    "%v": [
      {
        "%k": "int",
        "%v": 1
      },
      {
        "%k": "int",
        "%v": 2
      },
      {
        "%k": "int",
        "%v": 3
      }
    ]
  }
]


#### Command to run the code: 
1. /home/mdhanasekar/cs571/projects/prj1/extras/do-tests.sh ./run.sh (for remote.cs server)

2. ./run.sh (also, don't forget to include the run.sh file if your running in local )

#### Commands to Compile:
(no compilation needed)

##### ensure that you are in the correct folder before running it (path: i571/submit/prj1-sol)


