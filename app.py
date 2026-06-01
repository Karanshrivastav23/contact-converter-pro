from flask import Flask, render_template, request, send_file
import pandas as pd
import os

app = Flask(__name__)

UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/convert', methods=['POST'])
def convert():

    if 'file' not in request.files:
        return "No file uploaded"

    file = request.files['file']

    if file.filename == '':
        return "No file selected"

    try:

        if file.filename.endswith('.xlsx'):
            df = pd.read_excel(file)

        elif file.filename.endswith('.csv'):
            df = pd.read_csv(file)

        else:
            return "Please upload CSV or Excel file"

        vcf_path = os.path.join(
            UPLOAD_FOLDER,
            "contacts.vcf"
        )

        with open(vcf_path, 'w', encoding='utf-8') as vcf:

            for _, row in df.iterrows():

                name = str(row['Name']).strip()

                phone = str(
                    row['Mobile Number']
                ).replace(".0", "").strip()

                if phone == "" or phone.lower() == "nan":
                    continue

                vcf.write("BEGIN:VCARD\n")
                vcf.write("VERSION:3.0\n")
                vcf.write(f"FN:{name}\n")
                vcf.write(f"TEL;TYPE=CELL:{phone}\n")
                vcf.write("END:VCARD\n")

        return send_file(
            vcf_path,
            as_attachment=True
        )

    except Exception as e:
        return str(e)

if __name__ == "__main__":
    app.run(debug=True)