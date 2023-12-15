from dotenv import load_dotenv
load_dotenv()

import logging
logging.basicConfig(level=logging.INFO)

from pathlib import Path

from langchain_core.language_models import BaseLanguageModel
from langchain.chains.base import Chain
from langchain.chains import ConversationalRetrievalChain

from langsnapy import Project, Case
from langsnapy.langhcain import runner_from_chain

from cases import cases
from wiki_data import load_wiki_docs_faiss

prj = Project(
    snapshot_folder_path=Path(__file__).parent / "local-snapshots"
)

def create_qa_chain(
    llm: BaseLanguageModel
) -> Chain:
    wiki_docs_faiss = load_wiki_docs_faiss()
    retriever = wiki_docs_faiss.as_retriever(
        search_type="similarity", 
        search_kwargs={"k": 3}
    )

    return ConversationalRetrievalChain.from_llm(
        llm=llm,
        retriever=retriever,
        verbose=True,
    )


def run_bedrock():
    from langchain.llms.bedrock import Bedrock

    llm = Bedrock(
        model_id="anthropic.claude-v2:1", 
        model_kwargs={"temperature": 0}
    )

    chain = create_qa_chain(
        llm=llm
    )

    prj.run_cases(
        cases=cases,
        runner=runner_from_chain(chain),
        run_id="bedrock",
        meta={
            "llm_type": llm._llm_type,
            "model": llm.model_id,
            "model_args": llm.model_kwargs,
        }
    )

def run_openai():
    from langchain.chat_models import ChatOpenAI

    llm = ChatOpenAI(model_name="gpt-4")

    chain = create_qa_chain(
        llm=llm
    )

    prj.run_cases(
        cases=cases,
        runner=runner_from_chain(chain),
        run_id="openai",
        meta={
            "llm_type": llm._llm_type,
            "model": llm.model_name,
            "model_args": llm.model_kwargs,
        }
    )

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="OpenAI vs. Bedrock Battle!")
    
    parser.add_argument(
        "--participant",
        choices=["bedrock", "openai"],
        help="Which participant to run"
    )

    args = parser.parse_args()

    if args.participant == "bedrock":
        run_bedrock()
    elif args.participant == "openai":
        run_openai()
    else:
        parser.print_help()