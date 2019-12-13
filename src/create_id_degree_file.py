# Original Author: Yvonne-Anne Pignolet, ya@pignolet.ch, 31.5.2014
import time

input_edge_file = '../output/dblp_edges_maxAuthor20_simple.csv'
output_results_file = input_edge_file.replace('.csv', '_id_degree.csv')

print("edge input ", input_edge_file)
print("output ", output_results_file)

id_degree = {}
max_degree = 0
count = 0
with open(input_edge_file, 'r') as edge_file:
    for line in edge_file:
        if not line.startswith("#"):
            s = line.strip().split(',')
            for i in [0, 1]:
                curr_id = s[i].strip()
                if curr_id not in id_degree:
                    id_degree[curr_id] = 0
                    count += 1
                id_degree[curr_id] += 1
                max_degree = max(max_degree, id_degree[curr_id])
    print(f'There are {count} authors and the max degree is {max_degree}')

with open(output_results_file, 'w') as results:
    results.write("# " + time.strftime("%Y_%m_%d_%H_%M") + "\n")
    results.write("# edge input " + input_edge_file + "\n")
    results.write("# id, degree\n")

    degree_id_set_dict = {k: set() for k in range(1, max_degree + 1)}
    for author_id, degree in id_degree.items():
        degree_id_set_dict[degree].add(author_id)
    print("sorted degree list")

    degree = max_degree
    while degree > 0:
        id_set = degree_id_set_dict[degree]
        for author_id in id_set:
            results.write(f'{author_id},{degree}\n')
        degree -= 1
    print("printed sorted degree list")
