from datetime import datetime
import json
import tkinter as tk
from tkinter import filedialog
import filesave

class COMMANDS():
    def __init__(self, app):
        self.app = app

    def searchProjects(self, uid):
        foundFlag = False
        for project in self.app.projects:
            if project["UID"] == uid and foundFlag == False:
                out = project
                foundFlag == True
            elif project["UID"] == uid and foundFlag == True:
                print("Error: Duplicate UID's Found. Returning First Item Found")

        return out

    def saveprojectdata(self, event=None):
        for project in self.app.projects:
            if project["UID"] == self.app.activeUID:

                self.app.projects[self.app.projects.index(project)]["client"] = self.app.client.get()
                self.app.projects[self.app.projects.index(project)]["ProjectInfo"]["year"] = self.app.year.get()
                self.app.projects[self.app.projects.index(project)]["ProjectInfo"]["status"] = self.app.status.get()
                self.app.projects[self.app.projects.index(project)]["ProjectInfo"]["industry"] = self.app.industry.get()
                self.app.projects[self.app.projects.index(project)]["ProjectInfo"]["filingdate"] = self.app.filingdate.get()
                self.app.projects[self.app.projects.index(project)]["ProjectInfo"]["credit"] = self.app.credit.get()
                self.app.projects[self.app.projects.index(project)]["ProjectInfo"]["rate"] = self.app.P_rate.get()
                self.app.projects[self.app.projects.index(project)]["ProjectInfo"]["estimatedrevenue"] = self.app.estimatedrevenue.get()
                self.app.projects[self.app.projects.index(project)]["ProjectInfo"]["newclient"] = self.app.newclient.get()
                self.app.projects[self.app.projects.index(project)]["ProjectInfo"]["CPA"] = self.app.cpa.get()
                self.app.projects[self.app.projects.index(project)]["ProjectInfo"]["nextstep"] = self.app.nextstep.get()

                self.app.projects[self.app.projects.index(project)]["BillingInfo"]["rate"] = self.app.B_rate.get()
                self.app.projects[self.app.projects.index(project)]["BillingInfo"]["bill"] = self.app.bill.get()
                self.app.projects[self.app.projects.index(project)]["BillingInfo"]["billingdescription"] = self.app.billingdescription.get()
                self.app.projects[self.app.projects.index(project)]["BillingInfo"]["datebilled"] = self.app.datebilled.get()
                self.app.projects[self.app.projects.index(project)]["BillingInfo"]["datecollected"] = self.app.datecollected.get()
                self.app.projects[self.app.projects.index(project)]["BillingInfo"]["billnumber"] = self.app.billnumber.get()
                self.app.projects[self.app.projects.index(project)]["BillingInfo"]["collected"] = self.app.collected.get()
                self.app.projects[self.app.projects.index(project)]["BillingInfo"]["referal"] = self.app.referal.get()
                self.app.projects[self.app.projects.index(project)]["BillingInfo"]["comment"] = self.app.comment.get()

                with open("data.json", "w+") as data:
                    for project in self.app.projects:
                        data.write(json.dumps(project)+"\n")
                self.app.loadprojects()
                self.app.updatedisplay()
                break

    def deleteprojectdata(self, event=None):

        #pop data from memory
        for project in self.app.projects:
            if project["UID"] == self.app.activeUID:
                UID = project["UID"]
                self.app.projects.pop(self.app.projects.index(project))
                break

        #pop data for storage
        with open("data.json", "w+") as data:
            for project in self.app.projects:
                data.write(json.dumps(project)+"\n")

        #reload data to memory and refresh display
        self.app.loadprojects()
        self.app.updatedisplay()
        self.app.displayproject(self.app.maxUID)

    def createnewproject(self, event=None):
        self.app.maxUID+=1
        time = datetime.now()
        newp = {
            "UID" : self.app.maxUID,
            "client":"New Client",
            "ProjectInfo":
            {
                "year" : str(time.year),
                "status" : "1-whatever status 1 means",
                "industry" : "",
                "filingdate" : "",
                "credit" : "",
                "rate" : "",
                "estimatedrevenue" : "",
                "newclient" : "",
                "CPA" : "",
                "nextstep" : ""
            },

            "BillingInfo":
            {
                "rate" : "",
                "bill" : "",
                "billingdescription" : "",
                "datebilled" : "",
                "datecollected" : "",
                "billnumber" : "",
                "collected" : "",
                "referal":"",
                "comment" : ""
            }
        }

        self.app.projects.append(newp)
        self.app.displayproject(self.app.maxUID)
        self.saveprojectdata()
        self.app.loadprojects()
        self.app.updatedisplay()

    def confirmdeletepop(self, event=None):
        top = tk.Toplevel()
        top.wm_title("Are You Sure?")

        msg = tk.Label(top, text="Do you want to delete this project?", pady=10)
        msg.pack()

        top.y = tk.Button(top, text="Yes", width=25, height=2)
        top.y.pack(side=tk.RIGHT)
        top.y.bind("<ButtonPress-1>", self.deleteprojectdata)
        top.y.bind("<ButtonRelease-1>", lambda e: top.destroy())
        tk.Button(top, text="No", command= top.destroy, width=25, height=2).pack(side=tk.LEFT)

    def saveasSpreadSheet(self, event=None):
        top = tk.Toplevel()
        top.wm_title("Save as Spreadsheet")

        tk.Label(top, text="Select Entries to Save", pady=10).pack()

        f = tk.Frame(top)
        f.pack()

        self.selectedprojects = []
        cbvars = [] #list of (id, variable) tuples
        for project in self.app.projects:
            cbvars.append((project["UID"],tk.IntVar()))
            tk.Checkbutton(f, text=project["client"], variable = cbvars[-1][1], command= lambda: self.updateSelectedProjects(cbvars)).pack()

        s = tk.Button(f, text="Save As...", pady=10, padx=10)
        s.bind("<ButtonPress-1>", lambda e: filesave.saveasSpread(filedialog.asksaveasfilename(initialdir = "/",title = "Save File",filetypes = (("csv files","*.csv"),("all files","*.*"))), self.selectedprojects))
        s.bind("<ButtonRelease-1>", lambda e: top.destroy())
        s.pack()

    def updateSelectedProjects(self, data):
        self.selectedprojects=[]
        for t in data:
            if (t[1]):
                self.selectedprojects.append(self.searchProjects(t[0]))

    def alert(self, message, title):
        top = tk.Toplevel()
        top.wm_title(title)

        msg = tk.Label(top, text=message, pady=10)
        msg.pack()

        btn = tk.Button(top, text="Ok", width=25, height=2, command= top.destroy)
        btn.pack()


    def findCollected(self):
        collected=0
        ar=0
        for project in self.app.projects:
            if project["BillingInfo"]["collected"].lower().strip() == "yes":
                collected += int(project["BillingInfo"]["bill"])
            elif project["BillingInfo"]["collected"].lower().strip() == "no":
                ar += int(project["BillingInfo"]["bill"])
        self.alert("Collected: "+str(collected)+"\nAR: "+str(ar),"Collected/AR")
