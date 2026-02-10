from asyncio import gather

from disnake import ButtonStyle, MessageInteraction, PermissionOverwrite
from disnake.ui import Button, View, button

from src.utils import Ticket, log


class TicketViews(View):
    """Class ticket buttons."""

    def __init__(self) -> None:
        """Init buttons."""
        super().__init__(timeout=None)

    @button(label="Закрыть тикет", style=ButtonStyle.red, custom_id="close_ticket_id")
    async def close_ticket_btn(self, _: Button, inter: MessageInteraction) -> None:
        """Ticket close button."""
        await self.close_ticket(inter)

    @button(label="Удалить тикет", style=ButtonStyle.red, custom_id="delete_ticket_id", disabled=True)
    async def delete_ticket_btn(self, _: Button, inter: MessageInteraction) -> None:
        """Ticket delete button."""
        await self.delete_ticket(inter)


    async def close_ticket(self, inter: MessageInteraction) -> None:
        """Ticket close action."""
        await inter.response.defer(with_message=True, ephemeral=True)
        try:
            ticket_db = await Ticket.get_or_none(channel_id=inter.channel.id)
            if ticket_db is None:
                await inter.followup.send("Тикет не найден, можете удалить канал.", delete_after=5)
                return

            close_category = inter.guild.get_channel(ticket_db.category_id)
            ticket_author = inter.guild.get_member(ticket_db.discord_id)

            if ticket_author:
                await inter.channel.send(f"{ticket_author.mention} Ваш тикет закрыт, и данный канал более не актуален.")
                await inter.channel.edit(
                    category=close_category, overwrites={
                        ticket_author: PermissionOverwrite(view_channel=False),
                        inter.guild.default_role: PermissionOverwrite(view_channel=False),
                    },
                )

            self.delete_ticket_btn.disabled = False
            self.close_ticket_btn.disabled = True
            await gather(
                ticket_db.delete(),
                inter.message.edit(view=self),
                inter.followup.send("Ви успешно закрыли тикет", delete_after=5),
            )

        except Exception as e:
            await inter.followup.send("Ошибка при попытке закрыть тикет", delete_after=5)
            log.error("Возникла ошибка при попытке закрыть тикет", exc_info=e)

    async def delete_ticket(self, inter: MessageInteraction) -> None:
        """Ticket delete action."""
        await inter.response.defer(with_message=True, ephemeral=True)
        await inter.channel.delete()
