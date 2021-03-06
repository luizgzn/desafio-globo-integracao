import datetime
import time
import logging
import csv
import os


logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

formatter = logging.Formatter('%(asctime)s:%(levelname)s - %(message)s')

if not os.path.exists('publisher/logs'):
    os.makedirs('publisher/logs')
    
file_handler = logging.FileHandler('publisher/logs/parser.log')
file_handler.setFormatter(formatter)

stream_handler = logging.StreamHandler()
stream_handler.setFormatter(formatter)

logger.addHandler(file_handler)
logger.addHandler(stream_handler)

class TextParser:
    def __blocks(self, files, size=65536):
        while True:
            b = files.read(size)
            if not b: break
            yield b

    def count_lines(self, file_path):
        with open(file_path, "r", encoding="utf-8", errors='ignore') as f:
            n_lines = sum(bl.count("\n") for bl in self.__blocks(f))
            return n_lines

    def generate_csv(self, dict_list):
        if not os.path.exists('publisher/parse_results'):
            os.makedirs('publisher/parse_results')
        filename = 'publisher/parse_results/filtered_videos.csv'
        file_exists = os.path.isfile(filename)
        with open('publisher/parse_results/filtered_videos.csv', 'a') as f:
            headers = [*dict_list[0]]
            w = csv.DictWriter(f, delimiter=',', lineterminator='\n',fieldnames=headers)
            if not file_exists:
                w.writeheader()
            w.writerows(dict_list)

    def parse_content(self, file_path, start_line = 0):
        with open(file_path, 'r', encoding="utf-8", errors='ignore') as f:
            result_list = []
            logger.info(f'Reading {file_path}')
            # definir a linha onde iniciar o parseamento da string
            for i, line in enumerate(f):
                if i == start_line:
                    break
            for line in f:
                # selecionar pedaços da string a partir do indice
                start_time = line[6:28]
                end_time = line[29:50]
                title = line[106:138].rstrip()
                duration = line[184:195]
                reconcile_key = line[279:298].rstrip()
                dictionary = { 'start_time': start_time, 
                            'end_time': end_time, 
                            'title': title,
                            'duration':duration,
                            'reconcile_key': reconcile_key
                            }
                duration_string = duration.split(';', 1)[0]
                dt = time.strptime(duration_string,'%H:%M:%S')
                duration_seconds = datetime.timedelta(hours=dt.tm_hour,minutes=dt.tm_min,seconds=dt.tm_sec).total_seconds()
                if duration_seconds > 30:
                    result_list.append(dictionary)
            if result_list:
                self.generate_csv(result_list)
            logger.info(f'File: {file_path} -> {result_list}')
            return(result_list)