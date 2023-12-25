PREFIX ?= /usr/local
ROOT ?= ~/
LIBDIR ?= $(PREFIX)/lib
SYSTEM_EXTENSION_DIR ?= $(LIBDIR)/safeman/
SRC ?= $(SYSTEM_EXTENSION_DIR)/src

install:
	@install -v -d "$(SYSTEM_EXTENSION_DIR)/"
	@install -v -d "$(SRC)/"
	@install -v -m0755 src/addpsw_window.py "$(SRC)/addpsw_window.py"
	@install -v -m0755 src/app_window.py "$(SRC)/app_window.py"
	@install -v -m0755 src/keygen_window.py "$(SRC)/keygen_window.py"
	@install -v -m0755 src/unlpsw_window.py "$(SRC)/unlpsw_window.py"
	@install -v -m0755 SafeMan.bash "$(SYSTEM_EXTENSION_DIR)/SafeMan.bash"
	@echo
	@echo "SafeMan is installed successfully!"
	@echo

uninstall:
	@rm -vrf \
		"$(LIBDIR)/safeman" \
	
	@rm -vrf \
		"$(SYSTEM_EXTENSION_DIR)/SafeMan.bash" \
	
	@rm -vrf \
		"$(SRC)/" \
	@echo "SafeMan is uninstalled successfully!"

.PHONY: install uninstall