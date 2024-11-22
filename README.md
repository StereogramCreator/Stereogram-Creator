# Stereogram Creator

This is a Python-based GUI application to create and visualize stereograms using depth maps and texture images. The project was developed as part of a the Matura project by Nuno Furrer in 2024.

## Features
- Import texture and depth images.
- Configure DPI and adjust stereogram settings.
- Toggle hidden surface removal.
- Create stereograms using different algorithms:
  - Left-Right constraint.
  - Right-Left constraint.
  - Center-Side constraint.
- Preview texture and depth maps before processing.
- Export the generated stereogram as an image file.
- Interactive visualization features such as sliders and toggles.

## Requirements
The application requires Python and the following libraries:
- `numpy`
- `Pillow`
- `tkinter` (comes pre-installed with Python)

## Setup Instructions
1. Clone the repository or download the project files.
2. Ensure Python (>=3.7) is installed on your system.
3. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
