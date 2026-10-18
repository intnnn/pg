import { mkdir, writeFile } from "node:fs/promises";
import { resolve } from "node:path";
import worker from "../worker/index.js";

const outputDir = resolve("dist");
const response = await worker.fetch(new Request("https://netlify.local/"));

if (!response.ok || !response.headers.get("content-type")?.includes("text/html")) {
  throw new Error(`Expected the site worker to return HTML, received ${response.status}.`);
}

await mkdir(outputDir, { recursive: true });
await writeFile(resolve(outputDir, "index.html"), await response.text());
console.log(`Wrote ${resolve(outputDir, "index.html")}`);
