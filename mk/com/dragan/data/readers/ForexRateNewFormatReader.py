from mk.com.dragan.utils.CsvUtils import readStringData
from mk.com.dragan.utils.DataUtils import getColumn, convertToNumbers


class ForexRateNewFormatReader(object):
    def __init__(self, currency, interval):
        fileName = 'C:/Users/Dragan/Dropbox/Magisterska/data/forexrate.co.uk/' + interval + '2/' + currency + '.csv'
        data = readStringData(fileName, delimiter=',')
        self.data = getColumn(data, 1)
        self.data = self.data[1:]
        self.data = convertToNumbers(self.data)

        self.dates = getColumn(data, 0)
        self.dates = self.dates[1:]

        assert len(self.data) == len(self.dates)

