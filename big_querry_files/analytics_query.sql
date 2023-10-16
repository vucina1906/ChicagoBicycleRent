create or replace table chicagobicyclerentusage.chicago_bicycle_rent_usage_dataset.tbl_analytics as (
select f.member_casual, d.started_at_datetime, d.ended_at_datetime, d.started_at_weekday, 
d.ended_at_weekday, r.rideable_type, s.start_station_name, s.start_lat, s.start_lng, e.end_station_name, e.end_lat, e.end_lng

from chicagobicyclerentusage.chicago_bicycle_rent_usage_dataset.fact_table as f 
inner join chicagobicyclerentusage.chicago_bicycle_rent_usage_dataset.datetime_dim as d on f.datetime_id = d.datetime_id
inner join chicagobicyclerentusage.chicago_bicycle_rent_usage_dataset.ride_dim as r on f.ride_index = r.ride_index
inner join chicagobicyclerentusage.chicago_bicycle_rent_usage_dataset.start_station_dim as s on f.start_station_index = s.start_station_index
inner join chicagobicyclerentusage.chicago_bicycle_rent_usage_dataset.end_station_dim as e on f.end_station_index = e.end_station_index)
