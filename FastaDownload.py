from Bio import Entrez
import pathlib

class FastaDownloader:

    def __init__(self, db, UIDs, out_dir, file_name, user_email):

        """
            db (str): an Entrez database
            UIDs (str): comma delimited Entrez Unique Identifiers
            out_dir (str): output directory of downloaded fastra file, must be absolute path
            file_name (str): name of output file
            user_email (str): user's email
        """
        self.db = db
        self.UIDs = UIDs 
        self.out_dir = str(pathlib.Path(out_dir))
        self.file_name = file_name
        self.email = user_email
        self.db_validator = DBValidator()
        self.fasta_compatible = FastaCompatible()

    def download(self):
        
        is_valid_db = self.db_validator.isValidDb(self.db)
        is_fasta_compatible = self.fasta_compatible.isFastaCompatibleDb(self.db)

        if not is_valid_db:
            raise ValueError('Please provide database supported by Entrez.')

        if not is_fasta_compatible:
            raise ValueError('Please provide database which is compatible with Fasta format.')

        UID_len = len(self.UIDs.split(','))
        if UID_len > 200:
            raise ValueError('Number of UIDs must be at most 200.')

        pathlib.Path(self.out_dir).mkdir(parents=True,exist_ok=True)
        data_folder = pathlib.Path(self.out_dir)
        final_file_name = data_folder / self.file_name

        Entrez.email = self.email
        entrez_out = Entrez.efetch(db=self.db, id=self.UIDs, rettype="fasta")
        out_file = open(final_file_name, 'w+')
        out_file.write(entrez_out.read())

        out_file.close()
        entrez_out.close()

class DBValidator:

    def __init__(self):

        """
            valid_dbs (dict): all the databases currently supported by Entrez library

        """
        self.valid_dbs = {'bioproject': 1, 'biosample':1, 'biosystems':1, 'books':1,
    'cdd':1, 'gap':1, 'dbvar':1, 'epigenomics':1, 'nucest': 1,
    'gene':1, 'genome':1, 'gds':1, 'geoprofiles':1, 'nucgss':1, 'homologene':1,
    'mesh':1, 'toolkit':1, 'ncbisearch':1, 'nlmcatalog':1, 'nuccore':1, 'omia':1,
    'popset':1, 'probe':1, 'protein':1, 'proteinclusters':1, 'pcassay':1, 'pccompound':1,
    'pcsubstance':1,'pubmed':1, 'pmc':1, 'snp':1, 'sra':1, 'structure':1, 'taxonomy':1, 
    'unigene':1, 'unists':1}

    def isValidDb(self, user_db):

        """
            user_db (string): user input database

        """
        #checks if user_db is supported by Entrez library
        isPresent = self.valid_dbs.get(user_db, 0)
        return isPresent == 1

class FastaCompatible:

    def __init__(self):
        self.compatible_db = {'homologene':1, 'nuccore':1, 'nucest':1, 'nucgss':1,
        'protein':1, 'popset':1, 'sequences':1, 'snp':1}

    def isFastaCompatibleDb(self, user_db):
        
        """
            user_db (string): user input database

        """
        isPresent = self.compatible_db.get(user_db, 0)
        return isPresent == 1

if __name__ == "__main__":
    dl = FastaDownloader(db='protein', UIDs='AAB35036',out_dir="C:/Users/Wei Chin/Desktop/diamond", file_name='pro.fasta', 
    user_email='hwc.howeichin@gmail.com')
    dl.download()
    #Q9H257


