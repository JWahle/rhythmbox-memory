PLUGIN_DIR = $(HOME)/.local/share/rhythmbox/plugins/memory

all:
	@echo "make install   - (re-)installs the plugin into your home folder."
	@echo "make uninstall - removes the plugin from your home folder."
	@echo "make debug     - runs rhythmbox with plugin-specific debugging output."
	@echo "make update    - updates the plugin to the most recent version."

install:
	mkdir -p $(PLUGIN_DIR)
	cp memory.plugin $(PLUGIN_DIR)/
	cp memory.py $(PLUGIN_DIR)/
	@echo "Plugin installed to $(PLUGIN_DIR)"

uninstall:
	rm -rf $(PLUGIN_DIR)
	@echo "Plugin uninstalled from $(PLUGIN_DIR)"

update:
	git pull
	@echo "Updated sources"
	@$(MAKE) install

debug:
	rhythmbox -d 2>&1 | grep memory.py

.PHONY: all install uninstall update debug
