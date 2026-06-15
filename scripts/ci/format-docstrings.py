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
import sys
from dataclasses import dataclass
from pathlib import Path

_DOCSTRING_RE = re.compile(
	r'^(?P<indent>\s*)'
	r'(?P<prefix>[rRuU]*)'
	r'(?P<quote>"""|\'\'\')'
	r'(?P<body>.*)'
	r'(?P=quote)'
	r'\s*$'
)


@dataclass(frozen=True)
class Replacement:
	"""
	Representa un reemplazo de líneas dentro de un archivo.

	Attributes:
		start: Línea inicial 1-based.
		end: Línea final 1-based.
		lines: Nuevas líneas que reemplazan el rango.
	"""

	start: int
	end: int
	lines: list[str]


def _is_documented_node(node: ast.AST) -> bool:
	"""Indica si un nodo puede tener docstring de función o clase."""
	return isinstance(node, ast.FunctionDef | ast.AsyncFunctionDef | ast.ClassDef)


def _first_statement(node: ast.AST) -> ast.stmt | None:
	"""Devuelve la primera sentencia del cuerpo del nodo, si existe."""
	body = getattr(node, 'body', None)
	if not body:
		return None
	first = body[0]
	if isinstance(first, ast.stmt):
		return first
	return None


def _is_string_expr(statement: ast.stmt) -> bool:
	"""Indica si una sentencia es una expresión string literal."""
	if not isinstance(statement, ast.Expr):
		return False
	if not isinstance(statement.value, ast.Constant):
		return False
	return isinstance(statement.value.value, str)


def _replacement_for_line(line: str) -> list[str] | None:
	"""Crea las líneas multilínea para un docstring single-line."""
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


def _collect_replacements(source: str) -> list[Replacement]:
	"""Encuentra docstrings single-line de funciones y clases."""
	tree = ast.parse(source)
	lines = source.splitlines()
	replacements: list[Replacement] = []

	for node in ast.walk(tree):
		if not _is_documented_node(node):
			continue

		statement = _first_statement(node)
		if statement is None:
			continue
		if not _is_string_expr(statement):
			continue
		if statement.lineno != statement.end_lineno:
			continue

		line = lines[statement.lineno - 1]
		new_lines = _replacement_for_line(line)
		if new_lines is None:
			continue

		replacements.append(
			Replacement(
				start=statement.lineno,
				end=statement.end_lineno,
				lines=new_lines,
			)
		)

	return replacements


def _apply_replacements(source: str, replacements: list[Replacement]) -> str:
	"""Aplica reemplazos sobre el contenido de un archivo."""
	lines = source.splitlines()

	for replacement in sorted(replacements, key=lambda item: item.start, reverse=True):
		del lines[replacement.start - 1 : replacement.end]
		lines[replacement.start - 1 : replacement.start - 1] = replacement.lines

	result = '\n'.join(lines)
	if source.endswith('\n') or result:
		result += '\n'
	return result


def _format_file(path: Path, *, check: bool) -> bool:
	"""
	Formatea un archivo Python.

	Returns:
		True si el archivo fue modificado o debería modificarse.
	"""
	source = path.read_text(encoding='utf-8')
	replacements = _collect_replacements(source)

	if not replacements:
		return False

	formatted = _apply_replacements(source, replacements)
	if formatted == source:
		return False

	if not check:
		path.write_text(formatted, encoding='utf-8')

	return True


def _iter_python_files(paths: list[str]) -> list[Path]:
	"""Filtra argumentos y devuelve solo archivos Python existentes."""
	files: list[Path] = []
	for raw_path in paths:
		path = Path(raw_path)
		if not path.exists():
			continue
		if not path.is_file():
			continue
		if path.suffix != '.py':
			continue
		files.append(path)
	return files


def _parse_args() -> argparse.Namespace:
	"""Parsea argumentos de línea de comandos."""
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
	"""Ejecuta el formateador de docstrings."""
	args = _parse_args()
	files = _iter_python_files(args.files)

	if not files:
		return 0

	changed: list[Path] = []
	for path in files:
		try:
			if _format_file(path, check=args.check):
				changed.append(path)
		except SyntaxError:
			print(
				f'format-docstrings: error de sintaxis en {path}, omitiendo',
				file=sys.stderr,
			)
		except OSError as exc:
			print(
				f'format-docstrings: error leyendo/escribiendo {path}: {exc}',
				file=sys.stderr,
			)

	if not changed:
		return 0

	for path in changed:
		print(f'format-docstrings: {path}')

	if args.check:
		print(
			'format-docstrings: hay docstrings single-line que deben formatearse.',
			file=sys.stderr,
		)
	else:
		print(
			f'format-docstrings: {len(changed)} archivo(s) formateado(s). '
			'Ejecuta git add para stagear los cambios.'
		)

	return 1 if changed else 0


if __name__ == '__main__':
	raise SystemExit(main())
