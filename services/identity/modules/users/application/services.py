class UserService:
    def __init__(self, register_user_interactor, update_user_interactor):
        self.register_user_interactor = register_user_interactor
        self.update_user_interactor = update_user_interactor

    async def register_user(self, dto):
        return await self.register_user_interactor.execute(dto)

    async def update_user(self, dto, user_id):
        return await self.update_user_interactor.execute(dto, user_id)
