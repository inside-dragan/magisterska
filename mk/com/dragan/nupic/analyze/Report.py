'''
Created on Aug 20, 2011

@author: dzaharie
'''
import logging
from nupic.bindings.network import CreateRuntimeNetwork, RuntimeRegion
from nupic.analysis import responses
from mk.com.dragan.nupic.config.ExecConfig import GENERATE_REPORTS
from mk.com.dragan.nupic.config.ResultContainer import ResultContainer


log = logging.getLogger('Report')

class Report():
    
    __trainedNetworkFile = None
    
    __levelNodes = None
    __topNode = None
    __folder = None
    
    def __init__(self, folder, levelNodes=["level1"], topNode="topNode"):
        self.__trainedNetworkFile = folder + "/network-trained.xml"
        self.__levelNodes = levelNodes
        self.__topNode = topNode
        self.__folder = folder
    
    def __writeGroups(self, out, node):
        out.write("*** GROUPS: " + str(responses.GetNumGroups(node)) + " ***\n")
        out.write("-----------------")
        Wd = responses.GetCoincidences(node).toDense()
        groups = responses.GetGroups(node)
        # Get each group
        for gindx, gg in enumerate(groups):
            lineText = "\n====> Group = " + str(gindx) + "\n"
            # For each group, get each coincidence index
            for cd in sorted(gg):
                lineText = lineText + '[' + str(cd) + ']: '
                # For each coincidence, print out each element
                for e in Wd[cd]:
                    if e == 0: 
                        lineText = lineText + '0'
                    elif e == 1: 
                        lineText = lineText + '1'
                    else: 
                        lineText = lineText + str(e)
                    lineText = lineText + ' '
                lineText = lineText + '\n'
            out.write(lineText)

    
    def __writeCoincidences(self, out, node, nodeName):
        coincs = responses.GetCoincidences(node).toDense()
        sizes = responses.GetCounts(node)
        
        ResultContainer().coincidences[nodeName] = {'num': responses.GetNumCoincidences(node), 'size-of-largest': max(sizes)}
        out.write("*** COINCIDENCES: " + str(responses.GetNumCoincidences(node)) + " ***\n\n")
        out.write('min number: ' + str(min(sizes)) + '\n')
        out.write('max number: ' + str(max(sizes)) + '\n')
        out.write('average: ' + str(float(sum(sizes)) / len(sizes)) + '\n')
        out.write("------------------------\n")
        
        for i in range(0, len(coincs)):
            out.write('[' + str(i) + ']' + ': appears ' + str(sizes[i]) + ' times \n')
#                      + self.__getListString(coincs[i]) + '\n')
        out.write('\n\n')
   
        
    def __getListString(self, listt):
        result = ''
        for l in listt:
            if l == 0 or l == 1:
                l = int(l)
            result = result + ' ' + str(l);
        return result
    
    def generateReport(self):
        if GENERATE_REPORTS:
            runtimeNet = CreateRuntimeNetwork(self.__trainedNetworkFile)
            
            for levelNode in self.__levelNodes:
                filename = self.__folder + "/report-" + levelNode + ".txt"
                out = open(filename, 'w')
                node = runtimeNet[levelNode]
                if isinstance(node, RuntimeRegion): 
                    node = node[0]
                #write information
                self.__writeCoincidences(out, node, levelNode)
                self.__writeGroups(out, node)
                out.close()
                log.info(filename + " created.")
            
            filename = self.__folder + "/report-" + self.__topNode + ".txt"
            out = open(filename, 'w')
            node = runtimeNet[self.__topNode]
            if isinstance(node, RuntimeRegion): 
                node = node[0]
            self.__writeCoincidences(out, node, self.__topNode)
            out.close()
            log.info(filename + " created.")
            
            runtimeNet.cleanupBundleWhenDone()    
