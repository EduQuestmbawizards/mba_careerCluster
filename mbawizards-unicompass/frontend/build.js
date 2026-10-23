const fs = require('fs');
const path = require('path');

const indexPath = path.join(__dirname, 'index.html');
if (fs.existsSync(indexPath)) {
  let html = fs.readFileSync(indexPath, 'utf8');
  const backendUrl = process.env.BACKEND_URL || process.env.NEXT_PUBLIC_BACKEND_URL || process.env.RENDER_BACKEND_URL || '';
  if (backendUrl) {
    html = html.replace(/__RENDER_BACKEND_URL__/g, backendUrl.replace(/\/+$/, ''));
    fs.writeFileSync(indexPath, html);
    console.log('[MBAWizards Build] Injected BACKEND_URL from environment:', backendUrl);
  } else {
    console.log('[MBAWizards Build] No BACKEND_URL found in environment, runtime detection will be used.');
  }
}
