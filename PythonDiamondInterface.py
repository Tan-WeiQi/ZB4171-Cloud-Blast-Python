import subprocess as bash
import pathlib
import shutil
import os
from Bio.Blast import NCBIXML

class DbFactory:
    def __init__(self, fasta_path, db_name):

        """
            fasta_path (str): absolute path to fasta files meant for diamond DB creation
            db_name (str): name of your diamond .dmnd file. 
                            for eg: if you give db_name = abc, the diamond db file will be output as abc.dmnd.
            
        """
        self.fasta_path = str(pathlib.Path(fasta_path))
        self.db_name = db_name
    
    def createDb(self):
        """
            executes the diamond bash command with subprocess library
            then stores the diamond db file into storage_dir
        """
        try:
            f = open(self.fasta_path)
            f.close()

        except FileNotFoundError:
            print('Please give a valid path to your fasta file')
            return

        #runs bash diamond command
        args = ['diamond', 'makedb', '--in', self.fasta_path, '--db', self.db_name]
        bash.Popen(args)

"""
    Only supports blastp from now
"""
class AlignUtil:

    def runBlast(self, db_path, query, index=None):
        """
            db_path (str): absolute path of .dmnd file, .dmnd file is generated when diamond makedb is called
            query (str): a query file name
            index (int): default is None, index is activated when a for loop is run.
        """
        out = 'results.xml'
        if index != None:
            out = 'results_' + str(index) + '.xml'
        args = ['diamond', 'blastp', '-d', db_path , '-q', query, '-o', out, '-f', '5' ]
        bash.Popen(args)

class BlastRunner:

    def __init__(self, query_folder, db_path):
        """
            query_folder (str): an absolute path to a folder which stores query or queries
            db_path (str): an absolute path to a .dmnd file.
        """
        self.align_util = AlignUtil()
        self.query_folder = query_folder
        self.db_path = db_path

    def run(self):
        try:
            queries = os.listdir(self.query_folder)
            for i in range(len(queries)):
                query = os.path.join(self.query_folder, queries[i])
                self.align_util.runBlast(self.db_path, query, i)

        except FileNotFoundError:
            print('please give a valid path to a folder')
            return

class XMLParser:
    def parseXML(self, xml_folder):

        files = os.listdir(xml_folder)
        result_subfolder = os.path.join(xml_folder, 'results')
        pathlib.Path(result_subfolder).mkdir(parents=True,exist_ok=True)

        for f in files:
            if '.xml' in f:
                file_prefix = f.split('.')[0]
                full_file_path_new = os.path.join(result_subfolder, file_prefix+'.txt')
                full_file_path  = os.path.join(os.getcwd(), f)

                open_file = open(full_file_path, 'r')
                parsed_file = NCBIXML.parse(open_file)
                result = list(parsed_file)
                result_dict = vars(result[0])

                query = result_dict['query']
                e = result_dict['expect']
                a = result_dict['alignments']
                new_f = open(full_file_path_new, 'w+')
                
                new_f.write('query: '+query + '\n')
                new_f.write('expect: '+e + '\n')
                new_f.write('alignments: '+str(a) + '\n')



if __name__ == "__main__":
    #f_path = '/home/hwc_howeichin/diamond_db/test.fasta'
    #dbF = DbFactory(fasta_path=f_path, db_name='testing')
    #dbF.createDb()
    query_folder = '/home/hwc_howeichin/queries'
    db_path = '/home/hwc_howeichin/test/testing.dmnd'
    blast_runner = BlastRunner(query_folder= query_folder, db_path= db_path)
    blast_runner.run()
    print('----Converting XML to Text now ----')
    blast_runner.parseXML()







        

