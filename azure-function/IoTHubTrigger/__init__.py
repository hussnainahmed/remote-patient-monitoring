from typing import List
import logging
import azure.functions as func
import json
import datetime 
import psycopg2

CONNECTION = "dbname=shifarpm user=rpmadmin@rpmdb password=SHEC9pers2fas@spom host=rpmdb.postgres.database.azure.com port=5432 sslmode=require"

def get_user_info(con,dev_id):
    try:
        cursor = con.cursor()
        postgreSQL_select_Query = "SELECT * FROM device_rentals WHERE device_id = %s AND (is_returned = FALSE OR is_returned IS NULL) ORDER BY rented_at DESC LIMIT 1"

        cursor.execute(postgreSQL_select_Query, (dev_id,))
        rental_record = cursor.fetchall()
        if len(rental_record) > 0:
            for row in rental_record:
                user_id = row[2]
                user_name = row[3]
        else:
            user_id = "null"
            user_name = "null"

    except (Exception, psycopg2.Error) as error:
        print("Error fetching data from PostgreSQL table", error)

    finally:
        cursor.close()
    return user_id,user_name

def main(events: List[func.EventHubEvent]):
    #create connection to db
    con = psycopg2.connect(CONNECTION)
    
    #SQL_CONT_VITALS = "INSERT INTO rpmc (recorded_at, device_id, temperature, oxygen_saturation, heart_rate, respiratory_rate ) VALUES (%s, %s, %s, %s, %s, %s);"
    #SQL_NON_CONT_VITALS = "INSERT INTO rpmnc (recorded_at, device_id, bp_systolic, bp_diastolic) VALUES (%s, %s, %s, %s);"
    SQL = "INSERT INTO rpm_data (recorded_at, device_id, rented_to_uid, rented_to_name,vital_type, vital_value) VALUES (%s, %s, %s, %s, %s, %s);"
 
    cur = con.cursor()
    # process events
    for event in events:
        try:
            stream_data = json.loads(event.get_body().decode('utf-8'))
            dev_id =  event.metadata['SystemPropertiesArray'][0]['iothub-connection-device-id']
            #stream_data['device_id'] = dev_id
            recorded_at = datetime.datetime.fromtimestamp(stream_data['recorded_at']).strftime('%Y-%m-%d %H:%M:%S')
            stream_data.pop('recorded_at', None)
            user_id,user_name = get_user_info(con,dev_id)
            if user_id != "null":
                for key in stream_data:
                    data = (recorded_at, dev_id, user_id ,user_name,key,stream_data[key])
                    cur.execute(SQL, data)
            else:
                logging.error("Device not rented to any user. Please check in EMR if the device is created and assigned,rented to the user")  
            
            '''
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
            '''
        except (Exception, psycopg2.Error) as error:
            logging.info(error)
    #close connection
    con.commit()
    cur.close()
    con.close()


