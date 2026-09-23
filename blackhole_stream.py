const WebSocket = require('ws');
const { spawn } = require('child_process');

const wss = new WebSocket.Server({ port: 8080 });
console.log('Serwer WebSocket nasłuchuje na porcie 8080...');

wss.on('connection', (ws) => {
    console.log('iPhone połączony!');

    const rec = spawn('python3', [
        '/Users/rassio/Desktop/radio-bridge/blackhole_stream.py'
    ]);

    rec.stdout.on('data', (data) => {
        if (ws.readyState === 1) {
            ws.send(data);
        }
    });

    rec.stderr.on('data', (data) => {
        console.log('rec:', data.toString());
    });

    const play = spawn('play', [
        '-q',
        '-b', '16',
        '-c', '1',
        '-r', '48000',
        '-e', 'signed-integer',
        '-t', 'raw',
        '-'
    ]);

    play.stdin.on('error', (err) => {
        console.log('play error:', err.message);
    });

    play.on('error', (err) => {
        console.log('play spawn error:', err.message);
    });

    ws.on('message', (data) => {
        if (play.stdin.writable) {
            play.stdin.write(data);
        }
    });

    ws.on('close', () => {
        console.log('iPhone rozłączony!');
        rec.kill();
        play.kill();
    });
});
});