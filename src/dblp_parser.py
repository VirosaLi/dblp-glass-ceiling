# Original author: Yvonne-Anne Pignolet, ya@pignolet.ch, 31.5.2014
import time
import html
from itertools import combinations

input_xml_filename = '../data/dblp-2013-12-23.xml'
output_edge_filename = '../output/dblp_edges_maxAuthor20.csv '
output_id_filename = '../output/dblp_id_name.csv '
max_author = 20

print(input_xml_filename, output_edge_filename, output_id_filename)

in_pub = False
author_list = []
year = -1
name = ""
count_r = 0
count_e = 0
count_i = 0
count_p = 0
name_dict = {}
id_paper_count_dict = {}
with open(input_xml_filename, 'r') as xml_file:
    edge_file = open(output_edge_filename, 'w')
    id_file = open(output_id_filename, 'w')
    edge_file.write("# Generated on " + time.strftime("%Y_%m_%d_%H_%M") + "\n")
    edge_file.write("# Based on file " + input_xml_filename + "\n")
    id_file.write("# Generated on " + time.strftime("%Y_%m_%d_%H_%M") + "\n")
    id_file.write("# Based on file " + input_xml_filename + "\n")
    for line in xml_file:
        count_r += 1
        if count_r % 1000000 == 0:
            print(f'Read {count_r} lines, wrote {count_i} ids, {count_e} edges, using {time.process_time()} seconds')
        if "<article" in line or "<inproceedings" in line or "<proceedings" in line:
            in_pub = True
            author_list = []
            year = -1
            name = ""
            count_p += 1
        elif in_pub and "<author" in line:
            i = line.find("author>")
            i = line.find(">", i)
            j = line.find("</author", i)
            name = html.unescape(line[i + 1:j])
            if name in name_dict:
                name_id = name_dict.get(name)
                id_paper_count_dict[name_id] += 1
            else:
                name_id = len(name_dict)
                name_dict[name] = name_id
                id_file.write(f'{name_id},{name}\n')
                id_paper_count_dict[name_id] = 1
                count_i += 1
            author_list.append(name_id)
            name = ""
        elif in_pub and "<year" in line and len(author_list) <= max_author:
            i = line.find("<year>")
            i = line.find(">", i)
            j = line.find("</year", i)
            year = line[i + 1:j]

            for a, b in combinations(author_list, 2):
                count_e += 1
                edge_file.write(f'{a},{b},{year}\n')

            in_pub = False
    edge_file.close()
    id_file.close()

print(f'Read {count_r} lines, wrote {count_i} ids, {count_e} edges, using {time.process_time()} seconds')

with open(output_edge_filename.replace(".csv", "_topNoPapers.csv"), 'w') as paper_file:
    for i, c in sorted(id_paper_count_dict.items(), key=lambda x: x[1], reverse=True):
        paper_file.write(f'{i},{c}\n')
