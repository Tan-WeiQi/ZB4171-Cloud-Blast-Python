from FastaDownload import *
from PythonDiamondInterface import *
import os.path
import os
import shlex
import sys

helptext = True
while True:
  if helptext:
    print("d: Download fasta files\n"
          "c: Create a Diamond database\n"
          "p: Perform a Blast search\n"
          "t: Convert .xml to .txt\n"
          "q. Quit")
    helptext = False
  i = input()
  bits = shlex.split(i)

  # Empty input.  Show them the help text again.
  if len(bits) <= 0:
    helptext = True
    continue
  
  # Download
  if bits[0] == "d":
    if len(bits) != 5:
      print("Please type: Syntax: d [database] [UIDs] [out_directory] [file_name]\n"
            "Multiple UIDs should be enclosed in quotes, e.g. \"AAB35036, NP_013796\"\n"
            "Eg: d protein 'AAB35036, Q9H257' /path/to/some/folder/ out.fasta")
      continue
    print('db', bits[1])
    dl = FastaDownloader(db=bits[1], UIDs=bits[2], out_dir=bits[3], file_name=bits[4], 
      user_email='hwc.howeichin@gmail.com')
    dl.download()
    print("Files downloaded to "+bits[3]+".")
    continue
  
  # Create
  if bits[0] == "c":
    if len(bits) != 3:
      print("Please type: Syntax: c [fasta_path] [database_name]\n"
            "Eg: c /path/to/fasta/file diamond_db")
      continue
    # Check that the fasta file exists.
    if not os.path.isfile(bits[1]):
      # Try to recover. Did they forget the file extension?
      if not os.path.isfile(bits[1] + ".fasta"):
        print("Invalid fasta file.")
        continue
      bits[1] = bits[1] + ".fasta"
    dbf = DbFactory(fasta_path=bits[1], db_name=bits[2])
    dbf.createDb()
    print("Database created at current directory: " + os.getcwd() +' .')
    continue
    
  # Perform
  if bits[0] == "p":
    if len(bits) != 3:
      print("Please type: Syntax: p [query_folder] [database_path]\n"
            "Eg: p /path/to/queries /path/to/db.dmnd")
      continue
    # Check that the folder exists and contains files.
    if not os.path.isdir(bits[1]):
      print("Folder does not exist.")
      continue
    if len(os.listdir(bits[1])) <= 0:
      print("Folder is empty.")
      continue
    # Check that the database file exists.
    if not os.path.isfile(bits[2]):
      # Try to recover. Did they forget the file extension?
      if not os.path.isfile(bits[2] + ".dmnd"):
        print("Invalid diamond database file.")
        continue
    blast_runner = BlastRunner(query_folder=bits[1], db_path=bits[2])
    blast_runner.run()
    print("Blast complete. Results were printed to result subdirectory.")
    continue

    # Perform
  if bits[0] == "t":
    if len(bits) != 2:
      print("Please type: Syntax: t [XML_folder]\n"
            "Eg: t /path/to/xml_files")
      continue
    # Check that the folder exists and contains files.
    if not os.path.isdir(bits[1]):
      print("Folder does not exist.")
      continue
    if len(os.listdir(bits[1])) <= 0:
      print("Folder is empty.")
      continue
    
    xml_parser = XMLParser()
    xml_parser.parseXML(bits[1])
    print("XML files converted.")
    continue
  
  # Quit
  if bits[0] == "q":
    print("Exiting. Please have a nice day.")
    sys.exit()
    continue
  
  # If we fell through, it just wraps to the start and prints the input instructions again.
  helptext = True
