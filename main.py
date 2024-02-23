import time
import openai
import config
import content_system
import typer
from rich import print
from rich.table import Table

def main():

    openai.api_key = config.api_key

    print("🤖💬 [bold blue]AI[/bold blue]")

    table = Table("Command", "Descripción")
    table.add_row("[bold blue]new[/bold blue]", "Crear una nueva conversación")
    table.add_row("[bold red]exit[/bold red]", "Salir de la app")

    print(table)

    # Condicionar asistente para darle contexto
    context = {"role": "system",
                "content": content_system.content}
    messages = [context]

    # Realiza respuesta en bucle
    while True:

        content = __prompt()

        if content == "new":
            print("🆕 Nueva conversación creada")
            messages = [context]
            content = __prompt()

        messages.append({"role":"user","content": content})

        response = openai.chat.completions.create(
            model = "gpt-3.5-turbo",
            messages = messages,
            temperature= 0.8
        )

        #guarda las respuestas
        response_content = response.choices[0].message.content

        # Contexto de todas sus respuestas(contexto inicial, contexto de todas las preguntas) sin perder el contexto
        messages.append({"role": "assistant", "content": response_content})

        print("🤖💬 ", response_content)

def __prompt() -> str:
    prompt = typer.prompt("\n¿Sobre qué quieres hablar? ")

    if prompt.lower() in["exit","salir","quit","stop","parar","para","no quiero hablar contigo","no te quiero ver más","detente","abort"]:
        exit = typer.confirm("😥✋ ¿Estás seguro?")
        if exit:
            print("👋 Fue un placer ayudarte, ¡Hasta luego!")
            time.sleep(3)
            raise typer.Abort()

        return __prompt()

    return prompt
        
if __name__ == "__main__":
    typer.run(main)