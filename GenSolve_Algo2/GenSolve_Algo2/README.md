# Curvetopia

Welcome to **Curvetopia** – a project dedicated to identifying, regularizing, and beautifying 2D curves. This advanced tool uses sophisticated algorithms to process and enhance various types of curves, making it ideal for projects involving line art and shape analysis.

## Table of Contents

1. [Introduction](#introduction)
2. [Features](#features)
3. [Directory Structure](#directory-structure)
4. [Installation](#installation)
5. [Usage](#usage)
6. [Detailed Workflow](#detailed-workflow)
7. [Dependencies](#dependencies)

## Introduction

**Curvetopia** is designed to transform and enhance 2D curves, starting from simple shapes and evolving to more complex forms. The primary tasks include:

- **Curve Regularization**: Transform irregular curves into standard forms like straight lines, circles, ellipses, and polygons.
- **Symmetry Detection**: Identify and process symmetrical shapes, including reflection symmetries.
- **Curve Completion**: Automatically fill in gaps and complete incomplete curves based on surrounding shapes.
- **SVG and CSV Output**: Provide both visual and data outputs for further analysis and use.

## Features

- **Curve Regularization**:
  - Straight Lines
  - Circles and Ellipses
  - Rectangles and Rounded Rectangles
  - Regular Polygons
  - Star Shapes

- **Symmetry Detection**:
  - Reflection Symmetries
  - Symmetric Bezier Curve Fitting

- **Curve Completion**:
  - Handle various levels of occlusion:
    - Fully Contained Shapes
    - Partially Contained Shapes
    - Disconnected Shapes

- **Output Formats**:
  - SVG for visual representation
  - CSV for data storage and manipulation

## Directory Structure

Here’s a detailed view of the project’s directory structure:
GenSolve_Algo2/

│

├── app.py # Main Flask application file that handles routing and logic

├── requirements.txt # List of Python dependencies required for the project

│

├── static/

│ ├── styles.css # CSS file for styling the web application

│

├── templates/

│ ├── index.html # HTML template for the home page

│

├── data/

│ ├── sample.csv # Sample CSV file for testing (optional)

│

└── README.md # This file

## Installation

1. **Clone the Repository**:
    ```bash
    git clone https://github.com/yourusername/curvetopia.git
    cd curvetopia
    ```

2. **Install the Required Python Packages**:
    ```bash
    pip install -r requirements.txt
    ```

   This will install Flask and other necessary packages.

3. **Install Cairo Dependencies**:
   - **Windows**:
     Download the Cairo graphics library from the [Cairo website](https://cairographics.org/download/). Follow the installation instructions and add the `bin` directory to your system’s `PATH` environment variable.
     
   - **Linux**:
     Install Cairo using your package manager, for example:
     ```bash
     sudo apt-get install libcairo2
     ```
   
   - **macOS**:
     Install Cairo using Homebrew:
     ```bash
     brew install cairo
     ```

## Usage

1. **Run the Flask Application**:
    ```bash
    python app.py
    ```

2. **Access the Web Application**:
   - Open a web browser and navigate to `http://127.0.0.1:5000/`.

3. **Upload a CSV File**:
   - The CSV file should contain paths defined as sequences of points. Ensure that the file is in the correct format as expected by the application.
   - After uploading, the application will process the file and generate visual and data outputs.

4. **View and Download Results**:
   - The processed results will be displayed on the web page.
   - You can download the generated SVG and CSV files using the provided links.

## Detailed Workflow

1. **File Upload**:
   - Users upload a CSV file containing polyline paths.

2. **Processing**:
   - The application reads the CSV and processes the paths to identify and regularize shapes.
   - Symmetry detection algorithms analyze the shapes for reflective symmetries.
   - Incomplete curves are completed based on neighboring shapes.

3. **Output Generation**:
   - The processed shapes are rendered into an SVG file for visualization.
   - Data about the shapes and their transformations are saved in a CSV file.

4. **Results**:
   - Users can view the SVG file directly in the browser.
   - Download links for the SVG and CSV files are provided for further use.

## Dependencies

The following Python packages are required:

- **Flask**: Web framework for building the web application.
- **svgwrite**: Library for creating SVG files.
- **cairosvg**: Library for converting SVG to PNG (optional).
- **numpy**: Numerical operations.
- **shapely**: Geometry operations for shape validation.

Ensure all dependencies are installed as described in the [Installation](#installation) section.

