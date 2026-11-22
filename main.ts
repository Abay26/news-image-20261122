// news-image-20261122 — "THE WORLD TODAY", Sunday 22 November 2026.
//
// The entry is one front-page image (entry.png, drawn for this day: the
// COP31 draft in Antalya, Taiwan's short-selling ban, the Hong Kong vote,
// the Gulf, a 10% credit-card cap, the Manipur toll, the Alzheimer's study,
// plus 19 more stories in the brief strip). This program draws nothing: it
// inspects the bundled PNG chunk by chunk, checks its checksums, size and
// dimensions, and copies it to $MAKEFUN_OUTPUT_DIR/entry.png, so two runs
// always produce identical bytes. Node 22, standard library only, no
// network; the grader runs it with /bot read-only and /output empty.
//
// Local run:  mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts

import { mkdirSync, readFileSync, writeFileSync } from "node:fs";
import { join } from "node:path";

const LIMIT_BYTES = 1048576;
const LIMIT_SIDE = 1024;
const PNG_MAGIC = [0x89, 0x50, 0x4e, 0x47, 0x0d, 0x0a, 0x1a, 0x0a];

// CRC-32 (the polynomial the PNG format uses), table filled at load time.
function makeCrcTable(): Uint32Array {
  const table = new Uint32Array(256);
  for (let value = 0; value < 256; value++) {
    let entry = value;
    for (let bit = 0; bit < 8; bit++) {
      entry = entry & 1 ? (0xedb88320 ^ (entry >>> 1)) >>> 0 : entry >>> 1;
    }
    table[value] = entry >>> 0;
  }
  return table;
}

const CRC_TABLE = makeCrcTable();

function crcOf(data: Buffer): number {
  let acc = 0xffffffff;
  for (const byte of data) {
    acc = CRC_TABLE[(acc ^ byte) & 0xff] ^ (acc >>> 8);
  }
  return (acc ^ 0xffffffff) >>> 0;
}

type Chunk = { kind: string; start: number; length: number };

function listChunks(bytes: Buffer): Chunk[] {
  const found: Chunk[] = [];
  let pos = 8;
  while (pos + 12 <= bytes.length) {
    const length = bytes.readUInt32BE(pos);
    const kind = bytes.toString("ascii", pos + 4, pos + 8);
    const payloadEnd = pos + 8 + length;
    if (payloadEnd + 4 > bytes.length) {
      throw new Error(`chunk ${kind} at offset ${pos} runs past the file end`);
    }
    const stored = bytes.readUInt32BE(payloadEnd);
    const computed = crcOf(bytes.subarray(pos + 4, payloadEnd));
    if (stored !== computed) {
      throw new Error(`chunk ${kind} at offset ${pos} fails its CRC check`);
    }
    found.push({ kind, start: pos, length });
    if (kind === "IEND") {
      if (length !== 0 || payloadEnd + 4 !== bytes.length) {
        throw new Error("IEND is not the final empty chunk");
      }
      break;
    }
    pos = payloadEnd + 4;
  }
  return found;
}

function inspectPng(bytes: Buffer): { width: number; height: number } {
  if (bytes.length < 8) {
    throw new Error("entry.png is shorter than the PNG signature");
  }
  for (let i = 0; i < 8; i++) {
    if (bytes[i] !== PNG_MAGIC[i]) {
      throw new Error("entry.png does not begin with the PNG signature");
    }
  }
  if (bytes.length > LIMIT_BYTES) {
    throw new Error(`entry.png is ${bytes.length} bytes, above the 1 MiB cap`);
  }
  const chunks = listChunks(bytes);
  const ihdr = chunks[0];
  if (!ihdr || ihdr.kind !== "IHDR" || ihdr.length !== 13) {
    throw new Error("the first chunk is not a 13-byte IHDR");
  }
  const width = bytes.readUInt32BE(ihdr.start + 8);
  const height = bytes.readUInt32BE(ihdr.start + 12);
  if (width < 1 || width > LIMIT_SIDE || height < 1 || height > LIMIT_SIDE) {
    throw new Error(`image is ${width} by ${height}, above the 1024 cap`);
  }
  const kinds = new Set(chunks.map((c) => c.kind));
  if (!kinds.has("IDAT") || !kinds.has("IEND")) {
    throw new Error("entry.png is missing its IDAT or IEND chunk");
  }
  return { width, height };
}

const here = new URL(".", import.meta.url).pathname;
const source = join(here, "entry.png");
const outDir = process.env.MAKEFUN_OUTPUT_DIR ?? "/output";
const target = join(outDir, "entry.png");

const png = readFileSync(source);
const dims = inspectPng(png);

mkdirSync(outDir, { recursive: true });
writeFileSync(target, png);

const reread = readFileSync(target);
if (!reread.equals(png)) {
  throw new Error("the copied file does not match entry.png");
}
console.log(`entry.png copied to ${target} (${png.length} bytes, ${dims.width}x${dims.height})`);
