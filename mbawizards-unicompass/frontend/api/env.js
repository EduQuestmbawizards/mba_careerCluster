export default function handler(req, res) {
  res.setHeader('Content-Type', 'application/javascript');
  res.setHeader('Cache-Control', 's-maxage=60, stale-while-revalidate');
  const backendUrl = process.env.BACKEND_URL || process.env.NEXT_PUBLIC_BACKEND_URL || process.env.RENDER_BACKEND_URL || '';
  res.status(200).send(`window.ENV = window.ENV || {}; window.ENV.BACKEND_URL = "${backendUrl}";`);
}
