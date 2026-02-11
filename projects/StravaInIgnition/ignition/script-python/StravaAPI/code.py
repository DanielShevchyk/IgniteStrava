access_token = system.tag.readBlocking("[default]AccessToken")[0].value
AUTH_URL = "https://www.strava.com/oauth/token"
#print access_token
client = system.net.httpClient(bypassCertValidation=True)
headers = {'Authorization': 'Bearer ' + access_token}
def get_athlete_profile():
    """
    Uses the access token to fetch the athlete's profile.
    
    """
    ATHLETE_URL = "https://www.strava.com/api/v3/athlete"
    
    print "Fetching Athlete Profile..."
    response = client.get(ATHLETE_URL, headers=headers)
    
    if response.good:
        return response.json
    else:
        print "Error fetching data: " + str(response.statusCode)
        return None
        
        
def get_activities():
	ACTIVITIES_URL = "https://www.strava.com/api/v3/athlete/activities"
	all_activities = []
	page_num = 1
	per_page = 50  # Max is usually around 200
	keep_fetching = True
	
	print "Starting to fetch activities..."
	
	while keep_fetching:
	    print "Fetching page " + str(page_num) + "..."
	    
	    params = {
	        "page": page_num,
	        "per_page": per_page
	    }
	    
	    response = client.get(ACTIVITIES_URL, params=params, headers=headers)
	    
	    if response.good:
	        page_data = response.json
	        
	        if len(page_data) == 0:
	            keep_fetching = False
	        else:
	            all_activities.extend(page_data)
	            page_num += 1
	    else:
	        print "Error fetching page " + str(page_num) + ": " + str(response.statusCode)
	        keep_fetching = False
	        
	print "Finished. Total activities found: " + str(len(all_activities))
	print all_activities
def get_activities_by_id(activity_id):
	BASE_URL = "https://www.strava.com/api/v3/activities/"
	url = BASE_URL + str(activity_id)
	
	headers = {'Authorization': 'Bearer ' + access_token}
	
	print "Fetching details for Activity ID: " + str(activity_id) + "..."
	response = client.get(url, headers=headers)
	
	if response.good:
		json_data = system.util.jsonEncode(response.json)
		#print json_data
		system.tag.writeBlocking('[default]ActivityJsonReturn', json_data)
		return response.json
	else:
	    print "Error fetching activity: " + str(response.statusCode)
	    print response.text
	    return None