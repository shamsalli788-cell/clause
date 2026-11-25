from app.services.agent import ClauseAgent


def main() -> None:
    clause = ClauseAgent()
    try:
        while True:
            query = input("You: ").strip()
            if not query:
                continue
            if query.lower() in ["exit", "quit", "bye"]:
                break

            result = clause.ask(question=query)
            print(f"AI: {result}")
    except (KeyboardInterrupt, EOFError):
        pass
    finally:
        clause.close()


if __name__ == "__main__":
    main()

    # cd api
    # uv run python -m app.cli
