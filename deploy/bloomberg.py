# -*- coding: utf-8 -*-
"""
# ------------------------------ Bloomberg API ------------------------------ #
@author: QUAN YUAN
"""
import blpapi
import pandas as pd

class Blpy:
    '''
    Demo:
    test = Blp()
    data = test.history_data(security = '700 HK Equity', fields = ['px_last', 'volume'], \
                             start = '20180201', end = '', freq = 'DAILY')
    '''
    def __init__(self):
        pass        
    def history_data(self, security, fields, start, end, freq):
        '''
        security: string Bloomberg code
        fields: list[string] 'px_last'
        start: string '20180201'
        end: string '20180201'
        freq: string 'DAILY' 'WEEKLY'
        '''
        #start session
        session = blpapi.Session()
        if not session.start():
            print('Fail to start session')
        #open service
        if not session.openService('//blp/refdata'):
            print('Fail to open service')
        #get service
        service = session.getService('//blp/refdata')
        request = service.createRequest('HistoricalDataRequest')
        request = request
        
        request.append('securities', security)
        for each_field in fields: request.append('fields', each_field)
        request.set('startDate', start) 
        request.set('endDate', end)
        request.set('periodicityAdjustment', 'ACTUAL')
        request.set('periodicitySelection', freq) # DAILY
        session.sendRequest(request)
        
        alldata = pd.DataFrame(columns = fields + ['date'])
        endReached = False
        while not endReached:
            ev = session.nextEvent()
            if ev.eventType() == blpapi.Event.RESPONSE or ev.eventType() == blpapi.Event.PARTIAL_RESPONSE:
                for msg in ev:
                    securityData = msg.getElement('securityData').getElement("fieldData")
                    iNum = securityData.numValues()   #because there are several outputs, so need the iNum to loop through them
                    for i in range(iNum):
                        each_row = []
                        for each_field in fields + ['date']:
                            each_row.append(securityData.getValue(i).getElement(each_field).getValue())       
                        alldata.loc[i] = each_row
            if ev.eventType() ==blpapi.Event.RESPONSE:     
                endReached = True
                session.stop()
        return alldata
    
