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
import webapp2, cgi, re


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

form_sign_up="""
<!DOCTYPE html>

<html>
  <head>
    <title>Sign Up</title>
    <style type="text/css">
      .label {text-align: right}
      .error {color: red}
    </style>

  </head>

  <body>
    <h2>Signup</h2>
    <form method="post">
      <table>
        <tr>
          <td class="label">
            Username
          </td>
          <td>
            <input type="text" name="username" value="%(username)s">
          </td>
          <td class="error">
            %(typeerror1)s
          </td>
        </tr>

        <tr>
          <td class="label">
            Password
          </td>
          <td>
            <input type="password" name="password" value="%(password)s">
          </td>
          <td class="error">
            %(typeerror2)s
          </td>
        </tr>

        <tr>
          <td class="label">
            Verify Password
          </td>
          <td>
            <input type="password" name="verify" value="%(verify)s">
          </td>
          <td class="error">
            %(typeerror3)s
          </td>
        </tr>

        <tr>
          <td class="label">
            Email (optional)
          </td>
          <td>
            <input type="text" name="email" value="%(email)s">
          </td>
          <td class="error">
            %(typeerror4)s
          </td>
        </tr>
      </table>

      <input type="submit">
    </form>
  </body>

</html>
"""

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

USER_RE = re.compile(r"^[a-zA-Z0-9_-]{3,20}$")
PWD_RE = re.compile(r"^.{3,20}$")
EMAIL_RE = re.compile(r"^[\S]+@[\S]+\.[\S]+$")

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

def valid_username(username):
    return USER_RE.match(username)
    
def valid_password(password):
    return PWD_RE.match(password)

def valid_email(email):
    return EMAIL_RE.match(email)        
 
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

class Unit2SignUpHandler(webapp2.RequestHandler):
    def write_form(self, username="", password="", verify="", email="", flag=""):
        
        typeerror1 = ""
        typeerror2 = ""
        typeerror3 = ""
        typeerror4 = ""
        
        if flag != "":
            if not valid_username(username) :
                typeerror1 = "That's not a valid username. "
                
            if not valid_password(password):
                typeerror2 = "That wasn't a valid password. "
            elif password != verify:
                typeerror3 = "Your passwords didn't match."
                
            if not valid_email(email) and email != "":
                typeerror4 = "That's not a valid email."
        
        self.response.out.write(form_sign_up % {"username": escape_html(username),
                                                "password": "",
                                                "verify": "",
                                                "email": escape_html(email),
                                                "typeerror1": typeerror1,
                                                "typeerror2": typeerror2,
                                                "typeerror3": typeerror3,
                                                "typeerror4": typeerror4})
                                                

    def get(self):
        self.write_form()
    def post(self):
        username = self.request.get('username')
        password = self.request.get('password')
        verify = self.request.get('verify')
        email = self.request.get('email')
        
        
        if not (valid_username(username), valid_password(password), valid_password(verify), valid_email(email)) or password != verify:
            self.write_form(username, password, verify, email, "1")
        else:
            self.redirect("/unit2/welcome?username="+username)
            
class Unit2WelcomeHandler(webapp2.RequestHandler):
    def get(self):
        username = self.request.get('username')
        self.response.out.write("Welcome, " +username+ "!")     

app = webapp2.WSGIApplication([
    ('/', MainHandler), ('/unit2/rot13', Unit2Rot13Handler), ('/unit2/signup', Unit2SignUpHandler), ('/unit2/welcome', Unit2WelcomeHandler)
], debug=True)
