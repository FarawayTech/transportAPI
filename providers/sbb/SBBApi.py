import os
import requests
from collections import defaultdict
from dateutil import tz
from providers.Api import Api
from xml.etree import ElementTree
from datetime import datetime


SBB_API_KEY = os.environ.get('SBB_API_KEY')
TIMEZONE = tz.gettz('Europe/Zurich')


class SBBApi(Api):
    DEPARTURES_URL = 'https://api.opentransportdata.swiss/trias'
    NS = {'default': 'http://www.vdv.de/trias'}

    def _parse_response(self, response_xml: ElementTree.Element) -> dict:
        response = {'departures': []}
        departures = defaultdict(list)

        for departure in response_xml.iterfind('.//default:StopEvent', self.NS):
            dep_time = departure.find(".//default:TimetabledTime", self.NS).text
            transport_name = departure.find(".//default:Mode/default:Name/default:Text", self.NS).text
            transport_type = departure.find(".//default:Mode/default:PtMode", self.NS).text
            destination_name = departure.find(".//default:DestinationText/default:Text", self.NS).text
            destination_id = departure.find(".//default:DestinationStopPointRef", self.NS).text
            destination_lang = departure.find(".//default:DestinationText/default:Language", self.NS).text

            line_name = departure.find(".//default:PublishedLineName/default:Text", self.NS).text  # can be empty for trains
            departures[destination_id].append({'dep_time': dep_time,
                                               'destination': {'name': destination_name,
                                                               'lang': destination_lang,
                                                               'id': destination_id},
                                               'transport': {'type': transport_type,
                                                             'name': transport_name,
                                                             'line': line_name}})
        for key, value in departures.items():
            connections = {'destination': {'id': key, 'name': value[0]['destination']['name'],
                                           'lang': value[0]['destination']['lang']},
                           'connections': value}
            response['departures'].append(connections)
        return response

    def get_departures(self, station_id, time: datetime):
        time = time.replace(tzinfo=TIMEZONE)
        request_xml = ElementTree.parse('providers/sbb/departures_request.xml').getroot()  # type: ElementTree.Element
        # there is always only one
        stop = request_xml.find(".//default:StopPointRef", self.NS)
        stop.text = str(station_id)
        dep_time = request_xml.find('.//default:DepArrTime', self.NS)
        dep_time.text = time.strftime("%Y-%m-%dT%H:%M:%S")

        request_xml_str = ElementTree.tostring(request_xml, encoding='utf-8', method='xml')
        r = requests.post(self.DEPARTURES_URL, headers={'Content-Type': 'application/xml',
                                                        'Authorization': SBB_API_KEY},
                          data=request_xml_str)
        r.encoding = 'utf-8'
        return self._parse_response(ElementTree.fromstring(r.text))