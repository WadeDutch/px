import csv

def saveasSpread(fname, data):
    if fname == "":
        return
    if not fname[-1:-5:-1] == "vsc.":
        fname += ".csv"


    titlerow = ["Client"]+["Project Info"]+["" for i in range(len(data[0]["ProjectInfo"]))]+["Billing Info"]+["" for i in range(len(data[0]["BillingInfo"])-1)]
    titlerow2 = [""]+list(data[0]["ProjectInfo"].keys())+[""]+list(data[0]["BillingInfo"].keys())

    table = [[project["client"]]+list(project["ProjectInfo"].values())+[""]+list(project["BillingInfo"].values()) for project in data]
    table = [titlerow] + [titlerow2] + table

    with open(fname, "w+", newline='') as csvfile:
        writer = csv.writer(csvfile)
        for row in table:
            writer.writerow(row)
