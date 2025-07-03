import os
# Produce a panchaanga
from jyotisha.panchaanga.spatio_temporal import City, annual, periodical
from jyotisha.panchaanga.temporal import ComputationSystem
TEST_DATA_PATH = os.path.join(os.path.dirname(__file__), 'computation_systems')
computation_system = ComputationSystem.read_from_file(
     filename=os.path.join(TEST_DATA_PATH, "vishvAsa_bhAskara.toml"))
from jyotisha.panchaanga.temporal.time import Date
city = City('Frisco', "33:09:19", "-96:49:7", "America/Chicago")
panchaanga = annual.get_panchaanga_for_civil_year(city=city, year=2025, computation_system=computation_system, allow_precomputed=False)



## Tex
from jyotisha.panchaanga.writer.tex.daily_tex_writer import emit
from indic_transliteration import sanscript
emit(panchaanga,
     output_stream=open("Tex_outputs/Panchanga.tex", 'w',encoding="utf-8"), languages=["sa"], scripts=[sanscript.DEVANAGARI])

# This produces a pdf file using the LaTeX file created above

from tex2pdf import compile_tex_with_xelatex
compile_tex_with_xelatex('Panchanga.tex')


# ## Markdown
# from jyotisha.panchaanga.writer import md
# from doc_curation.md.file import MdFile
# md_file = MdFile(file_path="/some/path.md")
# md_file.dump_to_file(metadata={"title": str(2019)}, content=md.make_md(panchaanga=panchaanga), dry_run=False)

# ## ICS
# from jyotisha.panchaanga.writer import ics
# ics_calendar = ics.compute_calendar(panchaanga)
# ics.write_to_file(ics_calendar, "/some/path.ics")
