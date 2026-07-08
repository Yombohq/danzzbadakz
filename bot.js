const { Telegraf, Markup } = require('telegraf');

const nodemailer = require('nodemailer');

const fs = require('fs');

const config = require('./config');

const bot = new Telegraf(config.BOT_TOKEN);

const usersFile = './users.json';

const mailFile = './mail.json';

let usersData = JSON.parse(fs.readFileSync(usersFile, 'utf-8'));

let mailData = JSON.parse(fs.readFileSync(mailFile, 'utf-8'));

// ===== GROUP =====

const GROUP_1_ID = -1003515213121;

const GROUP_2_ID = -1003574311686;

const GROUP_1_LINK = 'https://t.me/privatallinformationdanz';

const GROUP_2_LINK = 'https://t.me/publicdanzztfr';

// ===== SAVE =====

function saveUsers(){

  fs.writeFileSync(usersFile, JSON.stringify(usersData, null, 2));

}

function saveMail(){

  fs.writeFileSync(mailFile, JSON.stringify(mailData, null, 2));

}

function addUser(id){

  if(!usersData.users.includes(id)){

    usersData.users.push(id);

    saveUsers();

  }

}

// ===== VERIF =====

function isVerified(id){

  return usersData.verified.includes(id);

}

function setVerified(id){

  if(!usersData.verified.includes(id)){

    usersData.verified.push(id);

    saveUsers();

  }

}

// ===== RANDOM =====

function randomDigits(len = 6){

  let r = '';

  for(let i=0;i<len;i++) r += Math.floor(Math.random()*10);

  return r;

}

// ===== CEK MEMBER =====

async function isMember(ctx, userId, groupId){

  try{

    const m = await ctx.telegram.getChatMember(groupId, userId);

    return ['member','administrator','creator'].includes(m.status);

  }catch{

    return false;

  }

}

// ===== START UI =====

const startMessage = `

\`\`\`

╭──(    𝘿𝙖𝙣𝙯𝙯𝘼𝙡𝙬𝙖𝙮𝙨 ☇ 𝘿𝙖𝙣𝙯𝙯𝘼𝙡𝙬𝙖𝙮𝙨    )

║ᨒ 𝘿𝙖𝙣𝙯𝙯𝘼𝙡𝙬𝙖𝙮𝙨 𝘼𝘷𝗮𝗶𝗹𝗮𝗯𝗹𝗲 

│🎭 𝐍𝐚𝐦𝐞 : 𝙁𝙞𝙭 𝙈𝙚𝙧𝙖𝙝 𝘽𝙤𝙩

║▬▭▬▭▬▭▬▭▬▭

│🎭 𝐍𝐚𝐦𝐞 𝐒𝐜𝐫𝐢𝐩𝐭 : 𝙁𝙞𝙭 𝙈𝙚𝙧𝙖𝙝

║🎭 𝐃𝐞𝐯𝐞𝐥𝐨𝐩𝐞𝐫 : 𝘿𝙖𝙣𝙯𝙯𝘼𝙡𝙬𝙖𝙮𝙨

│🎭 𝐕𝐞𝐫𝐬𝐢𝐨𝐧: 4.0.4

║🎭 𝐏𝐫𝐞𝐟𝐢𝐱 : 𝐓𝐞𝐥𝐞𝐠𝐫𝐚𝐦

│▬▭「 𝙁𝙞𝙭 𝙈𝙚𝙧𝙖𝙝🐉 」▭▬

║› © DanzzAlways-X

╰━━━━━━━━━━━━━━━━━━━⬣

Silahkan pilih menu button di bawah

\`\`\`

`;

async function sendStart(ctx){

  addUser(ctx.from.id);

  await ctx.replyWithPhoto(

    { url: config.PHOTO_URL },

    {

      caption: startMessage,

      parse_mode: 'MarkdownV2',

      ...Markup.inlineKeyboard([

        [Markup.button.callback('FixMerah','FIXMERAH')],

        [Markup.button.callback('Settings Sender','SENDER_SETTING')],

        [Markup.button.callback('Info','INFO')],

        [Markup.button.url('Developer', config.DEVELOPER_URL)]

      ])

    }

  );

}

// ===== START =====

bot.start(async (ctx)=>{

  const uid = ctx.from.id;

  addUser(uid);

  if(isVerified(uid)){

    return sendStart(ctx);

  }

  const keyboard = Markup.inlineKeyboard([

    [Markup.button.url('📢JOIN GRUB 1', GROUP_1_LINK)],

    [Markup.button.url('📢JOIN GRUB 2', GROUP_2_LINK)],

    [Markup.button.callback('✅CEK VERIFIKASI', 'CHECK_JOIN')]

  ]);

  await ctx.reply(

    '📌 Silahkan join semua grup terlebih dahulu sebelum menggunakan bot!',

    keyboard

  );

});

// ===== CHECK JOIN =====

