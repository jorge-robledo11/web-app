// graphify — OpenCode plugin vendoreado para este proyecto.
//
// Inyecta reglas de uso de Graphify en el system prompt de OpenCode para que
// las preguntas sobre arquitectura, impacto y trazabilidad usen el grafo antes
// de leer archivos sueltos.

import fs from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);
const skillPath = path.join(__dirname, '..', 'skills', 'graphify', 'SKILL.md');

function stripFrontmatter(content) {
  return String(content || '').replace(/^---[\s\S]*?---\s*/, '').trim();
}

function findRepoRoot(startDir = process.cwd()) {
  let current = startDir;

  while (current && current !== path.dirname(current)) {
    if (
      fs.existsSync(path.join(current, 'AGENTS.md')) ||
      fs.existsSync(path.join(current, 'opencode.json')) ||
      fs.existsSync(path.join(current, '.git'))
    ) {
      return current;
    }
    current = path.dirname(current);
  }

  return startDir;
}

function readSkill() {
  try {
    return stripFrontmatter(fs.readFileSync(skillPath, 'utf8'));
  } catch (_error) {
    return [
      'GRAPHIFY ACTIVE',
      '',
      'For codebase questions, consult `graphify query` before browsing raw files when `graphify-out/graph.json` exists.',
      'Use `graphify path` for relationships and `graphify explain` for focused concepts.',
    ].join('\n');
  }
}

function graphStatus(root) {
  const graphJson = path.join(root, 'graphify-out', 'graph.json');
  const report = path.join(root, 'graphify-out', 'GRAPH_REPORT.md');
  const wiki = path.join(root, 'graphify-out', 'wiki', 'index.md');

  return [
    fs.existsSync(graphJson) ? '- `graphify-out/graph.json` existe.' : '- `graphify-out/graph.json` no existe todavía.',
    fs.existsSync(report) ? '- `graphify-out/GRAPH_REPORT.md` existe.' : '- `graphify-out/GRAPH_REPORT.md` no existe todavía.',
    fs.existsSync(wiki) ? '- `graphify-out/wiki/index.md` existe.' : '- `graphify-out/wiki/index.md` no existe todavía.',
  ].join('\n');
}

export default async ({ client } = {}) => {
  const log = (level, message) => {
    try {
      client?.app?.log?.({ body: { service: 'graphify', level, message } });
    } catch (_error) {
      // No bloquear OpenCode por logging.
    }
  };

  return {
    'experimental.chat.system.transform': async (_input, output) => {
      const root = findRepoRoot();
      output.system.push([
        readSkill(),
        '',
        'Estado local detectado:',
        graphStatus(root),
      ].join('\n'));
    },

    'command.execute.before': async (input) => {
      if (!input || input.command !== 'graphify') return;
      log('info', 'graphify ' + String(input.arguments || '').trim());
    },
  };
};
