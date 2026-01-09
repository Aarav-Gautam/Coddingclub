const {
    Client,
    IntentsBitField,
    REST,
    Routes,
    PermissionFlagsBits,
    EmbedBuilder,
    SlashCommandBuilder
} = require('discord.js');
require('dotenv').config();
const fetch = require('node-fetch');
const fs = require('fs');
const cron = require('node-cron');

const DISCORD_TOKEN = process.env.TOKEN;
const CLIENT_ID = process.env.CLIENT_ID || 'YOUR_CLIENT_ID';
const OPENROUTER_KEY = process.env.OPENROUTER_KEY;

// --- DATABASE SIMULATION ---
const DB_FILE = './db.json';
let db = {
    warnings: {},
    bans: [],
    mutes: [],
    customCommands: {},
    config: {
        restrictedChannels: {},
        blacklistedWords: ['badword1', 'badword2'],
        announcementChannel: {},
        autoModActions: {}
    },
    logs: [],
    cooldowns: {},
    rateLimits: {},
    scheduledMessages: {}
};

function loadDB() {
    if (fs.existsSync(DB_FILE)) db = JSON.parse(fs.readFileSync(DB_FILE, 'utf-8'));
}
function saveDB() { fs.writeFileSync(DB_FILE, JSON.stringify(db, null, 2)); }
function logAction(type, userId, moderator, action, reason = '') {
    db.logs.push({ type, timestamp: new Date().toISOString(), userId, moderator, action, reason });
    saveDB();
}
loadDB();

// --- CLIENT SETUP ---
const client = new Client({
    intents: [
        IntentsBitField.Flags.Guilds,
        IntentsBitField.Flags.GuildMessages,
        IntentsBitField.Flags.MessageContent,
        IntentsBitField.Flags.GuildMembers,
    ],
});

// --- COOLDOWN SYSTEM ---
function checkCooldown(userId, commandName, cooldownSeconds = 3) {
    const now = Date.now();
    if (!db.cooldowns[userId]) db.cooldowns[userId] = {};
    const lastUsed = db.cooldowns[userId][commandName];
    if (lastUsed && now - lastUsed < cooldownSeconds * 1000) {
        const timeLeft = Math.ceil((cooldownSeconds * 1000 - (now - lastUsed)) / 1000);
        return { onCooldown: true, timeLeft };
    }
    db.cooldowns[userId][commandName] = now;
    return { onCooldown: false };
}

// --- RATE LIMITING ---
function checkRateLimit(userId, maxRequests = 10, windowMinutes = 60) {
    const now = Date.now();
    if (!db.rateLimits[userId]) {
        db.rateLimits[userId] = { count: 1, resetTime: now + windowMinutes * 60 * 1000 };
        return { limited: false };
    }
    if (now > db.rateLimits[userId].resetTime) {
        db.rateLimits[userId] = { count: 1, resetTime: now + windowMinutes * 60 * 1000 };
        return { limited: false };
    }
    if (db.rateLimits[userId].count >= maxRequests) return { limited: true, resetTime: db.rateLimits[userId].resetTime };
    db.rateLimits[userId].count++;
    return { limited: false };
}

// --- AI LOGIC ---
async function getAIResponse(prompt) {
    try {
        const response = await fetch('https://openrouter.ai/api/v1/chat/completions', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json', 'Authorization': `Bearer ${OPENROUTER_KEY}` },
            body: JSON.stringify({
                model: "gpt-4o-mini",
                messages: [
                    { role: "system", content: "You are Comet, a friendly and helpful Discord bot. Be concise." },
                    { role: "user", content: prompt }
                ]
            }),
        });
        const data = await response.json();
        return data.choices?.[0]?.message?.content || "⚠️ I couldn't think of anything to say.";
    } catch (err) {
        console.error(err);
        return "⚠️ Error connecting to AI service.";
    }
}

// --- READY EVENT ---
client.on('ready', () => {
    console.log(`🚀 ${client.user.tag} is online!`);
});

