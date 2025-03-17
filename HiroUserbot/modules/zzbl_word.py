from HiroUserbot import *

@HIRO.MECHA()
async def _(c, m):
    print(m.text)
    await m.delete()