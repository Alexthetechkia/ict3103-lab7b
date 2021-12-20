from flask import Flask, redirect, url_for, render_template, request

app = Flask(__name__)


@app.route("/", methods=['GET','POST'])
def home():
    if request.method == 'POST':
        search_term = request.form['searchterm']
        
        excluded_chars = "*?!'^+%&/()=}][{$#;"
        for char in search_term:
            if char in excluded_chars:
                return render_template('index.html', rejected=True)
        return render_template('success.html', search_term=search_term)
                
    return render_template('index.html', rejected=False)


if __name__ == "__main__":
    app.run(debug=True, port=80)