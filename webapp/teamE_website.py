from flask import Flask, render_template, send_from_directory
app = Flask(__name__)

# home page
@app.route('/')
def index():
    return render_template('index.html')

# blank-page
@app.route('/blank-page.html')
def blank_page():
    return render_template('blank-page.html')

# bootstrap-elements
@app.route('/bootstrap-elements.html')
def bootstrap_elements():
    return render_template('bootstrap-elements.html')

# bootstrap-grid
@app.route('/bootstrap-grid.html')
def bootstrap_grid():
    return render_template('bootstrap-grid.html')

# charts
@app.route('/charts.html')
def charts():
    return render_template('charts.html')

#forms
@app.route('/forms.html')
def forms():
    return render_template('forms.html')# bootstrap-grid

#index-rtl
@app.route('/index-rtl.html')
def index_rtl():
    return render_template('index-rtl.html')

#tables
@app.route('/tables.html')
def tables():
      return render_template('tables.html')


#Rerouting
@app.route('/css/<path:path>')
def send_css(path):
    return send_from_directory('static/css', path)

@app.route('/font-awesome/<path:path>')
def send_font_awesome(path):
    return send_from_directory('static/font-awesome', path)

@app.route('/fonts/<path:path>')
def send_fonts(path):
    return send_from_directory('static/fonts', path)

@app.route('/js/<path:path>')
def send_js(path):
    return send_from_directory('static/js', path)




if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)
