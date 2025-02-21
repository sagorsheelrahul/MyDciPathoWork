class Config:
    def __init__(self):
        # Path to your uploaded CSV file (already in your repo)
        self.input_path = 'NCBI_22June_RefSeq_32927_Complete_1NP_2P_taxnonmy.csv'
        # Directory to save the downloaded FASTA files
        self.output_path = 'FASTA_files/'
        # Number of CPU workers (use fewer for Colab, as too many can cause issues)
        self.cpu_worker_num = 4
        # File suffix for the genomic FASTA files
        self.file_type = '_genomic.fna.gz'
        # Column name in your CSV that contains URLs
        self.csv_col = 'urls'
        # Number of retry attempts for each download
        self.retry_times = 10
        # Path to log file for any download failures
        self.fail_log_path = 'fail_log.txt'
