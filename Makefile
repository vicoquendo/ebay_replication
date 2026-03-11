.PHONY: all clean
all: paper/paper.pdf

# Preprocessing: data wrangling and figures
output/figures/figure_5_2.png output/figures/figure_5_3.png: input/PaidSearch.csv code/preprocess.py
	python3 code/preprocess.py

# DID estimation
output/tables/did_table.tex: input/PaidSearch.csv code/did_analysis.py
	python3 code/did_analysis.py

# Paper compilation
paper/paper.pdf: paper/paper.tex output/figures/figure_5_2.png output/figures/figure_5_3.png output/tables/did_table.tex
	cd paper && pdflatex paper.tex && pdflatex paper.tex

clean:
	rm -f output/figures/*.png output/tables/*.tex paper/paper.pdf paper/paper.aux paper/paper.log

# 1. If you edit code/preprocess.py, which targets will Make rebuild? Which targets will it skip?
#       * It will only rebuild the figure_5_3.png, and paper.pdf
# 	* It will skip did_table.tex and clean targets


# 2. If you edit code/did_analysis.py, which targets will Make rebuild? Which targets will it skip?
#  	* It will only rebuild did_table.tex and paper.pdf
#	* It will skip figure_5_3.png and clean

# 3. If you edit paper/paper.tex, which targets will Make rebuild? Which targets will it skip?
#	* It will rebuild preprocessing, did analysis, and paper compilation
#	* It will skip clean

###REFLECTIONS FROM VIC
# Makefile captures dependencies in an explicit way, through targets.
# Makefile helps collaborators understand the order of processing steps required.
# Makefile helps people understand what a "clean" reproduction requires.
# Makefile makes happiness explicit.
