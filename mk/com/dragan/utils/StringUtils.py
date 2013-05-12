'''
Created on Oct 2, 2011

@author: Dragan
'''
def after(s,pat):
    #returns the substring after pat in s.
    #if pat is not in s, then return a null string!
    pos =s.find(pat)
    if pos != -1:
        return s[pos+len(pat):]
    return "" 
 
 
def rafter(s,pat):
    #returns the substring after pat in s.
    #if pat is not in s, then return a null string!
    pos =s.rfind(pat)
    if pos != -1:
        return s[pos+len(pat):]
    return ""
 
 
def before(s, pat):
    #returns the substring before pat in s.
    #if pat is not in s, then return a null string!
    pos =s.find(pat)
    if pos != -1:
        return s[:pos]
    return ""
 
 
def rbefore(s, pat):
    #returns the substring before pat in s.
    #if pat is not in s, then return a null string!
    pos =s.rfind(pat)
    if pos != -1:
        return s[:pos+len(pat)]
    return ""
 
 
def between(s, bpat, apat):
    # returns substring between bpat and apat in s.
    # if bpat or apat is not in s, then return a null string.
    start = s.find(bpat)
    if start != -1:
        end = s[start+len(bpat):].find(apat)
        if end != -1:
            return s[start+len(bpat):start+len(bpat)+end] 
        return ""
    return ""
 
def rbetween(s, bpat, apat):
    # returns substring between bpat and apat in s.
    # if bpat or apat is not in s, then return a null string.
    end  = s.rfind(apat)
    if end != -1:
        before= s[:end].rfind(bpat)
        if before != -1:
            return s[before+len(bpat):end] 
        return ""
    return ""