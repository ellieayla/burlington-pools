# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy



from datetime import date, datetime
from dataclasses import dataclass, field
from scrapy.item import Item, Field
from itemloaders.processors import TakeFirst  # provided by scrapy


class BookableDate(scrapy.Item):
    #  EventId: 6315b694-88ac-5e35-e94d-9d3dc4ba154b
    #  CourseId: 00180789
    #  CourseIdTrimmed: 180789
    #  EventName: Combo Swim
    #  Details: This recreation program is a great opportunity for all ages to spend time together at Burlington’s indoor pools. The lap pool is divided into deep and shallow areas with a lane available. Capacity in the lane is monitored for safety by Aquatic staff. Diving board is not available during this program time. Regular Swim Admission & Supervision Standards apply. Details are listed at burlington.ca/playstandards.
    #  Spots: 24 spot(s) left
    #  OccurrenceDate: 20240426
    #  BookButtonText: Register
    #  BookButtonDescription: Register Combo Swim
    #  ClosedButtonName: Closed
    #  Instructor: {'Id': None, 'FullName': '', 'Type': '', 'Description': '', 'Image': '', 'Email': ''}
    #  Facility: Lap Pool
    #  DisplaySettings: {'DisplayInstructorsName': True, 'DisplayPrices': True, 'DisplaySpotsLeft': True, 'DisplayRegistrationDate': True, 'DisplayNumberOfSessions': True, 'DisplayCourseId': False, 'DisplayAgeRestrictions': True, 'DisplayRankRestrictions': False, 'DisplayGenderRestrictions': False, 'ButtonName': 'Register', 'UseBookMe5UiWidgetVersion': False, 'WidgetUIVersion': 0}
    #  PriceRange: $0.00 - $3.20
    #  AllDayEvent: False
    #  AnyTimeBrokenOccurrences: False
    #  FormattedStartDate: 2024 Apr 26th
    #  FormattedStartTime: 07:15 PM
    #  FormattedEndDate: Apr 26th
    #  FormattedEndTime: 08:15 PM
    #  FirstOccurrenceFormattedEndTime: None
    #  EventTimeDescription: 07:15 pm - 08:15 pm
    #  AlternativeLocation: None
    #  HasAlternativeLocation: False
    #  OccurrenceDescription:
    #  Occurrences: []
    #  NumberOfSessions: 10
    #  PrerequisiteEvents: 0
    #  DisplayablePrerequisiteEventsRestrictionsForCourses:
    #  DisplayableRestrictionsForCourses: Age: 0 to 110
    #  MinAge: 0
    #  MinAgeMonths: None
    #  MaxAge: 110
    #  MaxAgeMonths: None
    #  NoAgeRestriction: False
    #  AgeRestrictions: 0 to 110
    #  GenderRestrictions: Co-ed
    #  RankRestrictions:
    #  FromRank: None
    #  ToRank: None
    #  StartingRankId: None
    #  EndingRankId: None
    #  DurationInMinutes: 60
    #  FeeFrequency: None
    #  OrgLogo: //az12497.vo.msecnd.net/9cec288dde1f4cc8a295d27d60b5ccff/logo/live-play-burlington-logo-comp.png
    #  OrgIsSingleLocation: False
    #  OrgLegalName: City of Burlington
    #  OrgName: City of Burlington
    #  Address: {'AddressTag': 'Centennial Pool', 'Street': '5151 New Street', 'City': 'Burlington', 'PostalCode': 'L7P 4J5', 'CountryId': 0, 'Country': '', 'StateProvinceId': 0, 'AnyFieldMissing': True, 'Latitude': 43.37193, 'Longitude': -79.750327, 'Id': '1caa5785-bc69-469c-ac36-5ae3758860d3'}
    #  Location: Centennial Pool
    #  BookingType: 2

    event_id = Field()
    event_occurrence = Field()

    name = Field()
    details = Field()

    start_time = Field()
    end_time = Field()
    duration_minutes = Field()

    address = Field()
    location = Field()
    facility = Field()

    instructor = Field(default=None)

    displayable_restriction = Field(default=None)

    price_range = Field()

    spots_remaining = Field()

    url = Field()
