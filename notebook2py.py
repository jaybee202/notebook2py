import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QLabel, QPushButton, QFileDialog, QLineEdit, QTextEdit, QMessageBox, QHBoxLayout, QSpacerItem, QSizePolicy
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt
import nbformat
import os

class JupyterToPyConverterApp(QMainWindow):
   def __init__(self):
       super().__init__()
       self.init_ui()

   def init_ui(self):
       self.setWindowTitle("Jupyter to PY Converter")
       self.setGeometry(100, 100, 800, 450)

       main_widget = QWidget(self)
       main_h_layout = QHBoxLayout(main_widget)
       self.setCentralWidget(main_widget)

       left_spacer = QSpacerItem(150, 0, QSizePolicy.Fixed, QSizePolicy.Expanding)
       main_h_layout.addSpacerItem(left_spacer)

       center_layout = self.create_center_layout()
       main_h_layout.addLayout(center_layout)

       right_spacer = QSpacerItem(150, 0, QSizePolicy.Fixed, QSizePolicy.Expanding)
       main_h_layout.addSpacerItem(right_spacer)

       self.show()

   def create_center_layout(self):
       center_layout = QVBoxLayout()

       title_label = QLabel("Jupyter to PY Converter")
       title_label.setAlignment(Qt.AlignCenter)
       title_label.setFont(QFont("Helvetica", 30))
       center_layout.addWidget(title_label)

       # Add a spacer
       center_layout.addSpacerItem(QSpacerItem(0, 35, QSizePolicy.Minimum, QSizePolicy.Fixed))

       jupyter_notebook_label = QLabel("Select your Jupyter Notebook")
       center_layout.addWidget(jupyter_notebook_label)


       self.jupyter_notebook_path = QLineEdit()
       center_layout.addWidget(self.jupyter_notebook_path)

       browse_jupyter_button = QPushButton("Browse for Jupyter Notebook")
       browse_jupyter_button.clicked.connect(self.browse_jupyter_notebook)
       center_layout.addWidget(browse_jupyter_button)

       # Add a spacer
       center_layout.addSpacerItem(QSpacerItem(0, 35, QSizePolicy.Minimum, QSizePolicy.Fixed))

       dest_label = QLabel("Select Destination for your .py")
       center_layout.addWidget(dest_label)

       self.dest_path = QLineEdit()
       center_layout.addWidget(self.dest_path)

       browse_dest_button = QPushButton("Browse for .py Destination")
       browse_dest_button.clicked.connect(self.browse_dest_dir)
       center_layout.addWidget(browse_dest_button)

       # Add a spacer
       center_layout.addSpacerItem(QSpacerItem(0, 35, QSizePolicy.Minimum, QSizePolicy.Fixed))

       convert_button = QPushButton("Convert File")
       convert_button.clicked.connect(self.convert_file)
       center_layout.addWidget(convert_button)

       # Add a spacer at the bottom
       center_layout.addSpacerItem(QSpacerItem(0, 0, QSizePolicy.Minimum, QSizePolicy.Expanding))

       return center_layout


   def browse_jupyter_notebook(self):
       options = QFileDialog.Options()
       options |= QFileDialog.ReadOnly
       jupyter_path, _ = QFileDialog.getOpenFileName(self, "Select Jupyter Notebook", "", "Jupyter Notebook (*.ipynb);;All Files (*)", options=options)
       if jupyter_path:
           self.jupyter_notebook_path.setText(jupyter_path)

           # Set the destination path to the same folder as the selected Jupyter Notebook
           notebook_folder = os.path.dirname(jupyter_path)
           notebook_filename = os.path.splitext(os.path.basename(jupyter_path))[0]
           default_output_path = os.path.join(notebook_folder, f"{notebook_filename}.py")
           self.dest_path.setText(default_output_path)


   def browse_dest_dir(self):
       options = QFileDialog.Options()
       options |= QFileDialog.ShowDirsOnly
       dest_dir = QFileDialog.getExistingDirectory(self, "Select Destination Directory", options=options)
       if dest_dir:
           notebook_name = os.path.splitext(os.path.basename(self.jupyter_notebook_path.text()))[0]
           full_dest_path = os.path.join(dest_dir, f"{notebook_name}.py")
           self.dest_path.setText(full_dest_path)


   def convert_file(self):
       jupyter_path = self.jupyter_notebook_path.text()
       output_file = self.dest_path.text()  # Use the full path specified in dest_path

       # Check if the output file already exists
       if os.path.exists(output_file):
           response = QMessageBox.question(self, "File Exists", f"The file {output_file} already exists. Do you want to overwrite?", QMessageBox.Yes | QMessageBox.No)
           if response == QMessageBox.No:
               return

       try:
           with open(jupyter_path, "r", encoding="utf-8") as nb_file:
               notebook = nbformat.read(nb_file, as_version=4)

           with open(output_file, "w", encoding="utf-8") as py_file:
               for cell in notebook.cells:
                   if cell.cell_type == "code":
                       py_file.write(cell.source)
                       py_file.write("\n")
       except Exception as e:
           QMessageBox.critical(self, "Error", f"Error converting file: {e}")
           return

       QMessageBox.information(self, "Conversion Complete", "Jupyter Notebook converted to .py successfully!")



if __name__ == "__main__":
   app = QApplication(sys.argv)
   window = JupyterToPyConverterApp()
   sys.exit(app.exec_())