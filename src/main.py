# -*- coding: utf-8 -*-

# Sample Python code for youtube.channels.list
# See instructions for running these code samples locally:
# https://developers.google.com/explorer-help/guides/code_samples#python

import code
import os
import pickle

import google_auth_oauthlib.flow
import googleapiclient.discovery
import googleapiclient.errors
import logging

import pandas as pd
        
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
        self.oauth_token_file = 'credentials.pkl'

        self._youtube = googleapiclient.discovery.build(
            self.api_service_name, self.api_version, credentials=self.user_oauth())
        
    def user_oauth(self):
        filename = self.oauth_token_file
        # User is asked to grant app permission to access their youtube account, permission is saved to file
        if os.path.exists(filename):
            credentials = pickle.load(open(filename,'rb'))
        else:
            flow = google_auth_oauthlib.flow.InstalledAppFlow.from_client_secrets_file(
                self.client_secrets_file, self.scopes)
            credentials =  flow.run_console()
            pickle.dump(credentials, open(filename,'wb'))
        return credentials
        
    def list_playlists(self, id=None):
        kwargs = {'mine':True} if id is None else {}

        def request(nextPageToken=None, **kwargs):
            request = self._youtube.playlists().list(
                part="contentDetails,id,localizations,snippet,status",
                #part="id,snippet",
                maxResults=50,
                pageToken=nextPageToken,
                id=id,
                **kwargs
            )
            response = request.execute()
            return response
        
        nextPageToken=None
        responses=[]
        while True:
            response = request(nextPageToken=nextPageToken, **kwargs)
            responses.append(response)
            
            try:
                nextPageToken = response['nextPageToken']
            except:
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
        
        playlists = pd.DataFrame(playlists)
        return playlists
    
    def list_playlistitems(self, id):
        def request(nextPageToken=None):
            request = self._youtube.playlistItems().list(
                part="contentDetails,id,snippet,status",
                playlistId=id,
                maxResults=50,
                pageToken=nextPageToken
            )
            responses = request.execute()
            return responses
        
        nextPageToken=None
        videos=[]
        while True:
            response = request(nextPageToken=nextPageToken)
            videos+=response['items']
            
            try:
                nextPageToken = response['nextPageToken']
            except:
                break
        
        for video in videos:
            video.update(video.pop('contentDetails'))
            video.update(video.pop('status'))
            video.update(video.pop('snippet'))
            video.update(video.pop('resourceId'))
        videos = pd.DataFrame(videos)
        return videos

    # def __getattr__(self, item):
    #     func = getattr(self._youtube, item)
    #     return func

class Serenity:
    def __init__(self):
        ytc = YTConnector()
        self.playlists = ytc.list_playlists()
        self.videos = pd.concat(ytc.list_playlistitems(playlist) for playlist in self.playlists['id'])        
        pass
    

def main():
    yt = YTConnector()
    return yt

if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG, filename='myapp.log', format='%(asctime)s %(levelname)s:%(message)s')
    serenity = Serenity()
    yt = main()
    lists = yt.list_playlists()
    try:
        vid = yt.items_in_list(lists['id'][0])
    except:
        logging.error("Error getting access to a single playlist")

    code.interact(local=locals())
