update:
	@python utils/update.py

clean:
	@- rm -rf *pyc
	@echo 'Clean...'


.PHONY: update clean
