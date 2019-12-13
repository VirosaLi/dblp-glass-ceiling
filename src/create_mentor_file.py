# Original author: Yvonne-Anne Pignolet, ya@pignolet.ch, 31.5.2014
import time
from collections import Counter
import math

MENTOR_DIFFERENCE = 4
input_edge_filename = '../output/dblp_edges_maxAuthor20.csv'
output_mentor_filename = input_edge_filename.replace(".csv", "_mentee.csv")

print("Input: ", input_edge_filename)
print("Output: ", output_mentor_filename)

first_year = {}
frequent_mentor_candidates = {}
random_mentor_candidates = {}
count_e = 0
with open(input_edge_filename, 'r') as edge_file:
    for line in edge_file:
        if not line.startswith("#"):
            count_e += 1
            if count_e % 1000000 == 0:
                print(f'Read {count_e} lines, using {time.process_time()} seconds')

            s = line.strip().split(",")
            if len(s) < 3:
                print(s)
                continue
            author1 = s[0].strip()
            author2 = s[1].strip()
            year = int(s[2].strip())

            if author1 not in first_year:
                first_year[author1] = math.inf
                frequent_mentor_candidates[author1] = []
                random_mentor_candidates[author1] = []
            if author2 not in first_year:
                first_year[author2] = math.inf
                frequent_mentor_candidates[author2] = []
                random_mentor_candidates[author2] = []
            first_year[author1] = min(first_year[author1], year)
            first_year[author2] = min(first_year[author2], year)

count_e = 0
with open(input_edge_filename, 'r') as edge_file:
    for line in edge_file:
        if not line.startswith("#"):
            count_e += 1
            s = line.strip().split(",")
            if len(s) < 3:
                print(s)
                continue
            author1 = s[0].strip()
            author2 = s[1].strip()

            year = int(s[2].strip())
            if first_year[author1] > first_year[author2]:
                young_author = author1
                old_author = author2
            else:
                young_author = author2
                old_author = author1
            if first_year[young_author] > first_year[old_author] + MENTOR_DIFFERENCE:
                if first_year[young_author] + MENTOR_DIFFERENCE > year:
                    frequent_mentor_candidates[young_author].append(old_author)

count_e = 0
with open(output_mentor_filename, 'w') as mentor_file:
    for key, value in frequent_mentor_candidates.items():
        if len(value) > 0:
            c = Counter(value)
            mentor_file.write(f'{key},{c.most_common(1)[0][0]},{first_year[key]}\n')
            count_e += 1

print(f'Assigned {count_e} most frequent mentors out of {len(frequent_mentor_candidates)} people')
print(f'Wrote mentor file in {time.process_time()} seconds')
