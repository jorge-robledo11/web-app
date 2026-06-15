#!/usr/bin/env python3
"""
Formatea docstrings de funciones y clases a estilo multilínea.

Normaliza docstrings single-line y multilínea existentes respetando la
indentación del nodo y la convención Google de pydocstyle.

Usar como hook local de pre-commit.
"""

import argparse
import ast
import re
from dataclasses import dataclass
from pathlib import Path

_DOCSTRING_START_RE = re.compile(
	r'^(?P<indent>\s*)'
	r'(?P<prefix>[rRuU]*)'
	r'(?P<quote>"""|\'\'\')'
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
	"""
	Indica si un nodo puede tener docstring de función o clase.
	"""
	return isinstance(node, ast.FunctionDef | ast.AsyncFunctionDef | ast.ClassDef)


def _first_statement(node: ast.AST) -> ast.stmt | None:
	"""
	Devuelve la primera sentencia del cuerpo del nodo, si existe.
	"""
	body = getattr(node, 'body', None)

	if not body:
		return None

	first = body[0]

	if isinstance(first, ast.stmt):
		return first

	return None


def _is_string_expr(statement: ast.stmt) -> bool:
	"""
	Indica si una sentencia es una expresión string literal.
	"""
	if not isinstance(statement, ast.Expr):
		return False

	if not isinstance(statement.value, ast.Constant):
		return False

	return isinstance(statement.value.value, str)


def _docstring_parts(line: str) -> tuple[str, str, str] | None:
	"""
	Obtiene indentación, prefijo y comillas de apertura del docstring.
	"""
	match = _DOCSTRING_START_RE.match(line)

	if match is None:
		return None

	return (
		match.group('indent'),
		match.group('prefix'),
		match.group('quote'),
	)


def _normalized_docstring_lines(
	node: ast.AST,
	statement: ast.stmt,
	lines: list[str],
) -> list[str] | None:
	"""
	Construye el docstring normalizado para un nodo documentado.
	"""
	docstring = ast.get_docstring(node, clean=True)

	if docstring is None:
		return None

	if not docstring.strip():
		return None

	parts = _docstring_parts(lines[statement.lineno - 1])

	if parts is None:
		return None

	indent, prefix, quote = parts
	new_lines = [f'{indent}{prefix}{quote}']

	for doc_line in docstring.splitlines():
		if doc_line:
			new_lines.append(f'{indent}{doc_line}')
		else:
			new_lines.append(indent)

	new_lines.append(f'{indent}{quote}')

	if isinstance(node, ast.ClassDef):
		next_index = statement.end_lineno

		if next_index < len(lines) and lines[next_index].strip():
			new_lines.append('')

	return new_lines


def _collect_replacements(source: str) -> list[Replacement]:
	"""
	Encuentra docstrings de funciones y clases para normalizarlos.
	"""
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

		new_lines = _normalized_docstring_lines(node, statement, lines)

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
	"""
	Aplica reemplazos sobre el contenido de un archivo.
	"""
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
	"""
	Filtra argumentos y devuelve solo archivos Python existentes.
	"""
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
	"""
	Parsea argumentos de línea de comandos.
	"""
	parser = argparse.ArgumentParser(
		description='Formatea docstrings de funciones y clases a multilínea.'
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
	files = _iter_python_files(args.files)

	if not files:
		return 0

	changed = False
	failed = False

	for path in files:
		try:
			changed = _format_file(path, check=args.check) or changed
		except (OSError, SyntaxError):
			failed = True

	if failed:
		return 1

	if args.check and changed:
		return 1

	return 0


if __name__ == '__main__':
	raise SystemExit(main())
