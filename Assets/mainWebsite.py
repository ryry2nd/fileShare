from flask import Flask, render_template, request, redirect, url_for, send_file, flash
import html, os

class MainWebsite:
    def __init__(self, app:Flask):
        self.app = app
        self.init(app)

    def isForm(self):
        for idx, d in request.form.items():
            if idx == "password":
                return True
        return False

    def render_share(self):
        return render_template("fileShare.html", filenames=os.listdir(self.app.config["UPLOAD_FOLDER"]), password=self.app.config["password"])


    def init(self, app: Flask):
        @app.route("/", methods=["POST", "GET"])
        def index():
            if request.method == "GET":
                return render_template("index.html")
            else:
                if self.isForm():
                    if html.escape(request.form["password"]) == app.config["password"]:
                        return self.render_share()
                    else:
                        return render_template("index.html")
                else:
                    if 'file' not in request.files:
                        flash('No file part')
                        return self.render_share()

                    file = request.files['file']

                    if file.filename == '':
                        flash('No file selected for uploading')
                        return self.render_share()

                    file.save(os.path.join(self.app.config["UPLOAD_FOLDER"], file.filename))
                    return self.render_share()

        @app.route("/download_file", methods=["POST"])
        def download_file():
            print(request.form.get("comp_select"))
            if request.form["password"] == app.config["password"]:
                return send_file(os.path.join(self.app.config["UPLOAD_FOLDER"], request.form["fileName"]), as_attachment=True)
            else:
                return render_template("index.html")