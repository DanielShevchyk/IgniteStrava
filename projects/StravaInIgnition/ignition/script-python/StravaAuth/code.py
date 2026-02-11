# ==========================================
# User Config using built in 8.3 secrets
# Make sure to place your secrets under a single provider
# Include Client_ID, Client_Secret, and Refresh_Token
# This should be available after you login and register for API access on this web url:
# https://www.strava.com/settings/api
# You can also just place the secrets here instead of using built in secrets.
# Security ramificati
# ==========================================
pyPlaintext = system.secrets.readSecretValue("StravaSecrets", "Client_ID") # Provider name, secret
CLIENT_ID = pyPlaintext.getSecretAsString() 

pyPlaintext = system.secrets.readSecretValue("StravaSecrets", "Client_Secret")
CLIENT_SECRET = pyPlaintext.getSecretAsString()

pyPlaintext = system.secrets.readSecretValue("StravaSecrets", "PermRefresh")
REFRESH_TOKEN = pyPlaintext.getSecretAsString() 

# Strava API Endpoints. Shouldn't change unless Strava updates their API to v4, etc.
AUTH_URL = "https://www.strava.com/oauth/token"
ATHLETE_URL = "https://www.strava.com/api/v3/athlete"
client = system.net.httpClient(bypassCertValidation=True) #Bypassing cert validation. Might want to change
def get_access_token():
    """
    Exchanges the long-lived refresh token for a short-lived access token.
    Uses system.net.httpClient
    """

    
    payload = {
        'client_id': CLIENT_ID,
        'client_secret': CLIENT_SECRET,
        'refresh_token': REFRESH_TOKEN,
        'grant_type': 'refresh_token',
        'f': 'json'
    }

    print "Requesting new Access Token..."
    
    response = client.post(AUTH_URL, data=payload)
    
    if response.good:
        token_data = response.json
        access_token = token_data.get('access_token')
        print "Success! Access Token received.\n"
        return access_token
    else:
        print "Error authenticating: " + str(response.statusCode)
        #print response.text
        return None

def main():
	access_token = get_access_token()
	system.tag.writeBlocking("[default]AccessToken", access_token)