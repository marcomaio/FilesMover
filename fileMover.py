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
            aSourceFile = os.path.join(root, aFile)
            aDestinationFile = os.path.join(iDestination, aFile) 
            if aFile in os.listdir(iDestination):
                if os.stat(aSourceFile).st_size != os.stat(aDestinationFile).st_size:
                print ('Found file with same name \"' + aFile + '\" but different size') 
                # we should rename the file
            else:
                shutil.move(aSourceFile, aDestinationFile)
        
def checkInputIntegrity(iSource, iDestination):
    if (not os.path.isdir(iSource)):
        raise NameError('Source directory does not exist! Exiting the program!')
    if (not os.path.isdir(iDestination)):
        raise NameError('Destination directory does not exist! Exiting the program!')

if __name__ == '__main__':
    args = optionInit()
    aSource = args.source
    aDestination = args.destination
    checkInputIntegrity(aSource, aDestination)
    print('Moving from ' + aSource + ' to '+ aDestination)
    moveFiles(aSource, aDestination)
    
