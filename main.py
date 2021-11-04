from infrastructure.models.eclat import ECLAT
from infrastructure.data_source.data_provider import DataProvider

if __name__ == '__main__':
    completeFileName = input('enter file name which is under infrastructure/data_sources/dataset:   ')
    minSupport = int(input('enter minSupport in an integer format:   '))

    data = DataProvider.readData(completeFileName)
    eclat = ECLAT(data, minSupport)
    eclat.run()

    savedFrequentItemSetFileName = completeFileName.split('.')[0]
    eclat.saveAllFrequentItemSet(fileName=savedFrequentItemSetFileName)
