from typing import Any

from disnake import MessageInteraction, SelectOption
from disnake.ui import StringSelect

from src.commands.modules.ticket.ticket_modal import TicketModal


class TicketDrop(StringSelect):
    """Dropdown for ticket categories."""

    def __init__(self, ticket_config: dict[str, Any]) -> None:
        """Initialize the dropdown."""
        self.ticket_config = ticket_config
        options = [
            SelectOption(
                label=option["label"],
                description=option["desc"],
                emoji=option["emoji"],
                value=str(index),
            ) for index, option in enumerate(self.ticket_config["options"])
        ]
        super().__init__(placeholder="Выберите причину", options=options)

    async def callback(self, inter: MessageInteraction) -> None:
        """Select dropdown callback."""
        select_value = int(self.values[0])
        select_label = self.ticket_config["options"][select_value]["label"]

        await inter.response.send_modal(TicketModal(self.ticket_config, select_label))
        await inter.delete_original_response()
