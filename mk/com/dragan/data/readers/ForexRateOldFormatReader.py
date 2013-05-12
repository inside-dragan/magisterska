from mk.com.dragan.utils.CsvUtils import readStringData
from mk.com.dragan.utils.DataUtils import getColumn, convertToNumbers


class ForexRateOldFormatReader(object):

    __dates = None
    __data = None

    def __init__(self, currency, interval):

        fileName = '/Users/draganzahariev/Dropbox/Magisterska/data/forexrate.co.uk/' + interval + '/' + currency + '.csv'
        data = readStringData(fileName, ';')
        self.__data = getColumn(data, 3)
        self.__data = self.__data[1:]
        self.__data = convertToNumbers(self.__data)
        dates = getColumn(data, 0)
        minutes = getColumn(data, 1)
        self.__dates = []
        for d, m in zip(dates, minutes):
            self.__dates.append(d + ' - ' + m)
        self.__dates = self.__dates[1:]
