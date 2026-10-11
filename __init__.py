from typing_extensions import override

from comfy_api.latest import ComfyExtension, io

WEB_DIRECTORY = "./js"


class NamedPrompt(io.ComfyNode):
    @classmethod
    def define_schema(cls):
        return io.Schema(
            node_id="ESTARK_NamedPrompt",
            display_name="ESTARK Named Prompt",
            category="ESTARK/Text",
            inputs=[
                io.String.Input("name", default="Prompt", tooltip="Label shown in the ESTARK Prompt Selector list."),
                io.String.Input("prompt", multiline=True),
            ],
            outputs=[io.String.Output()],
        )

    @classmethod
    def execute(cls, name, prompt) -> io.NodeOutput:
        return io.NodeOutput(prompt)


class PromptSelector(io.ComfyNode):
    @classmethod
    def define_schema(cls):
        return io.Schema(
            node_id="ESTARK_PromptSelector",
            display_name="ESTARK Prompt Selector",
            category="ESTARK/Text",
            inputs=[
                io.Autogrow.Input(
                    "prompts",
                    template=io.Autogrow.TemplatePrefix(io.String.Input("prompt"), prefix="prompt", min=1, max=100),
                ),
                io.Int.Input("choice", default=1, min=1, max=100, tooltip="1-based position of the connected prompt to output. Set by the list."),
            ],
            outputs=[io.String.Output()],
        )

    @classmethod
    def execute(cls, prompts, choice) -> io.NodeOutput:
        connected = [prompts[k] for k in sorted(prompts, key=lambda k: int(k.removeprefix("prompt")))]
        return io.NodeOutput(connected[choice - 1])


class PromptSelectorExtension(ComfyExtension):
    @override
    async def get_node_list(self) -> list[type[io.ComfyNode]]:
        return [NamedPrompt, PromptSelector]


async def comfy_entrypoint() -> PromptSelectorExtension:
    return PromptSelectorExtension()
