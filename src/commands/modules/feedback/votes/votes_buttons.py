from disnake import ButtonStyle, Message, MessageInteraction
from disnake.ui import Button, View, button

from src.utils import Votes, settings


class VotesButtons(View):
    """Class for votes buttons."""

    def __init__(self) -> None:
        """Initialize votes buttons."""
        super().__init__(timeout=None)

    @button(label="0", emoji=settings.emoji.like, style=ButtonStyle.green, custom_id="votes_like_id")
    async def votes_like_btn(self, _: Button, inter: MessageInteraction) -> None:
        """Button like."""
        await self.votes_handle(inter, is_like=True)

    @button(label="0", emoji=settings.emoji.dislike, style=ButtonStyle.red, custom_id="votes_dislike_id")
    async def votes_dislike_btn(self, _: Button, inter: MessageInteraction) -> None:
        """Button Dislike."""
        await self.votes_handle(inter, is_like=False)


    async def votes_handle(self, inter: MessageInteraction, is_like: bool) -> None:
        """Handle votes button."""
        await inter.response.defer()

        votes_db = await Votes.get_or_none(votes_id=inter.message.id)
        user_id = inter.user.id

        if not votes_db:
            await inter.followup.send("Голосование не найдено", delete_after=5)
            return

        if is_like:
            if user_id in votes_db.dislikes:
                votes_db.dislikes.remove(user_id)
            if user_id not in votes_db.likes:
                votes_db.likes.append(user_id)
        else:
            if user_id in votes_db.likes:
                votes_db.likes.remove(user_id)
            if user_id not in votes_db.dislikes:
                votes_db.dislikes.append(user_id)

        await votes_db.save()
        await self._update_message(inter.message, len(votes_db.likes), len(votes_db.dislikes))

    async def _update_message(self, message: Message, like_count: int, dislike_count: int) -> None:
        """Update message with votes."""
        total_count = like_count + dislike_count
        like_percent = like_count / total_count * 100 if total_count > 0 else 0
        dislike_percent = dislike_count / total_count * 100 if total_count > 0 else 0
        embed_stats = f"За: `{like_percent:.0f}%` | Против: `{dislike_percent:.0f}%`"

        self.children[0].label = like_count
        self.children[1].label = dislike_count
        votes_embed = message.embeds[0]
        votes_embed.set_field_at(3, name="Статистика", value=embed_stats, inline=False)

        await message.edit(embed=votes_embed, view=self)
