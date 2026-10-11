import { app } from "../../scripts/app.js";

// Names come from the "name" widget of each connected node, so the list updates as soon as you connect or rename.
function connectedNames(node) {
    const names = [];
    for (const input of node.inputs ?? []) {
        if (input.link == null) continue;
        const link = app.graph.links[input.link];
        const origin = link && app.graph.getNodeById(link.origin_id);
        const label = origin?.widgets?.find((w) => w.name === "name")?.value;
        names.push(label || origin?.title || input.name);
    }
    return names;
}

app.registerExtension({
    name: "ESTARK.PromptSelector",
    nodeCreated(node) {
        if (node.comfyClass !== "ESTARK_PromptSelector") return;
        const choice = node.widgets.find((w) => w.name === "choice");
        choice.hidden = true;
        choice.computeSize = () => [0, -4];

        const combo = node.addWidget("combo", "prompt", "", (value) => {
            const index = connectedNames(node).indexOf(value);
            if (index >= 0) choice.value = index + 1;
        }, { values: () => connectedNames(node), serialize: false });

        // Keep the shown name in step with the stored choice after load or rewiring.
        const sync = () => {
            const names = connectedNames(node);
            combo.value = names[choice.value - 1] ?? names[0] ?? "";
            if (!names[choice.value - 1] && names.length) choice.value = 1;
        };
        const onConnectionsChange = node.onConnectionsChange;
        node.onConnectionsChange = function () {
            onConnectionsChange?.apply(this, arguments);
            sync();
        };
        const onConfigure = node.onConfigure;
        node.onConfigure = function () {
            onConfigure?.apply(this, arguments);
            setTimeout(sync, 0);
        };
        const onDrawForeground = node.onDrawForeground;
        node.onDrawForeground = function () {
            onDrawForeground?.apply(this, arguments);
            sync();
        };
    },
});
