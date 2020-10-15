import datetime
import logging
import azure.functions as func
import psycopg2
import json

import time

CONNECTION = "dbname=shifarpm user=rpmadmin@rpmdb password=SHEC9pers2fas@spom host=rpmdb.postgres.database.azure.com port=5432 sslmode=require"


def get_device_list(con):
    try:
        cursor = con.cursor()
        postgreSQL_select_Query = "SELECT device_id FROM device_rentals WHERE is_returned = FALSE OR is_returned IS NULL"

        cursor.execute(postgreSQL_select_Query)
        rental_active_users = cursor.fetchall()
        active_user_list = []
        for row in rental_active_users:
            active_user_list.append(row[0])
    except (Exception, psycopg2.Error) as error:
        logging.error("Error fetching data from PostgreSQL table ," + error)

    finally:
        cursor.close()
    return active_user_list

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
        logging.error("Error fetching data from PostgreSQL table, " + error)

    finally:
        cursor.close()
    return user_id,user_name

def get_user_latest_vitals(con,dev_id):
    vitals_to_check = ["temperature","respiratory_rate","heart_rate","oxygen_saturation","bp_systolic","bp_diastolic","consciousness"]
    user_id,user_name = get_user_info(con, dev_id)
    vitals = {} 
    vitals_list = []
    try:
        cursor = con.cursor()
        for vital in vitals_to_check:
            postgreSQL_select_Query = "select vital_value from rpm_data where device_id = %s and rented_to_uid = %s and vital_type = %s order by recorded_at desc limit 1"  

            cursor.execute(postgreSQL_select_Query, (dev_id,user_id,vital))
            data_records = cursor.fetchall()
            
            for row in data_records:
                vitals = {} 
                vitals['key'] = vital
                vitals['value'] = row[0]
            vitals_list.append(vitals)


    except (Exception, psycopg2.Error) as error:
        logging.error("Error fetching data from PostgreSQL table, " + error)

    finally:
        cursor.close()
    
    temperature = vitals_list[0]['value']
    respiratory_rate = vitals_list[1]['value']
    heart_rate = vitals_list[2]['value']
    oxygen_saturation = vitals_list[3]['value']
    bp_systolic = vitals_list[4]['value']
    bp_diastolic = vitals_list[5]['value']
    consciousness = vitals_list[6]['value']

    return user_id,user_name,temperature,respiratory_rate,heart_rate,oxygen_saturation,bp_systolic,bp_diastolic,consciousness

def get_mew_score(temperature,respiratory_rate,heart_rate,oxygen_saturation,bp_systolic,bp_diastolic,consciousness):
    mews = 0
    try:
        if temperature < 35.0:
            temp_score = 2
        elif temperature >= 38.5:
            temp_score = 2
        else:
             temp_score = 0
        mews += temp_score
    except Exception as e:
        logging.error(str(e))
    
    try:
        if bp_systolic <= 70:
            systolic_score = 3
        elif bp_systolic >= 200:
            systolic_score = 2
        elif 71 <= bp_systolic <= 80:
            systolic_score = 2
        elif 81 <= bp_systolic <= 100:
            systolic_score = 2
        else:
             systolic_score = 0
        mews += systolic_score
    except Exception as e:
        logging.error(str(e))
    
    try:
        if heart_rate <= 40:
            hr_score = 2
        elif heart_rate >= 130:
            hr_score = 3
        elif 41 <= heart_rate <= 50:
            hr_score = 1
        elif 101 <= heart_rate <= 110:
            hr_score = 1
        elif 111 <= heart_rate <= 129:
            hr_score = 2
        else:
             hr_score = 0
        mews += hr_score
    except Exception as e:
        logging.error(str(e))

    try:
        if respiratory_rate < 9:
            resprate_score = 2
        elif respiratory_rate >= 30:
            resprate_score = 3
        elif 15 <= respiratory_rate <= 20:
            resprate_score = 1
        elif 21 <= respiratory_rate <= 29:
            resprate_score = 2
        else:
             resprate_score = 0
        mews += resprate_score
    except Exception as e:
        logging.error(str(e))

    try:
        if consciousness == 2:
            cons_score = 1
        elif consciousness == 3:
            cons_score = 2
        elif consciousness == 4:
            cons_score = 3
        else:
            cons_score = 0
        mews += cons_score
    except Exception as e:
        logging.error(str(e))

    try:
        if oxygen_saturation >= 96:
            oxy_score = 0
        elif 94 <= oxygen_saturation <= 95:
            oxy_score = 1
        elif 92 <= oxygen_saturation <= 93:
            oxy_score = 2
        elif oxygen_saturation <= 91:
            oxy_score = 3
        mews += oxy_score
    except Exception as e:
        logging.error(str(e))

    return mews


def main(mytimer: func.TimerRequest) -> None:
    con = psycopg2.connect(CONNECTION)
    cur = con.cursor()
    SQL = "INSERT INTO rpm_data (recorded_at, device_id, rented_to_uid, rented_to_name,vital_type, vital_value) VALUES (%s, %s, %s, %s, %s, %s);"
    dev_id_list = get_device_list(con)
    recorded_at = datetime.datetime.fromtimestamp(int(time.time())).strftime('%Y-%m-%d %H:%M:%S')
    key = 'mew_score'
    #print(dev_id_list)
    for dev_id in dev_id_list:
        try:
            user_id,user_name,temperature,respiratory_rate,heart_rate,oxygen_saturation,bp_systolic,bp_diastolic,consciousness = get_user_latest_vitals(con,dev_id)
            score = get_mew_score(temperature,respiratory_rate,heart_rate,oxygen_saturation,bp_systolic,bp_diastolic,consciousness)
            #print(dev_id + "," + str(get_user_latest_vitals(con,dev_id)))
            data = (recorded_at, dev_id, user_id ,user_name,key,float(score))
            cur.execute(SQL, data)
            logging.info(data)
        except:
            pass
    
    con.commit()
    cur.close()
    con.close()
