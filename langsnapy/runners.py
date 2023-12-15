def from_langchain_chain(chain):

    if isinstance(case.inquery, str):
        return CaseRunResult.from_any(model.generate_answer(case.inquery))

    if isinstance(case.inquery, list):
        from langchain_core.messages import AIMessage, HumanMessage

        history = []

        for q in case.inquery:
            a = chain(
                {
                    "question": q,
                    "chat_history": history or None,
                }
            )

            history.append(HumanMessage(content=q))
            history.append(AIMessage(content=a))

        return CaseRunResult.from_any(a)

    raise ValueError(f"Unexpected case.inquery type: {type(case.inquery)}")