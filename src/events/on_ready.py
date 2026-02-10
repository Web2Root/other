from disnake.ext import commands

from src.commands.modules.feedback.feedback_buttons import FeedbackButtons
from src.commands.modules.feedback.offers.offers_buttons import OffersButtons
from src.commands.modules.feedback.votes.votes_buttons import VotesButtons
from src.commands.modules.ticket.ticket_button import TicketButton
from src.commands.modules.ticket.ticket_views import TicketViews
from src.utils import log


class OnReady(commands.Cog):
    """Handle the bot's on_ready event."""

    def __init__(self, bot: commands.Bot) -> None:
        """Initialize the OnReady cog with the bot instance."""
        self.bot = bot

    def _add_views(self) -> None:
        """Register button views for the bot."""
        buttons = [
            TicketButton,
            TicketViews,
            FeedbackButtons,
            OffersButtons,
            VotesButtons,
        ]
        for button in buttons:
            self.bot.add_view(button())

    async def on_ready(self) -> None:
        """Execute when the bot is ready and connected."""
        self._add_views()
        log.info("%s connected", self.bot.user.display_name)

def setup(bot: commands.Bot) -> None:
    """Load the OnReady cog into the bot."""
    bot.add_cog(OnReady(bot))
