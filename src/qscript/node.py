from textual import on
from textual.app import App, ComposeResult
from textual.containers import Vertical, Horizontal
from textual.widgets import Static, Input, Footer
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

class VisualPythonApp(App):
    BINDINGS = [
        Binding(key="v", action="add_variable_node", description="Add Variable Node"),
        Binding(key="p", action="add_print_node", description="Add Print Node"),
        Binding(key="a", action="add_addition_node", description="Add Addition Node"),
        Binding(key="c", action="connect_nodes", description="Connect Nodes"),
        Binding(key="e", action="execute_code", description="Execute Code"),
        Binding(key="r", action="clear_nodes", description="Clear Nodes"),
        Binding(key="q", action="quit", description="Quit the App"),
    ]

    selected_node: reactive[str | None] = reactive(None)
    nodes: reactive[list[tuple[Node, Input | None]]] = reactive([])

    def compose(self) -> ComposeResult:
        with Vertical():
            with Horizontal():
                yield Static("Selected Node: None", id="selected_node_display")
                yield Static("", id="connection_status")
                yield Static("Execution Result: None", id="execution_result")
            yield Vertical(id="node_container")
        yield Footer()

    def action_add_variable_node(self) -> None:
        self.add_variable_node()

    def action_add_print_node(self) -> None:
        self.add_node("Print", "print(x)")

    def action_add_addition_node(self) -> None:
        self.add_node("Addition", "result = sum(values)")

    def action_connect_nodes(self) -> None:
        self.connect_nodes()

    def action_execute_code(self) -> None:
        self.execute_code()

    def action_clear_nodes(self) -> None:
        self.clear_nodes()

    def action_quit(self) -> None:
        self.exit()

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
                elif node.node_type == "Addition":
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
        addition_code = ""
        for node, input_widget in self.nodes:
            if node.node_type == "Variable":
                code_segments.append(node.code)
                variable_map[node.label.lower()] = node.code.split('= ')[1]
            elif node.node_type == "Addition":
                values = [variable_map[var] for var in variable_map.keys()]
                addition_code = f"values = [{', '.join(values)}]\nresult = sum(values)"
                code_segments.append(addition_code)
        return "\n".join(code_segments)

    def clear_nodes(self) -> None:
        node_container = self.query_one("#node_container", Vertical)
        node_container.remove()
        self.nodes.clear()

        # Recreate the node container
        new_node_container = Vertical(id="node_container")
        self.mount(new_node_container)

        connection_status = self.query_one("#connection_status", Static)
        connection_status.update("")
        execution_result = self.query_one("#execution_result", Static)
        execution_result.update("Execution Result: None")
        selected_node_display = self.query_one("#selected_node_display", Static)
        selected_node_display.update("Selected Node: None")
        self.refresh()

if __name__ == "__main__":
    app = VisualPythonApp()
    app.run()
