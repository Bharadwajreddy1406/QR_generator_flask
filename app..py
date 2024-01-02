from flask import Flask, request, render_template, send_file,session
import qrcode
from io import BytesIO
app = Flask(__name__)
app.secret_key = "hilsd@1234$$dsgsfs"
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/generate_qr', methods=['POST'])
def generate_qr():
    input_text = request.form.get('qrtext')

    session[input_text] = input_text
    if not session[input_text]:
        return render_template("index.html")

    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=50,
        border=1,
    )
    qr.add_data(session[input_text])
    qr.make(fit=True)

    img = qr.make_image(fill_color="black", back_color="white")
    img.save("download.png")

    buffer = BytesIO()
    img.save(buffer)
    buffer.seek(0)

    return send_file(buffer, as_attachment=True, download_name=f'qrcode.png')

if __name__ == '__main__':
    app.run()
