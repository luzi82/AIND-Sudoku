import datetime
import urllib.request as urllib_request
import os

sample_count = 100
output_dir = 'dailysudoku'

if __name__ == '__main__':
    if not os.path.isdir(output_dir):
        os.makedirs(output_dir)
    day = datetime.datetime.today()
    end = day - datetime.timedelta(days=sample_count)
    while(day>=end):
        url = 'http://www.dailysudoku.com/cgi-bin/sudoku/get_board.pl?year={}&month={}&day={}'.format(day.year,day.month,day.day)
        filename = os.path.join(output_dir,day.strftime('%Y%m%d.json'))
        with urllib_request.urlopen(url) as response:
            if response.status == 200:
                with open(filename,'wb') as fout:
                    fout.write(response.read())
                    print('{} OK'.format(filename))
            else:
                print('{} FAIL'.format(filename))
        day = day - datetime.timedelta(days=1)
