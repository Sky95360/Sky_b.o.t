// ============================================
// 🤖 SKY_BOT v3.0 - MAIN FILE
// Repository: https://github.com/Sky95360/Sky_b.o.t
// ============================================

require('dotenv').config();
const { makeWASocket, useMultiFileAuthState, DisconnectReason } = require('@whiskeysockets/baileys');
const qrcode = require('qrcode-terminal');
const fs = require('fs');
const path = require('path');

// Bot Configuration
const CONFIG = {
    PREFIX: process.env.PREFIX || '!',
    BOT_NAME: process.env.BOT_NAME || 'Sky_BOT',
    OWNER: process.env.OWNER_NUMBER || ''
};

// ============================================
// 🚀 START BOT
// ============================================
async function startBot() {
    console.log(`
    ╔═══════════════════════════╗
    ║     🤖 SKY_BOT v3.0       ║
    ║     by: Sky95360          ║
    ║     Repo: Sky_b.o.t       ║
    ╚═══════════════════════════╝
    `);
    
    // Load session or create new
    const { state, saveCreds } = await useMultiFileAuthState('./sessions');
    
    // Create WhatsApp connection
    const sock = makeWASocket({
        auth: state,
        printQRInTerminal: true,
        browser: ['Sky_BOT', 'Chrome', '3.0.0'],
        markOnlineOnConnect: true
    });
    
    // ============================================
    // 📡 CONNECTION EVENTS
    // ============================================
    sock.ev.on('connection.update', (update) => {
        const { connection, lastDisconnect, qr } = update;
        
        // Show QR Code
        if (qr) {
            console.log('\n📱 SCAN THIS QR WITH WHATSAPP:');
            qrcode.generate(qr, { small: true });
            console.log('\n⚠️  QR expires in 60 seconds!');
        }
        
        // Handle connection close
        if (connection === 'close') {
            const shouldReconnect = lastDisconnect.error?.output?.statusCode !== DisconnectReason.loggedOut;
            console.log('Connection closed. Reconnecting...', shouldReconnect);
            if (shouldReconnect) {
                setTimeout(startBot, 5000);
            }
        }
        
        // Connection open
        if (connection === 'open') {
            console.log('✅ Connected to WhatsApp!');
            console.log('🤖 Bot is ready to use!');
            console.log(`Prefix: ${CONFIG.PREFIX}`);
            
            // Send owner notification
            if (CONFIG.OWNER) {
                sock.sendMessage(CONFIG.OWNER, { 
                    text: `✅ *Sky_BOT Activated!*\n\n📅 ${new Date().toLocaleString()}\n⚡ Version: 3.0.0\n📁 Repo: github.com/Sky95360/Sky_b.o.t` 
                });
            }
        }
    });
    
    // Save session updates
    sock.ev.on('creds.update', saveCreds);
    
    // ============================================
    // 💬 MESSAGE HANDLER
    // ============================================
    sock.ev.on('messages.upsert', async (m) => {
        const msg = m.messages[0];
        if (!msg.message || msg.key.fromMe) return;
        
        const text = msg.message.conversation || msg.message.extendedTextMessage?.text || '';
        const sender = msg.key.remoteJid;
        const isGroup = sender.endsWith('@g.us');
        
        // Check for prefix
        if (text.startsWith(CONFIG.PREFIX)) {
            const command = text.slice(CONFIG.PREFIX.length).trim().split(' ')[0].toLowerCase();
            const args = text.slice(CONFIG.PREFIX.length + command.length).trim();
            
            console.log(`Command: ${command} | From: ${sender}`);
            
            // Handle commands
            await handleCommand(sock, msg, command, args, sender, isGroup);
        }
    });
}

// ============================================
// 🎮 COMMAND HANDLER
// ============================================
async function handleCommand(sock, msg, command, args, sender, isGroup) {
    const commands = {
        // Info commands
        'menu': () => showMenu(sock, sender),
        'help': () => showHelp(sock, sender, args),
        'info': () => showInfo(sock, sender),
        
        // Fun commands
        'sticker': () => makeSticker(sock, msg, sender),
        'meme': () => sendMeme(sock, sender),
        'joke': () => sendJoke(sock, sender),
        
        // Tools
        'weather': () => getWeather(sock, sender, args),
        'calc': () => calculate(sock, sender, args),
        'time': () => sendTime(sock, sender),
        
        // Media
        'yt': () => downloadYT(sock, sender, args),
        'ig': () => downloadIG(sock, sender, args),
        
        // Owner
        'bc': () => broadcast(sock, sender, args),
        'eval': () => evalCode(sock, sender, args),
        'restart': () => restartBot(sock, sender)
    };
    
    if (commands[command]) {
        try {
            await commands[command]();
        } catch (error) {
            console.error(`Error in ${command}:`, error);
            sock.sendMessage(sender, { text: `❌ Error: ${error.message}` });
        }
    } else {
        sock.sendMessage(sender, { 
            text: `❓ Unknown command: ${command}\nType ${CONFIG.PREFIX}menu for available commands.` 
        });
    }
}

