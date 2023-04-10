from flask import Flask, redirect, abort

app = Flask(__name__)

@app.route('/<short_code>')
def redirect_to_url(short_code):
    link = Link.query.filter_by(short_code=short_code).first()
    if link:
        link.visits += 1
        db.session.commit()
        return redirect(link.url)
    else:
        abort(404)
