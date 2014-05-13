# GrammerArtistAPI.py
# Date created: 5/13/14
# trevor.prater@gmail.com (Trevor Prater)
# jun.huang.cs@gmail.com (Jun Huang)

from datetime import date
import tornado.escape
import tornado.ioloop
import tornado.web
 
 #dummy to check if the API is up
class VersionHandler(tornado.web.RequestHandler):
    def get(self):
        response = { 'version': '0.0.1',
                     'latest_build':  date.today().isoformat() }
        self.write(response)
 
#Generate the mosaic image with link supplied, and also given a search tag.
class GenerateMosaicByLinkHandler(tornado.web.RequestHandler):
    #initialize the response JSON payload with the correct format
    def initialize(self):
        self.response = {"imagePixel":[], #image pixel, each pixcel will be an array element with a int value, this int value will be mapped to link in imageLinkDict
                    "imageSize":{"x":0, #width of the image
                                 "y":0  #height of the image
                                },
                    "imageLinkDict":{

                    }#image link dictionary, will be mapping int value to an actual link of image
        }
    #Get method, get a link from the user, and the search tag of their input
    #returns payload with the image informations
    def get(self):
        imageLink = self.get_argument('imageLink')  #get post argument imageLlink
        searchTag = self.get_argument('searchTag')  #get post argument search tag
        
        #Todo: call the actual image composer here and pack the reponse with image information

        #return the response
        self.write(self.response)

#application url mapping
application = tornado.web.Application([
    (r"/version", VersionHandler), #dummy version handler to see what value it is
    (r"/generateMosaicByLink",GenerateMosaicByLinkHandler) #generate a mosaic image with user supplying a link of original image and a search tag of their like
])
 
if __name__ == "__main__":  
    application.listen(8888)
    tornado.ioloop.IOLoop.instance().start()