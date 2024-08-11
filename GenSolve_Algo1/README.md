
# Adobe GenSolve Algorithm 1

## Overview

The tool is a web application designed to process and visualize 2D curve data. Users can upload CSV files containing curve data, which are analyzed to identify and fit shapes such as lines, circles, ellipses, and rectangles. The results are visualized as SVG images, which can also be downloaded as PNG files.

## Features

- **Upload CSV Files**: Upload CSV files containing 2D curve data.
- **Shape Identification**: Automatically detects and fits shapes including lines, circles, ellipses, and rectangles.
- **SVG Generation**: Converts detected shapes into SVG files.
- **PNG Conversion**: Converts SVG files to PNG images.
- **Download**: Download the processed SVG and PNG files.

## Installation

### Prerequisites

1. **Python**: Python 3.6 or higher is required. Download it from [python.org](https://www.python.org/downloads/).
2. **Virtual Environment** (optional but recommended):
   ```bash
   python -m venv venv
   source venv/bin/activate   # On Windows use `venv\Scripts\activate`
   ```

### Dependencies

Install the necessary Python packages using `pip`:

```bash
pip install numpy svgwrite cairosvg scikit-learn scipy flask
```

## Setup

1. **Create Required Directories**: Ensure the `uploads/` and `output/` directories exist in your project directory. These directories are used to store uploaded files and generated outputs.
   ```bash
   mkdir uploads output
   ```

2. **Flask Application**: The Flask application handles file uploads, shape identification, SVG generation, and provides download links for the processed images.

## Usage

### Running the Web Application

1. **Start the Flask Server**:
   ```bash
   python app.py
   ```
   The application will run on `http://127.0.0.1:5000/`.

2. **Access the Application**: Open a web browser and go to `http://127.0.0.1:5000/`.

3. **Upload CSV File**: Use the form on the home page to upload a CSV file.

4. **View Results**: After processing, you will be redirected to a page where you can view and download the generated SVG and PNG files.

### CSV File Format

The CSV file should be formatted as follows:
```
path_id,point_id,x,y
1,1,0,0
1,2,1,1
...
```
- `path_id` identifies different curves.
- `point_id` represents the order of points in the curve.
- `x` and `y` are the coordinates of the points.

## Code Explanation

### Python Functions

- **`read_csv(csv_path)`**: Reads the CSV file and parses the curve data into a list of paths.
- **`identify_shapes(XY)`**: Identifies the shape of the curve (line, circle, ellipse, rectangle) and fits it.
- **Shape Functions** (`is_line`, `fit_line`, `is_circle`, `fit_circle`, etc.): Functions to detect and fit different shapes.
- **`generate_circle(center, radius, num_points)`**: Generates points for a circle based on its center and radius.
- **`polylines2svg(paths_XYs, svg_path)`**: Converts the shapes into SVG format and also converts it to a PNG image.

### Flask Web Application

- **Routes**:
  - `/` - Displays the home page with the file upload form.
  - `/upload` - Handles file upload, generates SVG, and displays the result.
  - `/download/<filename>` - Allows users to download the generated image files.
  - `/output/<filename>` - Displays the generated SVG image.

## Additional Notes

- Make sure to handle large files appropriately, as large CSV files may take longer to process.
- Customize the styles and templates located in the `static/css` and `templates` directories to fit your needs.

## Troubleshooting

- **File Not Displaying**: Verify file paths and filenames are correct. Check the server logs for errors.
- **Dependency Issues**: Ensure all required dependencies are installed with the correct versions. Consult package documentation if needed.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

```

Feel free to modify the content or add any additional information based on your specific needs and preferences.
