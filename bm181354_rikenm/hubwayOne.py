import urllib.request
import json
import pandas as pd
import dml
import prov.model
import datetime
import uuid

class hubwayOne(dml.Algorithm):
    contributor = 'bm181354_rikenm'
    reads = []
    writes = ['bm181354_rikenm.hubwayOne']
    
    @staticmethod
    def execute(trial = False):
        '''Retrieve some data sets (not using the API here for the sake of simplicity).'''
        startTime = datetime.datetime.now()
        
        # Set up the database connection.
        client = dml.pymongo.MongoClient()
        repo = client.repo
        repo.authenticate('bm181354_rikenm', 'bm181354_rikenm')
        
        # Dataset01
        url = 'http://datamechanics.io/data/bm181354_rikenm/201701-hubway-tripdata.csv'
 
        #hubway_df = pd.read_csv(url)
        # creating df that only contains city, total number of service, EMS_INDEX
        
#        if trial:
#            chunksize = 100
#            for chunk in pd.read_csv(url, chunksize=chunksize):
#                hubway_df = chunk
#        else:
        hubway_df = pd.read_csv(url)

   
        r = json.loads(hubway_df.to_json( orient='records'))
        s = json.dumps(r, sort_keys=False, indent=2)

        # clear
        repo.dropPermanent('hubwayOne')
        repo.createPermanent('hubwayOne')
        repo['bm181354_rikenm.hubwayOne'].insert_many(r)


        # logout
        repo.logout()
        endTime = datetime.datetime.now()
        return {"start":startTime, "end":endTime}
    
    @staticmethod
    def provenance(doc = prov.model.ProvDocument(), startTime = None, endTime = None):
        '''
            Create the provenance document describing everything happening
            in this script. Each run of the script will generate a new
            document describing that invocation event.
            '''
        
        # Set up the database connection.
        client = dml.pymongo.MongoClient()
        repo = client.repo
        
        repo.authenticate('bm181354_rikenm', 'bm181354_rikenm')
        doc.add_namespace('alg', 'http://datamechanics.io/?prefix=bm181354_rikenm/algorithm/') # The scripts are in <folder>#<filename> format.
        doc.add_namespace('dat', 'http://datamechanics.io/data/') # The data sets are in <user>#<collection> format.
        doc.add_namespace('ont', 'http://datamechanics.io/ontology#') # 'Extension', 'DataResource', 'DataSet', 'Retrieval', 'Query', or 'Computation'.
        doc.add_namespace('log', 'http://datamechanics.io/log/') # The event log.
        doc.add_namespace('bdp','http://datamechanics.io/?prefix=bm181354_rikenm/')
        
        this_script = doc.agent('alg:bm181354_rikenm#hubwayOne', {prov.model.PROV_TYPE:prov.model.PROV['SoftwareAgent'], 'ont:Extension':'py'})
        
        
        resource = doc.entity('bdp:201701-hubway-tripdata', {'prov:label':'dataset of hubway in Boston area', prov.model.PROV_TYPE:'ont:DataResource', 'ont:Extension':'csv'})
        
        get_hubwayOne = doc.activity('log:uuid'+str(uuid.uuid4()), startTime, endTime)
        
        doc.wasAssociatedWith(get_hubwayOne, this_script)
        
        #change this Done
        doc.usage(get_hubwayOne, resource, startTime, None,{prov.model.PROV_TYPE:'ont:Retrieval'})
                  
        hubwayOne = doc.entity('dat:bm181354_rikenm#hubwayOne', {prov.model.PROV_LABEL:'HubwayOne', prov.model.PROV_TYPE:'ont:DataSet'})
        
        doc.wasAttributedTo(hubwayOne, this_script)
        doc.wasGeneratedBy(hubwayOne, get_hubwayOne, endTime)
        doc.wasDerivedFrom(hubwayOne, resource, get_hubwayOne, get_hubwayOne, get_hubwayOne)
        
                  
        repo.logout()
        return doc

## eof


