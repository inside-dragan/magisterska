'''
Created on Dec 27, 2011

@author: dzaharie
'''
from create_data_oldtype import createRowPerDay, readCategories, addCategories, \
    transpose, modifyToDifferencesToLast, normalize, createInputCat
inputFile = 'C:/Users/dzaharie/Dropbox/Magisterska/data/forextester.com/EURUSD/EURUSD-07-08.csv'
path = 'C:/Users/dzaharie/Dropbox/Magisterska/analizi/cetvrta/2007-2008/4x3'
categoriesFile = 'C:/Users/dzaharie/Dropbox/Magisterska/data/forextester.com/EURUSD/per-day-categories.csv'


createRowPerDay(inputFile, path + '/row-per-day.csv', 120000, 125900)
categories = readCategories(categoriesFile)
addCategories(path + '/row-per-day.csv', categories, path + '/row-per-day-with-cats.csv')
transpose(path + '/row-per-day-with-cats.csv', 13, path + '/input-original-values.csv')
modifyToDifferencesToLast(path + '/input-original-values.csv', path + '/input-differences.csv')
normalize(path + '/input-differences.csv', path + '/input-diff-normalized.csv')
createInputCat(path + '/input-diff-normalized.csv', path + '/input.csv', path + '/cat.csv')
