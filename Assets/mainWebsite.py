from flask import Flask, render_template, request, redirect, url_for, send_file
import html, os

class MainWebsite:
    def __init__(self, app:Flask):
        self.app = app
        self.initPoll(app)

    def isForm(self):
        for idx, d in request.form.items():
            if idx == "password":
                return True
        return False

    def initPoll(self, app: Flask):
        @app.route("/", methods=["POST", "GET"])
        def index():
            if request.method == "GET":
                return render_template("index.html")
            else:
                if self.isForm():
                    if html.escape(request.form["password"]) == "Spongebob!":
                        return render_template("fileShare.html", filenames=os.listdir(self.app.config["UPLOAD_FOLDER"]))
                    else:
                        return render_template("index.html")
                else:
                    f = request.files['file']
                    f.save(os.path.join(self.app.config["UPLOAD_FOLDER"], f.filename))
                    return redirect(url_for('index'))

        @app.route('/download', methods=["POST"])
        def download_file():
            return send_file(os.path.join(self.app.config["UPLOAD_FOLDER"], request.form["fileName"]), as_attachment=True)