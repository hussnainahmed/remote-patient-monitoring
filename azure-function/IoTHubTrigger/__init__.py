from typing import List
import logging
import azure.functions as func
import json
import datetime 
import psycopg2

CONNECTION = "dbname=shifarpm user=rpmadmin@rpmdb password=SHEC9pers2fas@spom host=rpmdb.postgres.database.azure.com port=5432 sslmode=require"
def main(events: List[func.EventHubEvent]):
    #create connection to db
    con = psycopg2.connect(CONNECTION)
    cur = con.cursor()
    SQL_CONT_VITALS = "INSERT INTO rpmc (recorded_at, device_id, temperature, oxygen_saturation, heart_rate, respiratory_rate ) VALUES (%s, %s, %s, %s, %s, %s);"
    SQL_NON_CONT_VITALS = "INSERT INTO rpmnc (recorded_at, device_id, bp_systolic, bp_diastolic) VALUES (%s, %s, %s, %s);"
    # process events
    for event in events:
        try:
            stream_data = json.loads(event.get_body().decode('utf-8'))
            stream_data['device_id'] = event.metadata['SystemPropertiesArray'][0]['iothub-connection-device-id']
            stream_data['recorded_at'] = datetime.datetime.fromtimestamp(stream_data['recorded_at']).strftime('%Y-%m-%d %H:%M:%S') 
            if "bp_systolic" in stream_data:
                data = (stream_data['recorded_at'], stream_data['device_id'], stream_data['bp_systolic'],stream_data['bp_diastolic'])
                cur.execute(SQL_NON_CONT_VITALS, data)
            else:  
                #logging.info(event.metadata['SystemPropertiesArray'])
                #logging.info(meta_data.SystemPropertiesArray.iothub-connection-device-id)
                #logging.info(stream_data)
                logging.info(stream_data)
                data = (stream_data['recorded_at'], stream_data['device_id'], stream_data['temperature'],stream_data['oxygen_saturation'],stream_data['heart_rate'],stream_data['respiratory_rate'])
                cur.execute(SQL_CONT_VITALS, data)
        except (Exception, psycopg2.Error) as error:
            logging.info(error)
    #close connection
    con.commit()
    con.close()


