import dropbox
import os
from os import path
from viset.cache import Cache
import urlparse

class Dropbox():
    _access_token = os.environ.get('BUBO_DROPBOX_ACCESS_TOKEN')
    _app_key = os.environ.get('BUBO_DROPBOX_APP_KEY')
    _app_secret = os.environ.get('BUBO_DROPBOX_APP_SECRET_KEY')

    # save access token to cache
    # http://stackoverflow.com/questions/10549326/python-dropbox-api-save-token-file
    # should we put keys in this file?  everyone will use it
    
    def __init__(self):
        if self._access_token is None:
            self.link()
    
    def link(self):
        flow = dropboxapi.client.DropboxOAuth2FlowNoRedirect(self._app_key, self._app_secret)

        authorize_url = flow.start()
        print '1. Go to: ' + authorize_url
        print '2. Click "Allow" (you might have to log in first)'
        print '3. Copy the authorization code.'
        code = raw_input("Enter the authorization code here: ").strip()

        # This will fail if the user enters an invalid authorization code
        access_token, user_id = flow.finish(code)
        self._access_token = access_token
        return access_token

    def put(self, filename):
        client = dropbox.client.DropboxClient(self._access_token)
        print 'linked account: ', client.account_info()

        dropbox_path = '/'+path.basename(filename)
        f = open(filename)
        response = client.put_file(dropbox_path, f)
        print 'uploaded: ', response

        folder_metadata = client.metadata('/')
        print 'metadata: ', folder_metadata

        share = client.share(dropbox_path, short_url=False)

        # https://www.dropbox.com/help/201/en
        p = urlparse.urlparse(share['url'])
        public_url = urlparse.urlunsplit(('http','dl.dropboxusercontent.com',p[2],None,None))
        public_url = public_url + '?dl=1'
        return public_url
    
    def get(self, filename, cache=Cache()):
        client = dropbox.client.DropboxClient(self._access_token)
        f, metadata = client.get_file_and_metadata('/'+filename)
        cachefile = cache.cachefile(filename)
        out = open(cachefile, 'w')
        out.write(f.read())
        out.close()
        print metadata
        return cachefile

