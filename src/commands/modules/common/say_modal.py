from disnake import Embed, ModalInteraction, TextChannel, TextInputStyle
from disnake.ui import Modal, TextInput

from src.utils import log


class SayModal(Modal):
    """Modal for ticket."""

    def __init__(self, channel: TextChannel, mention: str, image_url: str) -> None:
        """Initialize the modal."""
        self.channel = channel
        self.mention = mention
        self.image_url = image_url

        components = [
            TextInput(
                label="Заголовок",
                custom_id="title",
                max_length=256,
            ),
            TextInput(
                label="Описание",
                custom_id="desc",
                max_length=4000,
                style=TextInputStyle.long,
            ),
            TextInput(
                label="Цвет HEX (Без #)",
                custom_id="color",
                max_length=6,
            ),
        ]
        super().__init__(
            title="Сообщение от бота",
            components=components,
            custom_id="bot_message_modal",
        )

    async def callback(self, inter: ModalInteraction) -> None:
        """Modal dropdown callback."""
        await inter.response.defer(with_message=True, ephemeral=True)

        try:
            title = inter.text_values["title"]
            desc = inter.text_values["desc"]
            color = int(inter.text_values["color"], 16)

            message_embed = Embed(title=title, description=desc,color=color)
            message_embed.set_image(self.image_url)

            sending_message = await self.channel.send(self.mention, embed=message_embed)
            await inter.followup.send(f"[**Сообщение отправлено ↗**]({sending_message.jump_url})", delete_after=5)

        except ValueError:
            await inter.followup.send("Неверный формат цвета", delete_after=5)
        except Exception as e:
            await inter.followup.send("Ошибка при отправке сообщения", delete_after=5)
            log.error("Возникла ошибка при отправке сообщения", exc_info=e)
