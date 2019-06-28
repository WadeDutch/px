import tkinter as tk
from vframe import VerticalScrolledFrame
import json
from commands import COMMANDS

class App(tk.PanedWindow):
    def __init__(self, master):
        tk.PanedWindow.__init__(self, master, bg="#252525", sashwidth=7)
        self.master = master
        self.pack(fill=tk.BOTH)

        #define vars
        self.left_widgets = []
        self.projects = []
        self.activeUID = 0
        self.UIDs = []

        #init left and right panes
        self.left = VerticalScrolledFrame(self)
        self.right = tk.Frame(self)
        self.add(self.left)
        self.add(self.right)

        #bind scroll wheel to scrolled Frame
        self.left.bind_all("<MouseWheel>", lambda e: self.left.canvas.yview_scroll(int(-1*(e.delta/120)), "units"))

        #load and update display on startup
        self.init_menu()
        self.init_right_frame()
        self.loadprojects()
        self.updatedisplay()

        #update sash and window height
        master.update()
        self.sash_place(0, int(master.winfo_width()*.25), int(master.winfo_height()*.5))
        self.config(height=master.winfo_height())

    def init_menu(self):
        #create Commands
        self.cmd = COMMANDS(self) #init commands class and pass calback needed
        # create menus
        menubar = tk.Menu(self.master)

        file = tk.Menu(menubar, tearoff=0)
        file.add_command(label="New Project (Ctrl+N)", command= self.cmd.createnewproject)
        file.add_command(label="Save Changes (Ctrl+S)", command= self.cmd.saveprojectdata)
        file.add_command(label="Save As Spreadsheet", command= self.cmd.saveasSpreadSheet)
        file.add_command(label="Delete Project (Ctrl+D)", command= self.cmd.confirmdeletepop)


        commands = tk.Menu(menubar, tearoff=0)
        commands.add_command(label="Calculate X")
        commands.add_command(label="Do Y")

        menubar.add_cascade(label="File", menu=file)
        menubar.add_cascade(label="Commands", menu=commands)
        self.master.config(menu=menubar)

        # create keyboard shortcuts
        self.master.bind("<Control-n>", self.cmd.createnewproject)
        self.master.bind("<Control-s>", self.cmd.saveprojectdata)
        self.master.bind("<Control-d>", self.cmd.confirmdeletepop)




    def init_right_frame(self):

        #labels
        tk.Label(self.right, text="Project Info").grid(column=1, row=0, columnspan=2, pady=20)
        tk.Label(self.right, text="Billing Info").grid(column=3, row=0, columnspan=2, pady=20)

        #setup project info
        tk.Label(self.right, text="Client", pady=10).grid(column=1, row=1)
        self.client = tk.Entry(self.right)
        self.client.bind("<Key>", lambda e: self.client.config(width = len(self.client.get())+1 if len(self.client.get()) > 20 else 20))
        self.client.grid(column=2, row=1, sticky="w")

        tk.Label(self.right, text="Year:", pady=10).grid(column=1, row=1+1)
        self.year = tk.Entry(self.right)
        self.year.bind("<Key>", lambda e: self.year.config(width = len(self.year.get())+1 if len(self.year.get()) > 20 else 20))
        self.year.grid(column=2, row=1+1, sticky="w")

        tk.Label(self.right, text="Status:", pady=10).grid(column=1, row=1+2)
        self.status = tk.Entry(self.right)
        self.status.bind("<Key>", lambda e: self.status.config(width = len(self.status.get())+1 if len(self.status.get()) > 20 else 20))
        self.status.grid(column=2, row=1+2, sticky="w")

        tk.Label(self.right, text="Industry:", pady=10).grid(column=1, row=1+3)
        self.industry = tk.Entry(self.right)
        self.industry.bind("<Key>", lambda e: self.industry.config(width = len(self.industry.get())+1 if len(self.industry.get()) > 20 else 20))
        self.industry.grid(column=2, row=1+3, sticky="w")

        tk.Label(self.right, text="FIling Date:", pady=10).grid(column=1, row=1+4)
        self.filingdate = tk.Entry(self.right)
        self.filingdate.bind("<Key>", lambda e: self.filingdate.config(width = len(self.filingdate.get())+1 if len(self.filingdate.get()) > 20 else 20))
        self.filingdate.grid(column=2, row=1+4, sticky="w")

        tk.Label(self.right, text="Credit:", pady=10).grid(column=1, row=1+5)
        self.credit = tk.Entry(self.right)
        self.credit.bind("<Key>", lambda e: self.credit.config(width = len(self.credit.get())+1 if len(self.credit.get()) > 20 else 20))
        self.credit.grid(column=2, row=1+5, sticky="w")

        tk.Label(self.right, text="Rate:", pady=10).grid(column=1, row=1+6)
        self.P_rate = tk.Entry(self.right)
        self.P_rate.bind("<Key>", lambda e: self.P_rate.config(width = len(self.P_rate.get())+1 if len(self.P_rate.get()) > 20 else 20))
        self.P_rate.grid(column=2, row=1+6, sticky="w")

        tk.Label(self.right, text="Estimated Revenue:", pady=10).grid(column=1, row=1+7)
        self.estimatedrevenue = tk.Entry(self.right)
        self.estimatedrevenue.bind("<Key>", lambda e: self.estimatedrevenue.config(width = len(self.estimatedrevenue.get())+1 if len(self.estimatedrevenue.get()) > 20 else 20))
        self.estimatedrevenue.grid(column=2, row=1+7, sticky="w")

        tk.Label(self.right, text="New Client:", pady=10).grid(column=1, row=1+8)
        self.newclient = tk.Entry(self.right)
        self.newclient.bind("<Key>", lambda e: self.newclient.config(width = len(self.newclient.get())+1 if len(self.newclient.get()) > 20 else 20))
        self.newclient.grid(column=2, row=1+8, sticky="w")

        tk.Label(self.right, text="CPA:", pady=10).grid(column=1, row=1+9)
        self.cpa = tk.Entry(self.right)
        self.cpa.bind("<Key>", lambda e: self.cpa.config(width = len(self.cpa.get())+1 if len(self.cpa.get()) > 20 else 20))
        self.cpa.grid(column=2, row=1+9, sticky="w")

        tk.Label(self.right, text="Next Step:", pady=10).grid(column=1, row=1+10)
        self.nextstep = tk.Entry(self.right)
        self.nextstep.bind("<Key>", lambda e: self.nextstep.config(width = len(self.nextstep.get())+1 if len(self.nextstep.get()) > 20 else 20))
        self.nextstep.grid(column=2, row=1+10, sticky="w")

        #setup billing frame
        tk.Label(self.right, text="Rate:", pady=10).grid(column=3, row=1)
        self.B_rate = tk.Entry(self.right)
        self.B_rate.bind("<Key>", lambda e: self.B_rate.config(width = len(self.B_rate.get())+1 if len(self.B_rate.get()) > 20 else 20))
        self.B_rate.grid(column=4, row=1, sticky="w")

        tk.Label(self.right, text="Bill:", pady=10).grid(column=3, row=2)
        self.bill = tk.Entry(self.right)
        self.bill.bind("<Key>", lambda e: self.bill.config(width = len(self.bill.get())+1 if len(self.bill.get()) > 20 else 20))
        self.bill.grid(column=4, row=2, sticky="w")

        tk.Label(self.right, text="Billing Description:", pady=10).grid(column=3, row=3)
        self.billingdescription = tk.Entry(self.right)
        self.billingdescription.bind("<Key>", lambda e: self.billingdescription.config(width = len(self.billingdescription.get())+1 if len(self.billingdescription.get()) > 20 else 20))
        self.billingdescription.grid(column=4, row=3, sticky="w")

        tk.Label(self.right, text="Date Billed:", pady=10).grid(column=3, row=4)
        self.datebilled = tk.Entry(self.right)
        self.datebilled.bind("<Key>", lambda e: self.datebilled.config(width = len(self.datebilled.get())+1 if len(self.datebilled.get()) > 20 else 20))
        self.datebilled.grid(column=4, row=4, sticky="w")

        tk.Label(self.right, text="Date Collected:", pady=10).grid(column=3, row=5)
        self.datecollected = tk.Entry(self.right)
        self.datecollected.bind("<Key>", lambda e: self.datecollected.config(width = len(self.datecollected.get())+1 if len(self.datecollected.get()) > 20 else 20))
        self.datecollected.grid(column=4, row=5, sticky="w")

        tk.Label(self.right, text="Bill Number:", pady=10).grid(column=3, row=6)
        self.billnumber = tk.Entry(self.right)
        self.billnumber.bind("<Key>", lambda e: self.billnumber.config(width = len(self.billnumber.get())+1 if len(self.billnumber.get()) > 20 else 20))
        self.billnumber.grid(column=4, row=6, sticky="w")

        tk.Label(self.right, text="Collected:", pady=10).grid(column=3, row=7)
        self.collected = tk.Entry(self.right)
        self.collected.bind("<Key>", lambda e: self.collected.config(width = len(self.collected.get())+1 if len(self.collected.get()) > 20 else 20))
        self.collected.grid(column=4, row=7, sticky="w")

        tk.Label(self.right, text="Referal Fees:", pady=10).grid(column=3, row=8)
        self.referal = tk.Entry(self.right)
        self.referal.bind("<Key>", lambda e: self.referal.config(width = len(self.referal.get())+1 if len(self.referal.get()) > 20 else 20))
        self.referal.grid(column=4, row=8, sticky="w")

        tk.Label(self.right, text="Comment:", pady=10).grid(column=3, row=9)
        self.comment = tk.Entry(self.right)
        self.comment.bind("<Key>", lambda e: self.comment.config(width = len(self.comment.get())+1 if len(self.comment.get()) > 20 else 20))
        self.comment.grid(column=4, row=9, sticky="w")

        #grid configure
        self.right.columnconfigure(0, minsize=75)
        self.right.rowconfigure(11, minsize = 50)

    def loadprojects(self):
        with open("data.json", "r+") as data:
            projectstrings = data.readlines()
            self.maxUID = 0
            self.projects = []
            for project in projectstrings:
                self.projects.append(json.loads(project))
                if self.projects[-1]["UID"] > self.maxUID:
                    self.maxUID = self.projects[-1]["UID"]

    def updatedisplay(self):
        #clear left pane
        for widget in self.left_widgets:
            widget.destroy()
        self.left_widgets = []
        self.UIDs = []

        #fill left pane with projects
        for project in self.projects:
            self.left_widgets.append(tk.Label(self.left.interior, text=project["client"]))
            self.UIDs.append(project["UID"])
            self.left_widgets[-1].pack(anchor="w", padx=25, pady=5)
            self.left_widgets[-1].bind("<1>", lambda e: self.displayproject(self.UIDs[self.left_widgets.index(e.widget)]))


    #sets text of any widget with a delete method
    def settext(self, widget, text):
        widget.delete(0, tk.END)
        widget.insert(0, text)
        if (len(text) > 20):
            widget.config(width=len(text))

    def displayproject(self, UID):
        #save data before changing project
        self.cmd.saveprojectdata()

        uidflag=False
        for project in self.projects:
            if (project["UID"] == UID):
                if (uidflag == True):
                    print("conflicint UID's, something went wrong.")
                    continue

                #project info
                self.activeUID = UID
                self.settext(self.client, project["client"])
                self.settext(self.year, project["ProjectInfo"]["year"])
                self.settext(self.status, project["ProjectInfo"]["status"])
                self.settext(self.industry, project["ProjectInfo"]["industry"])
                self.settext(self.filingdate, project["ProjectInfo"]["filingdate"])
                self.settext(self.credit, project["ProjectInfo"]["credit"])
                self.settext(self.P_rate, project["ProjectInfo"]["rate"])
                self.settext(self.estimatedrevenue, project["ProjectInfo"]["estimatedrevenue"])
                self.settext(self.newclient, project["ProjectInfo"]["newclient"])
                self.settext(self.cpa, project["ProjectInfo"]["CPA"])
                self.settext(self.nextstep, project["ProjectInfo"]["nextstep"])

                #billing info
                self.settext(self.B_rate, project["BillingInfo"]["rate"])
                self.settext(self.bill, project["BillingInfo"]["bill"])
                self.settext(self.billingdescription, project["BillingInfo"]["billingdescription"])
                self.settext(self.datebilled, project["BillingInfo"]["datebilled"])
                self.settext(self.datecollected, project["BillingInfo"]["datecollected"])
                self.settext(self.billnumber, project["BillingInfo"]["billnumber"])
                self.settext(self.collected, project["BillingInfo"]["collected"])
                self.settext(self.referal, project["BillingInfo"]["referal"])
                self.settext(self.comment, project["BillingInfo"]["comment"])

                uidflag = True
