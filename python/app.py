from authlib.integrations.flask_client import OAuth
from flask import Flask, url_for, session, render_template, make_response
from werkzeug.utils import redirect

app = Flask(__name__)
app.config.update(
    IDHUB_CLIENT_ID="ba0c161e-a22e-4caf-a8a2-b69d6f8b3bf0",
    IDHUB_CLIENT_SECRET="36b50957-6b51-4e15-b7ea-979e45413226"
)
app.secret_key = 'super secret key'
oauth = OAuth(app)

oauth.register("idhub",
               server_metadata_url='https://sso.idhub.io/auth/realms/external/.well-known/openid-configuration',
               client_kwargs={
                   'scope': 'openid email profile'
               })


@app.route('/auth')
def login():
    redirect_uri = url_for('authorize', _external=True)
    return oauth.idhub.authorize_redirect(redirect_uri)


@app.route('/logout')
def logout():
    resp = make_response(redirect('/'))
    resp.set_cookie('session', '', expires=0)
    return resp


@app.route('/auth/callback')
def authorize():
    token = oauth.idhub.authorize_access_token()
    user = oauth.idhub.parse_id_token(token)
    session['user'] = user
    return redirect('/')


@app.route('/')
def users():
    user = session.get('user')
    return render_template('home.html', user=user)


app.run('0.0.0.0', port=3000)
