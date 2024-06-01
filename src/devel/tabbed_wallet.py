from textual.app import App, ComposeResult
from textual.widgets import Footer, Header, Label, Button, Input, TabbedContent, TabPane, Tabs
from textual.containers import VerticalScroll


# Mock data for the wallets
WALLETS = {
    "QSE Wallet": {"balance": 1.234, "currency": "QSE"},
}

class CryptoWalletApp(App):
    """An example of a simple crypto wallet interface."""

    BINDINGS = [
        ("v", "view_wallets()", "View Wallets"),
        ("a", "add_wallet()", "Add Wallet"),
        ("r", "remove_wallet()", "Remove Wallet"),
        ("t", "transfer()", "Transfer Funds"),
    ]

    def compose(self) -> ComposeResult:
        """Compose app layout."""
        yield Header()
        yield Footer()
        yield Label("Crypto Wallet Interface", id="title")
        with TabbedContent(initial="view"):
            with TabPane("View Wallets", id="view"):
                yield VerticalScroll(id="wallets_view")
            with TabPane("Add Wallet", id="add"):
                yield VerticalScroll(id="add_wallet_view")
            with TabPane("Remove Wallet", id="remove"):
                yield VerticalScroll(id="remove_wallet_view")
            with TabPane("Transfer Funds", id="transfer"):
                yield VerticalScroll(id="transfer_view")

    async def on_mount(self) -> None:
        """Initialize views after mounting."""
        await self.refresh_wallets_view()
        await self.create_add_wallet_view()
        await self.create_remove_wallet_view()
        await self.create_transfer_view()

    async def refresh_wallets_view(self) -> None:
        """Refresh the wallets view."""
        container = self.query_one("#wallets_view", VerticalScroll)
        for wallet_name, details in WALLETS.items():
            container.mount(Label(f"{wallet_name}: {details['balance']} {details['currency']}"))

    async def create_add_wallet_view(self) -> None:
        """Create the add wallet view."""
        container = self.query_one("#add_wallet_view", VerticalScroll)
        container.mount(Label("Add a New Wallet"))
        container.mount(Input(placeholder="Wallet Name", id="new_wallet_name"))
        container.mount(Input(placeholder="Initial Balance", id="new_wallet_balance"))
        container.mount(Button("Add Wallet", id="add_wallet_button"))

    async def create_remove_wallet_view(self) -> None:
        """Create the remove wallet view."""
        container = self.query_one("#remove_wallet_view", VerticalScroll)
        container.mount(Label("Remove a Wallet"))
        container.mount(Input(placeholder="Wallet Name", id="remove_wallet_name"))
        container.mount(Button("Remove Wallet", id="remove_wallet_button"))

    async def create_transfer_view(self) -> None:
        """Create the transfer funds view."""
        container = self.query_one("#transfer_view", VerticalScroll)
        container.mount(Label("Transfer Funds"))
        container.mount(Input(placeholder="From Wallet", id="from_wallet"))
        container.mount(Input(placeholder="To Wallet", id="to_wallet"))
        container.mount(Input(placeholder="Amount", id="transfer_amount"))
        container.mount(Button("Transfer", id="transfer_button"))

    async def on_button_pressed(self, event: Button.Pressed) -> None:
        """Handle button press events."""
        if event.button.id == "add_wallet_button":
            await self.add_wallet()
        elif event.button.id == "remove_wallet_button":
            await self.remove_wallet()
        elif event.button.id == "transfer_button":
            await self.transfer_funds()

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
            self.log(f"Added new wallet: {wallet_name} with balance {initial_balance} BTC")
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

if __name__ == "__main__":
    app = CryptoWalletApp()
    app.run()
