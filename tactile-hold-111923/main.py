#!/usr/bin/env python
#
# Copyright 2007 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
import webapp2, cgi

ciper_dict = {
'A':'N','B':'O','C':'P','D':'Q','E':'R','F':'S',
'G':'T','H':'U','I':'V','J':'W','K':'X','L':'Y',
'M':'Z','N':'A','O':'B','P':'C','Q':'D','R':'E',
'S':'F','T':'G','U':'H','V':'I','W':'J','X':'K',
'Y':'L','Z':'M',
'a':'n','b':'o','c':'p','d':'q','e':'r','f':'s',
'g':'t','h':'u','i':'v','j':'w','k':'x','l':'y',
'm':'z','n':'a','o':'b','p':'c','q':'d','r':'e',
's':'f','t':'g','u':'h','v':'i','w':'j','x':'k',
'y':'l','z':'m',}

def escape_html(s):
    return cgi.escape(s, quote = True)

def ciper_char(text):
    result = ""
    for char in text:
        if char in ciper_dict.keys():
            result = result + ciper_dict[char]
        else:
            result = result + char
    return result
        

form="""
<!DOCTYPE html>

<html>
  <head>
    <title>Unit 2 Rot 13</title>
  </head>

  <body>
    <h2>Enter some text to ROT13:</h2>
    <form method="post">
      <textarea name="text"
                style="height: 100px; width: 400px;">%(gTxt)s</textarea>
      <br>
      <input type="submit">
    </form>
  </body>

</html>
"""
class MainHandler(webapp2.RequestHandler):
    def get(self):
        self.response.write('Hello world!')

class Unit2Rot13Handler(webapp2.RequestHandler):
    def write_form(self, gTxt=""):
        self.response.out.write(form % {"gTxt": escape_html(gTxt)})
    def get(self):
        self.write_form()
    def post(self):
        gTxt = self.request.get('text')
        gTxt = ciper_char(gTxt)
        self.write_form(gTxt)


app = webapp2.WSGIApplication([
    ('/', MainHandler), ('/unit2/rot13', Unit2Rot13Handler)
], debug=True)
