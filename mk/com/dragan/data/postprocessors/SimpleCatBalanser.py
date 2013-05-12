import logging

log = logging.getLogger('Simple Categories Balanser')

"""
    Data must be rows of input and the category as last element in the rows.
"""
class SimpleCatsBalanser(object):

    __result = None

    def getBalansed(self, data):
        zeros = []
        ones = []
        for i, row in enumerate(data):
            cat = row[-1]
            if cat == 0 or cat == 'A':
                zeros.append(i)
            elif cat == 1 or cat == 'B':
                ones.append(i)
            else:
                log.error('category found which is neither 0 nor 1, nor A or B')
        lz = len(zeros)
        lo = len(ones)
        if lz > lo:
            zeros = zeros[:lo]
        elif lo > lz:
            ones = ones[:lz]

        result = []
        for z, o in zip(zeros, ones):
            result.append(data[z])
            result.append(data[o])
        return result
