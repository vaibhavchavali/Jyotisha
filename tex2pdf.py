import subprocess
import os


def compile_tex_with_xelatex(tex_file, tex_dir="Tex_outputs"):
    """
    Compile an existing .tex file to PDF using xelatex,
    running the command inside the specified output directory.
    """
    full_path = os.path.join(tex_dir, tex_file)
    if not os.path.exists(full_path):
        print(f"  [WARN] .tex file not found: {full_path}, skipping PDF compilation.")
        return False

    print(f"  Compiling {full_path} with xelatex...")
    result = subprocess.run(
        ['xelatex', '-interaction=nonstopmode', tex_file],
        cwd=tex_dir,
        capture_output=True, text=True
    )
    if result.returncode != 0:
        print(f"  [ERROR] xelatex failed for {tex_file}. Check logs in {tex_dir}.")
        return False
    print(f"  -> PDF generated successfully.")
    return True
