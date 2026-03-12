"""
Generate Panchanga for 2026 and 2027 in Devanagari, English (IAST), and Telugu
for multiple cities. Then compile each to PDF using xelatex.

Usage:
    python generate_2026_2027.py
"""
import os
import sys

# --- Configuration ---
YEARS = [2026, 2027]

# Cities to generate Panchanga for.
# Format: (display_name, latitude, longitude, timezone)
# Use sexagesimal "dd:mm:ss" or decimal for lat/lon.
CITIES = [
    ("Frisco",    "33:09:19.3428", "-96:49:7.4388",  "America/Chicago"),
    ("Hyderabad", "17.3615104",    "78.474743",       "Asia/Calcutta"),
    ("Chennai",   "13:05:24",      "80:16:12",        "Asia/Calcutta"),
]

# --- Imports ---
from jyotisha.panchaanga.spatio_temporal import City, annual
from jyotisha.panchaanga.temporal import ComputationSystem
from jyotisha.panchaanga.writer.tex.daily_tex_writer import emit
from indic_transliteration import sanscript

from convert_panchanga import convert_to_english, convert_to_telugu, setup_output_dir
from tex2pdf import compile_tex_with_xelatex

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
TEST_DATA_PATH = os.path.join(BASE_DIR, 'computation_systems')
computation_system = ComputationSystem.read_from_file(
    filename=os.path.join(TEST_DATA_PATH, "vishvAsa_bhAskara.toml"))


def get_output_dirs(city_name):
    """Return (devanagari_dir, english_dir, telugu_dir) for a given city."""
    deva_dir    = os.path.join(BASE_DIR, 'Tex_outputs',         city_name)
    english_dir = os.path.join(BASE_DIR, 'Tex_outputs_english', city_name)
    telugu_dir  = os.path.join(BASE_DIR, 'Tex_outputs_telugu',  city_name)
    return deva_dir, english_dir, telugu_dir


def generate_for_city_year(city_obj, year, deva_dir):
    """Generate Devanagari .tex for a given city and year. Returns the .tex path."""
    print(f"  Computing Panchaanga for {city_obj.name} {year}...")
    panchaanga = annual.get_panchaanga_for_civil_year(
        city=city_obj, year=year,
        computation_system=computation_system,
        allow_precomputed=False)

    setup_output_dir(deva_dir)
    tex_filename = f'Panchanga_{year}.tex'
    output_path = os.path.join(deva_dir, tex_filename)
    emit(panchaanga,
         output_stream=open(output_path, 'w', encoding="utf-8"),
         languages=["sa"], scripts=[sanscript.DEVANAGARI])
    print(f"  -> Written: {output_path}")
    return output_path, tex_filename


def main():
    total_cities = len(CITIES)
    total_years = len(YEARS)
    print(f"\n{'#'*70}")
    print(f"# Panchanga Pipeline: {total_cities} cities x {total_years} years")
    print(f"# Cities: {', '.join(c[0] for c in CITIES)}")
    print(f"# Years:  {', '.join(str(y) for y in YEARS)}")
    print(f"{'#'*70}\n")

    all_outputs = []

    for city_tuple in CITIES:
        city_name = city_tuple[0]
        city_obj = City(*city_tuple)
        deva_dir, english_dir, telugu_dir = get_output_dirs(city_name)

        for year in YEARS:
            print(f"\n{'='*60}")
            print(f"  [{city_name}] [{year}] Generating Panchanga...")
            print(f"{'='*60}")

            # Step 1: Generate Devanagari .tex
            deva_tex_path, tex_filename = generate_for_city_year(city_obj, year, deva_dir)

            # Step 2: Convert to English (IAST)
            eng_filename = f'Panchanga_{year}_English.tex'
            print(f"\n  [{city_name}] [{year}] Converting to English (IAST)...")
            convert_to_english(deva_tex_path, english_dir, eng_filename)

            # Step 3: Convert to Telugu
            tel_filename = f'Panchanga_{year}_Telugu.tex'
            print(f"\n  [{city_name}] [{year}] Converting to Telugu...")
            convert_to_telugu(deva_tex_path, telugu_dir, tel_filename)

            all_outputs.append({
                'city': city_name,
                'year': year,
                'devanagari': (deva_dir, tex_filename),
                'english':    (english_dir, eng_filename),
                'telugu':     (telugu_dir, tel_filename),
            })

    # Step 4: Compile all .tex to PDF
    print(f"\n\n{'#'*70}")
    print(f"# Compiling all .tex files to PDF with xelatex...")
    print(f"{'#'*70}\n")

    pdf_results = []
    for entry in all_outputs:
        city = entry['city']
        year = entry['year']
        for lang_key in ['devanagari', 'english', 'telugu']:
            tex_dir, tex_file = entry[lang_key]
            print(f"  [{city}] [{year}] [{lang_key.capitalize()}]")
            success = compile_tex_with_xelatex(tex_file, tex_dir)
            pdf_results.append((city, year, lang_key, success))

    # Summary
    print(f"\n\n{'#'*70}")
    print(f"# PIPELINE COMPLETE - Summary")
    print(f"{'#'*70}\n")

    for city, year, lang, success in pdf_results:
        status = "✓ OK" if success else "✗ FAILED"
        print(f"  [{status}] {city} / {year} / {lang.capitalize()}")

    failed = [r for r in pdf_results if not r[3]]
    if failed:
        print(f"\n  WARNING: {len(failed)} PDF(s) failed to compile. Check logs above.")
    else:
        print(f"\n  All {len(pdf_results)} PDFs generated successfully!")


if __name__ == '__main__':
    main()
