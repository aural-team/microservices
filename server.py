from flask import Flask
from flask import request
from polly import generate_audio
import os
app = Flask(__name__)

@app.route("/polly")
def polly():
    count = request.args.get('count', 15)
    tmpfile, audiofile = generate_audio(article_count=int(count))
    with open(audiofile, 'r') as f:
        content = f.read()
    os.remove(tmpfile)
    os.remove(audiofile)
    return content, 200

if __name__ == "__main__":
	app.run(host = "0.0.0.0", port=8000)