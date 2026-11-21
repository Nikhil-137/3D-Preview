// Turns index.html (which loads three.js from a CDN) into a fully offline www/index.html
import { build } from 'esbuild';
import fs from 'node:fs';

const html = fs.readFileSync('index.html', 'utf8');
const m = html.match(/<script type="module">([\s\S]*?)<\/script>/);
if (!m) throw new Error('Module script not found in index.html');

fs.mkdirSync('.tmp', { recursive: true });
fs.writeFileSync('.tmp/entry.js', m[1]);

const out = await build({
  entryPoints: ['.tmp/entry.js'],
  bundle: true, minify: true, format: 'iife', write: false,
  nodePaths: ['node_modules'],
  alias: { 'three/addons': 'three/examples/jsm' }
});
const code = out.outputFiles[0].text.replace(/<\/script/g, '<\\/script');

const result = html
  .replace(/<script type="importmap">[\s\S]*?<\/script>/, '')
  .replace(/<script type="module">[\s\S]*?<\/script>/, () => `<script>${code}</script>`)
  .replace(' accept=".stl,.3mf"', ''); // Android file picker greys out unknown types

fs.mkdirSync('www', { recursive: true });
fs.writeFileSync('www/index.html', result);
console.log('Built www/index.html', (result.length / 1024).toFixed(0) + ' KB');
