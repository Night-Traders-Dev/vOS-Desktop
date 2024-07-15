from textual.app import App, ComposeResult
from textual.containers import Vertical, Horizontal
from textual.widgets import Button, Static, Input
from textual.reactive import reactive
from textual.message import Message

class Node(Static):
    class Selected(Message):
        def __init__(self, node: "Node"):
            super().__init__()
            self.node = node

    def __init__(self, label: str, node_type: str, code: str, **kwargs):
        super().__init__(**kwargs)
        self.label = label
        self.node_type = node_type
        self.code = code
        self.connections = []
        self.border_title = f"{label} ({node_type})"
        self.result = None

    def render(self) -> str:
        result_str = f"\nResult: {self.result}" if self.result is not None else ""
        return f"[ {self.label} ({self.node_type}) ]\nCode: {self.code}{result_str}"

    def on_click(self) -> None:
        self.post_message(self.Selected(self))

    def add_connection(self, node: "Node") -> None:
        if node not in self.connections:
            self.connections.append(node)

class VisualPythonApp(App):
    selected_node: reactive[str | None] = reactive(None)
    nodes: reactive[list[Node]] = reactive([])

    def compose(self) -> ComposeResult:
        with Vertical():
            with Horizontal():
                yield Button(label="Add Variable Node", name="add_variable_node_button")
                yield Button(label="Add Print Node", name="add_print_node_button")
                yield Button(label="Connect Nodes", name="connect_nodes_button")
                yield Button(label="Execute", name="execute_button")
                yield Button(label="Quit", name="quit_button")
            yield Vertical(id="node_container")
            yield Static("Selected Node: None", id="selected_node_display")
            yield Static("", id="connection_status")

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.name == "add_variable_node_button":
            self.add_node("Variable", "x = 10")
        elif event.button.name == "add_print_node_button":
            self.add_node("Print", "print(x)")
        elif event.button.name == "connect_nodes_button":
            self.connect_nodes()
        elif event.button.name == "execute_button":
            self.execute_code()
        elif event.button.name == "quit_button":
            self.exit()

    def add_node(self, node_type: str, code: str) -> None:
        node_label = f"Node {len(self.nodes) + 1}"
        node = Node(label=node_label, node_type=node_type, code=code)
        node_container = self.query_one("#node_container", Vertical)
        node_container.mount(node)
        self.nodes.append(node)

    def connect_nodes(self) -> None:
        if len(self.nodes) >= 2:
            self.nodes[-2].add_connection(self.nodes[-1])
            connection_status = self.query_one("#connection_status", Static)
            connection_status.update(f"Connected {self.nodes[-2].label} to {self.nodes[-1].label}")

    def on_node_selected(self, message: Node.Selected) -> None:
        self.selected_node = message.node.label

    def watch_selected_node(self, selected_node: str) -> None:
        selected_node_display = self.query_one("#selected_node_display", Static)
        selected_node_display.update(f"Selected Node: {selected_node}")

    def execute_code(self) -> None:
        code = self.generate_code()
        exec(code, globals(), locals())
        for node in self.nodes:
            if node.node_type == "Print":
                node.result = eval(node.code.split('(')[1][:-1])
        self.refresh()

    def generate_code(self) -> str:
        code_segments = []
        for node in self.nodes:
            code_segments.append(node.code)
        return "\n".join(code_segments)

if __name__ == "__main__":
    app = VisualPythonApp()
    app.run()
