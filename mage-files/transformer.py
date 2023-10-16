import pandas as pd
import math

if 'transformer' not in globals():
    from mage_ai.data_preparation.decorators import transformer
if 'test' not in globals():
    from mage_ai.data_preparation.decorators import test


@transformer
def transform(df, *args, **kwargs):
    """
    Template code for a transformer block.

    Add more parameters to this function if this block has multiple parent blocks.
    There should be one parameter for each output variable from each parent block.

    Args:
        data: The output from the upstream parent block
        args: The output from any additional upstream blocks (if applicable)

    Returns:
        Anything (e.g. data frame, dictionary, array, int, str, etc.)
    """
    # Specify your transformation logic here

    def haversine_distance(lat1, lon1, lat2, lon2):
    # Radius of the Earth in kilometers
        R = 6371.0

        # Convert latitude and longitude from degrees to radians
        lat1 = math.radians(lat1)
        lon1 = math.radians(lon1)
        lat2 = math.radians(lat2)
        lon2 = math.radians(lon2)

        # Haversine formula
        dlon = lon2 - lon1
        dlat = lat2 - lat1
        a = math.sin(dlat / 2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon / 2)**2
        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
        distance = R * c

        return distance

    df['distance_in_km'] = df.apply(lambda row: haversine_distance(row['start_lat'], row['start_lng'], row['end_lat'], row['end_lng']), axis=1)

    df['started_at'] = pd.to_datetime(df['started_at'])
    df['ended_at'] = pd.to_datetime(df['ended_at'])

    df = df.drop_duplicates().reset_index(drop=True)
    df['rent_id'] = df.index

    datetime_dim = df[['started_at', 'ended_at']].reset_index(drop=True)
    datetime_dim['started_at_datetime'] = datetime_dim['started_at']
    datetime_dim['started_at_hour'] = datetime_dim['started_at_datetime'].dt.hour
    datetime_dim['started_at_day'] = datetime_dim['started_at_datetime'].dt.day
    datetime_dim['started_at_month'] = datetime_dim['started_at_datetime'].dt.month
    datetime_dim['started_at_year'] = datetime_dim['started_at_datetime'].dt.year
    datetime_dim['started_at_weekday'] = datetime_dim['started_at_datetime'].dt.weekday

    datetime_dim['ended_at_datetime'] = datetime_dim['ended_at']
    datetime_dim['ended_at_hour'] = datetime_dim['ended_at_datetime'].dt.hour
    datetime_dim['ended_at_day'] = datetime_dim['ended_at_datetime'].dt.day
    datetime_dim['ended_at_month'] = datetime_dim['ended_at_datetime'].dt.month
    datetime_dim['ended_at_year'] = datetime_dim['ended_at_datetime'].dt.year
    datetime_dim['ended_at_weekday'] = datetime_dim['ended_at_datetime'].dt.weekday

    datetime_dim['datetime_id'] = datetime_dim.index

    datetime_dim = datetime_dim[['datetime_id','started_at_datetime','started_at_hour','started_at_day',
                            'started_at_month','started_at_year','started_at_weekday','ended_at_datetime',
                            'ended_at_hour','ended_at_day','ended_at_month','ended_at_year','ended_at_weekday']]
    
    ride_dim = df[['ride_id', 'rideable_type']].reset_index(drop=True)
    ride_dim['ride_index'] = ride_dim.index
    ride_dim = ride_dim[['ride_index','ride_id', 'rideable_type']]

    start_station_dim = df[['start_station_id','start_station_name','start_lat','start_lng']].reset_index(drop=True)
    start_station_dim['start_station_index'] = start_station_dim.index
    start_station_dim = start_station_dim[['start_station_index','start_station_id','start_station_name','start_lat','start_lng']]

    end_station_dim = df[['end_station_id','end_station_name','end_lat','end_lng']].reset_index(drop=True)
    end_station_dim['end_station_index'] = end_station_dim.index
    end_station_dim = end_station_dim[['end_station_index','end_station_id','end_station_name','end_lat','end_lng']]

    fact_table = df.merge(datetime_dim,left_on='rent_id',right_on='datetime_id')\
    .merge(ride_dim,left_on='rent_id',right_on='ride_index')\
    .merge(start_station_dim,left_on='rent_id',right_on='start_station_index')\
    .merge(end_station_dim,left_on='rent_id',right_on='end_station_index')\
    [['member_casual','datetime_id','ride_index','start_station_index','end_station_index','distance_in_km']]

    return {"datetime_dim":datetime_dim.to_dict(orient="dict"),
    "ride_dim":ride_dim.to_dict(orient="dict"),
    "start_station_dim":start_station_dim.to_dict(orient="dict"),
    "end_station_dim":end_station_dim.to_dict(orient="dict"),
    "fact_table":fact_table.to_dict(orient="dict")}


@test
def test_output(output, *args) -> None:
    """
    Template code for testing the output of the block.
    """
    assert output is not None, 'The output is undefined'
