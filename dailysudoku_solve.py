import json
import dailysudoku_download
import os
import solution

output_dir = dailysudoku_download.output_dir

if __name__ == '__main__':
    for fname in os.listdir(output_dir):
        print(fname)
        ffname = os.path.join(output_dir,fname)
        with open(ffname,'r') as ff:
            numbers = json.load(ff)['numbers']
        solution.assignments=[]
        solution.display(solution.solve(numbers,False))
        solution.assignments=[]
        print()
