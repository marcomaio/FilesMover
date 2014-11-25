import argparse
import os
import shutil

def optionInit():
    parser = argparse.ArgumentParser(description='Move files from nested folders to a new destination, removing duplicates.')
    parser.add_argument('source', help='the source folder')
    parser.add_argument('destination', help='the destination folder')
    return parser.parse_args()

def moveFiles(iSource, iDestination):
    for root, dirs, files in os.walk(iSource):
        for aFile in files:
            aSourceFile = root + '\\' + aFile
            aDestinationFile = iDestination + '\\' + aFile
            if aFile in os.listdir(iDestination):
                if os.stat(aSourceFile).st_size != os.stat(aDestinationFile).st_size:
                    print ('Trovato file con stesso nome ' + aFile + ' ma diverse dimensioni')
            else:
                shutil.move(aSourceFile, aDestinationFile)
                
        
def checkInputIntegrity(iSource, iDestination):
    if (not os.path.isdir(iSource)):
        raise NameError('Source directory does not exists! Exiting the program!')
    if (not os.path.isdir(iDestination)):
        os.makedirs(iDestination)
        os.chmod(iDestination, 0o776)
        #aUid = os.stat(iSource).st_uid
        #aGid = os.stat(iSource).st_gid
        #os.chown(aNewDirPath, aUid, aGid)
        

if __name__ == '__main__':
    args = optionInit()
    aSource = args.source
    aDestination = args.destination
    print('Moving from ' + aSource + ' to '+ aDestination)
    print(os.listdir(args.source))
    checkInputIntegrity(aSource, aDestination)
    moveFiles(aSource, aDestination)
    
