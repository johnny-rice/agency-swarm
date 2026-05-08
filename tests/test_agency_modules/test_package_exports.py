import agents
from openai.types.responses import tool_param

import agency_swarm
import agency_swarm.tools as agency_tools

ROOT_SHADOWED_SDK_EXPORTS = {"Agent", "Handoff", "function_tool", "__version__"}
TOOLS_SHADOWED_SDK_EXPORTS = {"function_tool"}
TOOL_PARAM_IGNORED_EXPORTS = {
    "Dict",
    "Literal",
    "Optional",
    "Required",
    "SequenceNotStr",
    "TypeAlias",
    "TypedDict",
    "Union",
    "annotations",
}
TOOL_PARAM_SHADOWED_EXPORTS = {"WebSearchTool"}


def _is_sdk_tool_export(name: str) -> bool:
    return (
        "Tool" in name
        or "Computer" in name
        or name.startswith("ApplyPatch")
        or name.startswith("Shell")
        or name.startswith("MCP")
        or name
        in {
            "Button",
            "CustomTool",
            "Environment",
            "FunctionToolResult",
            "LocalShellCommandRequest",
            "LocalShellExecutor",
        }
    )


def test_root_exports_agents_sdk_public_imports() -> None:
    expected_exports = set(agents.__all__) - ROOT_SHADOWED_SDK_EXPORTS

    missing_exports = sorted(expected_exports - set(agency_swarm.__all__))

    assert missing_exports == []
    assert agency_swarm.SDKAgent is agents.Agent
    assert agency_swarm.SDKHandoff is agents.Handoff
    assert agency_swarm.Agent is not agents.Agent
    assert agency_swarm.Handoff is not agents.Handoff
    for name in expected_exports:
        assert getattr(agency_swarm, name) is getattr(agents, name)


def test_tools_exports_agents_sdk_tool_imports() -> None:
    expected_exports = {name for name in agents.__all__ if _is_sdk_tool_export(name)} - TOOLS_SHADOWED_SDK_EXPORTS

    missing_exports = sorted(expected_exports - set(agency_tools.__all__))

    assert missing_exports == []
    for name in expected_exports:
        assert getattr(agency_tools, name) is getattr(agents, name)


def test_tools_exports_openai_tool_param_imports() -> None:
    expected_exports = {
        name
        for name in dir(tool_param)
        if not name.startswith("_")
        and name not in TOOL_PARAM_IGNORED_EXPORTS
        and name not in TOOL_PARAM_SHADOWED_EXPORTS
    }

    missing_exports = sorted(expected_exports - set(agency_tools.__all__))

    assert missing_exports == []
    for name in expected_exports:
        assert getattr(agency_tools, name) is getattr(tool_param, name)
