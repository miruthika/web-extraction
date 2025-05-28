from flask import Flask, render_template, request
from extractor import extract_web_data

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        url = request.form.get('url')
        data = extract_web_data(url)
        return render_template('result.html', url=url, data=data)
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
