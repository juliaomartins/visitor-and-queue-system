"""Test-only builders. Production code never imports this module."""

import secrets

from django.contrib.auth import get_user_model
from langchain_core.language_models.fake_chat_models import GenericFakeChatModel

from apps.visitors.models import Visitor


def make_admin(username: str = "admin"):
    return get_user_model().objects.create_user(username, password="x", is_staff=True)


def make_visitor(full_name: str, country: str = "Timor-Leste", **extra) -> Visitor:
    return Visitor.objects.create(
        full_name=full_name,
        country=country,
        photo="visitors/x.jpg",
        badge_serial=secrets.token_hex(4).upper(),
        token_hash=secrets.token_hex(32),
        **extra,
    )


class FakeToolModel(GenericFakeChatModel):
    """A scripted chat model that accepts tools, so `create_agent` can bind it.

    `seen` records the messages of every call, which is how a test asserts on
    what the model was actually sent (system prompt, history) rather than on
    what the code meant to send.
    """

    seen: list = []

    def bind_tools(self, tools, **kwargs):
        return self

    def _generate(self, messages, stop=None, run_manager=None, **kwargs):
        self.seen.append(list(messages))
        return super()._generate(messages, stop=stop, run_manager=run_manager, **kwargs)


def fake_model(*replies) -> FakeToolModel:
    model = FakeToolModel(messages=iter(replies))
    model.seen = []
    return model
