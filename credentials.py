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

#For SSO/CI sites, you can retrieve a personal access token 
# via: https://developer.webex.com/docs/api/getting-started
# For non-SSO/CI sites, provide a password
# If both are provided, the sample will attempt to use the access token

# (Common) Modify the below credentials to match your Webex Meeting site, host Webex ID and password

# Webex ID, Password, and sitename are required.

username = ""
password = ""

# Example: username@cisco.webex.com sitename = "cisco"
sitename= ""

access_token = None

#admin_token is the Webex REST API token for the site admin
admin_token = ""

# the following are the time/date ranges to consider for retrieveing meeting qualities statisitics
# start_timeStart and start_timeEnd is the range of date/times of the starting times of the meetings to consider
# end_timeStart and end_timeEnd is the range of date/times of the ending times of the meetings to consider
start_timeStart="02/24/2021 00:00:00"
start_timeEnd="03/03/2021 00:00:00"
end_timeStart="02/24/2021 00:01:00"
end_timeEnd="03/03/2021 00:01:00"

# (oauth2.py) Credentials for use with Webex SSO/CI OAuth sites

client_id=""
client_secret=""
