from pathlib import Path

import scrapy

from burlington_pools.items import BookableDate
from datetime import date, datetime, timedelta
import dateutil
import pytz
import uuid


def _parse_date_time(formatted_date: str, formatted_time: str) -> datetime:
    return dateutil.parser.parse(f"{formatted_date} {formatted_time}")

DEFAULT_SEARCH = {
    'values[0][Name]': 'Keyword',
    'values[0][Value]': '',
    'values[0][Value2]': '',
    'values[0][ValueKind]': '9',

    'values[1][Name]': 'Date Range',
    'values[1][Value]': '%sT00:00:00.000Z' % date.today(),
    'values[1][Value2]': '%sT00:00:00.000Z' % date.today() + datetime.timedelta(days=40),
    'values[1][ValueKind]': '6',

    'values[2][Name]': 'Age',
    'values[2][Value]': '0',
    'values[2][Value2]': '1188',
    'values[2][ValueKind]': '0',
}

class BurlingtonPools(scrapy.Spider):
    name = "BurlingtonPools"
    allowed_domains = ["cityofburlington.perfectmind.com"]

    calendarId = '598fc12b-1445-4708-8de3-4a997690a6a3'  # Swimming
    widgetId = 'ee6566f5-1e27-433c-9c19-86e76a0e3556'  # Drop-in?
    def start_requests(self):
        urls = [
            f"https://cityofburlington.perfectmind.com/22818/Clients/BookMe4BookingPages/Classes?calendarId={self.calendarId}&widgetId={self.widgetId}",
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        # this page contains a form with an Input element "__RequestVerificationToken" whose value must be included on subsequent requests
        verification_token = response.xpath('//form[@id="AjaxAntiForgeryForm"]/input[@name="__RequestVerificationToken"]/@value').get()
        # print(">>>>> verification_token: ", verification_token)

        return scrapy.FormRequest(
            url='https://cityofburlington.perfectmind.com/22818/Clients/BookMe4BookingPagesV2/ClassesV2',
            formdata={
                'calendarId': self.calendarId,
                'widgetId': self.widgetId,
                'page': '0',
                **DEFAULT_SEARCH,
                '__RequestVerificationToken': verification_token
            },
            callback=self.parse_classes_v2_json,
            cb_kwargs={
                'verification_token': verification_token
            },
        )



    def parse_classes_v2_json(self, response, verification_token):
        payload = response.json()

        self.logger.info(f">>>>> got {len(payload['classes'])} classes")
        for c in payload['classes']:
            # >>>>> c {'EventId': '6315b694-88ac-5e35-e94d-9d3dc4ba154b', 'CourseId': '00180789', 'CourseIdTrimmed': '180789', 'EventName': 'Combo Swim', 'Details': 'This recreation program is a great opportunity for all ages to spend time together at Burlington’s indoor pools. The lap pool is divided into deep and shallow areas with a lane available. Capacity in the lane is monitored for safety by Aquatic staff. Diving board is not available during this program time. Regular Swim Admission & Supervision Standards apply. Details are listed at burlington.ca/playstandards.', 'Spots': '24 spot(s) left', 'OccurrenceDate': '20240426', 'BookButtonText': 'Register', 'BookButtonDescription': 'Register Combo Swim', 'ClosedButtonName': 'Closed', 'Instructor': {'Id': None, 'FullName': '', 'Type': '', 'Description': '', 'Image': '', 'Email': ''}, 'Facility': 'Lap Pool', 'DisplaySettings': {'DisplayInstructorsName': True, 'DisplayPrices': True, 'DisplaySpotsLeft': True, 'DisplayRegistrationDate': True, 'DisplayNumberOfSessions': True, 'DisplayCourseId': False, 'DisplayAgeRestrictions': True, 'DisplayRankRestrictions': False, 'DisplayGenderRestrictions': False, 'ButtonName': 'Register', 'UseBookMe5UiWidgetVersion': False, 'WidgetUIVersion': 0}, 'PriceRange': '$0.00 - $3.20', 'AllDayEvent': False, 'AnyTimeBrokenOccurrences': False, 'FormattedStartDate': '2024 Apr 26th', 'FormattedStartTime': '07:15 PM', 'FormattedEndDate': 'Apr 26th', 'FormattedEndTime': '08:15 PM', 'FirstOccurrenceFormattedEndTime': None, 'EventTimeDescription': '07:15 pm - 08:15 pm', 'AlternativeLocation': None, 'HasAlternativeLocation': False, 'OccurrenceDescription': '', 'Occurrences': [], 'NumberOfSessions': 10, 'PrerequisiteEvents': 0, 'DisplayablePrerequisiteEventsRestrictionsForCourses': '', 'DisplayableRestrictionsForCourses': 'Age: 0 to 110', 'MinAge': 0, 'MinAgeMonths': None, 'MaxAge': 110, 'MaxAgeMonths': None, 'NoAgeRestriction': False, 'AgeRestrictions': '0 to 110', 'GenderRestrictions': 'Co-ed', 'RankRestrictions': '', 'FromRank': None, 'ToRank': None, 'StartingRankId': None, 'EndingRankId': None, 'DurationInMinutes': 60, 'FeeFrequency': None, 'OrgLogo': '//az12497.vo.msecnd.net/9cec288dde1f4cc8a295d27d60b5ccff/logo/live-play-burlington-logo-comp.png', 'OrgIsSingleLocation': False, 'OrgLegalName': 'City of Burlington', 'OrgName': 'City of Burlington', 'Address': {'AddressTag': 'Centennial Pool', 'Street': '5151 New Street', 'City': 'Burlington', 'PostalCode': 'L7P 4J5', 'CountryId': 0, 'Country': '', 'StateProvinceId': 0, 'AnyFieldMissing': True, 'Latitude': 43.37193, 'Longitude': -79.750327, 'Id': '1caa5785-bc69-469c-ac36-5ae3758860d3'}, 'Location': 'Centennial Pool', 'BookingType': 2}
            # print(">>>>> c", c)

            url = f'https://cityofburlington.perfectmind.com/22818/Clients/BookMe4LandingPages/Class?widgetId={self.widgetId}&redirectedFromEmbededMode=False&classId={c["EventId"]}&occurrenceDate={c["OccurrenceDate"]}'
            b = BookableDate(
                # EventId is not unique, can occur multiple times (eg on different dates)
                event_id = c['EventId'],
                event_occurrence = c['OccurrenceDate'],
    
                name = str.strip(c['EventName']),
                location = str.strip(c['Location']),
                facility = str.strip(c['Facility']),
                details = str.strip(c['Details']),

                start_time = _parse_date_time(c['FormattedStartDate'], c['FormattedStartTime']),
                end_time = _parse_date_time(c['FormattedEndDate'], c['FormattedEndTime']),
                time_range_description = str.strip(c['EventTimeDescription']),
                duration_minutes = c['DurationInMinutes'],

                #  Address: {'AddressTag': 'Centennial Pool', 'Street': '5151 New Street', 'City': 'Burlington', 'PostalCode': 'L7P 4J5', 'CountryId': 0, 'Country': '', 'StateProvinceId': 0, 'AnyFieldMissing': True, 'Latitude': 43.37193, 'Longitude': -79.750327, 'Id': '1caa5785-bc69-469c-ac36-5ae3758860d3'}
                address = f"{c['Address']['AddressTag']}, {c['Address']['Street']}, {c['Address']['City']}, {c['Address']['PostalCode']}",

                instructor = c['Instructor']['FullName'] or None,

                displayable_restriction = f"Restriction: {c['DisplayableRestrictionsForCourses'], c['GenderRestrictions']}",

                price_range = c['PriceRange'],
                spots_remaining = c['Spots'],
                url = url,
            )
            yield b

        self.logger.info(f">>>>>> classesMaxEndDateString: {payload['classesMaxEndDateString']}")
        self.logger.info(f">>>>>> nextKey: {payload['nextKey']}")
        
        if payload['nextKey'] and payload['nextKey'] != "0001-01-01":
            yield scrapy.FormRequest(
                url='https://cityofburlington.perfectmind.com/22818/Clients/BookMe4BookingPagesV2/ClassesV2',
                formdata={
                    'calendarId': self.calendarId,
                    'widgetId': self.widgetId,
                    'page': '0',
                    **DEFAULT_SEARCH,
                    'after': payload['nextKey'],
                    '__RequestVerificationToken': verification_token
                },
                callback=self.parse_classes_v2_json,
                cb_kwargs={
                    'verification_token': verification_token
                },
            )
