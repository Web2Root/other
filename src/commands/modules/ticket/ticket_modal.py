from asyncio import gather
from typing import Any

from disnake import Embed, ModalInteraction, TextChannel, TextInputStyle
from disnake.ui import Modal, TextInput

from src.commands.modules.ticket.ticket_views import TicketViews
from src.utils import Ticket, log, settings


class TicketModal(Modal):
    """Modal for ticket."""

    def __init__(self, ticket_config: dict[str, Any], select_label: str) -> None:
        """Initialize the modal."""
        self.create_category = ticket_config["create_category"]
        self.close_category = ticket_config["close_category"]
        self.allowed_roles = ticket_config["allowed_roles"]
        self.select_label = select_label

        components = [
            TextInput(
                label="Ваш игровой ник",
                custom_id="game_nick",
                max_length=50,
            ),
            TextInput(
                label="Ваш SteamID",
                custom_id="steam_id",
                min_length=17,
                max_length=20,
            ),
            TextInput(
                label="Опишите кратко проблему",
                custom_id="problem_desc",
                style=TextInputStyle.long,
                max_length=1024,
            ),
        ]
        super().__init__(
            title="Создать тикета",
            components=components,
            custom_id="create_ticket_modal",
        )

    async def callback(self, inter: ModalInteraction) -> None:
        """Modal dropdown callback."""
        await inter.response.defer(with_message=True, ephemeral=True)

        try:
            game_nick = inter.text_values["game_nick"]
            steam_id = inter.text_values["steam_id"]
            problem = inter.text_values["problem_desc"]

            ticket_channel = await self._create_channel(inter, game_nick)

            ticket_embed = Embed(title="Информация тикета", color=settings.color.green)
            ticket_embed.add_field(name="Причина", value=f"```{self.select_label}```", inline=False)
            ticket_embed.add_field(name="Игровой ник", value=f"```{game_nick}```", inline=False)
            ticket_embed.add_field(name="SteamID", value=f"```{steam_id}```", inline=False)
            ticket_embed.add_field(name="Описание проблемы", value=f"```{problem}```", inline=False)
            ticket_embed.add_field(name="Создатель", value=f"{inter.user.mention} ({inter.user.name})", inline=False)

            await Ticket.create(
                discord_id=inter.user.id,
                channel_id=ticket_channel.id,
                category_id=self.close_category,
            )
            await gather(
                self._add_permission(inter, ticket_channel),
                ticket_channel.send(content="@everyone", embed=ticket_embed, view=TicketViews()),
                inter.followup.send(f"Вы успешно создали тикет: {ticket_channel.mention}", delete_after=5),
            )

        except Exception as e:
            await inter.followup.send("Ошибка при попытке создать тикет", delete_after=5)
            log.error("Возникла ошибка при попытке создать тикет", exc_info=e)


    async def _create_channel(self, inter: ModalInteraction, game_nick: str) -> TextChannel:
        """Create ticket channel."""
        channel_name = f"{inter.created_at.strftime('%d-%m')}-{game_nick}"
        ticket_category = inter.guild.get_channel(self.create_category)
        return await inter.guild.create_text_channel(channel_name, category=ticket_category)

    async def _add_permission(self, inter: ModalInteraction, ticket_channel: TextChannel) -> None:
        """Add permission."""
        permissions = [(inter.user, True), (inter.guild.default_role, False)]
        permissions += [(inter.guild.get_role(role_id), True) for role_id in self.allowed_roles]
        for role, can_view in permissions:
            await ticket_channel.set_permissions(role, view_channel=can_view, read_messages=can_view)
