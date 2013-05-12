'''
Created on Jun 6, 2012

@author: dzaharie
'''

o = open('C:/data/svn/assembla/magisterska/src/generated-result/result-min.txt', 'w')
f = open('C:/data/svn/assembla/magisterska/src/generated-result/result.txt')
for line in f:
    if not line.startswith('0') and not line.startswith('1') and not line.startswith('2'):
        o.write(line)
f.close()
o.close()
