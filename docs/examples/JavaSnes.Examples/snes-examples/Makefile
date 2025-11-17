PROJECT_DIRS := $(wildcard out/*/)

all: $(PROJECT_DIRS)

$(PROJECT_DIRS):
	@echo "Processing project: $@"
	$(eval JAR_NAME := $(notdir $(patsubst %/,%,$@)))
	$(eval JAR_PATH := $@$(JAR_NAME).jar)
	@if [ -f "$(JAR_PATH)" ]; then \
		echo "Running JAR: $(JAR_PATH)"; \
		java -jar "$(JAR_PATH)"; \
		if [ -d "$@output" ]; then \
			echo "Entering $@output and running make..."; \
			cd "$@output" && $(MAKE); \
			echo "Build complete for $(JAR_NAME)"; \
		else \
			echo "WARNING: Subdirectory 'output' not found in $@"; \
		fi \
	else \
		echo "ERROR: JAR file not found: $(JAR_PATH)"; \
	fi

clean:
	@for dir in $(PROJECT_DIRS); do \
		if [ -d "$$dir/output" ]; then \
			echo "Cleaning $$dir/output"; \
			cd "$$dir/output" && $(MAKE) clean 2>/dev/null || true; \
			find "$$dir/output" -name "*.sfc" -delete; \
		fi \
	done
	@echo "Full cleanup"

distclean: clean
	@for dir in $(PROJECT_DIRS); do \
		echo "Removing build of $$dir"; \
		rm -rf "$$dir/output"; \
	done
	@echo "Full cleanup of all builds"

help:
	@echo "Available targets:"
	@echo "  all       - Build all projects (default)"
	@echo "  clean     - Remove generated .sfc files"
	@echo "  distclean - Remove all builds completely"
	@echo "  help      - Show this help"

.PHONY: all clean distclean help $(PROJECT_DIRS)

