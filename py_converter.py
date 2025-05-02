import nbformat
from nbconvert import PythonExporter

file_to_convert = input("Enter the path to the Jupyter notebook file : ")

# Load notebook
with open(file_to_convert, "r", encoding="utf-8") as f:
    nb = nbformat.read(f, as_version=4)

# Remove all markdown cells
nb.cells = [cell for cell in nb.cells if cell.cell_type == 'code']

# Export to Python script (without cell numbers)
python_exporter = PythonExporter()
python_exporter.exclude_input_prompt = True  # remove 'In [x]:'
python_exporter.exclude_output_prompt = True

# Convert notebook to script
script, _ = python_exporter.from_notebook_node(nb)

converted_script_name = file_to_convert.replace(".ipynb", ".py")

# Save the clean script
with open(converted_script_name, "w", encoding="utf-8") as f:
    f.write(script)

print(f"✅ Notebook successfully converted to code-only script: {converted_script_name}")
