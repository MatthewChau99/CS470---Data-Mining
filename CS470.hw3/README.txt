In this folder, there are 8 files:

1. kmeans.py --> the source file written in Python 3
2. iris.data --> input file 1
3. haberman.data --> input file 2
4. outputIris.txt --> output file for iris.data
5. outputHaberman --> output file for haberman.data
6. CS470 Homework 3.pdf --> the report
7. Homework3.tex --> the LaTeX source code
8. README.txt --> you're reading it

To run the program, you need to have the Python3 in your system. If not, download from https://www.python.org/downloads/

Go to the current directory in command line and type in the following command:

	python3 kmeans.py [dataset_file_name] [k] [output_file_name]

For example,

		python3 kmeans.py iris.data 3 outputIris.txt

will run kmeans.py with iris.data as dataset, with 3 different clusters, and generate an output file named outputIris.txt

Moreover, you need to have pandas and numpy installed in your environment. If not, open your terminal, and type 

		"pip3 install numpy"
		"pip3 install pandas"
		

Have fun grading it :)