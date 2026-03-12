BINDIR ?= $(HOME)/.local/bin

.PHONY: install uninstall

install: .venv/bin/python3 pdf-add-filename
	chmod +x pdf-add-filename
	mkdir -p "$(BINDIR)"
	ln -sf "$(CURDIR)/pdf-add-filename" "$(BINDIR)/pdf-add-filename"
	@echo "Installed: $(BINDIR)/pdf-add-filename"
	@echo "Verify PATH contains $(BINDIR) or add to ~/.bashrc:"
	@echo "  export PATH=\"$(BINDIR):\$$PATH\""

.venv/bin/python3:
	python3 -m venv .venv
	.venv/bin/pip install --require-hashes -r requirements.txt

uninstall:
	rm -f "$(BINDIR)/pdf-add-filename"
	@echo "Removed: $(BINDIR)/pdf-add-filename"
	@echo "To fully remove the program, delete this directory."
