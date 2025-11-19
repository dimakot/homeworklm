from textual.app import App, ComposeResult
from textual.widgets import Header, Footer, Input, RichLog, Static, Button
from textual.containers import Horizontal

from openai import OpenAI
from settings import OpenAISettings
import dotenv

dotenv.load_dotenv(dotenv.find_dotenv())


class NEUROBATUSHKAAPP(App):

    CSS = """

    Header { background: red 40%; }
    #footer { tint: hsl(300, 20%, 70%); }
    .accent { color: red 30%; }
    Screen { background: red 10%; }
    #chat_log { height: 1fr; border: solid $primary; margin: 1; background: red 5%; }
    #input_row { height: auto; dock: bottom; padding: 1; background: red 10%; }
    Input { width: 1fr; background: red 20%; }
    Button { min-width: 15; margin-left: 1; background: red 30%; }
    #help { color: $text-muted; text-align: center; padding: 1; }
    """

    BINDINGS = [("q", "quit", "Выйти"), ("ctrl+l", "clear", "Очистить")]

    def __init__(self):
        super().__init__()
        settings = OpenAISettings()
        self.client = OpenAI(
            api_key=settings.openai_api_key.get_secret_value(),
            base_url=str(settings.openai_base_url),
        )
        self.messages = [{
            "role": "system",
            "content": "Ты русский православный батюшка матершинник, который составляет молитвы людям с кучей мата и эмодзи",
        }]

    def compose(self) -> ComposeResult:
        yield Header()
        yield Static(
            "[bold green]Дарова[/bold green] | [red]/exit[/red  ] - покинуть, [blue]/clear[/blue] - очиститься от грехов, [pink]/system <текст>[/pink] - зачесть промпт",
            id="help"
        )
        yield RichLog(id="chat_log", wrap=True, highlight=True, markup=True)
        with Horizontal(id="input_row"):
            yield Input(placeholder="Введите сообщение...", id="user_input")
            yield Button("Отправить", variant="primary", id="send_button")
        yield Footer()

    def on_mount(self):
        ascii_art = """⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⠟⠛⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⠟⠄⠄⠄⠄⠹⢿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⡟⠄⠄⠄⢀⡀⠄⠄⠄⢹⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣧⡀⠄⠄⢸⡇⠄⠄⢀⣼⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⠛⠉⠛⢿⣿⣷⠄⢸⡇⠄⢸⣿⡿⠛⠉⠛⣿⣿⣿⣿
⣿⡿⠟⠃⠄⠄⠄⠄⠛⠛⠄⢸⡇⠄⠘⠛⠄⠄⠄⠄⠘⠻⢿⣿
⣿⠁⠄⠄⠄⢠⣤⣤⣤⣤⣤⣼⣧⣤⣤⣤⣤⣤⡄⠄⠄⠄⠈⣿
⣿⣦⣀⠄⠄⠄⠄⠄⣀⣀⠄⢸⡇⠄⢀⣀⠄⠄⠄⠄⠄⣀⣴⣿
⣿⣿⣿⣧⡀⠄⠄⣠⣿⣿⠄⢸⡇⠄⢸⣿⣄⠄⠄⢀⣼⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠄⢸⡇⠄⢸⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠄⢸⡇⠄⢸⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⠏⠉⠻⠄⢸⡇⠄⢸⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⡿⠃⠄⢤⡀⠄⢸⡇⠄⢸⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣦⣄⠄⠙⠳⣼⡇⠄⠸⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣷⣤⠄⢸⡟⢦⣄⠄⠙⠿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠄⢸⡇⠄⠉⠓⠄⢀⣼⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠄⢸⡇⠄⢠⣀⣠⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⠟⠛⠄⢸⡇⠄⠘⠻⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⡇⠄⠄⠄⠸⠇⠄⠄⠄⢸⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣷⣄⡀⠄⠄⠄⠄⢀⣠⣾⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣄⠄⠄⣀⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿"""
        
        chat_log = self.query_one("#chat_log", RichLog)
        chat_log.write(f"[bold white]{ascii_art}[/bold white]")
        chat_log.write("\n[bold red]Батюшка готов зачесть молитву[/bold red]")
        self.query_one("#user_input", Input).focus()

    async def on_input_submitted(self, event):
        await self.send_message()
    
    async def on_button_pressed(self, event):
        if event.button.id == "send_button":
            await self.send_message()
    
    async def send_message(self):
        input_widget = self.query_one("#user_input", Input)
        user_input = input_widget.value.strip()
        
        if not user_input:
            return
        
        chat_log = self.query_one("#chat_log", RichLog)
        input_widget.value = ""
        
        chat_log.write(f"[bold green]Вы:[/bold green] {user_input}")
        
        if user_input == "/exit":
            chat_log.write("[bold red]Гудбай[/bold red]")
            self.exit()
            return
        
        if user_input == "/clear":
            system_prompt = self.messages[0]
            self.messages.clear()
            self.messages.append(system_prompt)
            chat_log.clear()
            chat_log.write("[bold yellow]История очищена! 🗑️[/bold yellow]")
            return
        
        if user_input.startswith("/system "):
            new_system_prompt = user_input[8:].strip()
            if new_system_prompt:
                self.messages[0] = {"role": "system", "content": new_system_prompt}
                chat_log.write(f"[bold yellow]По другому буду базарить, сорян[/bold yellow]\n\n{new_system_prompt}")
            else:
                chat_log.write("[bold red]Ты че сволочь, а ну сказала шо нить что базарить, чо ты такой скромный а[/bold red]")
            return
        
        self.messages.append({"role": "user", "content": user_input})
        chat_log.write("[dim]Думаю...[/dim]")
        
        try:
            completion = self.client.chat.completions.create(
                model="Qwen/Qwen3-Next-80B-A3B-Instruct",
                messages=self.messages,
            )
            
            assistant_response = completion.choices[0].message.content
            self.messages.append({"role": "assistant", "content": assistant_response})
            
            chat_log.write(assistant_response)
            
        except Exception as e:
            chat_log.write(f"[bold red]Ошибка: {str(e)}[/bold red]")
    
    def action_clear(self):
        system_prompt = self.messages[0]
        self.messages.clear()
        self.messages.append(system_prompt)
        
        chat_log = self.query_one("#chat_log", RichLog)
        chat_log.clear()
        chat_log.write("[bold yellow]История очищена! 🗑️[/bold yellow]")


if __name__ == "__main__":
    app = NEUROBATUSHKAAPP()
    app.run()