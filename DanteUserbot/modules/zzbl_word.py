from DanteUserbot import *

@DANTE.MECHA()
async def _(c, m):
    print(m.text)
    await m.delete()