function quote(file) {
  return `"${file.replaceAll("\\", "/")}"`;
}

export default {
  "backend/**/*.py": (filenames) => {
    const files = filenames.map(quote).join(" ");
    return [
      `node scripts/backend.mjs ruff check --fix ${files}`,
      `node scripts/backend.mjs ruff format ${files}`,
    ];
  },
  "frontend/**/*.{ts,tsx}": () => "npm --prefix frontend run typecheck",
};
