import os
# import shutil
# import atexit
from dotenv import load_dotenv
import discord
from discord import app_commands, Guild
from discord.ext import commands, tasks
from datetime import datetime
import gspread
# from google.oauth2.service_account import Credentials
# from google.oauth2 import service_account
# import json

load_dotenv()

TOKEN = os.environ['TOKEN_ID']

intents = discord.Intents.all()
client = discord.Client(intents=intents)
tree = app_commands.CommandTree(client)
bot = commands.Bot(command_prefix='/', intents=intents)

# service_account_key_str = os.environ.get('SERVICE_ACCOUNT')

# service_account_info = json.loads(service_account_key_str)

# scopes = [
#     'https://www.googleapis.com/auth/spreadsheets',
#     'https://www.googleapis.com/auth/drive'
# ]

# credentials = service_account.Credentials.from_service_account_info(
#     service_account_info, scopes=scopes
# )

# gc = gspread.authorize(credentials)

# sh = gc.open_by_key('1OitzgfW-9LMzPcxDpfbrL2PcNJArKowX836kNMVE2xs')

# ws = sh.get_worksheet(0)

# # messageログ
# log_path = f'log.csv'
# with open(log_path, 'w', encoding='utf-8') as f:
#     # f.write(f'Discord Version: {discord.__version__}\n#------------------------------#\n')
#     f.write(f'Discord Version: {discord.__version__}\n作成日時,編集日時,カテゴリ,カテゴリID,チャンネル,チャンネルID,作成者,作成者ID,メッセージID,メッセージ\n')

# def bot_exit():
#     # log.csvをどうにか保存する
#     if os.path.exists(log_path):
#         if not os.path.exists('log'):
#             os.mkdir('log')
#         current_time = datetime.utcnow()
#         formatted_time = current_time.strftime('%Y-%m-%d-%H-%M-%S-%f')[:22]
#         shutil.move(log_path, f'log\\{formatted_time}.csv') # [YYYY-MM-DD-hh-mm-ss-ms.csv]という名前で保存される

# atexit.register(bot_exit)

@client.event
async def on_ready():
    # time=datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    # print(f'{time} \033[34mINFO     \033[35mdiscord.py \033[0mv.{discord.__version__}')
    print('ready...')
    await tree.sync()
    loop_membercount.start()

# @client.event
# async def on_message(message):
#     # チャットのログをcsvfileに保存する
#     ## とりあえずlogカテゴリは無視する
#     if message.channel.category.id == int(os.environ['LOG_CATEGORY_ID']):
#         return
#     else:
#         msg_cont = message.content.replace("\n", "\\n")
#         ## とりあえずコンソールに簡易的なものを表示
#         print(f'{message.created_at} | {message.channel.category} | {message.channel} | @{message.author} | <{message.author.id}> | {msg_cont}')
#         ## 
#         with open(log_path, 'a', encoding='utf-8') as f:
#             f.write(f'{message.created_at},{message.edited_at},{message.channel.category},{message.channel.category.id},{message.channel},{message.channel.id},{message.author},{message.author.id},{message.id},{msg_cont}\n')
#         # 次にlogを表示する用のチャンネルにメッセージを送る
#         ## いつか...ね？

# @client.event
# async def on_message_edit(after):
#     msg_cont = after.message.content.replace("\n", "\\n")
#     print(f'{after.message.created_at} | {after.message.channel.category} | {after.message.channel} | {after.message.author} | <{after.message.author.id}> | {msg_cont}')
#     with open(log_path, 'a', encoding='utf-8') as f:
#         f.write(f'{after.message.created_at},{after.message.edited_at},{after.message.channel.category},{after.message.channel.category.id},{after.message.channel},{after.message.channel.id},{after.message.author},{after.message.author.id},{after.message.id},{msg_cont}\n')

# @tree.command(name='ping',description='BotのPing値を表示します')
# async def ping(interaction: discord.Interaction):
#     # Ping値を秒単位で取得
#     raw_ping = bot.latency
# 
#     # ミリ秒に変換して丸める
#     ping = round(raw_ping * 1000)
# 
#     # 送信する
#     await interaction.response.send_message(f"@砂糖鯖bot のPing値は{ping}msです。")

# @tree.command(name='sato',description='otinpo') # テストに使ったコマンド (本人曰く残せとのこと)
# async def sato(interaction: discord.Interaction):
#     await interaction.response.send_message('おちんちんじゅぽじゅぽ\nおいしい！')

@tree.command(name='membercount',description='メンバーカウンターを更新します')
async def membercount(interaction: discord.Interaction):
    satou_server=client.get_guild(1196218959867949198)
    satou_role=discord.utils.get(satou_server.roles, id=1196260747165040832)
    active_satou_role=[member for member in satou_server.members if member.status != discord.Status.offline and satou_role in member.roles]
    membercount_channel=client.get_channel(1197130806603292742)
    active_membercount_channel=client.get_channel(1197140859116847135)
    await membercount_channel.edit(name=f'🧂｜メンバー➤ {len(satou_role.members)}')
    await active_membercount_channel.edit(name=f'🧂｜アクティブ➤ {len(active_satou_role)}')
    # ws.update_cell(1, 2, len(satou_role.members))
    # ws.update_cell(2, 2, len(active_satou_role))
    await interaction.response.send_message('カウンターを更新しました。',ephemeral=True)
    print(f'------------------------------\n  コマンドでの実行検知\n\033[34m{datetime.now()}\033[0m\nsatou_role: {len(satou_role.members)}\nactive_satou_role: {len(active_satou_role)}\n------------------------------')

@tasks.loop(minutes=30)
async def loop_membercount():
    satou_server=client.get_guild(1196218959867949198)
    satou_role=discord.utils.get(satou_server.roles, id=1196260747165040832)
    active_satou_role=[member for member in satou_server.members if member.status != discord.Status.offline and satou_role in member.roles]
    membercount_channel=client.get_channel(1197130806603292742)
    active_membercount_channel=client.get_channel(1197140859116847135)
    await membercount_channel.edit(name=f'🧂｜メンバー➤ {len(satou_role.members)}')
    await active_membercount_channel.edit(name=f'🧂｜アクティブ➤ {len(active_satou_role)}')
    # ws.update_cell(1, 2, len(satou_role.members))
    # ws.update_cell(2, 2, len(active_satou_role))
    print(f'------------------------------\n  タスクでの実行検知\n\033[32m{datetime.now()}\033[0m\nsatou_role: {len(satou_role.members)}\nactive_satou_role: {len(active_satou_role)}\n------------------------------')

@tree.command(name='boostlv',description='テスト')
async def test(interaction: discord.Interaction):
    guild=client.get_guild(1196218959867949198)
    boost_lv=guild.premium_tier
    # ws.update_cell(3, 2, boost_lv)
    await interaction.response.send_message('うぇい:v: ',ephemeral=True)

@tasks.loop(hours=24)
async def everyday_task():
    guild=client.get_guild(1196218959867949198)
    boost_lv=guild.premium_tier
    # ws.update_cell(3, 2, boost_lv)


client.run(TOKEN)
