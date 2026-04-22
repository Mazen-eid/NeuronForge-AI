from __future__ import annotations

import pytest

from neuronforge.config import ChannelConfig
from neuronforge.llm import MockClient
from neuronforge.script import generate_script


@pytest.mark.asyncio
async def test_generate_script_with_mock():
    ch = ChannelConfig(id="t", language="en", niche="tech", tone="curious")
    llm = MockClient()
    plan = await generate_script(llm, ch, topic="LLM releases")
    assert plan.title
    assert plan.narration
    assert plan.captions
    assert isinstance(plan.hashtags, list)
    assert plan.full_narration.startswith(plan.hook)
