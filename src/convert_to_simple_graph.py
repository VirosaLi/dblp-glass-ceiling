# Original Author: Yvonne-Anne Pignolet, ya@pignolet.ch, 31.5.2014
import time

input_edge_file = '../output/dblp_edges_maxAuthor20.csv'
output_edge_file = input_edge_file.replace(".csv", "_simple.csv")

edge_dict = {}
count_r = 0
count_w = 0
id_degree_dict = {}
with open(input_edge_file, 'r') as edge_file:
    for line in edge_file:
        if count_r % 1000000 == 1:
            print(f'Read {count_r} lines, using {time.process_time()} seconds')
        if not line.startswith("#"):
            s = line.strip().split(',')
            if len(s) < 3:
                print(s)
                continue
            u = str(min(int(s[0].strip()), int(s[1].strip())))
            v = str(max(int(s[0].strip()), int(s[1].strip())))
            y = int(s[2].strip())
            count_r += 1
            key = f'{u},{v}'
            if key not in edge_dict:
                edge_dict[key] = y
                if u not in id_degree_dict:
                    id_degree_dict[u] = 0
                id_degree_dict[u] += 1
                if v not in id_degree_dict:
                    id_degree_dict[v] = 0
                id_degree_dict[v] += 1
            else:
                edge_dict[key] = min(y, edge_dict[key])

print(f'Read {count_r} lines, wrote {count_w} lines, using {time.process_time()} seconds')

with open(output_edge_file, 'w') as new_edge_file:
    count_w = 0
    for key, value in edge_dict.items():
        if id_degree_dict[key.split(",")[0]] > 0 and id_degree_dict[key.split(",")[1]] > 0:
            new_edge_file.write(f'{key},{value}\n')
            count_w += 1

print(f'Read {count_r} lines, wrote {count_w} lines, using {time.process_time()} seconds')
