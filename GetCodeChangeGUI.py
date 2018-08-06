from GetCodeChange import config_init
import tkinter, tkinter.filedialog

class Main:
    def __init__(self, rt):

        self.gui_interface_init(rt)
        dst_path, repo_path, commit_sha, branch = config_init()

        tkinter.Label(rt, text='Source Path', anchor='w').place(x=30, y=20, width=100, height=25)
        self.source_entry = tkinter.Entry(rt)
        self.source_entry.place(x=30, y=50, width=500, height=25)
        self.source_entry.insert(0, repo_path)
        tkinter.Button(rt, text='Browse', command=self.source_browser).place(x=540, y=50, width=80, height=25)

        tkinter.Label(rt, text='Destination Path', anchor='w').place(x=30, y=80, width=100, height=25)
        self.dst_entry = tkinter.Entry(rt)
        self.dst_entry.place(x=30, y=110, width=500, height=25)
        self.dst_entry.insert(0, dst_path)
        tkinter.Button(rt, text='Browse', command=self.dst_browser).place(x=540, y=110, width=80, height=25)

        tkinter.Label(rt, text='SHA', anchor='w').place(x=30, y=140, width=100, height=25)
        sha_entry = tkinter.Entry(rt)
        sha_entry.place(x=30, y=170, width=300, height=25)
        sha_entry.insert(0, commit_sha)

        tkinter.Label(rt, text='Branch', anchor='w').place(x=340, y=140, width=100, height=25)
        branch_entry = tkinter.Entry(rt)
        branch_entry.place(x=340, y=170, width=190, height=25)
        branch_entry.insert(0, branch)

        tkinter.Button(rt, text='Rabbit', command=self.rabbit).place(x=540, y=170, width=80, height=25)

    def gui_interface_init(self, rt):
        rt.title('Rabbit')
        rt.geometry("650x250+300+200")

    def source_browser(self):
        folder_path = tkinter.filedialog.askdirectory(title='Browse source path')
        if folder_path:
            self.source_entry.delete(0, 'end')
            self.source_entry.insert(0, folder_path)

    def dst_browser(self):
        folder_path = tkinter.filedialog.askdirectory(title='Browse destination path')
        if folder_path:
            self.dst_entry.delete(0, 'end')
            self.dst_entry.insert(0, folder_path)

    def rabbit(self):
        pass

root = tkinter.Tk()
app = Main(root)
root.mainloop()