// --- MESSAGE MENTION HANDLER ---
client.on('messageCreate', async message => {
    if (message.author.bot) return;

    if (!message.mentions.has(client.user)) return; // only respond to @Comet

    const userMessage = message.content
        .replace(`<@${client.user.id}>`, '')
        .replace(`<@!${client.user.id}>`, '')
        .trim();

    if (!userMessage) return message.reply("Hello! How can I help you today?");

    // Commands via mention start with '/'
    if (userMessage.startsWith('/')) {
        const args = userMessage.slice(1).split(' ');
        const cmd = args[0].toLowerCase();

        const targetMention = message.mentions.users.filter(u => u.id !== client.user.id).first();

        // --- Mute Command ---
        if (cmd === 'mute') {
            if (!message.member.permissions.has(PermissionFlagsBits.ModerateMembers))
                return message.reply('❌ You need **Moderate Members** permission.');

            if (!targetMention) return message.reply('❌ Mention a user to mute.');
            const duration = parseInt(args[1]) || 1; // default 1 minute
            const reason = args.slice(2).join(' ') || 'No reason provided';
            try {
                const target = await message.guild.members.fetch(targetMention.id);
                await target.timeout(duration * 60 * 1000, reason);
                logAction('mute', target.id, message.author.tag, `Muted for ${duration} minutes`, reason);
                return message.reply(`🔇 **${target.user.tag}** muted for ${duration} minute(s). Reason: ${reason}`);
            } catch (e) {
                return message.reply('❌ Failed to mute user. Check permissions.');
            }
        }

        // --- Unmute Command ---
        if (cmd === 'unmute') {
            if (!message.member.permissions.has(PermissionFlagsBits.ModerateMembers))
                return message.reply('❌ You need **Moderate Members** permission.');

            if (!targetMention) return message.reply('❌ Mention a user to unmute.');
            try {
                const target = await message.guild.members.fetch(targetMention.id);
                await target.timeout(null);
                logAction('unmute', target.id, message.author.tag, 'Unmuted');
                return message.reply(`🔊 **${target.user.tag}** has been unmuted.`);
            } catch (e) {
                return message.reply('❌ Failed to unmute user.');
            }
        }

        // --- Ban Command ---
        if (cmd === 'ban') {
            if (!message.member.permissions.has(PermissionFlagsBits.BanMembers))
                return message.reply('❌ You need **Ban Members** permission.');
            if (!targetMention) return message.reply('❌ Mention a user to ban.');
            const reason = args.slice(1).join(' ') || 'No reason provided';
            try {
                const target = await message.guild.members.fetch(targetMention.id);
                await target.ban({ reason });
                logAction('ban', target.id, message.author.tag, 'Banned', reason);
                return message.reply(`🔨 **${target.user.tag}** has been banned. Reason: ${reason}`);
            } catch (e) {
                return message.reply('❌ Failed to ban user. Check bot permissions.');
            }
        }

        // --- Kick Command ---
        if (cmd === 'kick') {
            if (!message.member.permissions.has(PermissionFlagsBits.KickMembers))
                return message.reply('❌ You need **Kick Members** permission.');
            if (!targetMention) return message.reply('❌ Mention a user to kick.');
            const reason = args.slice(1).join(' ') || 'No reason provided';
            try {
                const target = await message.guild.members.fetch(targetMention.id);
                await target.kick(reason);
                logAction('kick', target.id, message.author.tag, 'Kicked', reason);
                return message.reply(`👢 **${target.user.tag}** has been kicked. Reason: ${reason}`);
            } catch (e) {
                return message.reply('❌ Failed to kick user. Check permissions.');
            }
        }

        // --- Warn Command ---
        if (cmd === 'warn') {
            if (!message.member.permissions.has(PermissionFlagsBits.ModerateMembers))
                return message.reply('❌ You need **Moderate Members** permission.');
            if (!targetMention) return message.reply('❌ Mention a user to warn.');
            const reason = args.slice(1).join(' ') || 'No reason provided';
            if (!db.warnings[targetMention.id]) db.warnings[targetMention.id] = [];
            db.warnings[targetMention.id].push({
                reason,
                timestamp: new Date().toISOString(),
                moderator: message.author.tag
            });
            logAction('warn', targetMention.id, message.author.tag, 'Warned', reason);
            saveDB();
            return message.reply(`⚠️ **${targetMention.tag}** warned. Reason: ${reason}. Total warns: ${db.warnings[targetMention.id].length}`);
        }

        // --- Check Warnings ---
        if (cmd === 'warns') {
            if (!targetMention) return message.reply('❌ Mention a user to check warnings.');
            const warns = db.warnings[targetMention.id] || [];
            if (warns.length === 0) return message.reply(`${targetMention.tag} has no warnings.`);
            const embed = new EmbedBuilder()
                .setTitle(`Warnings for ${targetMention.tag}`)
                .setDescription(warns.map((w, i) => `${i + 1}. [${w.timestamp.split('T')[0]}] Mod: ${w.moderator} - Reason: ${w.reason}`).join('\n'))
                .setColor(0xFFA500);
            return message.reply({ embeds: [embed] });
        }

        // --- Help ---
        if (cmd === 'help') {
            const helpEmbed = new EmbedBuilder()
                .setTitle('🤖 Comet Bot Commands')
                .setDescription('Use these commands by mentioning me!')
                .addFields(
                    { name: '🛡️ Moderation', value: '`@Comet /mute <@user> [minutes] [reason]`\n`@Comet /unmute <@user>`\n`@Comet /ban <@user> [reason]`\n`@Comet /kick <@user> [reason]`\n`@Comet /warn <@user> [reason]`\n`@Comet /warns <@user>`' },
                    { name: '💬 AI & Fun', value: '`@Comet tell me a joke`\n`@Comet trivia`\n`@Comet fact`\n`@Comet quote`\n`@Comet poll <question>`' }
                )
                .setColor(0x00AE86);
            return message.reply({ embeds: [helpEmbed] });
        }
    }

    // --- AI chat ---
    const rateLimit = checkRateLimit(message.author.id, 20, 60);
    if (rateLimit.limited) {
        const resetMinutes = Math.ceil((rateLimit.resetTime - Date.now()) / 60000);
        return message.reply(`⚠️ Rate limit reached. Try again in ${resetMinutes} minutes.`);
    }

    await message.channel.sendTyping();
    const response = await getAIResponse(userMessage);
    await message.reply(response);
});

client.login(DISCORD_TOKEN);
