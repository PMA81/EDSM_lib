# -*- coding: utf-8 -*-
"""
Created on Sat Sep  9 15:59:28 3303

@author: CMDR CodexNecro81


"""
import time
import urllib.parse
import urllib.request
import json

#endpoint = 'https://beta.edsm.net/'
endpoint = 'https://www.edsm.net/'

# return range with user defined increment
def range_step(start, end, step):
    while start <= end:
        yield start
        start += step

# Print iterations progress
def printProgressBar (iteration, total, prefix = '', suffix = '', decimals = 1, length = 100, fill = '█'):
    """
    Call in a loop to create terminal progress bar
    @params:
        iteration   - Required  : current iteration (Int)
        total       - Required  : total iterations (Int)
        prefix      - Optional  : prefix string (Str)
        suffix      - Optional  : suffix string (Str)
        decimals    - Optional  : positive number of decimals in percent complete (Int)
        length      - Optional  : character length of bar (Int)
        fill        - Optional  : bar fill character (Str)
    """
    percent = ("{0:." + str(decimals) + "f}").format(100 * (iteration / float(total)))
    filledLength = int(length * iteration // total)
    bar = fill * filledLength + '-' * (length - filledLength)
    print('\r%s |%s| %s%% %s' % (prefix, bar, percent, suffix), end = '\r')
    # Print New Line on Complete
    if iteration == total: 
        print()

def static_vars(**kwargs):
    def decorate(func):
        for k in kwargs:
            setattr(func, k, kwargs[k])
        return func
    return decorate

@static_vars(endpoints={})
def NiceRequest(url, param=''):
    bRepeat=True
    iRetry=10
    while bRepeat:
        try:
            if(url not in NiceRequest.endpoints):
                NiceRequest.endpoints[url]={'X-Rate-Limit-Limit':9999,'X-Rate-Limit-Remaining':9999,'X-Rate-Limit-Reset':0,'Last-Call':time.time(),'Throttle':0}
            else:
                if(NiceRequest.endpoints[url]['X-Rate-Limit-Remaining']<NiceRequest.endpoints[url]['X-Rate-Limit-Limit']/2):
                    if(NiceRequest.endpoints[url]['Throttle']<60):
                        NiceRequest.endpoints[url]['Throttle'] += 1
                else:
                    if(NiceRequest.endpoints[url]['Throttle']>0):
                        NiceRequest.endpoints[url]['Throttle'] -= 1
                if(NiceRequest.endpoints[url]['Throttle']>0):
                    time.sleep(max(0,NiceRequest.endpoints[url]['Throttle']-(time.time()-NiceRequest.endpoints[url]['Last-Call'])))
                        
            with urllib.request.urlopen(url, param.encode(encoding='UTF-8',errors='strict')) as response:
                html = response.read().decode("utf-8")
                if('X-Rate-Limit-Limit' in response.headers and
                   'X-Rate-Limit-Remaining' in response.headers and
                   'X-Rate-Limit-Reset' in response.headers):
                    NiceRequest.endpoints[url]['X-Rate-Limit-Limit'] = int(response.headers['X-Rate-Limit-Limit'])
                    NiceRequest.endpoints[url]['X-Rate-Limit-Remaining'] = int(response.headers['X-Rate-Limit-Remaining'])
                    NiceRequest.endpoints[url]['X-Rate-Limit-Reset'] = int(response.headers['X-Rate-Limit-Reset'])
                NiceRequest.endpoints[url]['Last-Call'] = time.time()
            bRepeat=False
        except Exception:
            if(iRetry>0):
                time.sleep(1)
                iRetry-=1
            else:
                raise
    return json.loads(html)

# Get Elite: Dangerous server status
def GetStatus():
    url = endpoint+'api-status-v1/elite-server'
    return NiceRequest(url)
      
# Get commander ranks
# Set commander ranks
# Get commander credits
# Set commander credits
# Set commander current ship id
# Update commander ship, or insert if not found.
# Sell commander ship id
# Get commander materials/encoded data/cargo
# Set commander materials/encoded data/cargo

#Set a flight log entry
#Delete a flight log entry
#Get flight log entries


#Get commander last position
def GetCMDRLastPosition(commanderName, apiKey='', showId='0', showCoordinates='0'):
    url = endpoint+'api-logs-v1/get-position/'
    param = urllib.parse.urlencode({'commanderName':commanderName,
                                    'apiKey':apiKey,
                                    'showId':showId,
                                    'showCoordinates':showCoordinates})
    return NiceRequest(url, param)


#Set/Update a comment
#Get a comment
#Get comments

#Get information about celestial bodies in a system
#Get information about stations in a system
#Get information about factions in a system
def GetFactionData(systemName, showHistory='0'):
    url = endpoint+'api-system-v1/factions/'
    param = urllib.parse.urlencode({'systemName':systemName,
                                    'showHistory':showHistory})
    return NiceRequest(url, param)

#Get information about a system
def GetSysData(systemName, showId='0', showCoordinates='0', showPermit='0', showInformation='0', showPrimaryStar='0', includeHidden='0'):
    url = endpoint+'api-v1/system/'
    param = urllib.parse.urlencode({'systemName':systemName,
                                    'showId':showId,
                                    'showCoordinates':showCoordinates,
                                    'showPermit':showPermit,
                                    'showInformation':showInformation,
                                    'showPrimaryStar':showPrimaryStar,
                                    'includeHidden':includeHidden})
    return NiceRequest(url, param)

#Get information about systems
def GetSystemsData(systemName, showId='0', showCoordinates='0', showPermit='0', showInformation='0', showPrimaryStar='0', includeHidden='0', onlyKnownCoordinates='0', onlyUnknownCoordinates='0'):
    url = endpoint+'api-v1/systems/'
    param = urllib.parse.urlencode({'systemName':systemName,
                                    'showId':showId,
                                    'showCoordinates':showCoordinates,
                                    'showPermit':showPermit,
                                    'showInformation':showInformation,
                                    'showPrimaryStar':showPrimaryStar,
                                    'includeHidden':includeHidden,
                                    'onlyKnownCoordinates':onlyKnownCoordinates,
                                    'onlyUnknownCoordinates':onlyUnknownCoordinates})
    return NiceRequest(url, param)

#Get information about a body
def GetBodyData(systemName):
    url = endpoint+'api-system-v1/bodies'
    param = urllib.parse.urlencode({'systemName':systemName})
    return NiceRequest(url, param)

#Get information about systems
#Get systems in a sphere radius
def GetSphereSystemsXYZ(x, y, z, radius, minRadius='0', showId='0', showCoordinates='0', showPermit='0', showInformation='0', showPrimaryStar='0'):
    url = endpoint+'api-v1/sphere-systems/'
    param = urllib.parse.urlencode({'x':x,
                                    'y':y,
                                    'z':z,
                                    'minRadius':minRadius,
                                    'radius':radius,
                                    'showId':showId,
                                    'showCoordinates':showCoordinates,
                                    'showPermit':showPermit,
                                    'showInformation':showInformation,
                                    'showPrimaryStar':showPrimaryStar})
    return NiceRequest(url, param)

def GetSphereSystemsName(systemName, radius, minRadius='0', showId='0', showCoordinates='0', showPermit='0', showInformation='0', showPrimaryStar='0'):
    url = endpoint+'api-v1/sphere-systems/'
    param = urllib.parse.urlencode({'systemName':systemName,
                                    'minRadius':minRadius,
                                    'radius':radius,
                                    'showId':showId,
                                    'showCoordinates':showCoordinates,
                                    'showPermit':showPermit,
                                    'showInformation':showInformation,
                                    'showPrimaryStar':showPrimaryStar})
    return NiceRequest(url, param)

#Get systems in a cube
def GetCubeSystemsXYZ(x, y, z, size, showId='0', showCoordinates='0', showPermit='0', showInformation='0', showPrimaryStar='0'):
    url = endpoint+'api-v1/cube-systems'
    param = urllib.parse.urlencode({'x':x,
                                    'y':y,
                                    'z':z,
                                    'size':size,
                                    'showId':showId,
                                    'showCoordinates':showCoordinates,
                                    'showPermit':showPermit,
                                    'showInformation':showInformation,
                                    'showPrimaryStar':showPrimaryStar})
    return NiceRequest(url, param)

def GetCubeSystemsName(systemName, size, showId='0', showCoordinates='0', showPermit='0', showInformation='0', showPrimaryStar='0'):
    url = endpoint+'api-v1/cube-systems'
    param = urllib.parse.urlencode({'systemName':systemName,
                                    'size':size,
                                    'showId':showId,
                                    'showCoordinates':showCoordinates,
                                    'showPermit':showPermit,
                                    'showInformation':showInformation,
                                    'showPrimaryStar':showPrimaryStar})
    return NiceRequest(url, param)


# Get station data
def GetStationsName(systemName):
    url = endpoint+'api-system-v1/stations'
    param = urllib.parse.urlencode({'systemName':systemName})
    return NiceRequest(url, param)

def GetStationsId(systemId):
    url = endpoint+'api-system-v1/stations'
    param = urllib.parse.urlencode({'systemId':systemId})
    return NiceRequest(url, param)
