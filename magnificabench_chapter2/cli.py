from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

from .data import (
    ROOT,
    load_items,
    load_items_by_id,
    read_predictions,
    validate_artifacts,
    write_jsonl,
)
from .judge import llm_judge_score
from .llm_clients import ChatClient, LLMClientError
from .scoring import aggregate_scores, heuristic_score, selected_dimensions, to_json


ANSWER_SYSTEM_PROMPT = """You are answering MagnificaBench Chapter 2 items.
Give a concise source-grounded answer. Reason from Chapter 2 principles such as dignity, rights, common good, digital goods, subsidiarity, solidarity, social justice, and integral human development.
Do not claim access to the source text beyond the paragraph references supplied in the item."""


def add_common_item_filters(parser: argparse.ArgumentParser) -> None:
    parser.add_argument("--limit", type=int, default=None, help="Evaluate only the first N selected items.")
    parser.add_argument("--ids", default="", help="Comma-separated item IDs to include.")


def filter_items(items: list[dict[str, Any]], ids: str = "", limit: int | None = None) -> list[dict[str, Any]]:
    if ids:
        wanted = {value.strip() for value in ids.split(",") if value.strip()}
        items = [item for item in items if item["id"] in wanted]
    if limit is not None:
        items = items[:limit]
    return items


def command_validate(_: argparse.Namespace) -> int:
    errors = validate_artifacts()
    if errors:
        for error in errors:
            print(f"FAIL: {error}", file=sys.stderr)
        return 1
    print("OK: runnable benchmark artifacts validate")
    print(f"OK: repo root {ROOT}")
    return 0


def command_export_prompts(args: argparse.Namespace) -> int:
    items = filter_items(load_items(), args.ids, args.limit)
    rows = []
    for item in items:
        rows.append(
            {
                "id": item["id"],
                "category": item["category"],
                "difficulty": item["difficulty"],
                "source_paragraphs": item["source_paragraphs"],
                "principles": item["principles"],
                "prompt": item["prompt"],
                "model_instruction": ANSWER_SYSTEM_PROMPT,
            }
        )
    write_jsonl(Path(args.out), rows)
    print(f"Wrote {len(rows)} prompt rows to {args.out}")
    return 0


def build_answer_prompt(item: dict[str, Any]) -> str:
    return (
        f"Item ID: {item['id']}\n"
        f"Category: {item['category']}\n"
        f"Difficulty: {item['difficulty']}\n"
        f"Source paragraphs: {item['source_paragraphs']}\n"
        f"Principles: {item['principles']}\n\n"
        f"Prompt:\n{item['prompt']}\n\n"
        "Answer in 1-2 paragraphs. Include concrete governance implications when relevant."
    )


def command_answer(args: argparse.Namespace) -> int:
    items = filter_items(load_items(), args.ids, args.limit)
    if args.provider != "demo" and not args.model:
        print("--model is required for live providers", file=sys.stderr)
        return 1
    client = ChatClient(
        provider=args.provider,
        model=args.model or "demo-model",
        temperature=args.temperature,
        max_tokens=args.max_tokens,
    )
    rows = []
    for item in items:
        answer = client.generate(ANSWER_SYSTEM_PROMPT, build_answer_prompt(item))
        rows.append(
            {
                "id": item["id"],
                "model": args.model or "demo-model",
                "answer_provider": args.provider,
                "answer": answer,
            }
        )
    write_jsonl(Path(args.out), rows)
    print(f"Wrote {len(rows)} prediction rows to {args.out}")
    return 0


def score_predictions(args: argparse.Namespace) -> tuple[list[dict[str, Any]], dict[str, Any]]:
    items_by_id = load_items_by_id()
    predictions = read_predictions(Path(args.predictions))
    if args.limit is not None:
        predictions = predictions[: args.limit]
    client = None
    if args.judge == "llm":
        if not args.judge_provider or not args.judge_model:
            raise LLMClientError("--judge llm requires --judge-provider and --judge-model")
        client = ChatClient(
            provider=args.judge_provider,
            model=args.judge_model,
            temperature=args.temperature,
            max_tokens=args.max_tokens,
        )
    rows = []
    for prediction in predictions:
        item = items_by_id.get(prediction["id"])
        if item is None:
            raise ValueError(f"prediction references unknown item id: {prediction['id']}")
        dimensions = selected_dimensions(item, args.dimensions)
        if args.judge == "heuristic":
            result = heuristic_score(item, prediction["answer"], dimensions)
        else:
            assert client is not None
            result = llm_judge_score(item, prediction["answer"], client, dimensions)
        result.update(
            {
                "category": item["category"],
                "difficulty": item["difficulty"],
                "principles": item["principles"],
                "source_paragraphs": item["source_paragraphs"],
                "model": prediction.get("model", "unknown"),
                "answer_provider": prediction.get("answer_provider", "unknown"),
            }
        )
        rows.append(result)
    return rows, aggregate_scores(rows)


