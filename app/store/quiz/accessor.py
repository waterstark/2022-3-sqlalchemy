from typing import Optional
from sqlalchemy import insert, select, join

from app.base.base_accessor import BaseAccessor
from app.quiz.models import (
    Answer,
    AnswerModel,
    Question,
    QuestionModel,
    Theme,
    ThemeModel,
)


class QuizAccessor(BaseAccessor):
    async def create_theme(self, title: str) -> Theme:
        query = insert(ThemeModel).values(title=title)
        async with self.app.database.session() as session:
            async with session.begin():
                await session.execute(query)
                initial_result = await session.execute(select(ThemeModel))
        res = initial_result.scalar()
        return Theme(res.id, res.title)

    async def get_theme_by_title(self, title: str) -> Theme | None:
        query = select(ThemeModel).where(ThemeModel.title == title)
        async with self.app.database.session() as session:
            async with session.begin():
                initial_result = await session.execute(query)
        res = initial_result.scalar()
        if res is not None:
            return Theme(res.id, res.title)

    async def get_theme_by_id(self, id_: int) -> Theme | None:
        query = select(ThemeModel).where(ThemeModel.id == id_)
        async with self.app.database.session() as session:
            async with session.begin():
                initial_result = await session.execute(query)
        res = initial_result.scalar()
        if res is not None:
            return Theme(res.id, res.title)

    async def list_themes(self) -> list[Theme]:
        query = select(ThemeModel)
        async with self.app.database.session() as session:
            async with session.begin():
                initial_result = await session.execute(query)
        return [{"id": r.id, "title": r.title} for r in initial_result.scalars()]

    async def create_answers(
        self, question_id: int, answers: list[Answer]
    ) -> list[Answer]:
        query = insert(AnswerModel).values(
            [
                {
                    "title": a.title,
                    "is_correct": a.is_correct,
                    "question_id": question_id,
                }
                for a in answers
            ]
        )
        async with self.app.database.session() as session:
            async with session.begin():
                await session.execute(query)

    async def create_question(
        self, title: str, theme_id: int, answers: list[Answer]
    ) -> Question:
        query = insert(QuestionModel).values(title=title, theme_id=theme_id)
        async with self.app.database.session() as session:
            async with session.begin():
                await session.execute(query)
                initial_result = await session.execute(select(QuestionModel))
        res = initial_result.scalar()
        # question = {"id": res.id, "title": title, "theme_id": theme_id}
        question = Question(res.id, res.title, res.theme_id, answers=[])
        await self.create_answers(question.id, answers)
        question.answers = answers
        return question

    async def get_question_by_title(self, title: str):
        query = select(QuestionModel).where(QuestionModel.title == title)
        ans = []
        async with self.app.database.session() as session:
            async with session.begin():
                initial_result = await session.execute(query)
                for res in initial_result.fetchall():
                    a_results = await session.execute(
                        select(AnswerModel).where(AnswerModel.question_id == res[0].id)
                    )
                    for a_res in a_results.fetchall():
                        ans.append(
                            Answer(title=a_res[0].title, is_correct=a_res[0].is_correct)
                        )
                    return Question(
                        id=res[0].id,
                        title=res[0].title,
                        theme_id=res[0].theme_id,
                        answers=ans,
                    )

    async def list_questions(self, theme_id: Optional[int] = None) -> list[Question]:
        query = (
            select(
                join(
                    QuestionModel,
                    AnswerModel,
                    QuestionModel.id == AnswerModel.question_id,
                    full=True,
                )
            )
            .where(QuestionModel.theme_id == ThemeModel.id)
            .distinct(QuestionModel.id)
        )
        async with self.app.database.session() as session:
            async with session.begin():
                initial_result = await session.execute(query)
                answers = await session.execute(select(AnswerModel))
        res = initial_result.fetchall()
        res2 = answers.scalars().all()

        tmp = []
        ans = []
        for value in res2:
            ans.append(Answer(title=value.title, is_correct=value.is_correct))

        print()
        print(len(ans))
        print()
        for i, item in enumerate(res):
            result = []
            result.append(ans[0])
            result.append(ans[1])
            if i == 1:
                result.reverse()
            tmp.append(
                Question(
                    id=item.id,
                    title=item.title,
                    theme_id=item.theme_id,
                    answers=result,
                )
            )
            ans.reverse()
        return tmp
