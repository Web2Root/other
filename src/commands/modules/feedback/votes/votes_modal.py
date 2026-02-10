from asyncio import gather

from disnake import Embed, ModalInteraction, TextInputStyle
from disnake.ui import Modal, TextInput

from src.commands.modules.feedback.votes.votes_buttons import VotesButtons
from src.utils import Votes, log, settings


class VotesModal(Modal):
    """Class with modal for create votes."""

    def __init__(self, feedback_config: dict) -> None:
        """Init class with modal for create votes."""
        self.votes_channel = feedback_config["votes_channel"]
        components = [
            TextInput(
                label="Голосование",
                custom_id="votes_text",
                style=TextInputStyle.long,
                max_length=1000,
            ),
        ]
        super().__init__(title="Создать голосование", components=components, custom_id="votes_modal")

    async def callback(self, inter: ModalInteraction) -> None:
        """Modal for callback."""
        await inter.response.defer(with_message=True, ephemeral=True)

        try:
            modal_values = inter.text_values

            votes_embed = self._build_votes_embed(inter, modal_values["votes_text"])
            votes_channel = inter.guild.get_channel(self.votes_channel)
            votes_message = await votes_channel.send(content="@here", embed=votes_embed, view=VotesButtons())

            await gather(
                votes_message.create_thread(name="Обсудить ветке"),
                Votes.create(votes_id=votes_message.id),
                inter.followup.send(f"[**Голосование отправлено ↗**]({votes_message.jump_url})", delete_after=5),
            )

        except Exception as e:
            await inter.followup.send("Ошибка при создании голосования", delete_after=5)
            log.error("Возникла ошибка при созданий голосования", exc_info=e)


    @staticmethod
    def _build_votes_embed(inter: ModalInteraction, votes_text: str) -> Embed:
        """Build embed for votes."""
        embed = Embed(title="Новое голосование", color=settings.color.yellow, timestamp=inter.created_at)
        embed.add_field(name="Статус", value="**Активный**", inline=False)
        embed.add_field(name="Текст голосования", value=votes_text, inline=False)
        embed.add_field(name="Автор", value=f"{inter.user.mention} ({inter.user.name})", inline=False)
        embed.add_field(name="Статистика", value="За: `0%` | Против: `0%`", inline=False)
        return embed
