# Author: Yvonne-Anne Pignolet, ya@pignolet.ch, 31.5.2014
import time
import sys

MALE = 'm'
FEMALE = 'f'

if len(sys.argv) > 1:
    input_gender_file = sys.argv[1]
if len(sys.argv) > 2:
    input_edge_file = sys.argv[2]
else:
    print('input error')
    exit(1)

output_file_name = input_edge_file.replace(".csv", "_known_degree_v0.csv")
if "v1" in input_gender_file:
    output_file_name = output_file_name.replace("v0", "v1")

print("gender input: " + input_gender_file)
print("edge input: " + input_edge_file)
print("output file name: " + output_file_name)

##################

id_file = open(input_gender_file, 'rU')
id_gender_dict = eval(id_file.read())
id_file.close()

edge_file = open(input_edge_file, 'r')
id_degree = {}
max_degree = 0
count = 0
Fdegreesum = 0
Fcount = 0
for line in edge_file:
    if not line.startswith("#"):
        s = line.strip().split(',')
        g0 = id_gender_dict[s[0].strip()]
        g1 = id_gender_dict[s[1].strip()]
        if not (g0 in [FEMALE, MALE] and g1 in [FEMALE, MALE]):
            continue
        for i in [0, 1]:
            if s[i].strip() not in id_degree:
                id_degree[s[i].strip()] = 0
                count = count + 1
                if id_gender_dict[s[i].strip()] == FEMALE:
                    Fcount = Fcount + 1
            id_degree[s[i].strip()] = id_degree[s[i].strip()] + 1
            max_degree = max(max_degree, id_degree[s[i].strip()])
            if id_gender_dict[s[i].strip()] == FEMALE:
                Fdegreesum = Fdegreesum + 1

print("read edges")

F_degree_num = {k: 0 for k in range(1, max_degree + 1)}
total_degree_num = {k: 0 for k in range(1, max_degree + 1)}

count = 0
countF = 0
tops = []
for id, degree in id_degree.items():
    if id == '-1':
        continue
    if id_gender_dict[id] == FEMALE:
        F_degree_num[degree] += 1
        countF += 1
    total_degree_num[degree] += 1
    count += 1

Fcum_degree_num = {}
cum_degree_num = {}
ratio = {}
expected = []
Fcum = 0
cum = 0
cutoff = 0
for degree, num in total_degree_num.items():
    Fcum += F_degree_num[degree]
    cum += num
    cum_degree_num[degree] = count - cum
    Fcum_degree_num[degree] = countF - Fcum
    if degree > 1 and F_degree_num[degree] > 0 and cum_degree_num[degree - 1] > 0:
        ratio[degree] = Fcum_degree_num[degree - 1] * 1.0 / cum_degree_num[degree - 1]
    if degree == 1:
        ratio[degree] = countF * 1.0 / count
    expected.append(countF * 100.0 / count)
##################
print(countF * 100.0 / count)

csv_file = open(output_file_name, 'w')
csv_file.write("# created " + time.strftime("%Y_%m_%d_%H_%M") + "\n")
csv_file.write("# based on file " + input_edge_file + "\n")
csv_file.write("# based on gender dict " + input_gender_file + "\n")
label = "It is organised as follows (4 lines of comments, then per line (starting with 0): degree,number of female " \
        "nodes, number of male nodes, number of both, total number of nodes\n0,0,0,0,0 "
x = range(1, max_degree + 1)
y = [str(F_degree_num[k]) + "," + str(total_degree_num[k] - F_degree_num[k]) + "," + str(
    total_degree_num[k]) + "," + str(total_degree_num[k]) for k in x]
csv_file.write("# " + label + "\n")
i = 0
while i < len(x):
    csv_file.write(f'{x[i]},{y[i]}')
    i += 1
csv_file.close()
