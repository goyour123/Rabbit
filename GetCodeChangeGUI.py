from GetCodeChange import config_init, dir_creator, dir_tree_creator
import tkinter, tkinter.filedialog
import os, shutil, json
import git

def json_restore(json_path, dic):
    with open(json_path, 'r+') as f:
        j = json.load(f)
        j.update(dic)
        f.truncate(0)
        f.seek(0)
        f.write(json.dumps(j, indent=4))

class Main:
    def __init__(self, rt):
        self.rt = rt
        self.gui_interface_init()
        self.dst_path, self.repo_path, self.commit_sha, branch = config_init()

        tkinter.Label(self.rt, text='Source Path', anchor='w').place(x=30, y=20, width=100, height=25)
        self.source_entry = tkinter.Entry(self.rt)
        self.source_entry.place(x=30, y=50, width=500, height=25)
        self.source_entry.insert(0, self.repo_path)
        tkinter.Button(self.rt, text='Browse', command=self.source_browser).place(x=540, y=50, width=80, height=25)

        tkinter.Label(self.rt, text='Destination Path', anchor='w').place(x=30, y=80, width=100, height=25)
        self.dst_entry = tkinter.Entry(self.rt)
        self.dst_entry.place(x=30, y=110, width=500, height=25)
        self.dst_entry.insert(0, self.dst_path)
        tkinter.Button(self.rt, text='Browse', command=self.dst_browser).place(x=540, y=110, width=80, height=25)

        tkinter.Label(self.rt, text='SHA', anchor='w').place(x=30, y=140, width=100, height=25)
        self.sha_entry = tkinter.Entry(self.rt)
        self.sha_entry.place(x=30, y=170, width=300, height=25)
        self.sha_entry.insert(0, self.commit_sha)

        tkinter.Label(self.rt, text='Branch', anchor='w').place(x=340, y=140, width=100, height=25)
        branch_entry = tkinter.Entry(self.rt)
        branch_entry.place(x=340, y=170, width=190, height=25)
        branch_entry.insert(0, branch)

        tkinter.Button(self.rt, text='Rabbit', command=self.rabbit).place(x=540, y=170, width=80, height=25)

        self.status_text = tkinter.StringVar()
        self.status_bar = tkinter.Label(self.rt, textvariable=self.status_text, anchor='w', bd=1, relief='sunken')
        self.status_bar.pack(side='bottom', fill='x')

    def gui_interface_init(self):
        self.rt.title('Rabbit')
        self.rt.geometry("650x250+300+200")

    def source_browser(self):
        if os.path.isdir(self.repo_path):
            initDir = self.repo_path
        else:
            initDir = os.getcwd()
        folder_path = tkinter.filedialog.askdirectory(title='Browse source path', initialdir=initDir)
        if folder_path:
            self.source_entry.delete(0, 'end')
            self.source_entry.insert(0, folder_path)
            self.repo_path = folder_path

    def dst_browser(self):
        if os.path.isdir(self.dst_path):
            initDir = self.dst_path
        else:
            initDir = os.getcwd()
        folder_path = tkinter.filedialog.askdirectory(title='Browse destination path', initialdir=initDir)
        if folder_path:
            self.dst_entry.delete(0, 'end')
            self.dst_entry.insert(0, folder_path)
            self.dst_path = folder_path

    def rabbit(self):

        repo = git.Repo(self.repo_path)
        self.commit_sha = self.sha_entry.get()
        commit = repo.commit(self.commit_sha)
        pre_commit = commit.parents[0]

        self.status_text.set("Comparing diff files...")
        self.rt.update()
        diffs = commit.diff(pre_commit)

        self.status_text.set("Checking out to " + self.commit_sha + "...")
        self.rt.update()
        repo.git.checkout(commit)

        dst_mod_path, dst_org_path = self.dst_path + '/Modified', self.dst_path + '/Original'
        self.status_text.set("Creating folders...")
        self.rt.update()
        for dirt in [dst_mod_path, dst_org_path]:
            dir_creator(dirt)

        tree_files = []
        for f in diffs:
            dst_path_target = dir_tree_creator(f.a_blob.path, dst_mod_path)
            tree_files.append(f.a_blob.path)
            src_path = self.repo_path + '/' + f.a_blob.path
            if os.path.isfile(src_path):
                self.status_text.set('Copying ' + src_path + ' to ' + dst_path_target)
                self.rt.update()
                shutil.copy(src_path, dst_path_target)

        self.status_text.set('Checking out to previous commit')
        self.rt.update()
        repo.git.checkout(pre_commit)

        for f in tree_files:
            dst_path_target = dir_tree_creator(f, dst_org_path)
            src_path = self.repo_path + '/' + f
            if os.path.isfile(src_path):
                self.status_text.set('Copying ' + src_path + ' to ' + dst_path_target)
                self.rt.update()
                shutil.copy(src_path, dst_path_target)

        self.status_text.set("Checking back to original branch...")
        self.rt.update()
        repo.git.checkout(repo.head)

        self.status_text.set("Restoring config.json...")
        self.rt.update()
        json_restore('config.json', {"source_path": self.repo_path, "dest_path": self.dst_path, "sha": self.commit_sha})

        self.status_text.set("Completed")

root = tkinter.Tk()
app = Main(root)
root.mainloop()
