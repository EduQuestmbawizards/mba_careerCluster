const fs = require('fs');
const path = require('path');

const publicDir = path.join(__dirname, 'public');
if (!fs.existsSync(publicDir)) {
  fs.mkdirSync(publicDir, { recursive: true });
}

// 1. Process index.html with BACKEND_URL injection
const srcHtmlPath = path.join(__dirname, 'index.html');
let html = fs.readFileSync(srcHtmlPath, 'utf8');

const backendUrl = process.env.BACKEND_URL || process.env.NEXT_PUBLIC_BACKEND_URL || process.env.RENDER_BACKEND_URL || '';
if (backendUrl) {
  html = html.replace(/__RENDER_BACKEND_URL__/g, backendUrl.replace(/\/+$/, ''));
  console.log('[MBAWizards Build] Injected BACKEND_URL from environment:', backendUrl);
} else {
  console.log('[MBAWizards Build] No BACKEND_URL found in environment, runtime detection will be used.');
}

// Write to both frontend/index.html and frontend/public/index.html
fs.writeFileSync(path.join(publicDir, 'index.html'), html);
fs.writeFileSync(srcHtmlPath, html);

// 2. Recursively copy static directory to public/static
function copyDir(src, dest) {
  if (!fs.existsSync(src)) return;
  fs.mkdirSync(dest, { recursive: true });
  for (const item of fs.readdirSync(src, { withFileTypes: true })) {
    const s = path.join(src, item.name);
    const d = path.join(dest, item.name);
    if (item.isDirectory()) {
      copyDir(s, d);
    } else {
      fs.copyFileSync(s, d);
    }
  }
}

copyDir(path.join(__dirname, 'static'), path.join(publicDir, 'static'));
console.log('[MBAWizards Build] Output directory "public" successfully generated for Vercel.');
