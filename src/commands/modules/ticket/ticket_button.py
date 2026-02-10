from disnake import ButtonStyle, MessageInteraction
from disnake.ui import Button, View, button

from src.commands.modules.ticket.ticket_drop import TicketDrop
from src.utils import Ticket, commons, log


class TicketButton(View):
    """Class ticket button."""

    def __init__(self) -> None:
        """Initialize the ticket button."""
        super().__init__(timeout=None)

    @button(label="Создать тикет", style=ButtonStyle.green, custom_id="create_ticket_id")
    async def create_ticket_btn(self, _: Button, inter: MessageInteraction) -> None:
        """Create ticket."""
        await inter.response.defer(with_message=True, ephemeral=True)

        try:
            if await Ticket.exists(discord_id=inter.user.id):
                await inter.followup.send("У вас уже есть открытый тикет", delete_after=5)
                return

            ticket_config = commons.read_json("settings/config.json", "ticket")
            ticket_view = View(timeout=60)
            ticket_view.add_item(TicketDrop(ticket_config))

            await inter.followup.send(view=ticket_view)

        except Exception as e:
            await inter.followup.send("Ошибка при попытке открыть список", delete_after=5)
            log.error("Возникла ошибка при попытке открыть список", exc_info=e)
