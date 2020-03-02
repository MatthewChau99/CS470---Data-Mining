This folder consists of:
1. Apriori.py -- the program source code written in Python 3.7.3
2. result500.txt -- output file for running the dataset T10I4D100K.txt with minimum support count 500.
3. CS470_Homework_2.pdf -- report written in LaTeX
4. Homework2.tex -- LaTeX source code

To run the program, you need to have the Python3 in your system. If not, download from https://www.python.org/downloads/

Go to the current directory in command line and type in the following command:

	python3 Apriori.py [dataset_file_name] [min_support] [output_file_name] 

For example

	python3 Apriori.py T10I4D100K.txt 500 result500.txt

will run Apriori.py with T10I4D100K.txt as dataset, with minimum support count 500, and generate an output file named result500.txt

Have fun grading it :)