"""Image Generation Tool Example

This example shows how to:
- attach OpenAI's hosted ImageGenerationTool to an Agency Swarm agent
- use a mainline model for the agent, while the tool uses GPT Image models internally
- save the first image_generation_call result to a local PNG file

Run:
    uv run python examples/image_generation.py

Requires OPENAI_API_KEY (or .env). Uses live API (network + usage).
"""

import base64
from pathlib import Path
from typing import Any

from agency_swarm import Agency, Agent, ImageGenerationTool

OUTPUT_PATH = Path("image_generation_output.png")


def build_image_generation_agent() -> Agent:
    return Agent(
        name="ImageGenerator",
        model="gpt-5.5",
        instructions="Generate the requested image. Keep any text response short.",
        tools=[
            ImageGenerationTool(
                tool_config={
                    "type": "image_generation",
                    "action": "generate",
                    "size": "1024x1024",
                    "quality": "high",
                    "output_format": "png",
                }
            )
        ],
    )


def save_first_image_generation_result(result: Any, output_path: Path = OUTPUT_PATH) -> Path | None:
    for item in getattr(result, "new_items", []):
        raw_item = getattr(item, "raw_item", None)
        if getattr(raw_item, "type", None) == "image_generation_call" and getattr(raw_item, "result", None):
            output_path.write_bytes(base64.b64decode(raw_item.result))
            return output_path
    return None


def main() -> None:
    agent = build_image_generation_agent()
    agency = Agency(agent)
    result = agency.get_response_sync("Draw a clean product mockup of a voice agent app running on an iPhone.")
    saved_path = save_first_image_generation_result(result)

    if saved_path is None:
        print("No image_generation_call result was returned.")
        return
    print(f"Saved image to {saved_path}")


if __name__ == "__main__":
    main()
