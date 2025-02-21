class Config:
    def __init__(self):
        # Path to your uploaded CSV file
        self.input_path = 'NCBI_22June_RefSeq_32927_Complete_1NP_2P_taxnonmy.csv'
        # Directory to save the downloaded FASTA files
        self.output_path = 'FASTA_files/'
        # Number of CPU workers
        self.cpu_worker_num = 4
        # File suffix for the genomic FASTA files
        self.file_type = '_genomic.fna.gz'
        # ✅ Correct FTP column name
        self.csv_col = 'ftp_path'  # <-- Updated here
        # Number of retry attempts for each download
        self.retry_times = 10
        # Path to log file for any download failures
        self.fail_log_path = 'fail_log.txt'
