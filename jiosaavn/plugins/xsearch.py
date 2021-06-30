from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from ..tools.request import req


@Client.on_message(filters.text & filters.incoming & filters.private & ~filters.regex('.*http.*') & ~filters.edited & ~filters.via_bot)
async def search(c, m):
    send_msg = await m.reply_text('__**Processing... ⏳**__', quote=True)

    if not await c.db.is_user_exist(m.from_user.id):
        await c.db.add_user(m.from_user.id)

    api_url = 'https://www.jiosaavn.com/api.php?'
    params = {
        'p': 1,
        'q': m.text,
        '_format': 'json',
        '_marker': 0,
        'api_version': 4,
        'ctx': 'wap6dot0',
        'n': 10
    }

    type = (await c.db.get_user(m.from_user.id))['type']
    if type == 'all':
        params = {
            '__call': 'autocomplete.get',
            'query': m.text,
            '_format': 'json',
            '_marker': 0,
            'ctx': 'wap6dot0'
        }
    elif type == 'album':
        params['__call'] = 'search.getAlbumResults'
    elif type == 'song':
        params['__call'] = 'search.getResults'
    elif type == 'artists':
        params['__call'] = 'search.getArtistResults'
    elif type == 'playlist':
        params['__call'] = 'search.getPlaylistResults'

    data = await req(api_url, params)
    buttons = []

    if type != 'all':
        if not 'results' in data:
            return await send_msg.edit(f'🔎 No search result found for your query `{m.text}`')
        total_results = data['total']
        for result in data['results']:
            id = result['id'] if 'id' in result else None
            if 'type' in result:
                title = result['title'] if 'title' in result else ''
                if result['type'] == 'song':
                    album = ''
                    if 'more_info' in result:
                        album = result['more_info']['album'] if 'album' in result['more_info'] else ''
                    buttons.append([InlineKeyboardButton(f"🎙 {title} from '{album}'", callback_data=f'open+{id}')])
                elif result['type'] == 'album':
                    buttons.append([InlineKeyboardButton(f"📚 {title}", callback_data=f'album+{id}')])
                elif result['type'] == 'playlist':
                    buttons.append([InlineKeyboardButton(f"💾 {title}", callback_data=f'playlist+{id}')])
            else:
                buttons.append([InlineKeyboardButton(f"👨‍🎤 {result['name']}", callback_data=f'artist+{id}')])

    else:
        if not 'albums' in data:
            return await send_msg.edit(f'🔎 No search result found for your query `{m.text}`')
        index_btn = []
        for album in data['albums']['data']:
            title = album['title'] if 'title' in album else ''
            id = album['id'] if 'id' in album else None
            buttons.append([InlineKeyboardButton(f"📚 {title}", callback_data=f'album+{id}')])
        if len(buttons) != 0:
            index_btn.append(InlineKeyboardButton('Albums 📖', callback_data='nxt+album+1'))
        for i, song in enumerate(data['songs']['data']):
            title = song['title'] if 'title' in song else ''
            id = song['id'] if 'id' in song else None
            album = song['album'] if 'album' in song else ''
            try:
                buttons[i].append(InlineKeyboardButton(f"🎙 {title} from '{album}'", callback_data=f'open+{id}'))
            except:
                buttons.append([InlineKeyboardButton(f"🎙 {title} from '{album}'", callback_data=f'open+{id}')])
        if len(buttons) == 0:
            return await send_msg.edit(f'🔎 No search result found for your query `{m.text}`')
        index_btn.append(InlineKeyboardButton('Songs 🎧', callback_data='nxt+song+1'))
        buttons.insert(0, index_btn)

    text = f"**🔍 Search Query:** {m.text}\n\n__Your search result 👇__"
    if type != "all":
        text = f'**📈 Total Results:** {total_results}\n\n**🔍 Search Query:** {m.text}\n\n**📜 Page No:** 1'
        if total_results > 10:
            buttons.append([InlineKeyboardButton("➡️", callback_data=f"nxt+{type}+2")])

    if len(buttons) == 0:
        return await send_msg.edit(f'🔎 No search result found for your query `{m.text}`')

    await send_msg.edit(text, reply_markup=InlineKeyboardMarkup(buttons))



