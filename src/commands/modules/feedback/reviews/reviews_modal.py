from disnake import Embed, ModalInteraction, TextInputStyle
from disnake.ui import Modal, TextInput

from src.utils import log, settings


class ReviewsModal(Modal):
    """Modal review."""

    def __init__(self, feedback_config: dict) -> None:
        """Init modal."""
        self.review_channel = feedback_config["review_channel"]
        components = [
            TextInput(label="Ваш отзыв", custom_id="review_text", style=TextInputStyle.long, max_length=1000),
            TextInput(label="Оценка (1-5)", custom_id="review_rating", max_length=1),
        ]
        super().__init__(title="Оставить отзыв", components=components, custom_id="reviews_modal")

    @staticmethod
    def get_star_rating(evaluation: int) -> str:
        """Get star rating."""
        return "⭐" * evaluation if evaluation < 5 else "⭐" * 5  # noqa: PLR2004

    async def callback(self, inter: ModalInteraction) -> None:
        """Handle modal callback."""
        await inter.response.defer(with_message=True, ephemeral=True)

        try:
            modal_values = inter.text_values

            if not modal_values["review_rating"].isdigit():
                await inter.followup.send("Оценка должна быть числом.", delete_after=5)
                return

            review_rating = self.get_star_rating(int(modal_values["review_rating"]))
            review_embed = self._build_reviews_embed(inter, modal_values["review_text"], review_rating)

            review_channel = inter.guild.get_channel(self.review_channel)
            review_message = await review_channel.send(embed=review_embed)
            await inter.followup.send(f"[**Отзыв отправлен ↗**]({review_message.jump_url})", delete_after=5)

        except Exception as e:
            await inter.followup.send("Ошибка при отправке отзыва", delete_after=5)
            log.error("Возникла ошибка при отправке отзыва", exc_info=e)


    @staticmethod
    def _build_reviews_embed(inter: ModalInteraction, text: str, rating: str) -> Embed:
        """Build reviews embed."""
        embed = Embed(title="Новый отзыв", color=settings.color.yellow, timestamp=inter.created_at)
        embed.add_field(name="Отзыв", value=text, inline=False)
        embed.add_field(name="Оценка", value=rating, inline=False)
        embed.add_field(name="Автор", value=f"{inter.user.mention} ({inter.user.name})", inline=False)
        return embed
