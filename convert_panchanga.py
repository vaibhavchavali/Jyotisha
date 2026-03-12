"""
Convert Devanagari Panchanga .tex files to English (IAST) and Telugu versions.
Performs script transliteration without changing any content or context.

Can be used as a library (import convert_panchanga) or run standalone.
"""

import os
import re
import shutil
from indic_transliteration import sanscript

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
TEMPLATE_FONTS_DIR = os.path.join(BASE_DIR, 'jyotisha', 'panchaanga', 'writer', 'tex', 'templates', 'fonts')
TEMPLATE_DIR = os.path.join(BASE_DIR, 'jyotisha', 'panchaanga', 'writer', 'tex', 'templates')

# Devanagari Unicode range pattern (includes digits, marks, signs)
DEVANAGARI_PATTERN = re.compile(r'[\u0900-\u097F\u200B-\u200D]+')


def transliterate_devanagari(text, target_script):
    """Replace all Devanagari character runs with transliterated equivalents."""
    def replace_match(m):
        return sanscript.transliterate(m.group(0), sanscript.DEVANAGARI, target_script)
    return DEVANAGARI_PATTERN.sub(replace_match, text)


def fix_preamble_english(content):
    """Fix font and digit settings for English/IAST output."""
    content = content.replace(
        r'\setmainfont{siddhanta.ttf}[Path=templates/fonts/,Script=Devanagari]',
        r'\setmainfont{NotoSansUI-Regular.ttf}[Path=templates/fonts/]'
    )
    # Replace Devanagari digit macro with pass-through (use Arabic numerals)
    content = content.replace(
        r'\newcommand{\devanumber}[1]{%' + '\n' + r'\num=#1\devanumberrecurse}',
        r'\newcommand{\devanumber}[1]{#1}'
    )
    # Also handle \r\n line endings
    content = content.replace(
        r'\newcommand{\devanumber}[1]{%' + '\r\n' + r'\num=#1\devanumberrecurse}',
        r'\newcommand{\devanumber}[1]{#1}'
    )
    return content


def fix_preamble_telugu(content):
    """Fix font and digit settings for Telugu output."""
    content = content.replace(
        r'\setmainfont{siddhanta.ttf}[Path=templates/fonts/,Script=Devanagari]',
        r'\setmainfont{Nirmala UI}[Script=Telugu]'
    )
    return content


def setup_output_dir(output_dir):
    """Create output directory and copy supporting files."""
    os.makedirs(output_dir, exist_ok=True)
    
    # Create templates/fonts directory
    fonts_dest = os.path.join(output_dir, 'templates', 'fonts')
    os.makedirs(fonts_dest, exist_ok=True)
    
    # Copy font files
    for font_file in os.listdir(TEMPLATE_FONTS_DIR):
        src = os.path.join(TEMPLATE_FONTS_DIR, font_file)
        dst = os.path.join(fonts_dest, font_file)
        if not os.path.exists(dst):
            shutil.copy2(src, dst)
    
    # Copy supporting TeX files
    for support_file in ['listofitems.sty', 'listofitems.tex']:
        src = os.path.join(TEMPLATE_DIR, support_file)
        if os.path.exists(src):
            dst = os.path.join(output_dir, support_file)
            if not os.path.exists(dst):
                shutil.copy2(src, dst)


def convert_panchanga(source_tex, target_script, output_dir, output_filename, preamble_fixer):
    """Convert a Devanagari Panchanga .tex to the target script.
    
    Args:
        source_tex: Path to the source .tex file (Devanagari)
        target_script: Target script constant from sanscript (e.g. sanscript.IAST)
        output_dir: Directory to write the output file
        output_filename: Name of the output .tex file
        preamble_fixer: Function to fix preamble for the target script
    
    Returns:
        Path to the output .tex file
    """
    print(f"  Reading source: {source_tex}")
    with open(source_tex, 'r', encoding='utf-8') as f:
        content = f.read()
    
    print(f"  Transliterating to {target_script}...")
    content = transliterate_devanagari(content, target_script)
    
    print(f"  Fixing preamble...")
    content = preamble_fixer(content)
    
    setup_output_dir(output_dir)
    
    output_path = os.path.join(output_dir, output_filename)
    print(f"  Writing output: {output_path}")
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"  Done! Output saved to: {output_path}")
    return output_path


def convert_to_english(source_tex, output_dir, output_filename):
    """Convenience wrapper to convert a Devanagari .tex to English (IAST)."""
    return convert_panchanga(
        source_tex=source_tex,
        target_script=sanscript.IAST,
        output_dir=output_dir,
        output_filename=output_filename,
        preamble_fixer=fix_preamble_english
    )


def convert_to_telugu(source_tex, output_dir, output_filename):
    """Convenience wrapper to convert a Devanagari .tex to Telugu."""
    return convert_panchanga(
        source_tex=source_tex,
        target_script=sanscript.TELUGU,
        output_dir=output_dir,
        output_filename=output_filename,
        preamble_fixer=fix_preamble_telugu
    )


if __name__ == '__main__':
    # Standalone mode: convert the existing single-year Panchanga.tex
    SOURCE_TEX = os.path.join(BASE_DIR, 'Tex_outputs', 'Panchanga.tex')
    
    # Generate English (IAST) version
    print("=" * 60)
    print("Generating English (IAST) version...")
    print("=" * 60)
    english_dir = os.path.join(BASE_DIR, 'Tex_outputs_english')
    convert_to_english(SOURCE_TEX, english_dir, 'Panchanga_English.tex')
    
    # Generate Telugu version
    print()
    print("=" * 60)
    print("Generating Telugu version...")
    print("=" * 60)
    telugu_dir = os.path.join(BASE_DIR, 'Tex_outputs_telugu')
    convert_to_telugu(SOURCE_TEX, telugu_dir, 'Panchanga_Telugu.tex')
    
    print()
    print("=" * 60)
    print("All conversions complete!")
    print(f"English .tex: {os.path.join(english_dir, 'Panchanga_English.tex')}")
    print(f"Telugu .tex:  {os.path.join(telugu_dir, 'Panchanga_Telugu.tex')}")
    print("=" * 60)
