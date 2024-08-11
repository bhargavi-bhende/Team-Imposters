from flask import Flask, render_template, request, redirect, url_for, send_file
import os
import numpy as np
import svgwrite
import cairosvg
from sklearn.linear_model import LinearRegression
from scipy.optimize import leastsq

app = Flask(__name__)

UPLOAD_FOLDER = 'uploads/'
OUTPUT_FOLDER = 'output/'

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['OUTPUT_FOLDER'] = OUTPUT_FOLDER

def read_csv(csv_path):
    np_path_XYs = np.genfromtxt(csv_path, delimiter=',')
    path_XYs = []
    for i in np.unique(np_path_XYs[:, 0]):
        npXYs = np_path_XYs[np_path_XYs[:, 0] == i][:, 1:]
        XYs = []
        for j in np.unique(npXYs[:, 0]):
            XY = npXYs[npXYs[:, 0] == j][:, 1:]
            XYs.append(XY)
        path_XYs.append(XYs)
    return path_XYs

def identify_shapes(XY):
    if is_line(XY):
        return 'line', fit_line(XY)
    elif is_circle(XY):
        return 'circle', fit_circle(XY)
    elif is_ellipse(XY):
        return 'ellipse', fit_ellipse(XY)
    elif is_rectangle(XY):
        return 'rectangle', fit_rectangle(XY)
    else:
        return 'unknown', XY

def is_line(XY):
    model = LinearRegression()
    X = XY[:, 0].reshape(-1, 1)
    y = XY[:, 1]
    model.fit(X, y)
    score = model.score(X, y)
    return score > 0.95

def fit_line(XY):
    return np.array([XY[0], XY[-1]])

def is_circle(XY):
    center, radius = fit_circle(XY)
    distances = np.linalg.norm(XY - center, axis=1)
    return np.std(distances) < 0.05

def fit_circle(XY):
    A = np.hstack([2 * XY, np.ones((XY.shape[0], 1))])
    b = np.sum(XY ** 2, axis=1)
    center = np.linalg.lstsq(A, b, rcond=None)[0][:2]
    radius = np.sqrt(np.mean(np.sum((XY - center) ** 2, axis=1)))
    return center, radius

def is_ellipse(XY):
    params = fit_ellipse(XY)
    center = params[:2]
    distances = np.linalg.norm(XY - center, axis=1)
    return np.std(distances) < 0.05

def fit_ellipse(XY):
    x = XY[:, 0]
    y = XY[:, 1]

    def ellipse_residuals(params, x, y):
        xc, yc, a, b, theta = params
        cos_theta, sin_theta = np.cos(theta), np.sin(theta)
        x_rot = cos_theta * (x - xc) + sin_theta * (y - yc)
        y_rot = -sin_theta * (x - xc) + cos_theta * (y - yc)
        return ((x_rot / a) ** 2 + (y_rot / b) ** 2 - 1)

    xc_guess, yc_guess = np.mean(x), np.mean(y)
    a_guess, b_guess = np.ptp(x) / 2, np.ptp(y) / 2
    theta_guess = 0
    params_guess = [xc_guess, yc_guess, a_guess, b_guess, theta_guess]

    params_opt, _ = leastsq(ellipse_residuals, params_guess, args=(x, y))
    return params_opt

def is_rectangle(XY):
    if len(XY) != 4:
        return False
    d1 = np.linalg.norm(XY[0] - XY[1])
    d2 = np.linalg.norm(XY[1] - XY[2])
    d3 = np.linalg.norm(XY[2] - XY[3])
    d4 = np.linalg.norm(XY[3] - XY[0])
    diag1 = np.linalg.norm(XY[0] - XY[2])
    diag2 = np.linalg.norm(XY[1] - XY[3])
    return np.isclose(d1, d3, atol=0.05) and np.isclose(d2, d4, atol=0.05) and np.isclose(diag1, diag2, atol=0.05)

def fit_rectangle(XY):
    return np.array([XY[0], XY[1], XY[2], XY[3], XY[0]])

def generate_circle(center, radius, num_points=100):
    angles = np.linspace(0, 2 * np.pi, num_points)
    circle_points = np.array([
        center[0] + radius * np.cos(angles),
        center[1] + radius * np.sin(angles)
    ]).T
    return circle_points