bot.action('CHECK_JOIN', async (ctx)=>{

  const uid = ctx.from.id;

  const j1 = await isMember(ctx, uid, GROUP_1_ID);

  const j2 = await isMember(ctx, uid, GROUP_2_ID);

  if(j1 && j2){

    setVerified(uid);

    await ctx.deleteMessage();

    await sendStart(ctx);

  }else{

    await ctx.answerCbQuery('❌ Kamu belum join semua grup!', { show_alert:true });

  }

});

// ===== SETTINGS SENDER UI =====

bot.action('SENDER_SETTING', async (ctx)=>{

  await ctx.deleteMessage();

  await ctx.replyWithPhoto(

    { url: config.PHOTO_URL },

    {

      caption: `

\`\`\`

╭──(   SETTINGS SENDER ☇   )

│ /setsender <gmail> | <password>

│ /mysender

│ /delsender

│ Gmail + App Password

╰────────────────────────

\`\`\`

`,

      parse_mode:'MarkdownV2',

      ...Markup.inlineKeyboard([

        [Markup.button.callback('Delete Sender','DELETE_SENDER')],

        [Markup.button.callback('Back','BACK')]

      ])

    }

  );

});

// ===== BACK =====

bot.action('BACK', async (ctx)=>{

  await ctx.deleteMessage();

  await sendStart(ctx);

});

// ===== SET SENDER =====

bot.command('setsender', (ctx)=>{

  const args = ctx.message.text.split(' ');

  if(args.length < 4 || args[2] !== '|'){

    return ctx.reply('❌ Format: /setsender gmail | password');

  }

  const uid = ctx.from.id;

  mailData.senders[uid] = {

    email: args[1],

    pass: args[3].replace(/\s+/g,'')

  };

  saveMail();

  ctx.reply(`✅ Sender disimpan\n📧 ${args[1]}`);

});

// ===== MY SENDER =====

bot.command('mysender', (ctx)=>{

  const uid = ctx.from.id;

  if(!mailData.senders[uid]){

    return ctx.reply('❌ Kamu belum set sender');

  }

  ctx.reply(`📧 Sender kamu:\n${mailData.senders[uid].email}`);

});

// ===== DELETE SENDER =====

bot.command('delsender', (ctx)=>{

  const uid = ctx.from.id;

  if(!mailData.senders[uid]){

    return ctx.reply('❌ Kamu tidak punya sender');

  }

  delete mailData.senders[uid];

  saveMail();

  ctx.reply('✅ Sender berhasil dihapus');

});

bot.action('DELETE_SENDER', async (ctx)=>{

  const uid = ctx.from.id;

  if(!mailData.senders[uid]){

    return ctx.answerCbQuery('❌ Sender tidak ditemukan', { show_alert:true });

  }

  delete mailData.senders[uid];

  saveMail();

  await ctx.deleteMessage();

  await ctx.reply('✅ Sender berhasil dihapus');

});

// ===== FIX MERAH UI (BUTTON) =====
bot.action('FIXMERAH', async (ctx) => {
  await ctx.answerCbQuery();
  await ctx.deleteMessage().catch(()=>{});

  await ctx.replyWithPhoto(
    { url: config.PHOTO_URL },
    {
      caption: `
\`\`\`
╭──(    FIX MERAH MENU ☇     )
║ᨒ 𝘿𝙖𝙣𝙯𝙯𝘼𝙡𝙬𝙖𝙮𝙨
║▬▭▬▭▬▭▬▭▬▭
│🎭 Gunakan perintah:
│ /fix <nomor>
│
│ Contoh:
│ /fix 628123456789
│
│▬▭「 𝙁𝙞𝙭 𝙈𝙚𝙧𝙖𝙝🐉 」▭▬
║› © DanzzAlways-X
╰━━━━━━━━━━━━━━━━━━━⬣
\`\`\`
`,
      parse_mode: 'MarkdownV2',
      ...Markup.inlineKeyboard([
        [Markup.button.callback('⚙ Settings Sender','SENDER_SETTING')],
        [Markup.button.callback('⬅ Back','BACK')]
      ])
    }
  );
});


// ===== INFO UI (SUDAH DI-UPGRADE) =====
bot.action('INFO', async (ctx) => {
  await ctx.answerCbQuery();
  await ctx.deleteMessage().catch(()=>{});

  const totalSender = Object.keys(mailData.senders || {}).length;
  const totalUser = (usersData.users || []).length;

  await ctx.replyWithPhoto(
    { url: config.PHOTO_URL },
    {
      caption: `
\`\`\`
╭──(      INFO BOT ☇      )
║ᨒ 𝘿𝙖𝙣𝙯𝙯𝘼𝙡𝙬𝙖𝙮𝙨
║▬▭▬▭▬▭▬▭▬▭
│🎭 Name          : Fix Merah Bot
│🎭 Script       : Fix Merah
│🎭 Version      : 4.0.4
│🎭 Prefix       : Telegram
│🎭 Total Sender : ${totalSender}
│🎭 Total User   : ${totalUser}
│
│ Support :
│ - DanzzAlways
│ - MarkAnjay
│
│▬▭「 𝙁𝙞𝙭 𝙈𝙚𝙧𝙖𝙝🐉 」▭▬
║› © DanzzAlways-X
╰━━━━━━━━━━━━━━━━━━━⬣
\`\`\`
`,
      parse_mode: 'MarkdownV2',
      ...Markup.inlineKeyboard([
        [Markup.button.callback('⬅ Back','BACK')]
      ])
    }
  );
});

