from disnake import ButtonStyle, Message, MessageInteraction, User
from disnake.ui import Button, View, button

from src.utils import commons, log, settings


class OffersButtons(View):
    """Class with buttons for offers."""

    def __init__(self) -> None:
        """Init class with buttons for offers."""
        super().__init__(timeout=None)

    @button(label="Одобрить", style=ButtonStyle.green, custom_id="offers_approve_id")
    async def offers_approve_btn(self, _: Button, inter: MessageInteraction) -> None:
        """Button approve offer."""
        await self.offers_solution(inter, is_approve=True)

    @button(label="Отклонить", style=ButtonStyle.red, custom_id="offers_decline_id")
    async def offers_decline_btn(self, _: Button, inter: MessageInteraction) -> None:
        """Button decline offer."""
        await self.offers_solution(inter, is_approve=False)


    async def offers_solution(self, inter: MessageInteraction, is_approve: bool) -> None:
        """Обработать предложение."""
        await inter.response.defer(with_message=True, ephemeral=True)

        try:
            allowed_roles = commons.read_json("settings/config.json", "feedback", "allowed_roles")

            if not self.check_permission(inter.user, allowed_roles):
                await inter.followup.send("У вас нет прав для этого действия.", delete_after=5)
                return

            if is_approve:
                await self._update_status(inter.message, "Одобрено", settings.color.green)
            else:
                await self._update_status(inter.message, "Отклонено", settings.color.red)

            await inter.followup.send("Предложение обработано", delete_after=5)

        except Exception as e:
            await inter.followup.send("Ошибка при попытке одобрить или отклонить предложение", delete_after=5)
            log.error("Возникла ошибка при попытке одобрить или отклонить предложение", exc_info=e)


    @staticmethod
    async def _update_status(message: Message, value: str, color: int) -> None:
        """Update status offer."""
        offers_embed = message.embeds[0]
        offers_embed.set_field_at(0, name="Статус", value=value, inline=False)
        offers_embed.color = color
        await message.edit(embed=offers_embed, view=None)

    @staticmethod
    def check_permission(user: User, role_ids: list[int]) -> bool:
        """Check permission user."""
        return any(role.id in role_ids for role in user.roles)
