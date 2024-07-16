from textual import on
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
    nodes: reactive[list[tuple[Node, Input | None]]] = reactive([])

    def compose(self) -> ComposeResult:
        with Vertical():
            with Horizontal():
                yield Button(label="Add Variable Node", name="add_variable_node_button")
                yield Button(label="Add Print Node", name="add_print_node_button")
                yield Button(label="Add Addition Node", name="add_addition_node_button")
                yield Button(label="Connect Nodes", name="connect_nodes_button")
                yield Button(label="Execute", name="execute_button")
                yield Button(label="Clear Nodes", name="clear_nodes_button")
                yield Button(label="Quit", name="quit_button")
            yield Vertical(id="node_container")
            yield Static("Selected Node: None", id="selected_node_display")
            yield Static("", id="connection_status")
            yield Static("Execution Result: None", id="execution_result")

    @on(Button.Pressed)
    def handle_button_press(self, event: Button.Pressed) -> None:
        if event.button.name == "add_variable_node_button":
            self.add_variable_node()
        elif event.button.name == "add_print_node_button":
            self.add_node("Print", "print(x)")
        elif event.button.name == "add_addition_node_button":
            self.add_node("Addition", "result = sum(values)")
        elif event.button.name == "connect_nodes_button":
            self.connect_nodes()
        elif event.button.name == "execute_button":
            self.execute_code()
        elif event.button.name == "clear_nodes_button":
            self.clear_nodes()
        elif event.button.name == "quit_button":
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

    def add_node(self, node_type: str, code: str) -> None:
        node_label = f"Node{len(self.nodes) + 1}"
        node = Node(label=node_label, node_type=node_type, code=code)
        node_container = self.query_one("#node_container", Vertical)
        node_container.mount(node)
        self.nodes.append((node, None))

    def connect_nodes(self) -> None:
        if len(self.nodes) >= 2:
            self.nodes[-2][0].add_connection(self.nodes[-1][0])
            connection_status = self.query_one("#connection_status", Static)
            connection_status.update(f"Connected {self.nodes[-2][0].label} to {self.nodes[-1][0].label}")

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
                node.code += event.input.value
                node.refresh()

    def execute_code(self) -> None:
        code = self.generate_code()
        local_vars = {}
        try:
            exec(code, globals(), local_vars)
            for node, input_widget in self.nodes:
                if node.node_type == "Print":
                    node.result = str(eval(node.code.split('(')[1][:-1], globals(), local_vars))
                elif input_widget is not None:
                    node.result = local_vars.get(node.label.lower())
                elif node.node_type == "Addition":
                    node.result = local_vars.get('result')
        except Exception as e:
            for node, _ in self.nodes:
                node.result = str(e)
        
        execution_result = self.query_one("#execution_result", Static)
        execution_result.update(f"Execution Result: {local_vars}")
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
    app = VisualPythonApp()
    app.run()
