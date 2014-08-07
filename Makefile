tests:
	python tests.py

clean:
	@-rm -rf CLMsgr/*pyc \
			CLMsgr/__pycache__ \
			CLMsgr/chs/__pycache__ \
			CLMsgr/chs/*pyc \
			CLMsgr/core/__pycache__ \
			CLMsgr/core/*pyc \
			.accounts.db
	@echo 'Cleaned....'
