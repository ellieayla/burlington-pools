
from scrapy.exporters import BaseItemExporter


import icalendar
import json
from datetime import datetime, date, tzinfo
import pytz
from uuid import uuid5, UUID

from .items import BookableDate


ns = UUID('94e2caf7-fc1e-463b-bd82-08be0237f689')


class ICalItemExporter(BaseItemExporter):
    # similar to the XML exporter
    def __init__(self, file, **kwargs):
        super().__init__(**kwargs)
        self.file = file  # already-open file handle

        self.cal = icalendar.Calendar()
        self._kwargs.setdefault('ensure_ascii', not self.encoding)

    def start_exporting(self):
        self.cal.add('prodid', '-//BurlingtonPools//verselogic.net//')
        self.cal.add('version', '2.0')

    def export_item(self, item: BookableDate):

        itemdict = dict(self._get_serialized_fields(item))

        e = icalendar.Event()
        e.add('last-modified', icalendar.vDatetime(datetime.now(pytz.UTC)))
        e.add('dtstamp', icalendar.vDatetime(itemdict['start_time']))
        e.add('summary', icalendar.vText(f"{itemdict['name']}, {itemdict['location']}, {itemdict['facility']}"))
        e.add('location', icalendar.vText(itemdict['address']))

        e.add('uid', icalendar.vText(uuid5(ns, itemdict['event_id'] + itemdict['event_occurrence'])))

        e.add('description', icalendar.vText(f"{itemdict['details']}\n\n{itemdict['time_range_description']}\n{itemdict['price_range']}\n{itemdict['spots_remaining']}"))

        e.add('dtstart', icalendar.vDatetime(itemdict['start_time']))
        e.add('dtend', icalendar.vDatetime(itemdict['end_time']))

        e.add('url', icalendar.vText(itemdict['url']))

        self.cal.add_component(e)


    def finish_exporting(self):
        self.cal.add_missing_timezones()
        self.cal.subcomponents = sorted(self.cal.subcomponents, key=lambda e: e.get("UID"))  # stable ordering; sort top-level subcomponents by UID
        self.file.write(self.cal.to_ical(sorted=True))  # stable ordering; sort properties
