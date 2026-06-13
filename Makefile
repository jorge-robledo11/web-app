.PHONY: help backend context \
        db-up db-down db-reset db-migrate db-create \
        db-logs db-status db-shell \
        test lint format typecheck check clean visual-check hooks-install

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
	bash scripts/dev/backend.sh

# ╔══════════════════════════════════════════╗
# ║            BASE DE DATOS                 ║
# ╚══════════════════════════════════════════╝

db-up: ## Levanta PostgreSQL con Docker Compose
	bash scripts/dev/up.sh

db-down: ## Detiene PostgreSQL
	bash scripts/dev/down.sh

db-reset: ## Reinicia PostgreSQL BORRANDO datos (pide confirmación)
	bash scripts/dev/reset.sh

db-migrate: ## Aplica migraciones pendientes de Alembic
	bash scripts/dev/migrate.sh

db-create: ## Crea nueva migración (requiere name="descripción")
	bash scripts/dev/create.sh "$(name)"

db-logs: ## Muestra logs de PostgreSQL
	docker compose logs db --tail=50

# ╔══════════════════════════════════════════╗
# ║          	  CI Y TESTS                 ║
# ╚══════════════════════════════════════════╝

test: ## Ejecuta la suite de tests
	bash scripts/ci/test.sh

lint: ## Verifica linting y formato sin modificar archivos
	bash scripts/ci/lint.sh

format: ## Formatea código con ruff
	bash scripts/ci/format.sh

typecheck: ## Verifica tipos con mypy --strict
	bash scripts/ci/typecheck.sh

check: ## Ejecuta lint + typecheck + test (verificación completa)
	bash scripts/ci/check.sh

clean: ## Elimina __pycache__, .pytest_cache, .ruff_cache, .mypy_cache, *.pyc
	bash scripts/ci/clean.sh

# ╔══════════════════════════════════════════╗
# ║               TOOLING                    ║
# ╚══════════════════════════════════════════╝

context: ## Genera el estado del repositorio en docs/context/repo-state.xml
	bash scripts/tools/context.sh

hooks-install: ## Instala hooks Git del proyecto (post-commit changelog)
	bash scripts/tools/install-git-hooks.sh

visual-check: ## Audit trail visual contrast feature‑activa
	bash scripts/tools/check-visual-trace.sh