@Client.on_callback_query(filters.regex('^nxt'))
async def nxt_cb(c, m):
    await m.answer()
    cmd, type, page = m.data.split('+')
    page = int(page)
    query = m.message.reply_to_message
    
    api_url = 'https://www.jiosaavn.com/api.php?'
    params = {
        'p': page,
        'q': query.text,
        '_format': 'json',
        '_marker': 0,
        'api_version': 4,
        'ctx': 'wap6dot0',
        'n': 10
    }
    if type == 'all':
        params = {
            '__call': 'autocomplete.get',
            'query': query.text,
            '_format': 'json',
            '_marker': 0,
            'ctx': 'wap6dot0'
        }
    elif type == 'album':
        params['__call'] = 'search.getAlbumResults'
    elif type == 'song':
        params['__call'] = 'search.getResults'
    elif type == 'artists':
        params['__call'] = 'search.getArtistResults'
    elif type == 'playlist':
        params['__call'] = 'search.getPlaylistResults'

    data = await req(api_url, params)

    buttons = []
    if type != 'all':
        total_results = data['total']
        for result in data['results']:
            title = result['title'] if 'title' in result else ''
            id = result['id'] if 'id' in result else None
            if result['type'] == 'song':
                album = ''
                if 'more_info' in result:
                    album = result['more_info']['album'] if 'album' in result['more_info'] else ''
                buttons.append([InlineKeyboardButton(f"🎙 {title} from '{album}'", callback_data=f'open+{id}')])
            elif result['type'] == 'album':
                buttons.append([InlineKeyboardButton(f"📚 {title}", callback_data=f'album+{id}')])
    else:
        index_btn = []
        for album in data['albums']['data']:
            title = album['title'] if 'title' in album else ''
            id = album['id'] if 'id' in album else None
            buttons.append([InlineKeyboardButton(f"📚 {title}", callback_data=f'album+{id}')])
        if len(buttons) != 0:
            index_btn.append(InlineKeyboardButton('Albums 📖', callback_data='nxt+album+1'))
        for i, song in enumerate(data['songs']['data']):
            title = song['title'] if 'title' in song else ''
            id = song['id'] if 'id' in song else None
            album = song['album'] if 'album' in song else ''
            try:
                buttons[i].append(InlineKeyboardButton(f"🎙 {title} from '{album}'", callback_data=f'open+{id}'))
            except:
                buttons.append([InlineKeyboardButton(f"🎙 {title} from '{album}'", callback_data=f'open+{id}')])
        if len(buttons) == 0:
            return await m.message.edit(f'🔎 No search result found for your query `{m.text}`')
        index_btn.append(InlineKeyboardButton('Songs 🎧', callback_data='nxt+song+1'))
        buttons.insert(0, index_btn)

    nxt_btn = []
    text = f"**🔍 Search Query:** {query.text}\n\n__Your search result 👇__"
    if type != "all":
        text = f'**📈 Total Results:** {total_results}\n\n**🔍 Search Query:** {query.text}\n\n**📜 Page No:** {page}'

        if page != 1:
            nxt_btn.append(InlineKeyboardButton("⬅️", callback_data=f"nxt+{type}+{page-1}"))
        if total_results > 10 * page:
            nxt_btn.append(InlineKeyboardButton("➡️", callback_data=f"nxt+{type}+{page+1}"))
    buttons.append(nxt_btn)

    if len(buttons) == 1:
        return await m.message.edit('__Nothing found here 👀__')

    try:
        await m.message.edit(text, reply_markup=InlineKeyboardMarkup(buttons))
    except:
        pass
