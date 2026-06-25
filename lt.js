const localtunnel = require('localtunnel');

(async () => {
  try {
    const tunnel = await localtunnel({ port: 8080 });
    console.log('[URL]', tunnel.url);
    // keep alive
    setInterval(() => {}, 60000);
    tunnel.on('close', () => {
      console.log('[CLOSED]');
      process.exit(1);
    });
  } catch (e) {
    console.error('[ERROR]', e.message);
    process.exit(1);
  }
})();
