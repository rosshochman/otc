import os, subprocess
from flask import Flask, request, abort
from gce_command import cmd

app = Flask(__name__)

@app.route("/")
def main():
    os.system(cmd)
    return "completed otc request"

if __name__ == "__main__":
    app.run(
        debug=True,
        host="0.0.0.0",
        port=int(os.environ.get("PORT", 8080))
    )
