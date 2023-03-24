class Dbf:
    def __init__(self, db):
        self.db = db

    async def get_chat_list(self):
        return (eval((await self.db.get("CHAT_LIST")) or "{}"))


    async def set_chat_list(self, chat, time):
        chats = await self.get_chat_list()
        if chat not in chats:
            chats.update({chat: time})
            await self.db.set("CHAT_LIST", str(chats))
            return True
        return False

    async def rem_chat_list(self, chat):
        chats = await self.get_chat_list()
        if chat in chats:
            chats.pop(chat)
            await self.db.set("CHAT_LIST", str(chats))
            return True
        return False
