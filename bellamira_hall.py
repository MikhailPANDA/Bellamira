from Common import urls
from db_controller import *

google_reg = {"web": {"client_id":"890621792831-7gh2uv62k8rpovqs3lrh5bc5q90unh8f.apps.googleusercontent.com",
                      "project_id":"bellamira-146516","auth_uri":"https://accounts.google.com/o/oauth2/auth",
                      "token_uri":"https://accounts.google.com/o/oauth2/token",
                      "auth_provider_x509_cert_url":"https://www.googleapis.com/oauth2/v1/certs",
                      "client_secret":"dcpF93fM7ktZzoXRsX5aUykR"}}

dbCreator().execute()

app = web.application(urls, globals())

if __name__ == '__main__':
    print "http://localhost:8080/renters/"
    print "http://localhost:8080/halls/"
    app.run()
