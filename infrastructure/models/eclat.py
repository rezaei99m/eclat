from domain.entity.eclat_entity import ECLATEntity
from itertools import chain, combinations


class ECLAT(ECLATEntity):

    def __init__(self, data, minSupport):
        super().__init__(data, minSupport)
        self.allFrequentItemSet = []

    def run(self):
        allFrequentItemSet = {}
        # {
        #   '1': [ [['I1'], [0, 1, 2, 3]], [['I2'] ,[2, 3, 5, 6]]],
        #   '2': [ [['I1', 'I2'], [2, 3]], ],
        #   ...
        # }

        invertedDatasetDict = self.__invertDataset()

        allFrequentItemSet['1'] = []
        for item in invertedDatasetDict.keys():
            if len(invertedDatasetDict[item]) >= self.minSupport:
                frequentItemSetList = [[], []]
                frequentItemSetList[0].append(item)
                frequentItemSetList[1] = list(invertedDatasetDict[item])
                allFrequentItemSet['1'].append(frequentItemSetList)

        allSubset = self.__allSubset(list(invertedDatasetDict.keys()))

        _1FrequentItemSet = []
        for itemSet in allFrequentItemSet['1']:
            _1FrequentItemSet.append(itemSet[0][0])

        k = 2
        while True:
            kMemberSubSet = []
            allFrequentItemSet[str(k)] = []
            if k > len(list(invertedDatasetDict.keys())):
                break
            for subset in allSubset:
                if len(subset) == k:
                    kMemberSubSet.append(subset)

            for subset in kMemberSubSet:
                # First: check if all single item in subset are frequent. if not then go to next subset
                # Second: find intersection list of all subset items and check
                # Third: check if len of the previous step is greater or equal to minSupport. if not then go to next
                #        subset.
                # Fourth: Then create list of list of found frequent subset like the format under "allFrequentItemSet"
                # Fifth: Then append previous list to allFrequentItemSet in the "k" key

                areAllItemInSubsetFrequent = True
                for item in subset:
                    if item not in _1FrequentItemSet:
                        areAllItemInSubsetFrequent &= False
                        break

                if not areAllItemInSubsetFrequent:
                    continue

                allSingleItemTransaction = []
                for item in subset:
                    for i in range(0, len(allFrequentItemSet['1'])):
                        if allFrequentItemSet['1'][i][0][0] == item:
                            allSingleItemTransaction.append(allFrequentItemSet['1'][i][1])

                if len(allSingleItemTransaction) > 0:
                    intersections = set(allSingleItemTransaction[0]).intersection(*allSingleItemTransaction)
                    if len(intersections) >= self.minSupport:
                        allFrequentItemSet[str(k)].append([list(subset), list(intersections)])
                    else:
                        continue
                else:
                    continue

            k += 1
        self.allFrequentItemSet = allFrequentItemSet

    def saveAllFrequentItemSet(self, fileName: str):
        with open('{0}.txt'.format(fileName), 'w') as txtFile:
            txtFile.write('minSupport is {0}. \n'.format(self.minSupport))
            for key in self.allFrequentItemSet:
                if len(self.allFrequentItemSet[key]) > 0:
                    txtFile.write('.::::::::::::::::::::::::::::::::::::::::::::::: {0}-item sets '
                                  ':::::::::::::::::::::::::::::::::::::::::::::::. \n'.format(key))
                    for frequentItemSet in self.allFrequentItemSet[key]:
                        txtFile.write('{0} is in {1} transactions.'.format(frequentItemSet[0], len(frequentItemSet[1])))
                        txtFile.write('\n')
        print('all extracted frequent patterns saved into {0}.txt'.format(fileName))

    def __invertDataset(self) -> dict:
        invertedDataset = {}
        # invertedDataset format
        # {
        #   'I1': [0, 1, 2, 3],
        #   'I2': [1, 4, 5],
        #   ...
        # }
        for i in range(0, len(self.data)):
            for item in self.data[i]:
                if str(item) not in invertedDataset:
                    invertedDataset[str(item)] = []

        for i in range(0, len(self.data)):
            for item in invertedDataset.keys():
                if item in self.data[i]:
                    invertedDataset[item].append(i+1)

        return invertedDataset

    def __allSubset(self, data: list) -> list:
        return list(chain.from_iterable(combinations(data, r) for r in range(len(data) + 1)))
