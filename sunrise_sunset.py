# -*- coding: utf-8 -*-

"""
This module is a wrapper to compute sunset and sunrise for a given day,
location, and zenith value. Sunset and sunrise are returned for the local time
zone.
"""

import math
import datetime

CIVIL_ZENITH = 90.83333 # civil

class SunriseSunset(object):
    """
    This class wraps the computation for sunset and sunrise. It relies on the
    datetime class as input and output.
    """
    def __init__(self, dt, latitude, longitude, localOffset=0, zenith=None):
        self.dt          = dt.replace(hour=0, minute=0, second=0, microsecond=0)
        if latitude < -90 or latitude > 90:
            raise ValueError('Invalid latitude value')
        if longitude < -180 or longitude > 180:
            raise ValueError('Invalid longitude value')
        if localOffset < -12 or localOffset > 14:
            raise ValueError('Invalid localOffset value')
        self.latitude    = latitude
        self.longitude   = longitude
        self.localOffset = localOffset
        self.zenith      = zenith if zenith is not None else CIVIL_ZENITH

    # ALGORITHM

    def calculate(self):
        """Computes the sunset and sunrise for the current day, in local time"""
        # Calculate the day of the year
        N = self.dt.timetuple().tm_yday

        # Convert the longitude to hour value and calculate an approximate time
        lngHour = self.longitude / 15
        t_rise = N + ((6 - lngHour) / 24)
        t_set = N + ((18 - lngHour) / 24)

        # Calculate the Sun's mean anomaly
        M_rise = (0.9856 * t_rise) - 3.289
        M_set = (0.9856 * t_set) - 3.289

        # Calculate the Sun's true longitude, and adjust angle to be between 0
        # and 360
        L_rise = (M_rise + (1.916 * math.sin(math.radians(M_rise))) + (0.020 * math.sin(math.radians(2 * M_rise))) + 282.634) % 360
        L_set = (M_set + (1.916 * math.sin(math.radians(M_set))) + (0.020 * math.sin(math.radians(2 * M_set))) + 282.634) % 360

        # Calculate the Sun's right ascension, and adjust angle to be between 0 and
        # 360
        RA_rise = (math.degrees(math.atan(0.91764 * math.tan(math.radians(L_rise))))) % 360
        RA_set = (math.degrees(math.atan(0.91764 * math.tan(math.radians(L_set))))) % 360

        # Right ascension value needs to be in the same quadrant as L
        Lquadrant_rise  = (math.floor(L_rise/90)) * 90
        RAquadrant_rise = (math.floor(RA_rise/90)) * 90
        RA_rise = RA_rise + (Lquadrant_rise - RAquadrant_rise)

        Lquadrant_set  = (math.floor(L_set/90)) * 90
        RAquadrant_set = (math.floor(RA_set/90)) * 90
        RA_set = RA_set + (Lquadrant_set - RAquadrant_set)

        # Right ascension value needs to be converted into hours
        RA_rise = RA_rise / 15
        RA_set = RA_set / 15

        # Calculate the Sun's declination
        sinDec_rise = 0.39782 * math.sin(math.radians(L_rise))
        cosDec_rise = math.cos(math.asin(sinDec_rise))

        sinDec_set = 0.39782 * math.sin(math.radians(L_set))
        cosDec_set = math.cos(math.asin(sinDec_set))

        # Calculate the Sun's local hour angle
        cos_zenith = math.cos(math.radians(self.zenith))
        radian_lat = math.radians(self.latitude)
        sin_latitude = math.sin(radian_lat)
        cos_latitude = math.cos(radian_lat)
        cosH_rise = (cos_zenith - (sinDec_rise * sin_latitude)) / (cosDec_rise * cos_latitude)
        cosH_set = (cos_zenith - (sinDec_set * sin_latitude)) / (cosDec_set * cos_latitude)

        # Finish calculating H and convert into hours
        H_rise = (360 - math.degrees(math.acos(cosH_rise))) / 15
        H_set = math.degrees(math.acos(cosH_set)) / 15

        # Calculate local mean time of rising/setting
        T_rise = H_rise + RA_rise - (0.06571 * t_rise) - 6.622
        T_set = H_set + RA_set - (0.06571 * t_set) - 6.622

        # Adjust back to UTC, and keep the time between 0 and 24
        UT_rise = (T_rise - lngHour) % 24
        UT_set = (T_set - lngHour) % 24

        # Convert UT value to local time zone of latitude/longitude
        localT_rise = (UT_rise + self.localOffset) % 24
        localT_set = (UT_set + self.localOffset) % 24

        # Conversion
        h_rise = int(localT_rise)
        m_rise = int(localT_rise % 1 * 60)
        h_set = int(localT_set)
        m_set = int(localT_set % 1 * 60)

        # Create datetime objects with same date, but with hour and minute
        # specified
        rise_dt = self.dt.replace(hour=h_rise, minute=m_rise)
        set_dt = self.dt.replace(hour=h_set, minute=m_set)
        return rise_dt, set_dt

if __name__ == "__main__":
    # INPUTS
    # Date -- uses current date
    # Longitude and latitude
    latitude = 46.805
    longitude = -71.2316
    # Sun's zenith for sunrise/sunset
    zenith = CIVIL_ZENITH
    # Offset from UTC (GMT)
    localOffset = -5 # Eastern standard time

    right_now = datetime.datetime.now()
    # zenith is optional and defaults to the CIVIL_ZENITH value
    rise_obj = SunriseSunset(dt=right_now, latitude=latitude,
                             longitude=longitude, localOffset=localOffset,
                             zenith=zenith)
    rise_time, set_time = rise_obj.calculate()

    print "Using information for Quebec City"
    print "Sunrise", rise_time
    print "Sunset", set_time
