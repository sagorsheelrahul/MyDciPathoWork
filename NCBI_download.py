import os
import time
import urllib
from multiprocessing import Pool, Manager

import pandas as pd
import wget

from download_config import Config

config = Config()

def ftp_download(args):
    name = args[0]
    fna_file_url = args[1]
    output_file_name = args[2]
    successful_list = args[3]
    e = ''
    if os.path.exists(output_file_name):
        print('Output path exists:', output_file_name, '- skipping')
        successful_list.append(1)
        print('Downloaded:', len(successful_list))
        return

    start = time.time()
    for i in range(config.retry_times):
        print('Downloading', fna_file_url, 'attempt:', str(i + 1) + '/' + str(config.retry_times))
        try:
            do = wget.download(fna_file_url, config.output_path)
        except urllib.error.URLError as e:
            print('Error:', e)
            now = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
            print(now, 'Download of', name, 'failed, retrying...')
            continue
        if do and os.path.exists(output_file_name):
            now = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
            print(now, 'Downloaded', fna_file_url, 'successfully')
            print(fna_file_url, 'took', time.time() - start, 'seconds')
            successful_list.append(1)
            print('Downloaded:', len(successful_list))
            break
        else:
            now = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
            print(now, 'Download of', fna_file_url, 'failed, retrying...')
            continue

    if not os.path.exists(output_file_name):
        with open(config.fail_log_path, 'a') as f:
            now = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
            if e:
                f.write(now + ',' + fna_file_url + ',' + str(e) + '\n')
            else:
                f.write(now + ',' + fna_file_url + '\n')

def multi_download(args):
    with Pool(config.cpu_worker_num) as p:
        p.map(ftp_download, args)

def main():
    # Create output directory if it doesn't exist
    if not os.path.exists(config.output_path):
        os.makedirs(config.output_path)
    
    successful_list = Manager().list()
    df = pd.read_csv(config.input_path, low_memory=False)
    df_all = pd.read_csv('NCBI_22June_RefSeq_32927_Complete_1NP_2P_taxnonmy.csv', low_memory=False)  # <-- UPDATED HERE
    ftp_list = df[config.csv_col].to_list()
    print('Number of URLs to download:', len(ftp_list))
    args = []
    for ftp in ftp_list:
        raw_name = ftp.split('/')[-1][:-4]
        # Match the accession number to get the correct FTP path
        real_ftp = df_all[df_all['assembly_accession'] == raw_name]['ftp_path'].to_list()[0]
        real_name = real_ftp.split('/')[-1]
        fna_file_url = real_ftp + '/' + real_name + config.file_type
        output_file_name = config.output_path + real_name + config.file_type
        args.append([real_name, fna_file_url, output_file_name, successful_list])
    multi_download(args)

if __name__ == '__main__':
    main()
