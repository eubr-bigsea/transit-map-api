# -*- coding: utf-8 -*-
import os
import sqlite3

from bigsea.transitmap import dbutil

DB_PATH = os.path.abspath(os.path.join(__file__, "../../../../gtfs.db"))


def get_services_ids():
    return []


def render_time(hms):
    """
    FIXME
    :argument hms Hour, minute, second
    """
    return hms


def get_trips_by_minute(hour_minute):
    """
    :argument hour_minute Hour plus minute for reference time (HHMM)
    :returns Trips found
    """

    service_ids = get_services_ids()
    trips = dbutil.get_trips_by_minute(hour_minute, service_ids)
    new_trips = []

    for i, row in enumerate(trips):
        trip = {'deps': [], 'arrs': [], 'sts': [], 'id': row['trip_id'],
                'stops': [],
                'name': row['route_short_name'], 'edges': []}
        stops = dbutil.get_stops_by_trip_id(row['trip_id'])
        edges = []
        for stop in stops:
            trip['deps'].append(stop['departure_time'])
            trip['arrs'].append(stop['arrival_time'])
            trip['sts'].append(stop['stop_id'])
            trip['stops'].append(stop)

        trip['trip_id'] = row['trip_id']
        trip['route_short_name'] = row['route_short_name']
        trip['shape_id'] = row['shape_id']
        trip['type'] = row['route_color']
        trip['service_type'] = 'd'
        new_trips.append(trip)

    return new_trips


def get_stops_by_trip_id(trip_id):
    """
    TODO: Avaliar se dá para fazer com um select apenas
    :argument trip_id Trip identifier
    """
    conn = sqlite3.connect(DB_PATH)
    sql = """SELECT stops.stop_id, stops.stop_name, arrival_time,
                    departure_time, stop_shape_percent
            FROM stop_times, stops
            WHERE stops.stop_id = stop_times.stop_id
                AND stop_times.trip_id = ? ORDER BY stop_sequence;"""
    cursor = conn.cursor()
    cursor.execute(sql, [trip_id])
    result = []
    for row in cursor:
        result.append(row)

    return result
