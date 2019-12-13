# Original Author: Yvonne-Anne Pignolet, ya@pignolet.ch, 31.5.2014
import time

MALE = 'm'
FEMALE = 'f'
input_gender_file = '../data/dblp_id_gender_dict_v1.dict'
input_id_name_file = '../output/dblp_id_name.csv'
input_edge_file = '../output/dblp_edges_maxAuthor20_simple.csv'
top_file_name = '../output/dblp_edges_maxAuthor20_simple_id_degree.csv'
output_results_file = top_file_name.replace(".csv", '_1000_edges_v1.csv')

print("Gender input ", input_gender_file)
print("Edge input ", input_edge_file)
print("Output ", output_results_file)


id_file = open(input_gender_file, 'r', newline=None)
id_gender_dict = eval(id_file.read())
id_file.close()

id_degree_dict = {k: 0 for k in id_gender_dict.keys()}

high_file = open(output_results_file.replace("edges", "nodes"), 'w')
high_file.write("# created by extract_top_graph.py, " + time.strftime("%Y_%m_%d_%H_%M") + "\n")
high_file.write("# edge input file: " + input_edge_file + "\n")
high_file.write("# gender dictionary file: " + input_gender_file + "\n")
high_file.write("# top file: " + top_file_name + "\n")
top_file = open(top_file_name, 'r')
top_id_set = set()
i = 0
deg = -1
for line in top_file:
    if line.startswith("#"):
        continue

    s = line.split(",")
    if i < 1000:
        if id_gender_dict[s[0]] in [FEMALE, MALE]:
            i += 1
            top_id_set.add(s[0])
            deg = s[1]
            high_file.write(line)
    elif i >= 1000 and s[1] == deg:
        if id_gender_dict[s[0]] in [FEMALE, MALE]:
            top_id_set.add(s[0])
            i += 1
            high_file.write(line)
    else:
        break
top_file.close()
high_file.close()
print(len(top_id_set), "found")

count = 0
high_file = open(output_results_file, 'w')
high_file.write("# created by extract_top_graph.py, " + time.strftime("%Y_%m_%d_%H_%M") + "\n")
high_file.write("# edge input file: " + input_edge_file + "\n")
high_file.write("# gender dictionary file: " + input_gender_file + "\n")
high_file.write("# top file: " + top_file_name + "\n")
edge_file = open(input_edge_file, 'r')
for line in edge_file:
    if not line.startswith("#"):
        s = line.strip().split(',')
        if s[0].strip() in top_id_set and s[1].strip() in top_id_set:
            high_file.write(line)
            count += 1
            if count % 100000 == 0:
                print(f'Wrote {count} edge lines')
high_file.close()
edge_file.close()
print(f'Wrote {count} edge lines')
