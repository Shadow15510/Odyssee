def save_send(data):
    save_file = open("save.txt", "w")
    save_file.write(data)
    save_file.close()

def save_read():
    save_file = open("save.txt", "r")
    content = save_file.read()
    save_file.close()
    return content

def save_delete():
    save_send("[[],[],0]")

    

