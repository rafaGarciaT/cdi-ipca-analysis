.PHONY: help install clean test run lint

help:
	@echo "Comandos disponíveis:"
	@echo "  make install    - Instala dependências"
	@echo "  make clean      - Limpa dados e cache"
	@echo "  make test       - Executa testes"
	@echo "  make run        - Executa pipeline"

install:
	pip install -r requirements.txt

clean:
ifeq ($(OS),Windows_NT)
	scripts\run_pipeline.bat --clear-data
else
	bash scripts/run_pipeline.sh --clear-data
endif

run:
ifeq ($(OS),Windows_NT)
	scripts\run_pipeline.bat $(ARGS)
else
	bash scripts/run_pipeline.sh $(ARGS)
endif

test:
	pytest tests/ -v