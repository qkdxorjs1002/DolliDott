import os

import discord
from discord.ext import commands, tasks

import requests
from bs4 import BeautifulSoup

_TOKEN = os.environ['DOLLIDOTT_TOKEN']

cmd_prefix = '!'
cmd_list = {'help': ['명령어', '이 메시지를 띄울 수 있는 명령어에요.'],
            'invite': ['초대', '돌리랑 도트를 다른 서버에 초대해보세요.'],
            'lyrics': ['가사', '돌리랑 도트 가사를 볼 수 있는 명령어에요.'],
            'damedane': ['다메다네', '다메다네~다메요~다메나노요~'],
            'crazy': ['테러', '돌리랑 도트가 그렇게 좋아? 그럼 계속 불러!'],
            'krw2usd': ['KRW2USD', '한화를 미국 달러로 실시간 환율을 반영해요.'],
            'usd2krw': ['USD2KRW', '미국 달러를 한화로  실시간 환율을 반영해요.'],
            'krw2cny': ['KRW2CNY', '한화를 중국 위안으로 실시간 환율을 반영해요.'],
            'cny2krw': ['CNY2KRW', '중국 위안을 한화로 실시간 환율을 반영해요.']}

lyrics_dollidott = ['돌리랑~ 도트가~ 제일~ 좋아~:musical_note:',
                    '돌리랑~ 도트가~ 제일~ 쪼아~:musical_note:',
                    '마차를~ 끌고~ 모래~ 언덕을~ 지나네~:musical_note: (찌나네~)',
                    '돌리랑~ 도트가~ 제일~ 좋아~:musical_note:',
                    '돌리랑~ 도트가~ 제일~ 쪼아~:musical_note:',
                    '이빨은~ 작아도~ 먹는걸~ 좋아해~:musical_note: (물진 않아요~)']

lyrics_damedane = ['だめだねだめよだめなのよ',
                   '다메다네 다메요 다메나노요',
                   '그건 안돼 안돼 절대 안돼',
                   '',
                   'あんたが好きで好きすぎて',
                   '안타가 스키데 스키스기테',
                   '당신이 좋아서 너무 좋아서',
                   '',
                   'どれだけ強いお酒でも',
                   '도레다케 츠요이 오사케데모',
                   '아무리 센 술로도',
                   '',
                   '歪まない思い出が馬鹿みたい',
                   '유가마나이 오모이데가 바카미타이',
                   '일그러지지 않는 추억이 바보 같아']

naver_finance_url = 'https://finance.naver.com/marketindex/'
naver_finance_1usd = 'body > div > table > tbody > tr:nth-child(1) > td.sale'
naver_finance_1cny = 'body > div > table > tbody > tr:nth-child(4) > td.sale'

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


def request_finance(url, path):
    res = requests.get(url)
    html = res.text

    soup = BeautifulSoup(html, 'html.parser')
    target = soup.select_one(path).text

    return target


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
    message = ''
    for comment in lyrics_dollidott:
        message += comment + '\n'

    await ctx.send(make_message(message))


# 명령 "다메다네"
@bot.command(name=cmd_list['damedane'][0])
async def lyrics(ctx):
    message = ''
    for comment in lyrics_damedane:
        message += comment + '\n'
    await ctx.send('https://tenor.com/view/damedane-gif-18432724')
    await ctx.send(make_message(message))


# 명령 "테러"
@bot.command(name=cmd_list['crazy'][0])
async def crazy(ctx, user: discord.User, cnt=1):
    await ctx.send(bot.user.avatar_url)
    message = make_message(user.display_name + ': ' + lyrics_dollidott[0])
    await ctx.send(message)

    if cnt > 20:
        cnt = 20

    for idx in range(cnt):
        for comment in lyrics_dollidott:
            comm = make_message(comment)
            await user.send(comm)


# 명령 "KRW2USD"
@bot.command(name=cmd_list['krw2usd'][0])
async def lyrics(ctx, value):
    rate = request_finance(naver_finance_url, naver_finance_1usd)
    result = round(value / rate, 2)
    message = value + ':flag_kr:은 ' + str(result) + ':flag_us:입니다.'

    await ctx.send(make_message(message))


# 명령 "USD2KRW"
@bot.command(name=cmd_list['usd2krw'][0])
async def lyrics(ctx, value):
    rate = request_finance(naver_finance_url, naver_finance_1usd)
    result = round(value * rate, 2)
    message = value + ':flag_us:는 ' + str(result) + ':flag_kr:입니다.'

    await ctx.send(make_message(message))


# 명령 "KRW2CNY"
@bot.command(name=cmd_list['krw2cny'][0])
async def lyrics(ctx, value):
    rate = request_finance(naver_finance_url, naver_finance_1cny)
    result = round(value / rate, 2)
    message = value + ':flag_kr:은 ' + str(result) + ':flag_cn:입니다.'

    await ctx.send(make_message(message))


# 명령 "CNY2KRW"
@bot.command(name=cmd_list['cny2krw'][0])
async def lyrics(ctx, value):
    rate = request_finance(naver_finance_url, naver_finance_1cny)
    result = round(value * rate, 2)
    message = value + ':flag_cn:은 ' + str(result) + ':flag_kr:입니다.'

    await ctx.send(make_message(message))


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
