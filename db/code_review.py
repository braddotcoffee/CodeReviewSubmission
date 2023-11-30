from db import Base, DB
from sqlalchemy import (
    BigInteger,
    SmallInteger,
    Boolean,
    Column,
    DateTime,
    Enum,
    ForeignKey,
    Integer,
    VARCHAR,
    func,
    insert
)
from models.code_review import CodeReview as CodeReviewModel, CodeReviewType

class CodeReview(Base):
    __tablename__ = "code_reviews"

    id = Column(Integer, primary_key=True)
    guild_id = Column(BigInteger, nullable=False)
    message_id = Column(BigInteger, nullable=False, unique=True)
    user_id = Column(BigInteger, nullable=False, )
    description = Column(VARCHAR(1000), nullable=False)
    review_type = Column(Enum(CodeReviewType), nullable=False)
    url = Column(VARCHAR(200), nullable=False)

    def __repr__(self):
        return (
            f"CodeReview(id={self.id!r}, url={self.url!r}, guild_id={self.guild_id!r},"
            f" user_id={self.user_id!r}, review_type={self.review_type!r})"
        )

class CodeReviewDB:
    def __init__(self, db: DB):
        self.db = db

    def new_code_review(self, code_review: CodeReviewModel):
        with self.db.get_session() as sess:
            sess.execute(insert(CodeReview).values(
                guild_id=code_review.guild_id,
                message_id=code_review.message_id,
                user_id=code_review.user_id,
                description=code_review.description,
                review_type=code_review.review_type,
                url=code_review.url,
            ))
