.PHONY: setup dev db-up db-down db-reset db-migrate db-create-migration

setup:
	bash scripts/dev-setup.sh

dev:
	bash scripts/dev.sh

db-up:
	bash scripts/db/up.sh

db-down:
	bash scripts/db/down.sh

db-reset:
	bash scripts/db/reset.sh

db-migrate:
	bash scripts/db/migrate.sh

db-create-migration:
	bash scripts/db/create-migration.sh "$(name)"
