import tkinter as tk
import webbrowser


class LinkLabel(tk.Label):
    def __init__(self, parent, text, url, *args, **kwargs):
        super().__init__(parent, text=text, fg="blue", cursor="hand2", *args, **kwargs)
        self.url = url
        self.bind("<Button-1>", self.open_link)

    def open_link(self, event):
        webbrowser.open_new(self.url)

# Example usage:
root = tk.Tk()

# Create a link label
link_label = LinkLabel(root, text="Click here to visit OpenAI's website", url="https://openai.com")
link_label.pack()

root.mainloop()
