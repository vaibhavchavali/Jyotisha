import subprocess
import os

def compile_tex_with_xelatex(tex_file):
    """
    Compile an existing .tex file to PDF using xelatex,
    running the command inside the 'Tex_Docs' folder.
    """
    tex_dir = "Tex_outputs"

    # Ensure the path is correct
    full_path = os.path.join(tex_dir, tex_file)

    # Run xelatex inside Tex_Docs
    subprocess.run(
        ['xelatex', tex_file],
        cwd=tex_dir  # <-- sets the working directory for the command
    )
