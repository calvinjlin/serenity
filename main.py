# -*- coding: utf-8 -*-

# Sample Python code for youtube.channels.list
# See instructions for running these code samples locally:
# https://developers.google.com/explorer-help/guides/code_samples#python

import os
import pickle

import google_auth_oauthlib.flow
import googleapiclient.discovery
import googleapiclient.errors

# class YTDataBase:
#     def __init__(self):
        
class YTConnector:
    def __init__(self) -> None:
        super().__init__()
        # Disable OAuthlib's HTTPS verification when running locally.
        # *DO NOT* leave this option enabled in production.
        os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

        self.api_service_name = 'youtube'
        self.api_version = 'v3'
        self.scopes = ["https://www.googleapis.com/auth/youtube.force-ssl"]

        self.client_secrets_file = 'client_secret.json'

        self.youtube = googleapiclient.discovery.build(
            self.api_service_name, self.api_version, credentials=self.user_oauth_approval())
        
    def user_oauth_approval(self, filename='credentials.pkl'):
        # User is asked to grant app permission to access their youtube account, permission is saved to file
        if os.path.exists(filename):
            credentials = pickle.load(open(filename,'rb'))
        else:
            flow = google_auth_oauthlib.flow.InstalledAppFlow.from_client_secrets_file(
                self.client_secrets_file, self.scopes)
            credentials =  flow.run_console()
            pickle.dump(credentials, open(filename,'wb'))
        return credentials
        
    def my_playlists(self):
        responses=[]
        def send_request(nextPageToken=None):
            request = self.youtube.playlists().list(
                part="contentDetails,id,localizations,snippet,status",
                maxResults=50,
                pageToken=nextPageToken,
                mine=True
            )
            response = request.execute()
            return response
        
        nextPageToken=None
        while True:
            response = send_request(nextPageToken=nextPageToken)
            responses.append(response)
            
            if 'nextPageToken' in response:
                nextPageToken = response['nextPageToken']
            else:
                break
        
        
        # YouTube's response returns 'pages' with 50 playlists per page, here
        # unpack/unstack the pages so that all playlists are under the same item
        playlists=[]
        for response in responses:
            playlists+=response['items']
            
        # YouTube has some nested items such as 'privacyStatus' within 'status',
        # here we unnest them
        for playlist in playlists:
            playlist.update(playlist.pop('contentDetails'))
            playlist.update(playlist.pop('status'))
            playlist.update(playlist.pop('snippet'))
        return playlists
    
    def items_in_list(self):
        request = self.youtube.playlistItems().list(
        part="contentDetails,id,snippet,status",
        playlistId="PLtfX33kWQSAVoRK6yxLHxD3_6rdtUa5WQ"
        )
        
def main():
    yt = YTConnector()
    return yt.my_playlists()

if __name__ == "__main__":
    yt = main()
    print(yt)