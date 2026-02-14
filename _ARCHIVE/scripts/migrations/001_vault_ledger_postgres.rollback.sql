-- Rollback: Remove VAULT999 PostgreSQL Ledger
-- WARNING: This destroys all vault data. Use with extreme caution.

DROP TABLE IF EXISTS vault_head;
DROP TABLE IF EXISTS vault_ledger;

-- Note: This intentionally does NOT drop the pgcrypto extension
-- as other tables may depend on it.