def polylines2svg(paths_XYs, svg_path):
    W, H = 0, 0
    for path_XYs in paths_XYs:
        for XY in path_XYs:
            W, H = max(W, np.max(XY[:, 0])), max(H, np.max(XY[:, 1]))
    padding = 0.1
    W, H = int(W + padding * W), int(H + padding * H)

    dwg = svgwrite.Drawing(svg_path, profile='tiny', shape_rendering='crispEdges')
    group = dwg.g()
    colours = ['black'] * len(paths_XYs)

    for i, path in enumerate(paths_XYs):
        shape_type, parameters = identify_shapes(path[0])
        c = colours[i % len(colours)]
        if shape_type == 'line':
            path_data = [("M", (parameters[0, 0], parameters[0, 1])),
                         ("L", (parameters[1, 0], parameters[1, 1]))]
        elif shape_type == 'circle':
            circle_points = generate_circle(parameters[0], parameters[1])
            path_data = [("M", (circle_points[0, 0], circle_points[0, 1]))]
            path_data += [("L", (x, y)) for x, y in circle_points[1:]]
            path_data.append(("Z", None))
        elif shape_type == 'ellipse':
            xc, yc, a, b, theta = parameters
            angles = np.linspace(0, 2 * np.pi, 100)
            ellipse_points = np.array([
                xc + a * np.cos(angles) * np.cos(theta) - b * np.sin(angles) * np.sin(theta),
                yc + a * np.cos(angles) * np.sin(theta) + b * np.sin(angles) * np.cos(theta)
            ]).T
            path_data = [("M", (ellipse_points[0, 0], ellipse_points[0, 1]))]
            path_data += [("L", (x, y)) for x, y in ellipse_points[1:]]
            path_data.append(("Z", None))
        elif shape_type == 'rectangle':
            path_data = [("M", (parameters[0, 0], parameters[0, 1]))]
            path_data += [("L", (x, y)) for x, y in parameters[1:]]
            path_data.append(("Z", None))
        else:
            path_data = [("M", (path[0][0, 0], path[0][0, 1]))]
            path_data += [("L", (x, y)) for x, y in path[0][1:]]

        group.add(dwg.path(d=path_data, fill='none', stroke=c, stroke_width=2))

    dwg.add(group)
    dwg.save()

    png_path = svg_path.replace('.svg', '.png')
    cairosvg.svg2png(url=svg_path, write_to=png_path, parent_width=W, parent_height=H,
                     output_width=W, output_height=H, background_color='white')


def main(csv_input_path, svg_output_path):
    paths_XYs = read_csv(csv_input_path)
    polylines2svg(paths_XYs, svg_output_path)
    
@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        
        if 'file' not in request.files:
            return redirect(request.url)
        file = request.files['file']
        if file.filename == '':
            return redirect(request.url)
        if file:
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
            file.save(file_path)
            
            svg_filename = os.path.splitext(file.filename)[0] + '.svg'
            svg_output_path = os.path.join(app.config['OUTPUT_FOLDER'], svg_filename)
            
            paths_XYs = read_csv(file_path)
            polylines2svg(paths_XYs, svg_output_path)
            
            return redirect(url_for('download_file', filename=svg_filename))
    
    return render_template('home.html')

@app.route('/')
def home():
    return render_template('home.html')


@app.route('/upload', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST':
        file = request.files['file']
        if file:
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
            file.save(file_path)
            
            svg_filename = os.path.splitext(file.filename)[0] + '.svg'
            svg_output_path = os.path.join(app.config['OUTPUT_FOLDER'], svg_filename)
            
            main(file_path, svg_output_path)
            
            png_filename = svg_filename.replace('.svg', '.png')
            return render_template('upload.html', image_url=png_filename)
    
    return render_template('upload.html')

@app.route('/download/<filename>')
def download_file(filename):
    return send_file(os.path.join(app.config['OUTPUT_FOLDER'], filename))

@app.route('/output/<filename>')
def display_image(filename):
    return send_file(os.path.join(app.config['OUTPUT_FOLDER'], filename))


@app.route('/download/<filename>')
def download_image(filename):
    return send_file(os.path.join('output', filename), as_attachment=True)


if __name__ == '__main__':
    os.makedirs(UPLOAD_FOLDER, exist_ok=True)
    os.makedirs(OUTPUT_FOLDER, exist_ok=True)
    app.run(debug=True)