// ============================================
// 📜 COMMAND FUNCTIONS
// ============================================

// Show menu
async function showMenu(sock, sender) {
    const menu = `
╔══════════════════════════╗
║     📜 SKY_BOT MENU      ║
╠══════════════════════════╣
║ 🔹 ${CONFIG.PREFIX}menu - Show this menu
║ 🔹 ${CONFIG.PREFIX}info - Bot information
║ 🔹 ${CONFIG.PREFIX}help <cmd> - Command help
╠══════════════════════════╣
║ 🎮 FUN COMMANDS:
║ ${CONFIG.PREFIX}sticker - Make sticker
║ ${CONFIG.PREFIX}meme - Random meme
║ ${CONFIG.PREFIX}joke - Funny joke
╠══════════════════════════╣
║ 🛠️  TOOLS:
║ ${CONFIG.PREFIX}weather <city> - Weather
║ ${CONFIG.PREFIX}calc <expr> - Calculator
║ ${CONFIG.PREFIX}time - Current time
╠══════════════════════════╣
║ 📥 MEDIA DOWNLOADER:
║ ${CONFIG.PREFIX}yt <url> - YouTube DL
║ ${CONFIG.PREFIX}ig <url> - Instagram DL
╠══════════════════════════╣
║ 👑 OWNER:
║ ${CONFIG.PREFIX}bc <msg> - Broadcast
║ ${CONFIG.PREFIX}eval <code> - Run code
║ ${CONFIG.PREFIX}restart - Restart bot
╚══════════════════════════╝

📁 Repo: github.com/Sky95360/Sky_b.o.t
    `;
    
    await sock.sendMessage(sender, { text: menu });
}

// Bot info
async function showInfo(sock, sender) {
    const info = `
🤖 *SKY_BOT INFORMATION*

👨‍💻 *Developer:* Sky95360
📁 *Repository:* Sky_b.o.t
🔗 *URL:* https://github.com/Sky95360/Sky_b.o.t
⚡ *Version:* 3.0.0
📅 *Started:* December 2024
🔧 *Platform:* Node.js
💾 *Session:* Multi-file Auth
🚀 *Deployment:* Render, Railway, Koyeb

📊 *Features:*
• Media Downloader (YT, IG)
• Sticker Maker
• Games & Fun Commands
• Tools & Utilities
• Group Management
• Broadcast System

Type ${CONFIG.PREFIX}menu for commands.
    `;
    
    await sock.sendMessage(sender, { text: info });
}

// ============================================
// 🎯 SIMPLE COMMAND IMPLEMENTATIONS
// ============================================

// Make sticker from image
async function makeSticker(sock, msg, sender) {
    if (msg.message.imageMessage) {
        await sock.sendMessage(sender, { 
            text: '🔄 Converting image to sticker...' 
        });
        // Sticker conversion logic here
        setTimeout(() => {
            sock.sendMessage(sender, { 
                text: '✅ Sticker created!\n(Note: Add sticker conversion code here)' 
            });
        }, 2000);
    } else {
        await sock.sendMessage(sender, { 
            text: '📸 Please send an image with caption !sticker' 
        });
    }
}

// Send random meme
async function sendMeme(sock, sender) {
    const memes = [
        'https://i.imgur.com/example1.jpg',
        'https://i.imgur.com/example2.jpg',
        'https://i.imgur.com/example3.jpg'
    ];
    const randomMeme = memes[Math.floor(Math.random() * memes.length)];
    
    await sock.sendMessage(sender, { 
        image: { url: randomMeme },
        caption: '😂 Random Meme'
    });
}

// YouTube downloader
async function downloadYT(sock, sender, args) {
    if (!args) {
        await sock.sendMessage(sender, { 
            text: `❌ Please provide YouTube URL\nUsage: ${CONFIG.PREFIX}yt <youtube-url>` 
        });
        return;
    }
    
    await sock.sendMessage(sender, { 
        text: `📥 Downloading YouTube video...\nURL: ${args}\n\n🔧 Add ytdl-core package for actual download.` 
    });
}

// ============================================
// 🚀 START THE BOT
// ============================================
startBot().catch(console.error);
