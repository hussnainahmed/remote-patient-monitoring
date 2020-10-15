SELECT * FROM pg_stat_activity;

select recorded_at,rented_to_uid,rented_to_name, array_agg(vital_type) as keys, array_agg(vital_value) as values from rpm_data group by recorded_at,rented_to_uid,rented_to_name order by recorded_at desc limit 4;

select recorded_at,rented_to_uid,rented_to_name,device_id, array_agg(vital_type) as keys, array_agg(vital_value) as values from rpm_data where device_id = 'rpm-pbi-dev-1' group by recorded_at,rented_to_uid,rented_to_name,device_id order by recorded_at desc limit 1;

select vital_value from rpm_data where device_id = 'rpm-pbi-dev-1' and rented_to_uid = '100001' and vital_type = 'temperature' order by recorded_at desc limit 1


SELECT
  recorded_at AS "time",
  (COALESCE(temp_mew,0) + COALESCE(hr_mew,0) + COALESCE(hr_mew,0) ) AS mews_score FROM
  (
  SELECT
  recorded_at,
  case
        when temperature < 35.00 then 2
        when temperature BETWEEN 35.00 AND 38.40 then 0
        when temperature > 38.4 then 2
    end as temp_mew,
  case
        when heart_rate < 40 then 2
        when heart_rate BETWEEN 41 AND 50 then 1
        when heart_rate BETWEEN 51 AND 100 then 0
        when heart_rate BETWEEN 101 AND 110 then 1
        when heart_rate BETWEEN 111 AND 129 then 2
        when heart_rate > 130 then 3
    end as hr_mew,
    case
        when oxygen_saturation < 90 then 2
        when oxygen_saturation BETWEEN 90 AND 94 then 1
        when oxygen_saturation >= 95 then 0
    end as oxy_mew
  FROM rpmc where device_id = 'rpm-dev-1' order by recorded_at desc limit 1
  )a
  
WHERE
  $__timeFilter(recorded_at)
ORDER BY 1

SELECT
  recorded_at AS "time",
  case
    when vital_value = '1' then "Alert"
    when vital_value = '2' then "Reacts to voice"
    when vital_value = '3' then "Reacts to Pain"
    when vital_value = '4' then "Unresponsive"
    end as consciousness
FROM rpm_data
WHERE
  vital_type = 'consciousness' AND 
  device_id = 'rpm-dev-1' AND
  $__timeFilter(recorded_at)
ORDER BY 1,2


SELECT
  recorded_at,vital_value,
  case
        when vital_value = 1 then 'Alert'
        when vital_value = 2 then 'Reacts to voice'
        when vital_value = 3 then 'Reacts to pain'
        when vital_value = 4 then 'Unresponsive'
    end as avpu
  FROM rpm_data where device_id = 'rpm-dev-1' and vital_type = 'consciousness' order by recorded_at desc limit 1;

SELECT
  recorded_at AS "time",
  avpu
  FROM
  (
  SELECT
  recorded_at,vital_value,
  case
        when vital_value = 1 then 'Alert'
        when vital_value = 2 then 'Reacts to voice'
        when vital_value = 3 then 'Reacts to pain'
        when vital_value = 4 then 'Unresponsive'
    end as avpu
  FROM rpm_data where device_id = 'rpm-dev-1' and vital_type = 'consciousness' order by recorded_at desc limit 1
  )a
  
WHERE
  $__timeFilter(recorded_at)
ORDER BY 1,2