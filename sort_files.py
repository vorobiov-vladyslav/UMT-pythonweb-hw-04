import argparse
import asyncio
import logging
from pathlib import Path

import aiofiles.os
import aioshutil

logging.basicConfig(
    level=logging.ERROR,
    format="%(asctime)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)


async def copy_file(file_path: Path, output_folder: Path) -> None:
    """Copy a file to a subfolder in output_folder based on its extension."""
    try:
        extension = file_path.suffix.lstrip(".") if file_path.suffix else "no_extension"
        target_dir = output_folder / extension
        await aiofiles.os.makedirs(target_dir, exist_ok=True)
        target_path = target_dir / file_path.name
        await aioshutil.copy2(str(file_path), str(target_path))
    except Exception as e:
        logger.error("Failed to copy %s: %s", file_path, e)


async def read_folder(source_folder: Path, output_folder: Path) -> None:
    """Recursively read all files in source_folder and copy them to output_folder."""
    tasks: list[asyncio.Task] = []
    try:
        for item in source_folder.iterdir():
            if item.is_dir():
                tasks.append(asyncio.create_task(read_folder(item, output_folder)))
            elif item.is_file():
                tasks.append(asyncio.create_task(copy_file(item, output_folder)))
        if tasks:
            await asyncio.gather(*tasks)
    except Exception as e:
        logger.error("Error reading folder %s: %s", source_folder, e)


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Async file sorter — distributes files into subfolders by extension."
    )
    parser.add_argument(
        "source",
        type=str,
        help="Path to the source folder with files to sort.",
    )
    parser.add_argument(
        "-o",
        "--output",
        type=str,
        default="dist",
        help="Path to the output folder (default: dist).",
    )
    args = parser.parse_args()

    source_path = Path(args.source)
    output_path = Path(args.output)

    if not source_path.exists():
        logger.error("Source folder does not exist: %s", source_path)
        print(f"Error: source folder '{source_path}' does not exist.")
        return

    if not source_path.is_dir():
        logger.error("Source path is not a directory: %s", source_path)
        print(f"Error: '{source_path}' is not a directory.")
        return

    asyncio.run(read_folder(source_path, output_path))
    print("Done. Files sorted into:", output_path.resolve())


if __name__ == "__main__":
    main()
