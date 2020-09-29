import os
import time
import discord
from discord.ext import commands, tasks

_TOKEN = os.environ['DOLLIDOTT_TOKEN']

bot = commands.Bot(command_prefix='!')

comments_lyrics = ['> 돌리랑~ 도트가~ 제일~ 좋아~:musical_note:\n> 돌리랑~ 도트가~ 제일~~~ 쪼아~:musical_note:',
                   '> 마차를~ 끌고~ 모래~ 언덕을~ 지나네~~~:musical_note: (찌나네~)',
                   '> 돌리랑~ 도트가~ 제일~ 좋아~:musical_note:\n> 돌리랑~ 도트가~ 제일~~~ 쪼아~:musical_note:',
                   '> 이빨은~ 작아도~ 먹는걸~ 좋아해~~~:musical_note: (물진 않아요~)']


@bot.event
async def on_ready():
    message = 'Logged in as' + bot.user.name + ', id: ' + bot.user.id + '\n'
    print(message)


@bot.command(name='가사')
async def lyrics(ctx):
    for comment in comments_lyrics:
        await ctx.send(comment)
        time.sleep(1)


@bot.command(name='테러')
async def crazy(ctx, user: discord.User, cnt=1):
    message = '> ' + user.display_name + ': \"돌리랑~ 도트가~ 제일~ 좋아~:musical_note:\"'
    await ctx.send(bot.user.avatar_url)
    await ctx.send(message)

    if cnt > 20:
        cnt = 20

    for idx in range(cnt):
        for comment in comments_lyrics:
            await user.send(comment)
            time.sleep(1)


@crazy.error
async def crazy_error(ctx, error):
    print(error)
    if '50007' in error:
        await ctx.send('> **에구구**\n**테러를 받은 유저가 저를 차단했어요...칫...:put_litter_in_its_place:**')
    else:
        await ctx.send('> **명령어 \"테러\" 사용법**\n**멈출 수 없으니 신중히 사용하세요!**\n```!테러 @<유저명> <반복 횟수(최대20)>```')


bot.run(_TOKEN)
