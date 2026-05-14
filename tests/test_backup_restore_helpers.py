from subprocess import CompletedProcess

from app.api.panel.routes.backup import (
    _PUBLIC_SCHEMA_RESET_SQL,
    _format_subprocess_error,
    _prepare_restore_sql,
)


def test_prepare_restore_sql_strips_transaction_timeout_set():
    restored = _prepare_restore_sql(
        b"SET statement_timeout = 0;\nSET transaction_timeout = 0;\nCREATE TABLE demo(id int);\n"
    ).decode("utf-8")

    assert restored.startswith(f"{_PUBLIC_SCHEMA_RESET_SQL}\n")
    assert "SET statement_timeout = 0;" in restored
    assert "SET transaction_timeout = 0;" not in restored
    assert "CREATE TABLE demo(id int);" in restored


def test_prepare_restore_sql_strips_transaction_timeout_set_config():
    restored = _prepare_restore_sql(
        b"SELECT pg_catalog.set_config('transaction_timeout', '0', false);\nSELECT 1;\n"
    ).decode("utf-8")

    assert "transaction_timeout" not in restored
    assert "SELECT 1;" in restored


def test_prepare_restore_sql_strips_restrict_commands():
    restored = _prepare_restore_sql(
        b"\\restrict token123\nCREATE TABLE demo(id int);\n\\unrestrict token123\n"
    ).decode("utf-8")

    assert "\\restrict" not in restored
    assert "\\unrestrict" not in restored
    assert "CREATE TABLE demo(id int);" in restored


def test_format_subprocess_error_prefers_actual_error_over_drop_notice():
    result = CompletedProcess(
        args=["psql"],
        returncode=1,
        stdout=b"",
        stderr=(
            b"NOTICE: drop cascades to table broadcasts\n"
            b"NOTICE: drop cascades to table admins\n"
            b'psql:<stdin>:18: ERROR: unrecognized configuration parameter "transaction_timeout"\n'
        ),
    )

    formatted = _format_subprocess_error(result)

    assert 'ERROR: unrecognized configuration parameter "transaction_timeout"' in formatted
    assert "NOTICE: drop cascades" not in formatted
