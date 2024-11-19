from gbd_core.api import GBD

f=open("../instances_families.txt")
lines=f.readlines()
fams = lines[0].split()[1].split(",")

famstring = "(family=" + fams[0]

for i in range(1, len(fams)):
    famstring += " or family=" + fams [i]
famstring += ")"


instlist = []
with GBD(["/nfs/home/rzipperer/git/Kissat_hyperparamoptimization/instances/database/meta.db" , "/nfs/home/rzipperer/git/Kissat_hyperparamoptimization/instances/database/instances.db"]) as gbd:
    
    feat = ["instances:local"]
    df = gbd.query ( "(track=main_2023 or track=main_2024) and " + famstring + " and minisat1m!=yes", resolve = feat)
    print(df["local"].tolist())
    instlist = df["local"].tolist()

f.close()


for i in list(map(lambda x : ("../instances/train/" + x.split("/")[-1])[:-3], instlist)):
    f2 = open('../instances/train/0.txt','w')