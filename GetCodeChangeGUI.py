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

# class GitRabbit(git.Repo):
#     def __init__(self, repo_path):
#         super().__init__(repo_path)

class Rabbit:
    def __init__(self, rt):
        self.rt = rt
        self.gui_interface_init()
        self.dst_path, self.repo_path, self.commit_sha, branch = config_init()

        self.opt_var = tkinter.StringVar()
        self.opt_rb1 = tkinter.Radiobutton(root, var=self.opt_var, text='HEAD', command=self.select_rb1, value=1)
        self.opt_rb2 = tkinter.Radiobutton(root, var=self.opt_var, text='SHA', command=self.select_rb2, value=2)
        self.opt_rb1.place(x=30, y=10)
        self.opt_rb2.place(x=100, y=10)
        self.opt_rb1.select()

        tkinter.Label(self.rt, text='Source Path', anchor='w').place(x=30, y=35, width=100, height=25)
        self.source_entry = tkinter.Entry(self.rt)
        self.source_entry.place(x=30, y=65, width=500, height=25)
        self.source_entry.insert(0, self.repo_path)
        tkinter.Button(self.rt, text='Browse', command=self.source_browser).place(x=540, y=65, width=80, height=25)

        tkinter.Label(self.rt, text='Destination Path', anchor='w').place(x=30, y=95, width=100, height=25)
        self.dst_entry = tkinter.Entry(self.rt)
        self.dst_entry.place(x=30, y=125, width=500, height=25)
        self.dst_entry.insert(0, self.dst_path)
        tkinter.Button(self.rt, text='Browse', command=self.dst_browser).place(x=540, y=125, width=80, height=25)

        tkinter.Label(self.rt, text='SHA', anchor='w').place(x=30, y=155, width=100, height=25)
        init_state = 'normal' if self.opt_var.get() == '2' else 'disable'
        self.sha_entry = tkinter.Entry(self.rt)
        self.sha_entry.place(x=30, y=185, width=300, height=25)
        self.sha_entry.insert(0, self.commit_sha)
        self.sha_entry.configure(state=init_state)

        tkinter.Label(self.rt, text='Branch', anchor='w').place(x=340, y=155, width=100, height=25)
        self.branch_entry = tkinter.Entry(self.rt)
        self.branch_entry.place(x=340, y=185, width=190, height=25)
        self.branch_entry.insert(0, branch)

        tkinter.Button(self.rt, text='Rabbit', command=self.rabbit).place(x=540, y=185, width=80, height=25)

        self.status_text = tkinter.StringVar()
        self.status_bar = tkinter.Label(self.rt, textvariable=self.status_text, anchor='w', bd=1, relief='sunken')
        self.status_bar.pack(side='bottom', fill='x')

    def gui_interface_init(self):
        self.rt.title('Rabbit')
        self.rt.geometry("650x260+300+200")

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

    def select_rb1(self):
        self.sha_entry.configure(state='disable')

    def select_rb2(self):
        self.sha_entry.configure(state='normal')

    def update_status_text(self, text):
        self.status_text.set (text)
        self.rt.update()

    def rabbit(self):

        self.repo_path = self.source_entry.get()
        repo = git.Repo(self.repo_path)

        if repo.is_dirty():
            self.update_status_text(repo.working_dir + ' is dirty. Uncommited changes exist.')
            return

        # Check whether the branch name in entry exists or not
        branch_name = self.branch_entry.get()
        org_branch_name = repo.active_branch.name
        if branch_name != org_branch_name:
            self.update_status_text('Checking out branch ' + branch_name + ' ...')
            try:
                repo.git.checkout(branch_name)
            except:
                self.update_status_text('Unable to check out ' + branch_name)
                return

        self.commit_sha = self.sha_entry.get()
        commit = repo.commit(self.commit_sha)
        pre_commit = commit.parents[0]

        self.update_status_text("Comparing diff files...")
        diffs = commit.diff(pre_commit)

        self.update_status_text("Checking out to " + self.commit_sha + "...")
        repo.git.checkout(commit)

        dst_mod_path, dst_org_path = self.dst_path + '/Modified', self.dst_path + '/Original'
        self.update_status_text("Creating folders...")
        for dirt in [dst_mod_path, dst_org_path]:
            dir_creator(dirt)

        tree_files = []
        for f in diffs:
            dst_path_target = dir_tree_creator(f.a_blob.path, dst_mod_path)
            tree_files.append(f.a_blob.path)
            src_path = self.repo_path + '/' + f.a_blob.path
            if os.path.isfile(src_path):
                self.update_status_text('Copying ' + src_path + ' to ' + dst_path_target)
                shutil.copy(src_path, dst_path_target)

        self.update_status_text('Checking out to previous commit')
        repo.git.checkout(pre_commit)

        for f in tree_files:
            dst_path_target = dir_tree_creator(f, dst_org_path)
            src_path = self.repo_path + '/' + f
            if os.path.isfile(src_path):
                self.update_status_text('Copying ' + src_path + ' to ' + dst_path_target)
                shutil.copy(src_path, dst_path_target)

        self.update_status_text("Checking back to original branch...")
        repo.git.checkout(org_branch_name)

        self.update_status_text("Restoring config.json...")
        json_restore('config.json', {"source_path": self.repo_path, "dest_path": self.dst_path, "sha": self.commit_sha})

        self.update_status_text("Completed")

if __name__ == "__main__":
    root = tkinter.Tk()
    app = Rabbit(root)
    root.mainloop()