// ===== LIST ALL SENDER (OWNER) =====

bot.command('listallsender', (ctx)=>{

  if(!usersData.owner.includes(ctx.from.id)){

    return ctx.reply('❌ Hanya owner.');

  }

  const senders = mailData.senders || {};

  const keys = Object.keys(senders);

  if(!keys.length){

    return ctx.reply('📭 Belum ada sender user.');

  }

  let text = '📋 LIST ALL SENDER USER\n\n';

  let no = 1;

  for(const uid of keys){

    text += `${no++}. ${senders[uid].email}\n`;

  }

  ctx.reply(text);

});

// ===== FIX =====

bot.command('fix', async (ctx)=>{

  const args = ctx.message.text.split(' ');

  if(args.length < 2){

    return ctx.reply('❌ Format salah.\nGunakan: /fix <nomor>');

  }

  const nomor = args[1];

  const uid = ctx.from.id;

  
    
    const loadingMessage = `
\`\`\`
╭──(    SEDANG MEMPROSES ☇     )
║ᨒ 𝘿𝙖𝙣𝙯𝙯𝘼𝙡𝙬𝙖𝙮𝙨
║▬▭▬▭▬▭▬▭▬▭
│🎭 Sedang menganalisis nomor...
│🎭 Nomor: ${nomor}
│🎭 Mohon tunggu sebentar
│▬▭「 𝙁𝙞𝙭 𝙈𝙚𝙧𝙖𝙝🐉 」▭▬
╰━━━━━━━━━━━━━━━━━━━⬣
\`\`\`
`;

  const loadingMsg = await ctx.reply(loadingMessage, { parse_mode: 'MarkdownV2' });


  let sender;

  if(usersData.owner.includes(uid)){

    const all = Object.values(mailData.senders || {});

    sender = all.length ? all[Math.floor(Math.random()*all.length)] : null;

  }else{

    sender = mailData.senders[uid];

  }

  if(!sender){

    await ctx.deleteMessage(loadingMsg.message_id).catch(()=>{});

    return ctx.reply('❌ Sender tidak tersedia');

  }

  // 🔥 FIX UTAMA DI SINI

  const transporter = nodemailer.createTransport({

    host: "smtp.gmail.com",

    port: 587,

    secure: false,

    auth: {

      user: sender.email,

      pass: sender.pass

    },

    tls: { rejectUnauthorized: false }

  });

  let success = false;

  try{

    await transporter.sendMail({

      from: `"Bot FixMerah" <${sender.email}>`,

      to: mailData.TO_EMAIL,

      subject: `Banding ${nomor} - ${Date.now()}${randomDigits(6)}`,

      text: `Halo pihak WhatsApp,

Perkenalkan, nama saya RizkyMaxz.

Saya ingin mengajukan banding terkait masalah pendaftaran nomor telepon saya.

Saat proses registrasi, muncul pesan "login tidak tersedia".

Mohon kiranya pihak WhatsApp dapat membantu memperbaiki masalah tersebut.

Nomor saya: +${nomor}

Terima kasih atas perhatian dan bantuannya.

Hormat saya,

DanzzAlways`,

    });

    success = true;

  }catch(e){

    console.error('FIX ERROR:', e);

    if(!usersData.owner.includes(uid)){

      delete mailData.senders[uid];

      saveMail();

    }

  }

  await ctx.deleteMessage(loadingMsg.message_id).catch(()=>{});

  await ctx.reply(`

\`\`\`

╭──(    STATUS BANDING ☇     )

║ᨒ 𝘿𝙖𝙣𝙯𝙯𝘼𝙡𝙬𝙖𝙮𝙨 

║▬▭▬▭▬▭▬▭▬▭

│🎭 STATUS : ${success ? 'SUCCES✅' : 'GAGAL❌'}

│🎭 NOMOR  : ${nomor}

│▬▭「 𝙁𝙞𝙭 𝙈𝙚𝙧𝙖𝙝🐉 」▭▬

╰━━━━━━━━━━━━━━━━━━━⬣

\`\`\`

`, { parse_mode: 'MarkdownV2' });

});

// ===== LAUNCH =====

bot.launch();

console.log('Bot berjalan...');
