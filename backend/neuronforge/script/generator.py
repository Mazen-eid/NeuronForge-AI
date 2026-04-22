from __future__ import annotations

import json
import re
from dataclasses import dataclass, field

from ..config import ChannelConfig
from ..llm import LLMClient

LANG_INSTRUCTIONS = {
    "en": "Write in natural, modern English.",
    "ar": "اكتب بعربية فصحى واضحة وسهلة، بدون ترجمة حرفية.",
    "fr": "Écrivez dans un français naturel et moderne.",
    "es": "Escribe en español natural y moderno.",
}


def build_system_prompt(channel: ChannelConfig) -> str:
    return f"""You are a short-form video scriptwriter for a {channel.platform} channel.
Niche: {channel.niche}. Tone: {channel.tone}.
{LANG_INSTRUCTIONS.get(channel.language, '')}
{channel.system_prompt_extra}

Output MUST be valid JSON with these exact keys:
- title (string, under 80 chars, click-worthy but not clickbait)
- description (string, 1-3 sentences, include a call to subscribe)
- hashtags (list of 5-10 short hashtag strings, each starting with #)
- hook (string, a one-sentence attention-grabber for the first 2 seconds)
- narration (string, the full spoken script; target ~{channel.target_duration_seconds} seconds
  when read at a moderate pace; ~150 words per minute)
- captions (list of short strings, each 3-8 words, used as on-screen captions)

Do not include any text outside the JSON object."""


def build_user_prompt(topic: str, channel: ChannelConfig) -> str:
    return (
        f"Topic: {topic}\n"
        f"Duration target: {channel.target_duration_seconds} seconds.\n"
        f"Language: {channel.language}.\n"
        f"Return JSON only."
    )


@dataclass
class ScriptPlan:
    title: str
    description: str
    hashtags: list[str] = field(default_factory=list)
    hook: str = ""
    narration: str = ""
    captions: list[str] = field(default_factory=list)

    @property
    def full_narration(self) -> str:
        return (self.hook + " " if self.hook else "") + self.narration

    def to_dict(self) -> dict:
        return {
            "title": self.title,
            "description": self.description,
            "hashtags": self.hashtags,
            "hook": self.hook,
            "narration": self.narration,
            "captions": self.captions,
        }


_JSON_BLOCK_RE = re.compile(r"\{.*\}", re.DOTALL)


def _extract_json(raw: str) -> dict:
    raw = raw.strip()
    # Strip markdown fences if present
    if raw.startswith("```"):
        raw = re.sub(r"^```(?:json)?\s*", "", raw)
        raw = re.sub(r"\s*```$", "", raw)
    try:
        return json.loads(raw)
    except json.JSONDecodeError:
        match = _JSON_BLOCK_RE.search(raw)
        if match:
            return json.loads(match.group(0))
        raise


async def generate_script(llm: LLMClient, channel: ChannelConfig, topic: str) -> ScriptPlan:
    system = build_system_prompt(channel)
    user = build_user_prompt(topic, channel)
    raw = await llm.complete(system=system, user=user, temperature=0.8, max_tokens=1500)
    data = _extract_json(raw)
    return ScriptPlan(
        title=str(data.get("title", topic))[:95],
        description=str(data.get("description", "")),
        hashtags=[str(h) for h in data.get("hashtags", [])],
        hook=str(data.get("hook", "")),
        narration=str(data.get("narration", "")),
        captions=[str(c) for c in data.get("captions", [])],
    )
