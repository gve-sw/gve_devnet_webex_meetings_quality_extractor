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

import functions
import credentials
import requests


if __name__ == "__main__":


    meetings_uid=[]

    # AuthenticateUser and get sesssionTicket
    try:
        functions.sessionSecurityContext = functions.AuthenticateUser(
            credentials.sitename,
            credentials.username,
            credentials.password,
            credentials.access_token
        )

    # If an error occurs, print the error details and exit the script
    except functions.SendRequestError as err:
        print(err)
        raise SystemExit

    print("Authentication Accepted")
    print()
    print('Session Ticket:', '\n')
    print(functions.sessionSecurityContext['sessionTicket'])
    print()





    try:
        response = functions.LstmeetingusageHistory(functions.sessionSecurityContext,credentials.start_timeStart, credentials.start_timeEnd, credentials.end_timeStart, credentials.end_timeEnd)
        #print("response=",response)

        #session_key = response.find('{*}body/{*}bodyContent/{*}meetingUsageHistory/{*}sessionKey').text
        #print('Session Key:', session_key)

        meetings= response.findall('{*}body/{*}bodyContent/{*}meetingUsageHistory')
        for theMeeting in meetings:
            conf_id = theMeeting.find('{*}confID').text
            meeting_uuid = theMeeting.find('{*}meetingUUID').text
            print("Conf ID: ",conf_id, " meeting UUID: ",meeting_uuid)
            u_meeting_id = meeting_uuid+ "_I_"+conf_id
            print("Unique Meeting ID: ",u_meeting_id)
            meetings_uid.append(u_meeting_id)


    except functions.SendRequestError as err:
        if err.reason!='The host WebExID does not exist':
            #this is some other error that we are not anticipating, so just print and exit
            print(err)
            raise SystemExit
        else:
            try:
                # since the error was specific to not liking the WebExID without host and we know with some sites
                # that it is the case, now let's try it without removing the domain from host email
                print("taking this extra path...")

            except functions.SendRequestError as err:
                # this is still some other error that we are not anticipating, so just print and exit
                print(err)
                raise SystemExit

    # now go get stats for each unique meeting instance
    payload = {}
    headers = {
        'Authorization': 'Bearer '+ credentials.admin_token
    }

    print("Obtaining meeting qualities for the following meetings: ",meetings_uid)
    for a_meeting in meetings_uid:
        # can only make this call every 5 minutes for a particular meeting
        url = "https://analytics.webexapis.com/v1/meeting/qualities?meetingId="+a_meeting
        print("Getting qualities for meeting ",a_meeting)
        response = requests.request("GET", url, headers=headers, data=payload)

        # print(response.text.encode('utf8'))
        data = response.content
        print("writing out file...")
        with open(a_meeting+'_data.json', 'wb') as f:
            f.write(data)

