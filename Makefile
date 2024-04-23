PYTHON := python3
MAIN_FILE := main.py
WORD_LIST := wordlist.txt
VALID_WORDS_LIST := valid-wordle-words.txt
ASSET_DIR := assets

all: run

run:
	$(PYTHON) $(MAIN_FILE)