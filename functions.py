# Copyright (c) 2020 Cisco and/or its affiliates.
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

import requests
import datetime
from lxml import etree
import credentials
import xml.etree.ElementTree as ET

# Change to true to enable request/response debug output
DEBUG = False

# Once the user is authenticated, the sessionTicket for all API requests will be stored here
sessionSecurityContext = {}


# Custom exception for errors when sending requests
class SendRequestError(Exception):

    def __init__(self, result, reason):
        self.result = result
        self.reason = reason

    pass


# Generic function for sending XML API requests
#   envelope : the full XML content of the request
def sendRequest(envelope):
    if DEBUG:
        print(envelope)

    # Use the requests library to POST the XML envelope to the Webex API endpoint
    headers = {'Content-Type': 'application/xml'}
    response = requests.post('https://api.webex.com/WBXService/XMLService', envelope)

    # Check for HTTP errors
    try:
        response.raise_for_status()
    except requests.exceptions.HTTPError as err:
        raise SendRequestError('HTTP ' + str(response.status_code), response.content.decode("utf-8"))

    # Use the lxml ElementTree object to parse the response XML
    message = etree.fromstring(response.content)

    if DEBUG:
        print(etree.tostring(message, pretty_print=True, encoding='unicode'))

        # Use the find() method with an XPath to get the 'result' element's text
    # Note: {*} is pre-pended to each element name - ignores namespaces
    # If not SUCCESS...
    if message.find('{*}header/{*}response/{*}result').text != 'SUCCESS':
        result = message.find('{*}header/{*}response/{*}result').text
        reason = message.find('{*}header/{*}response/{*}reason').text

        # ...raise an exception containing the result and reason element content
        raise SendRequestError(result, reason)

    return message


def AuthenticateUser(siteName, webExId, password, accessToken):
    # If an access token is provided in .env, we'll use this form
    if (accessToken):
        request = f'''<?xml version="1.0" encoding="UTF-8"?>
            <serv:message xmlns:serv="http://www.webex.com/schemas/2002/06/service"
                xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">
                <header>
                    <securityContext>
                        <siteName>{siteName}</siteName>
                        <webExID>{webExId}</webExID>
                    </securityContext>
                </header>
                <body>
                    <bodyContent xsi:type="java:com.webex.service.binding.user.AuthenticateUser">
                        <accessToken>{accessToken}</accessToken>
                    </bodyContent>
                </body>
            </serv:message>'''
    else:
        # If no access token, assume a password was provided, using this form
        request = f'''<?xml version="1.0" encoding="UTF-8"?>
            <serv:message xmlns:serv="http://www.webex.com/schemas/2002/06/service"
                xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">
                <header>
                    <securityContext>
                        <siteName>{siteName}</siteName>
                        <webExID>{webExId}</webExID>
                        <password>{password}</password>
                    </securityContext>
                </header>
                <body>
                    <bodyContent xsi:type="java:com.webex.service.binding.user.AuthenticateUser"/>
                </body>
            </serv:message>'''

    # Make the API request
    response = sendRequest(request)

    # Return an object containing the security context info with sessionTicket
    return {
        'siteName': siteName,
        'webExId': webExId,
        'sessionTicket': response.find('{*}body/{*}bodyContent/{*}sessionTicket').text
    }

def SetDelegatePermissions(sessionSecurityContext, host):
    request = f'''<?xml version="1.0" encoding="UTF-8"?>
                <serv:message xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
                xmlns:serv="http://www.webex.com/schemas/2002/06/service">
                  <header>
                    <securityContext>
                    <siteName>{sessionSecurityContext["siteName"]}</siteName>
                    <webExID>{sessionSecurityContext["webExId"]}</webExID>
                    <sessionTicket>{sessionSecurityContext["sessionTicket"]}</sessionTicket>  
                    </securityContext>
                  </header>
                  <body>
                    <bodyContent xsi:type="java:com.webex.service.binding.user.SetUser">
                      <webExId>{host}</webExId>
                      <schedulingPermission>{sessionSecurityContext["webExId"]}</schedulingPermission>
                    </bodyContent>
                  </body>
                </serv:message>'''
    response = sendRequest(request)
    return response


def LstmeetingusageHistory(sessionSecurityContext,sStartTStart="",sStartTEnd="",sEndTStart="", sEndTEnd=""):
    print("About to request LstmeetingusageHistory.....")

    request = f'''<?xml version="1.0" encoding="UTF-8"?>
                    <serv:message xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">
                        <header>
                            <securityContext>
                                <siteName>{sessionSecurityContext["siteName"]}</siteName>
                                <webExID>{sessionSecurityContext["webExId"]}</webExID>
                                <sessionTicket>{sessionSecurityContext["sessionTicket"]}</sessionTicket>  
                            </securityContext>
                        </header>
                        <body>
                            <bodyContent xsi:type=
                                "java:com.webex.service.binding.history.LstmeetingusageHistory">
                                <startTimeScope>
                                    <sessionStartTimeStart>{sStartTStart}
                                    </sessionStartTimeStart>
                                    <sessionStartTimeEnd>{sStartTEnd}</sessionStartTimeEnd>
                                </startTimeScope>
                                <endTimeScope>
                                    <sessionEndTimeStart>{sEndTStart}</sessionEndTimeStart>
                                    <sessionEndTimeEnd>{sEndTEnd}</sessionEndTimeEnd>
                                </endTimeScope>
                                <listControl>
                                    <serv:startFrom>1</serv:startFrom>
                                    <serv:maximumNum>10</serv:maximumNum>
                                    <serv:listMethod>OR</serv:listMethod>
                                </listControl>
                                <order>
                                    <orderBy>CONFNAME</orderBy>
                                    <orderAD>ASC</orderAD>
                                </order>
                            </bodyContent>
                        </body>
                    </serv:message>'''

    response = sendRequest(request)

    return response

#below goes after </order>
#            <dateScope>
#                 <startDateStart></startDateStart>
#                 <startDateEnd></startDateEnd>
#                 <timeZoneID></timeZoneID>
#                 <endDateStart></endDateStart>
#                 <endDateEnd></endDateEnd>
#             </dateScope>