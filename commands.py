from datetime import datetime
import json
import tkinter as tk

class COMMANDS():
    def __init__(self, app):
        self.app = app


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
