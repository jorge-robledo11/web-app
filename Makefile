.PHONY: help backend context \
        db-up db-down db-reset db-migrate db-create \
        db-logs db-status db-shell \
        test lint format typecheck check clean

.DEFAULT_GOAL := help

# ╔══════════════════════════════════════════╗
# ║               AYUDA                      ║
# ╚══════════════════════════════════════════╝

help: ## Muestra esta ayuda
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | \
		awk 'BEGIN {FS = ":.*?## "}; {printf "  \033[36m%-22s\033[0m %s\n", $$1, $$2}'

# ╔══════════════════════════════════════════╗
# ║             DESARROLLO                   ║
# ╚══════════════════════════════════════════╝

backend: ## Arranca el backend de la aplicación
	bash scripts/backend.sh

context: ## Configura el entorno de desarrollo en un fichero
	bash scripts/context.sh

# ╔══════════════════════════════════════════╗
# ║            BASE DE DATOS                 ║
# ╚══════════════════════════════════════════╝

db-up: ## Levanta PostgreSQL con Docker Compose
	bash scripts/up.sh

db-down: ## Detiene PostgreSQL
	bash scripts/down.sh

db-reset: ## Reinicia PostgreSQL BORRANDO datos (pide confirmación)
	bash scripts/reset.sh

db-migrate: ## Aplica migraciones pendientes de Alembic
	bash scripts/migrate.sh

db-create: ## Crea nueva migración (requiere name="descripción")
	bash scripts/create.sh "$(name)"

db-logs: ## Muestra logs de PostgreSQL
	docker compose logs db --tail=50

# ╔══════════════════════════════════════════╗
# ║          CALIDAD Y TESTS                 ║
# ╚══════════════════════════════════════════╝

test: ## Ejecuta la suite de tests
	bash scripts/test.sh

lint: ## Verifica linting y formato sin modificar archivos
	bash scripts/lint.sh

format: ## Formatea código con ruff
	bash scripts/format.sh

typecheck: ## Verifica tipos con mypy --strict
	bash scripts/typecheck.sh

check: ## Ejecuta lint + typecheck + test (verificación completa)
	bash scripts/check.sh

clean: ## Elimina __pycache__, .pytest_cache, .ruff_cache, .mypy_cache, *.pyc
	bash scripts/clean.sh