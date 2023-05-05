import sys
import json

input_file_path = sys.argv[1]
output_file_path = sys.argv[2]

fin = open(input_file_path, 'r')
fout = open(output_file_path, 'w')

data = str(json.load(fin)).replace("\'", "\"")
fout.write(f'jsonGraphData = \'{data}\'')

fin.close()
fout.close()
