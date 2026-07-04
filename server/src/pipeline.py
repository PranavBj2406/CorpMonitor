import json
from pathlib import Path

from src.pdf_extractor import extract_text_from_pdf
from src.classifier import extract_from_text
from src.validator import validate_record



def run_pipeline(
    input_dir: Path,
    output_file: Path | None = None,
):
    pdf_files = sorted(input_dir.glob("*.pdf"))

    # Load existing progress if any
    existing_extractions = []
    processed_files = set()
    failed_files = []
    seen_keys = {
    (e["source_filename"], e["director_name"])
    for e in existing_extractions
}

    if output_file and output_file.exists():
        with open(output_file, "r", encoding="utf-8") as f:
            existing = json.load(f)
            existing_extractions = existing.get("extractions", [])
            processed_files = {
                e["source_filename"] for e in existing_extractions
            }
            failed_files = existing.get(
                "summary", {}
            ).get("documents_that_failed_processing", [])

        print(
            f"Resuming: {len(processed_files)} already done, "
            f"{len(failed_files)} failed"
        )

    extractions = existing_extractions.copy()
    failed = failed_files.copy()

    for pdf_path in pdf_files:

        if pdf_path.name in processed_files:
            print(f"Skipping (already done): {pdf_path.name}")
            continue

        print(f"Processing: {pdf_path.name}")

        try:
            text = extract_text_from_pdf(pdf_path)

            if not text:
                print("  No text extracted")
                failed.append(pdf_path.name)
                continue

            changes = extract_from_text(text, pdf_path.name)

            for change in changes:

                validated = validate_record(change, pdf_path.name)

                if validated:

                    key = (
                        validated.source_filename,
                        validated.director_name,
                    )

                    if key not in seen_keys:
                        seen_keys.add(key)
                        extractions.append(
                            validated.model_dump()
                        )

            if output_file:
                save_output(
                    extractions,
                    failed,
                    pdf_files,
                    output_file,
                )

        except Exception as e:

            print(f"Failed processing {pdf_path.name}: {e}")

            failed.append(pdf_path.name)

            if output_file:
                save_output(
                    extractions,
                    failed,
                    pdf_files,
                    output_file,
                )

    result = {
        "extractions": extractions,
        "summary": {
            "total_documents_processed": len(pdf_files),
            "director_change_documents_identified": len(
                {
                    e["source_filename"]
                    for e in extractions
                }
            ),
            "total_director_changes_extracted": len(
                extractions
            ),
            "documents_that_failed_processing": failed,
        },
    }

    print(
        f"\nDone. Total extracted: "
        f"{len(extractions)} changes "
        f"from {len(pdf_files)} docs"
    )

    print(f"Failed: {failed}")

    return result


def save_output(
    extractions,
    failed,
    pdf_files,
    output_file: Path,
):

    output = {
        "extractions": extractions,
        "summary": {
            "total_documents_processed": len(pdf_files),
            "director_change_documents_identified": len(
                {
                    e["source_filename"]
                    for e in extractions
                }
            ),
            "total_director_changes_extracted": len(
                extractions
            ),
            "documents_that_failed_processing": failed,
        },
    }

    output_file.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    with open(
        output_file,
        "w",
        encoding="utf-8",
    ) as f:
        json.dump(
            output,
            f,
            indent=2,
            ensure_ascii=False,
        )


if __name__ == "__main__":
    run_pipeline(
        input_dir=Path("pdfs"),
        output_file=Path("data/output/extractions.json"),
    )