# ESTARK Prompt Tools

Two ComfyUI nodes for keeping several prompts in one workflow and running one of them.

- **ESTARK Named Prompt** (`ESTARK/Text`): a `name` and a multiline `prompt`. Outputs the prompt as `STRING`.
- **ESTARK Prompt Selector** (`ESTARK/Text`): connect any number of Named Prompt nodes (a new input appears after each connection) and pick one by name from the list. Outputs the chosen text as `STRING`, so it plugs into anything that takes text.

The list is built in the browser from the `name` widgets of the connected nodes, so it updates as soon as you connect or rename, without running the workflow. Duplicate names pick the first match.

Install: clone into `ComfyUI/custom_nodes/` and restart ComfyUI.
