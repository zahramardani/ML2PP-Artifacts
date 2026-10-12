import os


def explain_with_llm(payload: dict) -> str:
    """Use LangChain/OpenAI when configured; otherwise return a local explanation."""
    api_key = os.getenv("OPENAI_API_KEY")
    if api_key:
        try:
            from langchain_core.prompts import ChatPromptTemplate
            from langchain_openai import ChatOpenAI

            prompt = ChatPromptTemplate.from_messages([
                ("system", "You explain machine-health anomaly predictions concisely and cautiously."),
                ("human", "Explain this result and suggest one engineering follow-up: {payload}"),
            ])
            chain = prompt | ChatOpenAI(model=os.getenv("OPENAI_MODEL", "gpt-4.1-mini"), temperature=0)
            return chain.invoke({"payload": payload}).content
        except Exception as exc:
            return f"LLM explanation unavailable ({type(exc).__name__}); local explanation: " + _local_explanation(payload)
    return _local_explanation(payload)


def _local_explanation(payload: dict) -> str:
    reading = payload["reading"]
    pred = payload["prediction"]
    return (
        f"Risk is {pred['risk_level']} with anomaly score {pred['anomaly_score']}. "
        f"Observed temperature={reading['temperature']}, vibration={reading['vibration']}, load={reading['load']}. "
        "Review recent sensor history and equipment operating limits before taking action."
    )
