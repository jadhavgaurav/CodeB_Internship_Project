import nbformat
from nbconvert import PythonExporter

# Load notebook
with open("Internship_CodeB_week 5 & 6 copy.ipynb", "r", encoding="utf-8") as f:
    nb = nbformat.read(f, as_version=4)

# Remove all markdown cells
nb.cells = [cell for cell in nb.cells if cell.cell_type == 'code']

# Export to Python script (without cell numbers)
python_exporter = PythonExporter()
python_exporter.exclude_input_prompt = True  # remove 'In [x]:'
python_exporter.exclude_output_prompt = True

# Convert notebook to script
script, _ = python_exporter.from_notebook_node(nb)

# Save the clean script
with open("final_project.py", "w", encoding="utf-8") as f:
    f.write(script)

print("✅ Notebook successfully converted to code-only script: output_script.py")
