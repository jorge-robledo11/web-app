#!/usr/bin/env python3
"""
Formatea docstrings single-line de funciones y clases a multilínea.

Convierte docstrings de una línea en funciones y clases a formato multilínea
respetando la indentación original y la convención Google de pydocstyle.

Usar como hook local de pre-commit.
"""

import argparse
import ast
import re
from pathlib import Path

_DOCSTRING_RE = re.compile(
	r'^(?P<indent>\s*)'
	r'(?P<prefix>[rRuU]*)'
	r'(?P<quote>"""|\'\'\')'
	r'(?P<body>.*)'
	r'(?P=quote)'
	r'\s*$'
)

_DOCUMENTED_NODES = ast.FunctionDef | ast.AsyncFunctionDef | ast.ClassDef


def _replacement_for(line: str) -> list[str] | None:
	match = _DOCSTRING_RE.match(line)

	if match is None:
		return None

	indent = match.group('indent')
	prefix = match.group('prefix')
	quote = match.group('quote')
	body = match.group('body').strip()

	if not body:
		return None

	return [
		f'{indent}{prefix}{quote}',
		f'{indent}{body}',
		f'{indent}{quote}',
	]


def _is_docstring_statement(statement: ast.stmt) -> bool:
	return (
		isinstance(statement, ast.Expr)
		and isinstance(statement.value, ast.Constant)
		and isinstance(statement.value.value, str)
		and statement.lineno == statement.end_lineno
	)


def _format_source(source: str) -> str:
	lines = source.splitlines()
	replacements: list[tuple[int, int, list[str]]] = []

	for node in ast.walk(ast.parse(source)):
		if not isinstance(node, _DOCUMENTED_NODES):
			continue

		if not node.body:
			continue

		statement = node.body[0]

		if not _is_docstring_statement(statement):
			continue

		new_lines = _replacement_for(lines[statement.lineno - 1])

		if new_lines is None:
			continue

		replacements.append((statement.lineno, statement.end_lineno, new_lines))

	for start, end, new_lines in sorted(replacements, reverse=True):
		lines[start - 1 : end] = new_lines

	result = '\n'.join(lines)

	if source.endswith('\n') or result:
		result += '\n'

	return result


def _python_files(paths: list[str]) -> list[Path]:
	return [
		path
		for raw_path in paths
		if (path := Path(raw_path)).is_file() and path.suffix == '.py'
	]


def _parse_args() -> argparse.Namespace:
	parser = argparse.ArgumentParser(
		description='Formatea docstrings single-line a multilínea.'
	)
	parser.add_argument(
		'--check',
		action='store_true',
		help='No modifica archivos; falla si hay cambios pendientes.',
	)
	parser.add_argument(
		'files',
		nargs='*',
		help='Archivos Python a procesar.',
	)

	return parser.parse_args()


def main() -> int:
	"""
	Ejecuta el formateador de docstrings.
	"""
	args = _parse_args()
	changed = False
	failed = False

	for path in _python_files(args.files):
		try:
			source = path.read_text(encoding='utf-8')
			formatted = _format_source(source)
		except (OSError, SyntaxError):
			failed = True
			continue

		if formatted == source:
			continue

		changed = True

		if not args.check:
			try:
				path.write_text(formatted, encoding='utf-8')
			except OSError:
				failed = True

	if failed:
		return 1

	if args.check and changed:
		return 1

	return 0


if __name__ == '__main__':
	raise SystemExit(main())
