from dataclasses import dataclass
from enum import Enum
from typing import Optional


class CodeReviewType(Enum):
    general = "general"
    specific_question = "specific_question"
    bug = "bug"


@dataclass
class CodeReviewURL:
    url: str
    owner: str
    repo: str
    branch: Optional[str]


@dataclass
class CodeReview:
    guild_id: int
    message_id: Optional[int]
    user_id: int
    description: str
    url: str
    review_type: CodeReviewType
