# BASH TASK 1: MAKE VIDEO TRANSCRIPTS READABLE

grep -vE '^[0-9]+$|-->' MYFILE.en.srt | sed 's/\[.*\]//g' | sed 's/[[:space:]]\+/ /g; s/^[[:space:]]\+//; s/[[:space:]]\+$//' | grep -v '^[[:space:]]*$' | awk '!visited[$0]++' | awk '/^>>/ { if (s) print s "\n"; s = $0; next } { s = s " " $0 } END { print s }' | sed -e 's/^>> /- /' | PROJECT_ROOT/python/non_punctuated_text_to_paragraphized.py

# BASH TASK 2: PYTHON VENV MANAGEMENT

# venv creation
python3 -m venv python/rmavenv

# venv activation
source python/rmavenv/bin/activate

# venv setup
python3 -m pip install --upgrade pip

# dependency download (as is)
pip3 install deepmultilingualpunctuation spacy
python3 -m spacy download en_core_web_sm

# dependency list generation
pip3 freeze > python/requirements.txt

# dependency download (from dependency list)
pip3 install -r python/requirements.txt

# BASH TASK 3: WRITING EXERCISE IN TEX

# Edit
nano rma.tex
nano Biblography.bib
# View code
cat rma.tex
# Render
pdflatex rma.tex
biber rma
pdflatex rma.tex
pdflatex rma.tex
# Cleanup
rm *.aux *.bbl *.bcf *.blg *.log *.run.xml *.toc
# View
evince rma.pdf # or qpdfviewer or whatever pdf viewer is available
