from __future__ import annotations
from functools import partial
from pathlib import Path

from textual import on
from textual.app import App, ComposeResult
from textual.command import Hit, Hits, Provider
from textual.containers import Vertical, Horizontal, VerticalScroll
from textual.widgets import Static, Input, Header
from textual.reactive import reactive
from textual.message import Message
from textual.binding import Binding


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


class CommandProvider(Provider):
    """Command provider for QScriptNodes commands."""

    async def startup(self) -> None:
        """Called once when the command palette is opened, prior to searching."""
        self.commands = [
            "add_variable_node",
            "add_print_node",
            "add_addition_node",
            "add_subtraction_node",
            "add_multiplication_node",
            "add_division_node",
            "connect_nodes",
            "execute_code",
            "clear_nodes",
        ]

    async def search(self, query: str) -> Hits:
        """Search for commands."""
        matcher = self.matcher(query)

        app = self.app
        assert isinstance(app, QScriptNodes)

        for command in self.commands:
            score = matcher.match(command)
            if score > 0:
                yield Hit(
                    score,
                    matcher.highlight(command),
                    partial(app.run_command, command),
                    help=f"Run {command.replace('_', ' ')}",
                )


class QScriptNodes(App):
    COMMANDS = App.COMMANDS | {CommandProvider}

    selected_node: reactive[str | None] = reactive(None)
    nodes: reactive[list[tuple[Node, Input | None]]] = reactive([])

    def compose(self) -> ComposeResult:
        with Vertical():
            with Horizontal():
                yield Static("Selected Node: None", id="selected_node_display")
                yield Static("", id="connection_status")
                yield Static("Execution Result: None", id="execution_result")
            yield Vertical(id="node_container")
        with VerticalScroll():
            yield Static(id="command_output", expand=True)
        yield Header()

    def run_command(self, command: str) -> None:
        """Run a command by its name."""
        getattr(self, command)()

    def add_variable_node(self) -> None:
        node_label = f"Node{len(self.nodes) + 1}"
        code = f"{node_label.lower()} = "
        node = Node(label=node_label, node_type="Variable", code=code)
        node_container = self.query_one("#node_container", Vertical)
        input_widget = Input(placeholder="Enter value", id=f"{node_label.lower()}_input")
        node_container.mount(node)
        node_container.mount(input_widget)
        self.nodes.append((node, input_widget))
        self.post_message(Node.Selected(node))  # Select the node when created
        input_widget.focus()

    def add_print_node(self) -> None:
        self.add_node("Print", "print(x)")

    def add_addition_node(self) -> None:
        self.add_node("Addition", "result = sum(values)")

    def add_subtraction_node(self) -> None:
        self.add_node("Subtraction", "result = values[0] - sum(values[1:])")

    def add_multiplication_node(self) -> None:
        self.add_node("Multiplication", "result = 1\nfor v in values:\n    result *= v")

    def add_division_node(self) -> None:
        self.add_node("Division", "result = values[0]\nfor v in values[1:]:\n    result /= v")

    def add_node(self, node_type: str, code: str) -> None:
        node_label = f"Node{len(self.nodes) + 1}"
        node = Node(label=node_label, node_type=node_type, code=code)
        node_container = self.query_one("#node_container", Vertical)
        node_container.mount(node)
        self.nodes.append((node, None))
        self.post_message(Node.Selected(node))  # Select the node when created

    def connect_nodes(self) -> None:
        if len(self.nodes) >= 2:
            self.nodes[-2][0].add_connection(self.nodes[-1][0])
            connection_status = self.query_one("#connection_status", Static)
            connection_status.update(f"Connected {self.nodes[-2][0].label} to {self.nodes[-1][0].label}")
            self.notify(f"Connected {self.nodes[-2][0].label} to {self.nodes[-1][0].label}")

    @on(Node.Selected)
    def node_selected(self, message: Node.Selected) -> None:
        self.selected_node = message.node.label

    def watch_selected_node(self, selected_node: str) -> None:
        selected_node_display = self.query_one("#selected_node_display", Static)
        selected_node_display.update(f"Selected Node: {selected_node}")

    @on(Input.Submitted)
    def store_variable_value(self, event: Input.Submitted) -> None:
        node_name = event.input.id.replace("_input", "")
        for node, input_widget in self.nodes:
            if node.label.lower() == node_name:
                try:
                    value = int(event.input.value)
                except ValueError:
                    value = event.input.value  # Fall back to string if conversion fails
                node.code += repr(value)
                node.refresh()
                input_widget.blur()
                self.post_message(Node.Selected(node))  # Re-select the node after input submission

    def execute_code(self) -> None:
        code = self.generate_code()
        local_vars = {}
        try:
            exec(code, globals(), local_vars)
            for node, input_widget in self.nodes:
                if node.node_type == "Print":
                    variable_name = node.code.split('(')[1].split(')')[0].strip()
                    node.result = local_vars.get(variable_name, "Undefined")
                elif input_widget is not None:
                    node.result = local_vars.get(node.label.lower())
                elif node.node_type in ["Addition", "Subtraction", "Multiplication", "Division"]:
                    node.result = local_vars.get('result')
        except Exception as e:
            for node, _ in self.nodes:
                node.result = str(e)
                self.notify(str(e))

        execution_result = self.query_one("#execution_result", Static)
        execution_result.update(f"Execution Result: {local_vars}")
        self.notify(f"Execution Result: {local_vars}")
        self.refresh()

    def generate_code(self) -> str:
        code_segments = []
        variable_map = {}
        for node, input_widget in self.nodes:
            if node.node_type == "Variable":
                code_segments.append(node.code)
                variable_map[node.label.lower()] = node.code.split('= ')[1]
            elif node.node_type == "Addition":
                values = [variable_map[var] for var in variable_map.keys()]
                code_segments.append(f"values = [{', '.join(values)}]\nresult = sum(values)")
            elif node.node_type == "Subtraction":
                values = [variable_map[var] for var in variable_map.keys()]
                code_segments.append(f"values = [{', '.join(values)}]\nresult = values[0] - sum(values[1:])")
            elif node.node_type == "Multiplication":
                values = [variable_map[var] for var in variable_map.keys()]
                code_segments.append(f"values = [{', '.join(values)}]\nresult = 1\nfor v in values:\n    result *= v")
            elif node.node_type == "Division":
                values = [variable_map[var] for var in variable_map.keys()]
                code_segments.append(f"values = [{', '.join(values)}]\nresult = values[0]\nfor v in values[1:]:\n    result /= v")
        return "\n".join(code_segments)

    def clear_nodes(self) -> None:
        node_container = self.query_one("#node_container", Vertical)
        node_container.clear()
        self.nodes.clear()
        connection_status = self.query_one("#connection_status", Static)
        connection_status.update("")
        execution_result = self.query_one("#execution_result", Static)
        execution_result.update("Execution Result: None")
        selected_node_display = self.query_one("#selected_node_display", Static)
        selected_node_display.update("Selected Node: None")
        self.refresh()


if __name__ == "__main__":
    app = QScriptNodes()
    app.run()
