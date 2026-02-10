"""Модуль для создание предложение."""
from disnake import Embed, ModalInteraction, TextInputStyle
from disnake.ui import Modal, TextInput

from src.commands.modules.feedback.offers.offers_buttons import OffersButtons
from src.utils import log, settings


class OffersModal(Modal):
    """Modal for offers."""

    def __init__(self, feedback_config: dict) -> None:
        """Init modal."""
        self.offers_channel = feedback_config["offers_channel"]
        components = [
            TextInput(
                label="Ваше предложение",
                custom_id="offers_text",
                style=TextInputStyle.long,
                max_length=1000,
            ),
        ]
        super().__init__(title="Создать предложение", components=components, custom_id="offers_modal")

    async def callback(self, inter: ModalInteraction) -> None:
        """Modal from callback."""
        await inter.response.defer(with_message=True, ephemeral=True)

        try:
            modal_values = inter.text_values

            offers_embed = self._build_offers_embed(inter, modal_values["offers_text"])
            offers_channel = inter.guild.get_channel(self.offers_channel)
            offers_message = await offers_channel.send(embed=offers_embed, view=OffersButtons())

            await offers_message.create_thread(name="Обсудить ветке")
            await inter.followup.send(f"[**Предложение отправлено↗**]({offers_message.jump_url})", delete_after=5)

        except Exception as e:
            await inter.followup.send("Ошибка при создании предложений", delete_after=5)
            log.error("Возникла ошибка при созданий предложений", exc_info=e)


    @staticmethod
    def _build_offers_embed(inter: ModalInteraction, offers_text: str) -> Embed:
        """Build embed for offers."""
        embed = Embed(title="Новое предложение",  timestamp=inter.created_at, color=settings.color.yellow)
        embed.add_field(name="Статус", value="В ожидании", inline=False)
        embed.add_field(name="Предложение", value=offers_text, inline=False)
        embed.add_field(name="Автор", value=f"{inter.user.mention} ({inter.user.name})", inline=False)
        return embed
