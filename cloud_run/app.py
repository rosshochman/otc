import os, subprocess
from flask import Flask, request, abort

app = Flask(__name__)

@app.route("/", methods=["POST"])
def main():
    data = request.json
    os.environ["ROOT_FOLDER_ID"] = data["root"]
    o = subprocess.run(
        ["./gce_run.sh $ROOT_FOLDER_ID"],
        stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True
    )

    return "results"

if __name__ == "__main__":
    app.run(
        debug=True,
        host="0.0.0.0",
        port=int(os.environ.get("PORT", 8080))
    )
