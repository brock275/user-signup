from flask import Flask, request, redirect
import cgi
import os

template_dir = os.path.join(os.path.dirname(__file__), 'templates')

app = Flask(__name__)
app.config['DEBUG'] = True

form = """
    <!doctype html>
    <html>
        <head>
            <style>
                .error {{ color: red; }}
            </style>
        </head>
        <body>
            <h1>Signup</h1>
            <form method="post">
                <table>
                    <tbody>
                        <tr>
                            <td>
                                <label for="username">Username</label>
                            </td>
                            <td>
                                <input name="username" type="text" value='{{username}}'>
                                <span class="error"></span>
                            </td>
                        </tr>
                        <tr>
                            <td>
                                <label for="password">Password</label>
                            </td>
                            <td>
                                <input name="password" type="password" value='{{password}}'>
                                <span class="error"></span>
                            </td>
                        </tr>
                        <tr>
                            <td>
                                <label for="verify">Verify</label>
                            </td>
                            <td>
                                <input name="verify" type="password" value='{{verify}}'>
                                <span class="error"></span>
                            </td>
                        </tr>
                        <tr>
                            <td>
                                <label for="email">Email (optional)</label>
                            </td>
                            <td>
                                <input name="email" value='{{email}}'>
                                <span class="error"></span>
                            </td>
                        </tr>
                    </tbody>
                </table>
                <input type="submit">
            </form>
        </body>
    </html>
"""


@app.route("/", methods=['POST'])
def index():
    return form.format(username='', password='', verify='', email='')

def empty(word):
    if word:
        return True
    else:
        return False

def count(word):
    if len(word) < 3 or len(word) >20:
        return False
    else:
        return True

def is_same(password, verify):
    if password == verify:
        return True
    else:
        return False

def character_test(word):
    good_characters = 'abcdefghijklmnopqrstuvwxyz.@'
    for i in word:
        if i in good_characters:
            return True
        else:
            return False
def count_char(word, char):
    char_count = 0
    for i in word:
        if i == char:
            char_count = char_count + 1
    if char_count == 1:
        return True
    else:
        return False

@app.route("/", methods=["POST"  ])
def signup_complete():
    username=request.form['username']
    password=request.form['password']
    verify=request.form['verify']
    email=request.form['email']

    username_error = ""
    password_error = ""
    password_validate_error = ""
    email_error = ""

    error_required = "Required field"
    error_reenter_pw = "Please re-enter password"
    error_char_count = "must be between 3 and 20 characters"
    error_no_spaces = "must not contain spaces"

# Password tests

    if not empty(password):
        password_error = error_required
        password = ''
        password_validate = ''
    elif not count(password):
        password_error = "Password " + error_char_count
        password = ''
        password_validate = ''
        password_validate_error = error_reenter_pw
    else:
        if " " in password:
            password_error = "Password " + error_no_spaces
            password = ''
            password_validate = ''
            password_validate_error = error_reenter_pw

    if verify != password:
        password_validate_error = "Passwords must match"
        password = ''
        password_validate = ''
        password_error = 'Passwords must match'
            

#Username tests

    if not empty(username):
        username_error = error_required
        password = ''
        password_validate = ''
        password_error = error_reenter_pw
        password_validate_error = error_reenter_pw
    elif not count(username):
        username_error = "Username " + error_char_count
        password = ''
        password_validate = ''
        password_error = error_reenter_pw
        password_validate_error = error_reenter_pw
    else:
        if " " in username:
            username_error = "Username " + error_no_spaces
            password = ''
            password_validate = ''
            password_error = error_reenter_pw
            password_validate_error = error_reenter_pw

#Email tests

    if empty(email):
        if not count(email):
            email_error = "Email " + error_char_count
            password = ''
            password_validate = ''
            password_error = error_reenter_pw
            password_validate_error = error_reenter_pw
        elif not count_char(email, "@"):
            email_error = "Email must contain the @ symbol once."
            password = ''
            password_validate = ''
            password_error = error_reenter_pw
            password_validate_error = error_reenter_pw
        
        elif not count_char(email, "."):
            email_error = 'Email must contain one "."'
            password = ''
            password_validate = ''
            password_error = error_reenter_pw
            password_validate_error = error_reenter_pw
        else:
            if " " in email:
                email_error = "Email " + error_no_spaces
                password = ''
                password_validate = ''
                password_error = error_reenter_pw
                password_validate_error = error_reenter_pw
    if not username_error and not password_error and not password_validate_error and not email_error:
        username = username
        return redirect('/welcome?username={0}'.format(username))
    else:
        return form.format(username_error=username_error, username=username, password_error=password_error, password=password, password_validate_error=password_validate_error, password_validate=password_validate, email_error=email_error, email=email)



@app.route('/welcome')
def valid_signup():
    username = request.args.get('username')
    return render_template('welcome.html', username=username)

app.run()


