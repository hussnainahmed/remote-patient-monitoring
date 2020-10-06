import datetime 
import psycopg2
import json
import datetime 

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

def main():
    print("Hello World!")
    con = psycopg2.connect(CONNECTION)
    cur = con.cursor()
    SQL = "INSERT INTO rpm_data (recorded_at, device_id, rented_to_uid, rented_to_name,vital_type, vital_value) VALUES (%s, %s, %s, %s, %s, %s);"
    dev_id = 'rpm-pbi-dev-1'
    user_id,user_name = get_user_info(con, dev_id)
    if user_id != "null":
        print(user_id + ',' + user_name)
    else:
        print("device not rented to any user")
    stream_data = {"recorded_at": 1602014383.985482,"temperature": 36.13,"oxygen_saturation": 97, "heart_rate": 144,"respiratory_rate": 12}
   # stream_data = {"recorded_at": 1602014383.985482,"bp_systolic": 117,"bp_diastolic": 75}
    
    #stream_data = json.loads(s) , bp_diastolic
    recorded_at = datetime.datetime.fromtimestamp(stream_data['recorded_at']).strftime('%Y-%m-%d %H:%M:%S')
    stream_data.pop('recorded_at', None)
    # device_id, rented_to_uid, rented_to_name

    

    for key in stream_data:
        data = (recorded_at, dev_id, user_id ,user_name,key,stream_data[key])
        cur.execute(SQL, data)
        print(data)
   # print(records_list)
    
    #
    con.commit()
    cur.close()
    con.close()

if __name__ == "__main__":
    main()