# ================================
# Color definitions (ANSI)
# ================================
GREEN  = \033[0;32m
BLUE   = \033[0;34m
YELLOW = \033[1;33m
RED    = \033[0;31m
CYAN   = \033[0;36m
RESET  = \033[0m

# ================================
# Virtual environment name
# ================================
VENV = venv

# ================================
# Python & pip paths inside venv
# ================================
PY  = $(VENV)/bin/python
PIP = $(VENV)/bin/pip

# ================================
# Phony targets (not real files)
# ================================
.PHONY: info install run debug clean lint lint-strict venv

# ================================
# Global Variables
# ================================

CONFIG ?= default_config.txt

# ================================
# Show available commands
# ================================
info:
	@echo "$(CYAN)Available Makefile Commands:$(RESET)"
	@echo ""
	@echo "$(YELLOW)install$(RESET)      -> Create venv & Install dependencies"
	@echo "$(YELLOW)run$(RESET)          -> Execute the main script"
	@echo "$(YELLOW)debug$(RESET)        -> Run the main script in debug mode (pdb)"
	@echo "$(YELLOW)clean$(RESET)        -> Remove temporary files and caches"
	@echo "$(YELLOW)lint$(RESET)         -> Run flake8 and mypy with strict flags"
	@echo "$(YELLOW)lint-strict$(RESET)  -> Run flake8 and mypy in full strict mode"

# ================================
# Create virtual environment
# ================================
venv:
	@echo "$(BLUE)Checking virtual environment...$(RESET)"
	@if [ ! -d $(VENV) ]; then \
		python3 -m venv $(VENV); \
		echo "$(GREEN)Virtual environment created.$(RESET)"; \
	fi

# ================================
# Install dependencies into venv
# ================================
install: venv
	@echo "$(BLUE)Installing dependencies from requirements.txt...$(RESET)"
	@if ! $(PIP) install -r requirements.txt >/dev/null 2>&1; then \
		echo "$(RED)pip install failed. See logs by running manually:$(RESET)"; \
		echo "$(YELLOW)  $(PIP) install -r requirements.txt$(RESET)"; \
		exit 1; \
	fi
	@echo "$(GREEN)Dependencies installed.$(RESET)"

# ================================
# Run the main script
# ================================
run: install
	@echo "$(BLUE)Running the project...$(RESET)"
	@$(PY) main.py --config_file $(CONFIG)
	@echo "$(GREEN)Execution finished.$(RESET)"

# ================================
# Run the main script in debug mode
# ================================
debug: install
	@echo "$(BLUE)Running the project in debug mode (pdb)...$(RESET)"
	@$(PY) -m pdb main.py
	@echo "$(GREEN)Debug session finished.$(RESET)"

# ================================
# Remove caches and virtual env
# ================================
clean:
	@echo "$(RED)Cleaning cache files and virtual environment...$(RESET)"
	@rm -rf __pycache__ .mypy_cache .pytest_cache $(VENV)
	@echo "$(GREEN)Clean complete.$(RESET)"

# ================================
# Run flake8 + mypy with custom rules
# ================================
lint: install
	@echo "$(BLUE)Running flake8...$(RESET)"
	@$(VENV)/bin/flake8 .
	@echo "$(BLUE)Running mypy with custom rules...$(RESET)"
	@$(VENV)/bin/mypy . --warn-return-any --warn-unused-ignores --ignore-missing-imports --disallow-untyped-defs --check-untyped-defs
	@echo "$(GREEN)Lint completed successfully.$(RESET)"

# ================================
# Run flake8 + mypy in full strict mode
# ================================
lint-strict: install
	@echo "$(BLUE)Running flake8...$(RESET)"
	@$(VENV)/bin/flake8 .
	@echo "$(BLUE)Running mypy in FULL strict mode...$(RESET)"
	@$(VENV)/bin/mypy . --strict
	@echo "$(GREEN)Strict lint completed successfully.$(RESET)"
