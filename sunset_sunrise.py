# -*- coding: utf-8 -*-
import math

#INPUTS
#Date
day = 1
month = 1
year = 2014
#Longitude and latitude
latitude = 46.805
longitude = -71.2316
#Sun's zenith for sunrise/sunset
zenith = 90.83333 #civil
#Offset from UTC (GMT)
localOffset = -5 #Eastern standard time

#Useful functions
def adjustAngle(L):
    if L < 0:
        return L + 360
    elif L >= 360:
        return L - 360
    return L

def adjustTime(L):
    if L < 0:
        return L + 24
    elif L >= 24:
        return L - 24
    return L

#ALGORITHM

#Calculate the day of the year
N1 = math.floor(275 * month / 9)
N2 = math.floor((month + 9) / 12)
N3 = (1 + math.floor((year - 4 * math.floor(year / 4) + 2) / 3))
N = N1 - (N2 * N3) + day - 30

#Convert the longitude to hour value and calculate an approximate time
lngHour = longitude / 15
t_rise = N + ((6 - lngHour) / 24)
t_set = N + ((18 - lngHour) / 24)

#Calculate the Sun's mean anomaly
M_rise = (0.9856 * t_rise) - 3.289
M_set = (0.9856 * t_set) - 3.289

#Calculate the Sun's true longitude
L_rise = adjustAngle(M_rise + (1.916 * math.sin(math.radians(M_rise))) + (0.020 * math.sin(math.radians(2 * M_rise))) + 282.634)
L_set = adjustAngle(M_set + (1.916 * math.sin(math.radians(M_set))) + (0.020 * math.sin(math.radians(2 * M_set))) + 282.634)

#Calculate the Sun's right ascension
RA_rise = adjustAngle(math.degrees(math.atan(0.91764 * math.tan(math.radians(L_rise)))))
RA_set = adjustAngle(math.degrees(math.atan(0.91764 * math.tan(math.radians(L_set)))))

#Right ascension value needs to be in the same quadrant as L
Lquadrant_rise  = (math.floor(L_rise/90)) * 90
RAquadrant_rise = (math.floor(RA_rise/90)) * 90
RA_rise = RA_rise + (Lquadrant_rise - RAquadrant_rise)

Lquadrant_set  = (math.floor(L_set/90)) * 90
RAquadrant_set = (math.floor(RA_set/90)) * 90
RA_set = RA_set + (Lquadrant_set - RAquadrant_set)

#Right ascension value needs to be converted into hours
RA_rise = RA_rise / 15
RA_set = RA_set / 15

#Calculate the Sun's declination
sinDec_rise = 0.39782 * math.sin(math.radians(L_rise))
cosDec_rise = math.cos(math.asin(sinDec_rise))

sinDec_set = 0.39782 * math.sin(math.radians(L_set))
cosDec_set = math.cos(math.asin(sinDec_set))

#Calculate the Sun's local hour angle
cosH_rise = (math.cos(math.radians(zenith)) - (sinDec_rise * math.sin(math.radians(latitude)))) / (cosDec_rise * math.cos(math.radians(latitude)))
cosH_set = (math.cos(math.radians(zenith)) - (sinDec_set * math.sin(math.radians(latitude)))) / (cosDec_set * math.cos(math.radians(latitude)))

#Finish calculating H and convert into hours
H_rise = (360 - math.degrees(math.acos(cosH_rise))) / 15
H_set = math.degrees(math.acos(cosH_set)) / 15

#Calculate local mean time of rising/setting
T_rise = H_rise + RA_rise - (0.06571 * t_rise) - 6.622
T_set = H_set + RA_set - (0.06571 * t_set) - 6.622

#Adjust back to UTC
UT_rise = adjustTime(T_rise - lngHour)
UT_set = adjustTime(T_set - lngHour)

#Convert UT value to local time zone of latitude/longitude
localT_rise = adjustTime(UT_rise + localOffset)
localT_set = adjustTime(UT_set + localOffset)

#Conversion
h_rise = int(localT_rise)
m_rise = localT_rise % 1 * 60
h_set = int(localT_set)
m_set = localT_set % 1 * 60
print "Sunrise : %dh%02d" % (h_rise, m_rise)
print "Sunset : %dh%02d" % (h_set, m_set)
