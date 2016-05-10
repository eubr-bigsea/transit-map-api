# -*- coding: utf-8 -*-
import sqlite3
import os

DB_PATH = os.path.abspath(os.path.join(__file__, "../../../../gtfs.db"))


def select_column_and_value(cursor, sql, parameters=()):
    execute = cursor.execute(sql, parameters)
    result = []
    for row in cursor:
        result.append(
            {k[0]: v for k, v in list(zip(cursor.description, row))})
    return result


def get_trips_by_minute(hour_minute, service_ids=[]):
    """
    :argument hour_minute Hour plus minute for reference time (HHMM)
    :argument service_ids List of service ids to select trips. Empty means all
    services.
    :returns Trips found
    """
    seconds = int(hour_minute[:2]) * 3600 + int(hour_minute[2:]) * 60
    seconds_from_midnight = seconds + 24 * 3600

    conn = sqlite3.connect(DB_PATH)
    sql = """SELECT trip_id, route_short_name, route_long_name,
                    route_color, route_text_color, trip_headsign, shape_id,
                    service_id
            FROM trips, routes
            WHERE trips.route_id = routes.route_id
                AND (
                    (trip_start_seconds < ? AND trip_end_seconds > ?)
                    OR (trip_start_seconds < ? AND trip_end_seconds > ? ))
                    """
    cursor = conn.cursor()
    result = select_column_and_value(cursor, sql,
                                     [seconds, seconds, seconds_from_midnight,
                                      seconds_from_midnight])
    return result


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
    return select_column_and_value(cursor, sql, [trip_id])
