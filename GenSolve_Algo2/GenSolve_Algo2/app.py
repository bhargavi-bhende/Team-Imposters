from flask import Flask, render_template, request, redirect, url_for, send_from_directory
import os
import svgwrite
import cairosvg
import numpy as np
from shapely.geometry import Polygon
import random

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads/'
app.config['OUTPUT_FOLDER'] = 'output/'

def read_csv(csv_path):
    np_path_XYs = np.genfromtxt(csv_path, delimiter=',')
    path_XYs = []
    for i in np.unique(np_path_XYs[:, 0]):
        npXYs = np_path_XYs[np_path_XYs[:, 0] == i][:, 1:]
        XYs = [npXYs[npXYs[:, 0] == j][:, 1:] for j in np.unique(npXYs[:, 0])]
        path_XYs.append(XYs)
    return path_XYs

def is_polygon(XY):
    if len(XY) < 3:
        return False
    try:
        polygon = Polygon(XY)
        return polygon.is_valid and polygon.area > 0
    except:
        return False

def complete_incomplete_curve(XY):
    return np.vstack([XY, XY[0]])

def complete_curves(paths_XYs):
    completed_paths = []
    for path_XYs in paths_XYs:
        path = []
        for XY in path_XYs:
            if not np.allclose(XY[0], XY[-1]):
                XY = complete_incomplete_curve(XY)
            path.append(XY)
        completed_paths.append(path)
    return completed_paths

def generate_colors(num_paths):
    return [svgwrite.utils.rgb(random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)) for _ in range(num_paths)]

def polylines_to_svg(paths_XYs, colors, svg_path):
    W, H = 800, 600
    dwg = svgwrite.Drawing(svg_path, profile='tiny', size=(W, H))
    group = dwg.g()
    for path_XYs, color in zip(paths_XYs, colors):
        for XY in path_XYs:
            if XY.shape[0] > 1:
                path_data = "M " + " L ".join([f"{x},{y}" for x, y in XY]) + " Z"
                group.add(dwg.path(d=path_data, fill=color, stroke='black', stroke_width=2))
    dwg.add(group)
    dwg.save()
    png_path = svg_path.replace('.svg', '.png')
    cairosvg.svg2png(url=svg_path, write_to=png_path, output_width=W, output_height=H, background_color='white')

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        if 'file' not in request.files:
            return redirect(request.url)
        file = request.files['file']
        if file.filename == '':
            return redirect(request.url)
        if file:
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
            file.save(filepath)
            paths_XYs = read_csv(filepath)
            paths_XYs = complete_curves(paths_XYs)
            colors = generate_colors(len(paths_XYs))
            svg_filename = f"{file.filename.rsplit('.', 1)[0]}.svg"
            svg_path = os.path.join(app.config['OUTPUT_FOLDER'], svg_filename)
            polylines_to_svg(paths_XYs, colors, svg_path)
            return redirect(url_for('result', filename=svg_filename))
    return render_template('index.html')

@app.route('/result/<filename>')
def result(filename):
    return render_template('result.html', filename=filename)

@app.route('/output/<filename>')
def output_file(filename):
    return send_from_directory(app.config['OUTPUT_FOLDER'], filename)

if __name__ == "__main__":
    if not os.path.exists(app.config['UPLOAD_FOLDER']):
        os.makedirs(app.config['UPLOAD_FOLDER'])
    if not os.path.exists(app.config['OUTPUT_FOLDER']):
        os.makedirs(app.config['OUTPUT_FOLDER'])
    app.run(debug=True)
