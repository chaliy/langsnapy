import logging
from typing import Type, Callable

from langsnapy import Case, CaseRunResult

logger = logging.getLogger(__name__)

try:
    from langchain.chains.base import Chain
except ImportError:
    logger.error("Langchain is not installed. Please install it with `pip install langchain`")
    Chain = Type[any]
    
def runner_from_chain(chain: Chain) -> Callable[[Case], CaseRunResult]:

    def _invoke(q: str, history: list) -> str:
        return chain(
            {
                "question": q,
                "chat_history": history,
            }
        )["answer"]

    def runner(case: Case) -> CaseRunResult:
        if isinstance(case.inquiry, str):
            return CaseRunResult.from_any(_invoke(case.inquiry, []))

        if isinstance(case.inquiry, list):
            from langchain_core.messages import AIMessage, HumanMessage

            history = []

            for q in case.inquiry:
                a = _invoke(q, history)

                history.append(HumanMessage(content=q))
                history.append(AIMessage(content=a))

            return CaseRunResult.from_any(a)

        raise ValueError(f"Unexpected case.inquiry type: {type(case.inquiry)}")

    return runner