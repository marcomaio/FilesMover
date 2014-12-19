import argparse
import os
import shutil
import time

def getFolderSize(iSource):
    aSize = 0
    for root, dirs, files in os.walk(iSource):
        for aFile in files:   
            aSize += os.stat(os.path.join(root, aFile)).st_size
    return aSize
        
def optionInit():
    parser = argparse.ArgumentParser(description='Move files from nested folders to a new destination, removing duplicates.')
    parser.add_argument('source', help='the source folder')
    parser.add_argument('destination', help='the destination folder')
    return parser.parse_args()

def printProgress(iSourceSize, iTotalMovedSize, iStartTime):
    aPercentageMoved = int((iTotalMovedSize/iSourceSize)*100)
    aSecondsPassed = time.time() - iStartTime
    aSpeedBytesSecond = iTotalMovedSize/aSecondsPassed
    aTimeLeft = int(iSourceSize/aSpeedBytesSecond)
    aMinutesLeft = int(aTimeLeft/60)
    aSecondsLeft = aTimeLeft%60
    print(str(aPercentageMoved) + '% completed - ' + str(int(aSpeedBytesSecond/1024)) + ' kB/s - E.T.A.: ' + str(aMinutesLeft) + ' minutes ' + str(aSecondsLeft) + ' seconds left', end='\r')

def printStats(iStartTime, iMovedDataSize, iNotMovedFiles):
    aEndTime = int(time.time())
    if iNotMovedFiles:
        print('Following files have not been moved because already present in the origin destination:')
    for aFile in iNotMovedFiles:
        print(aFile)
    print('Moved a total of ' + str(iMovedDataSize/(1024*1024)) + 'MBytes of data')
    
    aMinutesSpent = str(int((aEndTime - iStartTime)/60))
    aSecondsSpent = str((aEndTime - iStartTime)%60)
    print('in ' + aMinutesSpent + ' minutes and ' + aSecondsSpent + ' seconds')
    
def moveAndRenameFile(iFileName, iModifiedFileName, iSource, iDestination):
    aFileName, aFileExtension = os.path.splitext(iModifiedFileName)
    aNewFileName = aFileName + '_copy' + aFileExtension
    if aNewFileName in os.listdir(iDestination):
        moveAndRenameFile(iFileName, aNewFileName, iSource, iDestination)
    else:
        aSourceFile = os.path.join(iSource, iFileName)
        aDestinationFile = os.path.join(iDestination, aNewFileName)
        shutil.move(aSourceFile, aDestinationFile)
    
def moveFiles(iSource, iDestination, iSourceSize):
    aTotalMovedSize = 0
    aStartTime = int(time.time())
    aNotMovedFiles = set()
    for root, dirs, files in os.walk(iSource):
        for aFile in files:
            aSourceFile = os.path.join(root, aFile)
            aDestinationFile = os.path.join(iDestination, aFile)
            aSourceFileSize = os.stat(aSourceFile).st_size
            if aFile in os.listdir(iDestination):
                if aSourceFileSize != os.stat(aDestinationFile).st_size:
                    moveAndRenameFile(aFile, aFile, root, iDestination)
                    aTotalMovedSize += aSourceFileSize
                    printProgress(iSourceSize, aTotalMovedSize, aStartTime)
                else:
                    aNotMovedFiles.add(aFile)
            else:
                shutil.move(aSourceFile, aDestinationFile)
                aTotalMovedSize += aSourceFileSize
                printProgress(iSourceSize, aTotalMovedSize, aStartTime)
    printStats(aStartTime, aTotalMovedSize, aNotMovedFiles)
        
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
    aSourceSize = getFolderSize(aSource)
    print('Source folder size: ' + str(aSourceSize/(1024*1024)) + ' MBytes')
    print('Moving from ' + aSource + ' to '+ aDestination)
    moveFiles(aSource, aDestination, aSourceSize)
    