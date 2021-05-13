
# Webex Meetings Qualities Extractor

This Python 3 sample code shows how to extract the "qualities" statistics of all meetings in a site using the site admin credentials.
More details on functionaliy and limitations can be found in the  [Webex REST API Meeting Qualities documentation](https://developer.webex.com/docs/api/v1/meeting-qualities)

 
### Authors:

* Gerardo Chaves (gchaves@cisco.com)

***

### Prerequisites
* Python 3
* Webex host accounts properly licensed for Meetings 
* Webex Pro Pack license
* Webex site admin ID, email address and Password. If the site has Single Sign-On (SSO) enabled, 
and integration will have to be created on the Webex Developer site: https://developer.webex.com/docs/integrations to be used
 with this sample code. More details in the [oauth2.py](oauth2.py) file in this repository
* Webex REST API access token for the admin account (this is only while a full OAuth flow is implemented)



# Setup instructions 
1. Install and clone this repo onto a machine that has python3 installed 
2. Install and create a virtual environment for your project (https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/)
3. Enter the virtual environment by running source (venv name)/bin/activate 
4. Install dependencies by running:  
```pip3 install -r requirements.txt```  
6. Edit [credentials.py](credentials.py) to include webex ID and password (sitename, webexid, and password/token are required) or, 
if your Webex site has **Single Sign-on (SSO)** enabled (https://help.webex.com/en-us/lfu88u/Single-Sign-On-Integration-in-Cisco-Webex-Control-Hub#CMGT_RF_S9BDF982_00) , 
follow the instructions in the [oauth2.py](oauth2.py) file to generate an access token to use instead of username/password with this sample code.
7. (TEMPORARY) Edit [credentials.py](credentials.py) to assign a valid Webex REST API access token for the site admin to the 'the admin_token' setting.
8. Edit [credentials.py](credentials.py) to specify the date ranges for the meetings to obtain quality statistics for (within the past 7 days only). 
   `start_timeStart` and `start_timeEnd` is the range of date/times of the starting times of the meetings to consider and `end_timeStart` and `end_timeEnd` is the range of date/times of the ending times of the meetings to consider


### Running the sample

Once everything is set up, you can run python script with this command:  
```python3 main.py```
 

### Output

The script will generate one JSON file per each meeting within the date/time range specified in the `credentials.py` file

 

### API Reference/Documentation:

* [Webex Meetings XML API Reference Guide](https://developer.cisco.com/docs/webex-xml-api-reference-guide/#!meetings-xml-api-reference-guide)
* [Webex REST API Meeting Qualities documentation](https://developer.webex.com/docs/api/v1/meeting-qualities)


## License
Provided under Cisco Sample Code License, for details see [LICENSE](LICENSE)

## Code of Conduct 
Our code of conduct is available [here](CODE_OF_CONDUCT.md)

## Contributing 
See our contributing guidelines [here](CONTRIBUTING.md)

### DISCLAIMER:
<b>Please note:</b> This script is meant for demo purposes only. All tools/ scripts in this repo are released for use "AS IS" without any warranties of any kind, including, but not limited to their installation, use, or performance. Any use of these scripts and tools is at your own risk. There is no guarantee that they have been through thorough testing in a comparable environment and we are not responsible for any damage or data loss incurred with their use.
You are responsible for reviewing and testing any scripts you run thoroughly before use in any non-testing environment.
