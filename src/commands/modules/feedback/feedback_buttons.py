from disnake import ButtonStyle, MessageInteraction
from disnake.ui import Button, View, button

from src.commands.modules.feedback.offers.offers_modal import OffersModal
from src.commands.modules.feedback.reviews.reviews_modal import ReviewsModal
from src.commands.modules.feedback.votes.votes_modal import VotesModal
from src.utils import commons


class FeedbackButtons(View):
    """Class with buttons for feedback."""

    def __init__(self) -> None:
        """Init class with buttons for feedback."""
        super().__init__(timeout=None)
        self.feedback_config = commons.read_json("settings/config.json", "feedback")

    @button(label="Предложение", style=ButtonStyle.green, custom_id="create_offers_id")
    async def create_offers_btn(self, _: Button, inter: MessageInteraction) -> None:
        """Create offers."""
        await inter.response.send_modal(OffersModal(self.feedback_config))

    @button(label="Голосование", style=ButtonStyle.blurple, custom_id="create_vote_id")
    async def create_vote_btn(self, _: Button, inter: MessageInteraction) -> None:
        """Create votes."""
        await inter.response.send_modal(VotesModal(self.feedback_config))

    @button(label="ᅠОтзывᅠ", style=ButtonStyle.gray, custom_id="create_review_id")
    async def create_review_btn(self, _: Button, inter: MessageInteraction) -> None:
        """Create review."""
        await inter.response.send_modal(ReviewsModal(self.feedback_config))
