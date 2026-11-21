#!/usr/bin/env bash
mkdir -p bin
cat > package.json <<'JSON'
{
  "name": "csvtidy",
  "version": "0.3.1",
  "description": "Clean up messy CSV files from the command line",
  "bin": { "csvtidy": "bin/csvtidy.js" },
  "license": "MIT",
  "engines": { "node": ">=18" }
}
JSON
cat > bin/csvtidy.js <<'JS'
#!/usr/bin/env node
const fs = require("fs");

const args = process.argv.slice(2);
const opts = { trim: false, dedupe: false, out: null, delimiter: "," };
const files = [];
for (let i = 0; i < args.length; i++) {
  const a = args[i];
  if (a === "--trim") opts.trim = true;
  else if (a === "--dedupe") opts.dedupe = true;
  else if (a === "--out") opts.out = args[++i];
  else if (a === "--delimiter") opts.delimiter = args[++i];
  else if (a === "--help" || a === "-h") {
    console.log("usage: csvtidy [--trim] [--dedupe] [--delimiter <char>] [--out <file>] <input.csv>");
    process.exit(0);
  } else files.push(a);
}
if (files.length !== 1) {
  console.error("csvtidy: give exactly one input file (stdin is not supported)");
  process.exit(2);
}

let rows = fs.readFileSync(files[0], "utf8").split(/\r?\n/).filter((l) => l.length > 0)
  .map((l) => l.split(opts.delimiter));
if (opts.trim) rows = rows.map((r) => r.map((c) => c.trim()));
if (opts.dedupe) {
  const seen = new Set();
  rows = rows.filter((r) => { const k = r.join("|"); if (seen.has(k)) return false; seen.add(k); return true; });
}
const out = rows.map((r) => r.join(opts.delimiter)).join("\n") + "\n";
if (opts.out) fs.writeFileSync(opts.out, out); else process.stdout.write(out);
JS
printf 'MIT License\n\nCopyright (c) 2026 csvtidy authors\n' > LICENSE
