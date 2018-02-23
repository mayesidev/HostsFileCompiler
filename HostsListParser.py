import urllib.request
import re

def ParseHostsFileLine(hostsFileLine):
    # ip hostname alias|comment
    # ip hostname
    # hostname alias|comment
    # hostname
    # ip
    lineContainsComment = hostsFileLine.find('#')
    if(lineContainsComment>0):
        hostsFileLine = hostsFileLine[0:lineContainsComment]
    
    lineData = hostsFileLine.split()
    # NOTE: For now, if the string contains a colon (':'), it's considered an IPv6 address.
    # TODO: May need a real IPv6 regex if we want to validate/store those at some point...
    ipVFourRegex = r'((([2][5][0-5]|[2][0-4]\d|[1]\d{2}|\d{1,2})\.){3})([2][5][0-5]|[2][0-4]\d|[1]\d{2}|\d{1,2}(\D|$)){1}'
    if((len(lineData) > 1) and ((':' in lineData[0]) or re.match(ipVFourRegex, lineData[0]))):
        domain = lineData[1]
    else:
        domain = lineData[0]
    return domain

def ParseHostsFile(hostsFileUrl):
    hostsFile = urllib.request.urlopen(hostsFileUrl)
    domainSet = set()
    for line in hostsFile:
        # ignore blank lines and comments
        strippedLine = line.strip()
        if(not strippedLine or strippedLine.startswith(b'#')):
            continue
        else:
            domainSet.add(ParseHostsFileLine(str(line,'utf-8')))
    return domainSet

def ParseListFile(listFileUrl):
    listFile = urllib.request.urlopen(listFileUrl)
    parsedDomainSet = set()
    for url in listFile:
        # ignore blank lines and comments
        strippedUrl = url.strip()
        if(not strippedUrl or strippedUrl.startswith(b'#')):
            continue
        else:
            parsedDomainSet = parsedDomainSet|ParseHostsFile(str(url,'utf-8'))
    return parsedDomainSet


# Test url to a file containing a relatively small list of valid host files with various formats...
filePath = "https://raw.githubusercontent.com/pi-hole/pi-hole/master/adlists.default"
for val in ParseListFile(filePath):
    print(val)
