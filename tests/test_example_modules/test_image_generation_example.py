import base64
from types import SimpleNamespace

from agents import ImageGenerationTool

from examples.image_generation import build_image_generation_agent, save_first_image_generation_result


def test_build_image_generation_agent_uses_hosted_tool_with_mainline_model() -> None:
    agent = build_image_generation_agent()

    assert agent.model == "gpt-5.5"
    assert len(agent.tools) == 1
    assert isinstance(agent.tools[0], ImageGenerationTool)
    assert agent.tools[0].tool_config["type"] == "image_generation"
    assert agent.tools[0].tool_config["action"] == "generate"


def test_save_first_image_generation_result_writes_decoded_image(tmp_path) -> None:
    image_bytes = b"png-bytes"
    result = SimpleNamespace(
        new_items=[
            SimpleNamespace(raw_item=SimpleNamespace(type="message", result=None)),
            SimpleNamespace(
                raw_item=SimpleNamespace(
                    type="image_generation_call",
                    result=base64.b64encode(image_bytes).decode("ascii"),
                )
            ),
        ]
    )

    output_path = tmp_path / "output.png"

    assert save_first_image_generation_result(result, output_path) == output_path
    assert output_path.read_bytes() == image_bytes
