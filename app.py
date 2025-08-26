#for reg
from flask import Flask, render_template, request, send_from_directory
from reportlab.pdfgen import canvas
import secrets

#for bg task
import os, time, glob

TMP_DIR = "static/tmp"
def cleanup_old_pdfs():
    now = time.time()
    for file in glob.glob(os.path.join(TMP_DIR, "*.pdf")):
        if os.stat(file).st_mtime < now - 2 * 60 * 60:  # older than 2 hours
            os.remove(file)

app = Flask(__name__)
app.secret_key = secrets.token_hex(64)

@app.before_request
def auto_cleanup():
    cleanup_old_pdfs()

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        select = request.form.get('export_as')
        filename = secrets.token_hex(32)
        input_gl = request.form.get('text_input')

        if select=="txt":
            real_name = "static/tmp/" + filename + ".txt"
            with open(real_name, 'w') as f:
                f.write(input_gl)
            name = filename + ".txt"
            return send_from_directory("static/tmp", name, as_attachment=True)

        elif select=="pdf":
            real_name = "static/tmp/" + filename + ".pdf"
            # generate PDF
            c = canvas.Canvas(real_name, pagesize=(595.27, 841.89))
            c.drawString(50, 780, input_gl)
            c.showPage()
            c.save()
            name = filename + ".pdf"
            return send_from_directory("static/tmp", name, as_attachment=True)

        elif select=="html":
            real_name = "static/tmp/" + filename + ".html"
            with open(real_name, 'w') as f:
                f.write(input_gl)
            name=filename+".html"
            return send_from_directory("static/tmp", name, as_attachment=True)

    # GET -> fresh page
    return render_template("index.html")

if __name__ == "__main__":
    app.run()
