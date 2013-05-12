from mk.com.dragan.utils.CsvUtils import readStringData
from mk.com.dragan.utils.DataUtils import getColumn, convertToNumbers


class ForexRateOldFormatReader(object):


    def __init__(self, currency, interval):
        fileName = '/Users/draganzahariev/Dropbox/Magisterska/data/forexrate.co.uk/' + interval + '/' + currency + '.csv'
        data = readStringData(fileName, ';')
        self.data = getColumn(data, 3)
        self.data = self.data[1:]
        self.data = convertToNumbers(self.data)
        dates = getColumn(data, 0)
        minutes = getColumn(data, 1)
        self.dates = []
        for d, m in zip(dates, minutes):
            self.dates.append(d + ' - ' + m)
        self.dates = self.dates[1:]

        assert len(data) == len(dates)