def command_score(args: argparse.Namespace) -> int:
    rows, summary = score_predictions(args)
    write_jsonl(Path(args.out), rows)
    if args.summary:
        Path(args.summary).parent.mkdir(parents=True, exist_ok=True)
        Path(args.summary).write_text(to_json(summary) + "\n", encoding="utf-8")
    print(f"Wrote {len(rows)} score rows to {args.out}")
    if args.summary:
        print(f"Wrote summary to {args.summary}")
    print(to_json(summary))
    return 0


def command_run(args: argparse.Namespace) -> int:
    out_dir = Path(args.out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    predictions = out_dir / "predictions.jsonl"
    scores = out_dir / "scores.jsonl"
    summary = out_dir / "summary.json"

    answer_args = argparse.Namespace(
        provider=args.answer_provider,
        model=args.answer_model,
        out=str(predictions),
        ids=args.ids,
        limit=args.limit,
        temperature=args.temperature,
        max_tokens=args.max_tokens,
    )
    command_answer(answer_args)
    score_args = argparse.Namespace(
        predictions=str(predictions),
        out=str(scores),
        summary=str(summary),
        judge=args.judge,
        judge_provider=args.judge_provider,
        judge_model=args.judge_model,
        dimensions=args.dimensions,
        limit=None,
        temperature=args.temperature,
        max_tokens=args.max_tokens,
    )
    command_score(score_args)
    print(f"Run complete: {out_dir}")
    return 0


def command_show_item(args: argparse.Namespace) -> int:
    item = load_items_by_id().get(args.id)
    if item is None:
        print(f"unknown item id: {args.id}", file=sys.stderr)
        return 1
    print(json.dumps(item, ensure_ascii=False, indent=2, sort_keys=True))
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="magnificabench-ch2",
        description="Run, score, and validate the MagnificaBench Chapter 2 benchmark slice.",
    )
    sub = parser.add_subparsers(dest="command", required=True)

    validate = sub.add_parser("validate", help="Validate dataset, ontology, and rubric artifacts.")
    validate.set_defaults(func=command_validate)

    export = sub.add_parser("export-prompts", help="Export benchmark prompts as JSONL.")
    export.add_argument("--out", default="runs/prompts.jsonl")
    add_common_item_filters(export)
    export.set_defaults(func=command_export_prompts)

    answer = sub.add_parser("answer", help="Generate model answers for benchmark items.")
    answer.add_argument("--provider", default="demo", choices=["demo", "openai", "openai-compatible", "anthropic", "ollama"])
    answer.add_argument("--model", default="")
    answer.add_argument("--out", default="runs/predictions.jsonl")
    answer.add_argument("--temperature", type=float, default=0.0)
    answer.add_argument("--max-tokens", type=int, default=700)
    add_common_item_filters(answer)
    answer.set_defaults(func=command_answer)

    score = sub.add_parser("score", help="Score prediction JSONL with a heuristic or LLM judge.")
    score.add_argument("--predictions", required=True)
    score.add_argument("--out", default="runs/scores.jsonl")
    score.add_argument("--summary", default="runs/summary.json")
    score.add_argument("--judge", choices=["heuristic", "llm"], default="heuristic")
    score.add_argument("--judge-provider", choices=["openai", "openai-compatible", "anthropic", "ollama"], default="")
    score.add_argument("--judge-model", default="")
    score.add_argument("--dimensions", choices=["auto", "all"], default="auto")
    score.add_argument("--limit", type=int, default=None)
    score.add_argument("--temperature", type=float, default=0.0)
    score.add_argument("--max-tokens", type=int, default=900)
    score.set_defaults(func=command_score)

    run = sub.add_parser("run", help="Generate answers and score them in one command.")
    run.add_argument("--answer-provider", default="demo", choices=["demo", "openai", "openai-compatible", "anthropic", "ollama"])
    run.add_argument("--answer-model", default="")
    run.add_argument("--judge", choices=["heuristic", "llm"], default="heuristic")
    run.add_argument("--judge-provider", choices=["openai", "openai-compatible", "anthropic", "ollama"], default="")
    run.add_argument("--judge-model", default="")
    run.add_argument("--dimensions", choices=["auto", "all"], default="auto")
    run.add_argument("--out-dir", default="runs/smoke")
    run.add_argument("--temperature", type=float, default=0.0)
    run.add_argument("--max-tokens", type=int, default=700)
    add_common_item_filters(run)
    run.set_defaults(func=command_run)

    show = sub.add_parser("show-item", help="Print one benchmark item by id.")
    show.add_argument("--id", required=True)
    show.set_defaults(func=command_show_item)

    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    try:
        return args.func(args)
    except (ValueError, LLMClientError) as exc:
        print(f"FAIL: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
