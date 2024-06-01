from textual import on, work, events
from textual.app import App, ComposeResult
from textual.geometry import Region, Size
from textual.widgets import Footer, Header, Label, Button, Input
from textual.containers import Container, Vertical, Horizontal
import shutil


# Mock data for the wallets
WALLETS = {
    "QSE Wallet": {"balance": 1.234, "currency": "QSE"},
}

class Wallet(App):

    DEFAULT_CSS = """
            Wallet {
                layout: grid;
                grid-size: 3 3;
            }
            Container #view_wallets {
                dock: top;
            }

            #wallets_view {
                align: center top;
            }

            Container #add_wallet {
                dock: top;
            }

            Container #remove_wallet {
                dock: top;
            }

            Container #transfer_funds {
                dock: top;
            }

            Button {
                width: 1fr;
            }
            .nav_button {
                align: center top;
                width: 100%;
                height: auto;
                dock: bottom;
            }
            """

    def compose(self) -> ComposeResult:
        """Compose app layout."""

        # Views container
        with Container(id="views"):
            with Container(id="view_wallets"):
                yield Vertical(id="wallets_view")
            with Container(id="add_wallet"):
                yield Vertical(id="add_wallet_view")
            with Container(id="remove_wallet"):
                yield Vertical(id="remove_wallet_view")
            with Container(id="transfer_funds"):
                yield Vertical(id="transfer_view")


        # Navigation buttons
        yield Horizontal(
            Button("View Wallets", id="view_wallets"),
            Button("Add Wallet", id="add_wallet"),
            Button("Remove Wallet", id="remove_wallet"),
            Button("Transfer Funds", id="transfer_funds"),
            classes="nav_button")

        self.nav_buttons = ["view_wallets", "add_wallet", "remove_wallet", "transfer_funds"]
        self.def_buttons = ["add_wallet_button", "remove_wallet_button", "transfer_button"]

    def dock_nav(self) -> None:
        bounds = shutil.get_terminal_size()
        s_width = bounds.columns
        s_height = bounds.lines
        width, height = self.query_one("#nav", Horizontal).size
        self.query_one("#nav", Horizontal).offset = (0, (s_height - (height * 1.1)))

    @on(events.Resize)
    def handle_buttons(self) -> None:
        pass
#        self.dock_nav()

    @on(Button.Pressed)
    async def button_handler(self, event: Button.Pressed) -> None:
        """Handle button press events."""
        if event.button.id in self.nav_buttons:
            self.switch_view(event.button.id)()
        elif event.button.id in self.def_buttons:
            if event.button.id == "add_wallet_button":
                await self.add_wallet()
            elif event.button.id == "remove_wallet_button":
                new_offset = self.query_one("#add_wallet", Container).offset
                self.query_one("#remove_wallet", Container).offset = new_offset
                await self.remove_wallet()
            elif event.button.id == "transfer_button":
                await self.transfer_funds()

    def switch_view(self, view_id: str):
        """Switch between views."""
        def callback():
            views_container = self.query_one("#views")
            for child in views_container.children:
                child.visible = child.id == view_id
        return callback

    def on_ready(self) -> None:
        self.switch_view("view_wallets")()
#        self.dock_nav()

    async def on_mount(self) -> None:
        """Handle app mount event."""
        await self.refresh_wallets_view()
        await self.populate_add_wallet_view()
        await self.populate_remove_wallet_view()
        await self.populate_transfer_view()

    async def populate_add_wallet_view(self) -> None:
        container = self.query_one("#add_wallet_view", Vertical)
        container.mount(Label("Add a New Wallet"))
        container.mount(Input(placeholder="Wallet Name", id="new_wallet_name"))
        container.mount(Input(placeholder="Initial Balance", id="new_wallet_balance"))
        container.mount(Button("Add Wallet", id="add_wallet_button"))

    async def populate_remove_wallet_view(self) -> None:
        container = self.query_one("#remove_wallet_view", Vertical)
        container.mount(Label("Remove a Wallet"))
        container.mount(Input(placeholder="Wallet Name", id="remove_wallet_name"))
        container.mount(Button("Remove Wallet", id="remove_wallet_button"))

    async def populate_transfer_view(self) -> None:
        container = self.query_one("#transfer_view", Vertical)
        container.mount(Label("Transfer Funds"))
        container.mount(Input(placeholder="From Wallet", id="from_wallet"))
        container.mount(Input(placeholder="To Wallet", id="to_wallet"))
        container.mount(Input(placeholder="Amount", id="transfer_amount"))
        container.mount(Button("Transfer", id="transfer_button"))

    async def add_wallet(self) -> None:
        """Add a new wallet."""
        wallet_name = self.query_one("#new_wallet_name", Input).value
        try:
            initial_balance = float(self.query_one("#new_wallet_balance", Input).value)
        except ValueError:
            self.log("Invalid balance value.")
            return
        if wallet_name and wallet_name not in WALLETS:
            WALLETS[wallet_name] = {"balance": initial_balance, "currency": "QSE"}
            self.log(f"Added new wallet: {wallet_name} with balance {initial_balance} QSE")
            await self.refresh_wallets_view()

    async def remove_wallet(self) -> None:
        """Remove an existing wallet."""
        wallet_name = self.query_one("#remove_wallet_name", Input).value
        if wallet_name in WALLETS:
            del WALLETS[wallet_name]
            self.log(f"Removed wallet: {wallet_name}")
            await self.refresh_wallets_view()

    async def transfer_funds(self) -> None:
        """Transfer funds between wallets."""
        from_wallet = self.query_one("#from_wallet", Input).value
        to_wallet = self.query_one("#to_wallet", Input).value
        try:
            amount = float(self.query_one("#transfer_amount", Input).value)
        except ValueError:
            self.log("Invalid transfer amount.")
            return
        if from_wallet in WALLETS and to_wallet in WALLETS and WALLETS[from_wallet]["balance"] >= amount:
            WALLETS[from_wallet]["balance"] -= amount
            WALLETS[to_wallet]["balance"] += amount
            self.log(f"Transferred {amount} from {from_wallet} to {to_wallet}")
            await self.refresh_wallets_view()
        else:
            self.log("Invalid transfer operation.")

    async def refresh_wallets_view(self) -> None:
        """Refresh the wallets view."""
        container = self.query_one("#wallets_view", Vertical)
        for wallet_name, details in WALLETS.items():
            container.mount(Label(f"{wallet_name}: {details['balance']} {details['currency']}"))

if __name__ == "__main__":
    app = Wallet()
    app.run()
