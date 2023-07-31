PDFLATEXOPTS = -file-line-error -interaction=nonstopmode -halt-on-error -synctex=1

all: slides.pdf handout.pdf

.venv/bin/python:
	python3 -m venv .venv
	./.venv/bin/python -m pip install -r requirements.txt

slides.pdf: slides.tex .venv/bin/python $(wildcard images/*.py images/*.tex images/*.pdf images/*.tikz images/*.png) arlwide_theme/theme.tex
	$(MAKE) -C images all
	pdflatex $(PDFLATEXOPTS) slides
	pdflatex $(PDFLATEXOPTS) slides

handout.pdf: slides.pdf
	pdfjam slides.pdf 1,2,3,6,8,10,12,13,14,15,19,20,21,27,30,36,40,43,47,51,55,56,58,59,60,61,62,63,66,67,68,74,76,79,80,82,85,88,95,96,98,103,104,105,106,108,109,110,114,117,120,121,122 --fitpaper true -o handout.pdf


pdflatex:
	@echo "Compiling Main File ..."
	pdflatex $(PDFLATEXOPTS) slides
	@echo "Done"

update:
	pdflatex $(PDFLATEXOPTS) slides

clean:
	@echo "Cleaning up files from LaTeX compilation ..."
	$(MAKE) -C images clean
	rm -f *.aux
	rm -f *.log
	rm -f *.toc
	rm -f *.bbl
	rm -f *.blg
	rm -rf *.out
	rm -f *.bak
	rm -f *.ilg
	rm -f *.snm
	rm -f *.nav
	rm -f *.fls
	rm -f *.table
	rm -f *.gnuplot
	rm -f *.fdb_latexmk
	rm -f *.synctex.gz
	@echo "Done"

distclean: clean
	$(MAKE) -C images distclean
	rm -rf .venv
	rm -rf png
	rm -f slides.pdf
	rm -f handout.pdf

.PHONY: all pdflatex pdf png clean distclean
