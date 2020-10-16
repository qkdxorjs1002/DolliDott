import os

import discord
from discord.ext import commands, tasks

import requests
from bs4 import BeautifulSoup

from googletrans import Translator


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
            'cny2krw': ['CNY2KRW', '중국 위안을 한화로 실시간 환율을 반영해요.'],
            'ko': ['ko', '다른 언어를 한국어로 번역해요.'],
            'en': ['en', '다른 언어를 영어로 번역해요.'],
            'cn': ['cn', '다른 언어를 중국어로 번역해요.'],
            'cal': ['cal', '계산식을 처리해요.']}

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
naver_finance_1usd = '#exchangeList > li.on > a.head.usd > div > span.value'
naver_finance_1cny = '#exchangeList > li:nth-child(4) > a.head.cny > div > span.value'

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
    target = soup.select_one(path)

    return target.text.replace(',', '')


def translate(lang, text):
    translator = Translator()
    result = translator.translate(text, dest=lang)

    return result.text


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
async def krw2usd(ctx, value):
    invalue = float(value.replace(',', ''))
    rate = request_finance(naver_finance_url, naver_finance_1usd)
    result = round(invalue / float(rate), 2)
    message = '**' + "{:,}".format(invalue) + '** :flag_kr:   :left_right_arrow:   **' + \
              "{:,}".format(result) + '** :flag_us:'

    await ctx.send(make_message(message))


# 명령 "USD2KRW"
@bot.command(name=cmd_list['usd2krw'][0])
async def usd2krw(ctx, value):
    invalue = float(value.replace(',', ''))
    rate = request_finance(naver_finance_url, naver_finance_1usd)
    result = round(invalue * float(rate), 2)
    message = '**' + "{:,}".format(invalue) + '** :flag_us:   :left_right_arrow:   **' + \
              "{:,}".format(result) + '** :flag_kr:'

    await ctx.send(make_message(message))


# 명령 "KRW2CNY"
@bot.command(name=cmd_list['krw2cny'][0])
async def krw2cny(ctx, value):
    invalue = float(value.replace(',', ''))
    rate = request_finance(naver_finance_url, naver_finance_1cny)
    result = round(invalue / float(rate), 2)
    message = '**' + "{:,}".format(invalue) + '** :flag_kr:   :left_right_arrow:   **' + \
              "{:,}".format(result) + '** :flag_cn:'

    await ctx.send(make_message(message))


# 명령 "CNY2KRW"
@bot.command(name=cmd_list['cny2krw'][0])
async def cny2krw(ctx, value):
    invalue = float(value.replace(',', ''))
    rate = request_finance(naver_finance_url, naver_finance_1cny)
    result = round(invalue * float(rate), 2)
    message = '**' + "{:,}".format(invalue) + '** :flag_cn:   :left_right_arrow:   **' + \
              "{:,}".format(result) + '** :flag_kr:'

    await ctx.send(make_message(message))


# 명령 "ko"
@bot.command(name=cmd_list['ko'][0])
async def ko(ctx, *, text):
    message = translate("ko", str(text))

    await ctx.send(make_message(message))


# 명령 "en"
@bot.command(name=cmd_list['en'][0])
async def en(ctx, *, text):
    message = translate("en", str(text))

    await ctx.send(make_message(message))


# 명령 "cn"
@bot.command(name=cmd_list['cn'][0])
async def cn(ctx, *, text):
    message = translate("zh-cn", str(text))

    await ctx.send(make_message(message))


# 명령 "cal"
@bot.command(name=cmd_list['cal'][0])
async def cal(ctx, *, text):
    message = str(eval(str(text)))

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


@krw2usd.error
async def krw2usd_error(ctx, error):
    print(error)
    message = make_message('!KRW2USD <금액>',
                           '명령어 \"KRW2USD\" 사용법', '실시간 환율에 따라 한국 원을 미국 달러로 변환합니다.', 'command')

    await ctx.send(message)


@usd2krw.error
async def usd2krw_error(ctx, error):
    print(error)
    message = make_message('!USD2KRW <금액>',
                           '명령어 \"USD2KRW\" 사용법', '실시간 환율에 따라 미국 달러를 한국 원으로 변환합니다.', 'command')

    await ctx.send(message)


@krw2cny.error
async def krw2cny_error(ctx, error):
    print(error)
    message = make_message('!KRW2CNY <금액>',
                           '명령어 \"KRW2CNY\" 사용법', '실시간 환율에 따라 한국 원을 중국 위안으로 변환합니다.', 'command')

    await ctx.send(message)


@cny2krw.error
async def cny2krw_error(ctx, error):
    print(error)
    message = make_message('!CNY2KRW <금액>',
                           '명령어 \"CNY2KRW\" 사용법', '실시간 환율에 따라 중국 위안을 한국 원으로 변환합니다.', 'command')

    await ctx.send(message)


@ko.error
async def ko_error(ctx, error):
    print(error)
    message = make_message('!ko <변환할 문장>',
                           '명령어 \"ko\" 사용법', '문장을 한국어로 변환해줍니다.', 'command')

    await ctx.send(message)


@en.error
async def en_error(ctx, error):
    print(error)
    message = make_message('!en <변환할 문장>',
                           '명령어 \"en\" 사용법', '문장을 영어로 변환해줍니다.', 'command')

    await ctx.send(message)


@cn.error
async def cn_error(ctx, error):
    print(error)
    message = make_message('!cn <변환할 문장>',
                           '명령어 \"cn\" 사용법', '문장을 중국어로 변환해줍니다.', 'command')

    await ctx.send(message)


@cal.error
async def cal_error(ctx, error):
    print(error)
    message = make_message('!cal 계산식',
                           '명령어 \"cal\" 사용법', '계산식을 계산합니다.', 'command')

    await ctx.send(message)


bot.run(_TOKEN)
