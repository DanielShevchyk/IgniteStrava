access_token = system.tag.readBlocking("[default]AccessToken")[0].value
AUTH_URL = "https://www.strava.com/oauth/token"
print access_token
def get_athlete_profile():
    """
    Uses the access token to fetch the athlete's profile.
    
    """
    ATHLETE_URL = "https://www.strava.com/api/v3/athlete"
    client = system.net.httpClient(bypassCertValidation=True)
    
    # Headers dictionary
    headers = {'Authorization': 'Bearer ' + access_token}
    
    print "Fetching Athlete Profile..."
    response = client.get(ATHLETE_URL, headers=headers)
    
    if response.good:
        return response.json
    else:
        print "Error fetching data: " + str(response.statusCode)
        return None
        
        
def get_activities():
	ACTIVITIES_URL = "https://www.strava.com/api/v3/athlete/activities"
	client = system.net.httpClient(bypassCertValidation=True)
	headers = {'Authorization': 'Bearer ' + access_token}
	all_activities = []
	page_num = 1
	per_page = 50  # Max is usually around 200, but 50 is safer/faster per request
	keep_fetching = True
	
	print "Starting to fetch activities..."
	
	while keep_fetching:
	    print "Fetching page " + str(page_num) + "..."
	    
	    # We pass parameters to control which page we are viewing
	    params = {
	        "page": page_num,
	        "per_page": per_page
	    }
	    
	    # Ignition's client.get supports the 'params' keyword arg
	    response = client.get(ACTIVITIES_URL, params=params, headers=headers)
	    
	    if response.good:
	        page_data = response.json
	        
	        # If the list is empty, we have reached the end of the history
	        if len(page_data) == 0:
	            keep_fetching = False
	        else:
	            # Add this page's activities to our master list
	            all_activities.extend(page_data)
	            page_num += 1
	    else:
	        print "Error fetching page " + str(page_num) + ": " + str(response.statusCode)
	        keep_fetching = False
	        
	print "Finished. Total activities found: " + str(len(all_activities))
	print all_activities