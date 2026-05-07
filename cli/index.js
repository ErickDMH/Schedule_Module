#!/usr/bin/env node

const { spawn } = require('child_process');
const path = require('path');

const args = process.argv.slice(2);
const command = args[0] || 'help';

if (command === 'initial') {
    console.log('Running make initial...');
    const make = spawn('make', ['initial'], {
        cwd: path.resolve(__dirname, '..'),
        stdio: 'inherit'
    });

    make.on('close', (code) => {
        process.exit(code);
    });
} else {
    console.log(`
Schedule Module CLI

Usage:
  schedule-module initial    Initializes the module (runs 'make initial')
  schedule-module help       Shows this help message
`);
}
