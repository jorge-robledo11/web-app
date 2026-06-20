.PHONY: help server context \
        db-up db-down db-reset db-migrate db-create \
        db-logs db-status \
        auto-checks manual-checks ci \
        test coverage clean visual-check hooks-install

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

server: ## Arranca el server de la aplicación
	bash scripts/dev/server.sh

# ╔══════════════════════════════════════════╗
# ║            BASE DE DATOS                 ║
# ╚══════════════════════════════════════════╝

db-up: ## Levanta PostgreSQL con Docker Compose
	bash scripts/dev/up.sh

db-down: ## Detiene PostgreSQL
	bash scripts/dev/down.sh

db-reset: ## Reinicia PostgreSQL BORRANDO datos
	bash scripts/dev/reset.sh

db-migrate: ## Aplica migraciones pendientes de Alembic
	bash scripts/dev/migrate.sh

db-create: ## Crea nueva migración: make db-create name="descripción"
	bash scripts/dev/create.sh "$(name)"

db-logs: ## Muestra logs de PostgreSQL
	docker compose logs db --tail=50

db-status: ## Muestra el estado de los servicios Docker
	docker compose ps

# ╔══════════════════════════════════════════╗
# ║          		  CI                     ║
# ╚══════════════════════════════════════════╝

auto-checks: ## Ejecuta validaciones automáticas de pre-commit
	bash scripts/ci/auto-checks.sh

manual-checks: ## Ejecuta checks manuales del proyecto
	bash scripts/ci/test.sh && \
	bash scripts/ci/coverage.sh

ci: ## Ejecuta validaciones automáticas + manuales
	$(MAKE) auto-checks
	$(MAKE) manual-checks

test: ## Ejecuta la suite de tests
	bash scripts/ci/test.sh

coverage: ## Ejecuta tests con coverage
	bash scripts/ci/coverage.sh

clean: ## Elimina caches y archivos temporales
	bash scripts/ci/clean.sh

# ╔══════════════════════════════════════════╗
# ║               TOOLING                    ║
# ╚══════════════════════════════════════════╝

context: ## Genera el estado del repositorio con Repomix
	bash scripts/tools/context.sh

hooks-install: ## Instala hooks Git del proyecto
	bash scripts/tools/install-git-hooks.sh

visual-check: ## Audita trazabilidad visual de la feature activa
	bash scripts/tools/check-visual-trace.sh
