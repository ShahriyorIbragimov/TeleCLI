from colorama import init, Fore, Style
from telethon import TelegramClient
from telethon.tl import functions
import asyncio
import json
import time
import os

api_id = 21437398
api_hash = "35c031158e2d96f9f9c3d0f3a92da388"

init()


async def clean():
    os.system('cls' if os.name == 'nt' else 'clear')


async def contacts():
    async with TelegramClient('Terminally', api_id, api_hash) as client:
        contact = await client(functions.contacts.GetContactsRequest(hash=0))
        Params = [Style.BRIGHT, Style.RESET_ALL, Fore.BLUE, Fore.YELLOW]
        for i in contact.users:
            print(
                f"{Params[0]}{Params[3]}|UserName: {i.username}|FirstName: {i.first_name}{Params[1]}",
                f"{Params[0]}{Params[3]}\b|LastName: {i.last_name}|PhoneNumber: +{i.phone}|{Params[1]}"
            )
        input("To Go Back To Chat Press Enter: ")


async def refresh(client, username: str, limit: int, show: bool):
    num = 1
    Messages = []
    P = [Style.BRIGHT, Style.RESET_ALL, Fore.BLUE, Fore.YELLOW]
    # async with TelegramClient('Terminally', api_id, api_hash) as client:
    try:
        os.remove("history.json")
        os.remove("Terminal.session-journal")
    except Exception as e:
        with open("log.txt", "a", encoding="UTF-8") as file:
            file.write(f"ERROR: {e} TIME: {time.strftime("|%m/%d/%Y | %H:%M:%S|")}\n")
    try:
        async for m in client.iter_messages(username, limit=limit):
            if not show:
                if m.out:
                    if m.media is not None:
                        Messages.append([f"{P[0]}{P[2]}{num}) You: (Not Text){P[1]}", m.id])
                    else:
                        Messages.append([f"{P[0]}{P[2]}{num}) You: {m.text}{P[1]}", m.id])
                else:
                    if m.sender.last_name is None:
                        if m.media is not None:
                            Messages.append(
                                [f"{P[0]}{P[3]}{num}) {m.sender.first_name}: (Not Text){P[1]}",
                                 m.id])
                        else:
                            Messages.append(
                                [f"{P[0]}{P[3]}{num}) {m.sender.first_name}: {m.text}{P[1]}",
                                 m.id])
                    else:
                        Full_Name = m.sender.first_name + " " + m.sender.last_name
                        if m.media is not None:
                            Messages.append(
                                [f"{P[0]}{P[3]}{num}) {Full_Name}: (Not Text){P[1]}", m.id])
                        else:
                            Messages.append(
                                [f"{P[0]}{P[3]}{num}) {Full_Name}: {m.text}{P[1]}", m.id])
            else:
                if m.out:
                    if m.media is not None:
                        Messages.append([f"{P[0]}{P[2]}{num}) You: (Not Text) | ID: {m.id}{P[1]}", m.id])
                    else:
                        Messages.append(
                            [f"{P[0]}{P[2]}{num}) You: {m.text} | ID: {m.id}{P[1]}", m.id])
                else:
                    if m.sender.last_name is None:
                        if m.media is not None:
                            Messages.append(
                                [f"{P[0]}{P[3]}{num}) {m.sender.first_name}: (Not Text) | ID: {m.id}{P[1]}",
                                 m.id])
                        else:
                            Messages.append(
                                [
                                    f"{P[0]}{P[3]}{num}) {m.sender.first_name}: {m.text} | ID: {m.id}{P[1]}",
                                    m.id])
                    else:
                        Full_Name = m.sender.first_name + " " + m.sender.last_name
                        if m.media is not None:
                            Messages.append(
                                [f"{P[0]}{P[3]}{num}) {Full_Name}: (Not Text) | ID: {m.id}{P[1]}",
                                 m.id])
                        else:
                            Messages.append(
                                [f"{P[0]}{P[3]}{num}) {Full_Name}: {m.text} | ID: {m.id}{P[1]}",
                                 m.id])
                # Messages.append(message)
            num += 1

        Messages = Messages[::-1]
        Base = []

        with open("history.json", "a", encoding="UTF-8") as file:
            for i in Messages:
                Base.append({"Message": i[0], "Message_ID": i[1]})
            json.dump(Base, file, indent=2)
        Messages.clear()
        await clean()
        return True
    except Exception as e:
        with open("log.txt", "a", encoding="UTF-8") as file:
            file.write(f"ERROR: {e} TIME: {time.strftime("|%m/%d/%Y | %H:%M:%S|")}\n")
        print("Something Went Wrong! Check The log.txt File For More Details.")
        exit()


async def check():
    P = [Style.BRIGHT, Style.RESET_ALL, Fore.GREEN]
    name = input(f"{P[0]}{P[-1]}Type The User-Name or The Full-Name of Chat That You Want To Connect To: {P[1]}")
    return name


async def delete_message(client, msg_id):
    try:
        # dialogs = await client.get_dialogs()
        ids = [1394384072]
        # for dialog in dialogs:
        #     ids.append(dialog.id)
        client.delete_messages(ids[0], [msg_id])
    except Exception as d:
        with open("log.txt", "a", encoding="UTF-8") as file:
            file.write(f"ERROR: {d} TIME: {time.strftime("|%m/%d/%Y | %H:%M:%S|")}\n")


async def main():
    starter = True
    show = False
    async with TelegramClient('Terminal', api_id, api_hash) as client:
        while True:
            if starter:
                username = await check()
                if username == "contacts()":
                    await contacts()
                    continue
                elif username == "exit()":
                    break
            starter = False
            answer = await refresh(client, username, 1000, show)
            if not answer:
                starter = True
                continue
            else:
                with open("history.json", 'r', encoding="UTF-8") as file:
                    data = json.load(file)
                    for i in data:
                        print(i.get("Message"))
                output = input("Type Your Message: ")
                if output == "exit()":
                    break
                elif output == "refresh()":
                    await refresh(client, username, 100, False)
                elif output == "contacts()":
                    await contacts()
                elif output == "show_id()":
                    if show is False:
                        show = True
                        continue
                    if show is True:
                        show = False
                        continue
                elif output.startswith("delete_message("):
                    output = output.split("delete_message(")[-1]
                    output = output.split(")")[0]
                    output = output.split(",")[-1]
                    await delete_message(client, output)
                elif output == "restart()":
                    starter = True
                    await clean()
                    continue
                else:
                    starter = False
                    await client.send_message(username, output)


if __name__ == "__main__":
    asyncio.run(main())
