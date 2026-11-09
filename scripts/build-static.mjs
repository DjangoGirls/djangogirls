// Builds the static files Django serves, replacing the old gulp setup.
//
// Usage: node scripts/build-static.mjs <task>
//   local - one-off development build into static/local/
//   watch - local build, then rebuild when static/source/ changes
//   build - production build into static/build/: minified CSS & JS with
//           content-hashed filenames listed in static/rev-manifest.json
//   clean - remove everything the tasks above create
import { createHash } from "node:crypto";
import { cp, mkdir, readFile, readdir, rename, rm, writeFile } from "node:fs/promises";
import { watch as fsWatch } from "node:fs";
import path from "node:path";

import stylus from "stylus";
import { minify } from "terser";

const SOURCE = "static/source";
const DEST = { development: "static/local", production: "static/build" };
const MANIFEST = "static/rev-manifest.json";

// Each bundle is the compiled stylus file of the same name, prefixed by these vendor files
const CSS_BUNDLES = {
  global: ["node_modules/bootstrap/dist/css/bootstrap.min.css", `${SOURCE}/vendor/css/sss.css`],
  event: ["node_modules/bootstrap/dist/css/bootstrap.min.css"],
  admin: [],
};

const log = (message) => console.log(`[${new Date().toLocaleTimeString()}] ${message}`);

/**
 * Compiles each CSS bundle with stylus and concatenates its vendor files in front of it
 */
async function styles(dest, production) {
  await mkdir(`${dest}/css`, { recursive: true });
  const bundle = async ([name, vendorFiles]) => {
    const filename = `${SOURCE}/css/${name}.styl`;
    const [source, ...parts] = await Promise.all(
      [filename, ...vendorFiles].map((file) => readFile(file, "utf8")),
    );
    const css = stylus(source).set("filename", filename).set("compress", production).render();
    await writeFile(`${dest}/css/${name}.css`, [...parts, css].join("\n"));
  };
  await Promise.all(Object.entries(CSS_BUNDLES).map(bundle));
}

/**
 * Copies JS files, minifying them for production builds
 */
async function scripts(dest, production) {
  await mkdir(`${dest}/js`, { recursive: true });
  const copyScript = async (file) => {
    let code = await readFile(`${SOURCE}/js/${file}`, "utf8");
    if (production) {
      code = (await minify(code)).code;
    }
    await writeFile(`${dest}/js/${file}`, code);
  };
  const files = await readdir(`${SOURCE}/js`);
  await Promise.all(files.filter((file) => file.endsWith(".js")).map(copyScript));
}

/**
 * Copies everything else (images, fonts, vendor files) as is
 */
async function copyFiles(dest) {
  await cp(SOURCE, dest, {
    recursive: true,
    filter: (src) => {
      const relative = path.relative(SOURCE, src).split(path.sep);
      return relative[0] !== "css" && relative[0] !== "js";
    },
  });
}

/**
 * Appends a content hash to built CSS & JS filenames (`global.css` → `global-d41d8cd98f.css`)
 * so browsers fetch the new file after a deploy, and writes the mapping that
 * django-gulp-rev's {% static_rev %} tag reads.
 */
async function revision(dest) {
  const revisionFile = async (file) => {
    const contents = await readFile(`${dest}/${file}`);
    const hash = createHash("md5").update(contents).digest("hex").slice(0, 10);
    const { dir, name, ext } = path.parse(file);
    const revisioned = `${dir}/${name}-${hash}${ext}`;
    await rename(`${dest}/${file}`, `${dest}/${revisioned}`);
    return [file, revisioned];
  };
  const listDir = async (dir) => (await readdir(`${dest}/${dir}`)).map((file) => `${dir}/${file}`);
  const files = (await Promise.all(["css", "js"].map(listDir))).flat().sort();
  const manifest = Object.fromEntries(await Promise.all(files.map(revisionFile)));
  await writeFile(MANIFEST, JSON.stringify(manifest, null, 2));
}

async function clean() {
  await Promise.all(
    [DEST.development, DEST.production, MANIFEST].map((target) =>
      rm(target, { recursive: true, force: true }),
    ),
  );
}

async function build(production) {
  const dest = production ? DEST.production : DEST.development;
  await clean();
  await styles(dest, production);
  await scripts(dest, production);
  await copyFiles(dest);
  if (production) {
    await revision(dest);
  }
  log(`Built static files into ${dest}/`);
}

/**
 * Rebuilds the local static files whenever something in static/source/ changes
 */
async function watch() {
  await build(false);
  let timeout;
  fsWatch(SOURCE, { recursive: true }, () => {
    // editors often write several events per save, so wait for them to settle
    clearTimeout(timeout);
    timeout = setTimeout(() => build(false).catch((error) => log(error.message)), 100);
  });
  log(`Watching ${SOURCE}/ for changes...`);
}

const task = process.argv[2] ?? "watch";
switch (task) {
  case "local":
    await build(false);
    break;
  case "build":
    await build(true);
    break;
  case "watch":
    await watch();
    break;
  case "clean":
    await clean();
    break;
  default:
    console.error(`Unknown task "${task}". Available tasks: local, build, watch, clean`);
    process.exit(1);
}
