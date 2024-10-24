# theory-of-computing-project1
### K-partite matching algorithm for Theory of computing class
1. Team Name: tparisi </br>
2. Team members names and netids: Tim Parisi/tparisi </br>
3. Overall project attempted, with sub-projects: incremental k-partite solver </br>
4. Overall success of the project: Mostly a success, If I had more time I would have wanted to find a way to smooth out the graphs the program creates </br>
5. Approximately total time (in hours) to complete: 15 </br>
6. Link to github repository: https://github.com/tim-parisi/theory-of-computing-project1 </br>
7. List of included files (if you have many files of a certain type, such as test files of different sizes, list just the folder): (Add more rows as necessary). Add more rows as necessary. </br>

|File/folder Name|File Contents and Use|
| -------------- | ------------------- |
|Code Files                            |
|k_partite_matching_tparisi.py </br> graph_results_tparisi.py | k_partite_matching prompts the user for files and checks the k-partite completeness of the contained graphs, graph_results_tparisi is called by k_partite_matching_tparisi and holds all the functions to plot the timings. </br> TO USE: </br> run k_partite_patching.py </br> Type the names of any files you want to graph </br> Type “STOP” </br> Wait and let the program graph the results |
| Test Files |
| generate_graphs_tparisi.py </br> testing_graphs/ </br> check_k_partite_tparisi.py | testing_graphs/ contains csv files containing graphs used for data and testing </br> check_k_partite_tpaisi.py runs k_partite_matching_tparisi on the data in testing_graphs/check_test_data_tparisi.csv and compares that to known results </br> generate_graphs_tparisi.py is a helper program I used to generate graphs in large quantities </br> run generate_graphs_tparisi.py </br> type ‘gen_range’ </br> enter the minimum k-value </br> enter the maximum k-value </br> The program will generate various files based on the k-values entered </br> NOTE: Some of the graphs caused difficulty when uploading to github due to their size, so all graphs have been compressed to the file testing_graphs/graphs.tar.gz |
| Output Files |
| data_2_partite_tparisi_results.txt | Contains the truth value of each graph in data_2_partite_tparisi.csv and how long the graph took to solve
| Plots (as needed) |
| data_2_partite_tparisi_graph.png | Plot resulting from testing_graphs/data_2_partite_tparisi.csv |

8. Programming languages used, and associated libraries: Python with networkx, random, csv, sys, time, re, os, matplotllib, argparse, itertools libraries </br>
9. Key data structures (for each sub-project): networkx Graph, list, dictionary </br>
10. General operation of code (for each subproject): generate_graphs_tparisi.py generates data for the other two files to use, k_partite_matching_tparisi.py runs the k-partite matching algorithm. graph_results_tparisi.py uses matplotlib to graph the times </br>
11. What test cases you used/added, why you used them, what did they tell you about the correctness of your code. I had 7 test cases, checking k-values from 2 to 4 and at least one graph checking True/False for each k value. The k=2 graphs ensured that my shortcut worked which occurred on bipartite graphs, while the k=3 and k=4 graphs tested the code in general operation </br>
12. How you managed the code development: I broke the project into several smaller challenges, frequently researched Python libraries that could be beneficial to me, took advantage of builtin networkx functions as much as possible </br>
13. Detailed discussion of results:
 The provided plot shows extreme scaling as number of nodes increases. In the plot, the time of multiple graphs are measured, with each graph having a number of nodes ranging from 2 to 200, each testing bipartite solvability. As the data shows, the amount of time needed to solve the most extreme cases rose dramatically with each additional node, with each graph with 100 nodes or less taking no more than 5ms to solve and later graphs with node counts approaching 200 taking more than 25ms to solve. With the time to complete each graph rising dramatically as the number of nodes increases, it is clear that this is an NP problem. </br>
14. How team was organized: N/A </br>
15. What you might do differently if you did the project again: I would have taken better advantage of multiprocessing to complete multiple graphs at once and found a way to read the files incrementally </br>
16. Any additional material: All python libraries used are in the included virtual environment
