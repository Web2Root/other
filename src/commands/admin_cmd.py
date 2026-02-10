from disnake import ApplicationCommandInteraction, Embed, TextChannel
from disnake.ext import commands
from disnake.ext.commands import Param

from src.commands.modules.common.say_modal import SayModal
from src.commands.modules.feedback.feedback_buttons import FeedbackButtons
from src.commands.modules.ticket.ticket_button import TicketButton
from src.utils import commons, log, settings


class AdminCmd(commands.Cog):
    """Class admin commands."""

    @commands.slash_command(name="админ", description="Команды админа")
    async def admin_cmd(self, _: ApplicationCommandInteraction) -> None:
        """Group admin commands."""

    @admin_cmd.sub_command("удалить-сообщение", "Удалить сообщение чата")
    async def delete_message_cmd(self, inter: ApplicationCommandInteraction,
        limit: int = Param(name="количество", desc="Количество сообщений"),
    ) -> None:
        """Delete messages in channel."""
        await inter.response.defer(ephemeral=True)
        await inter.channel.purge(limit=limit)
        await inter.delete_original_response()

    @admin_cmd.sub_command("сообщение-бота", "Отправить сообщение от имени бота")
    async def say_cmd(self, inter: ApplicationCommandInteraction,
        channel: TextChannel = Param(name="канал", desc="Выберите нужный вам канал"),
        mention: str = Param(name="упоминание", desc="Упоминание", choices=["@everyone", "@here"], default=None),
        image: str = Param(name="ссылка-на-изображение", desc="Ссылка на изображение", default=None),
    ) -> None:
        """Send message from bot."""
        await inter.response.send_modal(SayModal(channel, mention , image)) #,image

    @admin_cmd.sub_command("отправить-панель", "Отправить панель")
    async def panel_cmd(self, inter: ApplicationCommandInteraction,
       module: str = Param(name="модуль", desc="Выберите модуль", choices=settings.bot.panel_cmd),
    ) -> None:
        """Send panel module."""
        await inter.response.defer(with_message=True, ephemeral=True)
        try:
            embed_config = commons.read_json("settings/embeds.json", module)
            embed_color = int(embed_config["color"], 16)

            panel_embed = Embed(title=embed_config["title"], description=embed_config["desc"], color=embed_color)
            panel_embed.set_image(embed_config["image"])

            if module == "ticket":
                panel_view = TicketButton()
            elif module == "feedback":
                panel_view = FeedbackButtons()

            await inter.channel.send(embed=panel_embed, view=panel_view)
            await inter.delete_original_response()

        except Exception as e:
            await inter.followup.send("Ошибка при отправке панели", delete_after=5)
            log.error("Возникла ошибка при попытке отправить панель", exc_info=e)

def setup(bot: commands.Bot) -> None:
    """Load the AdminCmd cog into the bot."""
    bot.add_cog(AdminCmd())
