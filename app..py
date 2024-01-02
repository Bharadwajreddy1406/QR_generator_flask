from flask import Flask, request, render_template, send_file
import qrcode
from io import BytesIO
# import base64
app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/generate_qr', methods=['POST'])
def generate_qr():
    input_text = request.form.get('qrtext')

    if not input_text:
        return render_template("index.html")

    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=50,
        border=1,
    )
    qr.add_data(input_text)
    qr.make(fit=True)

    img = qr.make_image(fill_color="black", back_color="white")

    buffer = BytesIO()
    img.save(buffer)
    buffer.seek(0)

    # preview = f"data:image/png;base64,{buffer.getvalue().decode('base64').encode('base64').decode('utf-8')}"
    # preview = base64.b64encode(buffer.read()).decode('utf-8')
    #
    # return render_template('index.html', preview=preview)

    return send_file(buffer, as_attachment=True, download_name=f'qrcode.png')

if __name__ == '__main__':
    app.run(debug=True, port=3000)
