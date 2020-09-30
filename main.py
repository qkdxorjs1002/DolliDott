import os
import time
import discord
from discord.ext import commands, tasks

_TOKEN = os.environ['DOLLIDOTT_TOKEN']

cmd_prefix = '!'
cmd_list = {'help': ['명령어', '이 메시지를 띄울 수 있는 명령어에요.'],
            'invite': ['초대', '돌리랑 도트를 다른 서버에 초대해보세요.'],
            'lyrics': ['가사', '돌리랑 도트 가사를 볼 수 있는 명령어에요.'],
            'crazy': ['테러', '돌리랑 도트가 그렇게 좋아? 그럼 계속 불러!']}

comments_lyrics = ['돌리랑~ 도트가~ 제일~ 좋아~:musical_note:',
                   '돌리랑~ 도트가~ 제일~~~ 쪼아~:musical_note:',
                   '마차를~ 끌고~ 모래~ 언덕을~ 지나네~~~:musical_note: (찌나네~)',
                   '돌리랑~ 도트가~ 제일~ 좋아~:musical_note:',
                   '돌리랑~ 도트가~ 제일~~~ 쪼아~:musical_note:',
                   '이빨은~ 작아도~ 먹는걸~ 좋아해~~~:musical_note: (물진 않아요~)']

bot = commands.Bot(command_prefix=cmd_prefix)


def make_message(contents, title='', sub='', contents_type='context'):
    message = ''
    if title != '':
        message += '> :llama: **' + title + '**\n\n'

    if sub != '':
        message += '**' + sub + '**\n'

    if contents_type == 'context':
        message += '>>> ' + contents
    elif contents_type == 'command':
        message += '```' + contents + '```'

    return message


@bot.event
async def on_ready():
    message = 'Logged in as ' + bot.user.name + ', id: ' + str(bot.user.id) + '\n'
    print(message)


# 명령 "명령어"
@bot.command(name=cmd_list['help'][0])
async def help(ctx):
    contents = ''

    for cmd, val in cmd_list.items():
        contents += ':round_pushpin: ' + cmd_prefix + val[0] + '\t' + val[1] + '\n\n'

    message = make_message(contents,
                           '사용 가능한 명령어 목록')

    await ctx.send(message)


# 명령 "초대"
@bot.command(name=cmd_list['invite'][0])
async def invite(ctx):
    message = make_message('https://discord.com/oauth2/authorize?client_id=' + str(bot.user.id) + '&scope=bot',
                           '돌리랑 도트를 다른 서버에 초대해보세요!')

    await ctx.send(message)


# 명령 "가사"
@bot.command(name=cmd_list['lyrics'][0])
async def lyrics(ctx):
    for comment in comments_lyrics:
        message = make_message(comment)
        await ctx.send(message)
        time.sleep(0.75)


# 명령 "테러"
@bot.command(name=cmd_list['crazy'][0])
async def crazy(ctx, user: discord.User, cnt=1):
    message = make_message(user.display_name + comments_lyrics[0],
                           bot.user.avatar_url)

    await ctx.send(message)

    if cnt > 20:
        cnt = 20

    for idx in range(cnt):
        for comment in comments_lyrics:
            await user.send(comment)
            time.sleep(0.75)


@crazy.error
async def crazy_error(ctx, error):
    print(error)
    if '50007' in str(error):
        message = make_message('테러를 받은 유저가 저를 차단했어요...칫...:put_litter_in_its_place:',
                               '에구구')

        await ctx.send(message)
    else:
        message = make_message('!테러 @<유저명> <반복 횟수(최대20)>',
                               '명령어 \"테러\" 사용법', '멈출 수 없으니 신중히 사용하세요!', 'command')

        await ctx.send(message)


bot.run(_TOKEN)
