import { spawnSync } from "node:child_process";
import { existsSync } from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";

const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), "..");
const backend = path.join(root, "backend");
const args = process.argv.slice(2);

if (args.length === 0) {
  console.error("usage: node scripts/backend.mjs <command> [args...]");
  process.exit(1);
}

const env = { ...process.env };
for (const bin of [
  path.join(backend, ".venv", "Scripts"),
  path.join(backend, ".venv", "bin"),
]) {
  if (existsSync(bin)) {
    env.PATH = `${bin}${path.delimiter}${env.PATH}`;
    break;
  }
}

const result = spawnSync(args[0], args.slice(1), {
  cwd: backend,
  env,
  stdio: "inherit",
  shell: true,
});

process.exit(result.status === null ? 1 : result.status);
