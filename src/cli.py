"""Command line interface for the AI agent."""

import argparse
import sys
import traceback
from typing import NoReturn

from IPython.display import Image, display

from graph.workflow import create_workflow, run_workflow


def visualize_graph() -> None:
    """Visualize the workflow graph."""
    try:
        workflow = create_workflow()
        graph_png = workflow["graph"].get_graph().draw_mermaid_png()

        # Save the image locally
        output_path = "workflow_graph.png"
        with open(output_path, "wb") as f:
            f.write(graph_png)
        print(f"Graph visualization saved to: {output_path}")

        # Also display it if in an interactive environment
        display(Image(graph_png))
    except Exception as e:
        print(f"Error: {e}")
        traceback.print_exc()
        pass


def run_interactive() -> None:
    """Run the agent in interactive mode."""
    print("Starting interactive mode. Type 'quit', 'exit', or 'q' to end the session.")
    while True:
        try:
            user_input = input("User: ")
            if user_input.lower() in ["quit", "exit", "q"]:
                print("Goodbye!")
                break

            response = run_workflow(user_input)
            print(f"Assistant: {response['response']}")
        except Exception as e:
            print(f"Error: {e}")
            traceback.print_exc()
            break


def main() -> NoReturn:
    """Run the CLI."""
    parser = argparse.ArgumentParser(description="AI Agent CLI")
    subparsers = parser.add_subparsers(dest="command", help="Command to run")

    # Query command
    query_parser = subparsers.add_parser("query", help="Run a query")
    query_parser.add_argument("-q", "--query", required=True, help="Query to run")

    # Visualize command
    subparsers.add_parser("visualize", help="Visualize the workflow graph")

    # Run command
    subparsers.add_parser("run", help="Run the agent in interactive mode")

    # Add documents command
    add_docs_parser = subparsers.add_parser("add-docs", help="Add documents to the vector store")
    add_docs_parser.add_argument("-p", "--path", required=True, help="Path to the folder containing documents")

    args = parser.parse_args()

    if args.command == "query":
        response = run_workflow(args.query)
        print(response)
        sys.exit(0)
    elif args.command == "visualize":
        visualize_graph()
        sys.exit(0)
    elif args.command == "run":
        run_interactive()
        sys.exit(0)
    elif args.command == "add-docs":
        from tools.vectorstore import VectorStore
        vectorstore = VectorStore()
        result = vectorstore.add_documents_from_folder(args.path)
        print(result)
        sys.exit(0)
    else:
        parser.print_help()
        sys.exit(1)


if __name__ == "__main__":
    main()
