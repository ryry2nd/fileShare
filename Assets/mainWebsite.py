from flask import Flask, render_template, request, redirect, url_for, send_file
import os

class MainWebsite:
    def __init__(self, app:Flask):
        self.app = app
        self.init(app)

    def render_share(self):
        return render_template("fileShare.html", filenames=os.listdir(self.app.config["UPLOAD_FOLDER"]), password=self.app.config["password"])

    def init(self, app: Flask):
        @app.route("/", methods=["GET"])
        def index():
            return render_template("index.html")
                
        @app.route("/fileShare", methods=["POST"])
        def fileShare():
            if request.form["password"] == app.config["password"]:
                return self.render_share()
            else:
                return redirect(url_for("index"))
        
        @app.route("/upload_file", methods=["POST"])
        def upload_file():
            if request.form["password"] == app.config["password"]:
                file = request.files['file']
                file.save(os.path.join(self.app.config["UPLOAD_FOLDER"], file.filename))
                return self.render_share()
            else:
                return redirect(url_for("index"))

        @app.route("/download_file", methods=["POST"])
        def download_file():
            if request.form["password"] == app.config["password"]:
                return send_file(os.path.join(self.app.config["UPLOAD_FOLDER"], request.form["fileName"]), as_attachment=True)
            else:
                return redirect(url_for("index"))
        
        @app.route("/delete_file", methods=["POST"])
        def delete_file():
            if request.form["password"] == app.config["password"]:
                os.remove(os.path.join(self.app.config["UPLOAD_FOLDER"], request.form["fileName"]))
                return self.render_share()
            else:
                return redirect(url_for("index"))