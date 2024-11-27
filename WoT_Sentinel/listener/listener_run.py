import time
import os
import subprocess
import json
import database.db_connector
import json
import datetime
from data import data
from datetime import date
#docker ps -a --format {{.Status}},{{.ID}}
try:
    #update status values when starts the service
    process1 = subprocess.Popen(['docker','ps','-a','--format', '{{.Status}},{{.ID}}'], stdout=subprocess.PIPE)
    output1, error1 = process1.communicate()
    output1 = output1.decode('utf-8')
    if output1 != "":
        output1= output1.split("\n")
        for i in range(len(output1)-1):
            line = output1[i].split(",")
            status0 = line[0]
            id_container = line[1]
            id_container = id_container[0:12]
            status1 = status0.split(" ")
            if(status1[0]!="Kill" and status1[0]!="Die"):
                if(status1[0] == "Up"):
                    status = "running"
                if(status1[0] == "Exited"):
                    status = "exited"
                if(status1[0] == "Created"):
                    status = "created"
                if(status1[0] == "Restarting"):
                    status = "restarting"
                try:
                    database.db_connector.update_container_status(id_container,status)
                except: 
                    print("")

    while True: 
        #update status values
        process = subprocess.Popen(['docker','events','--since', '15s', '--filter', 'type=container', '--format', '{{.Status}},{{.ID}}', '--until', '0s'], stdout=subprocess.PIPE)

        output, error = process.communicate()
        output = output.decode('utf-8')
        #print("actualziar status")
        if output != "":
            output = output.split("\n")
            for i in range(len(output)-1):
                line = output[i].split(",")
                status = line[0]
                id_container = line[1]
                id_container = id_container[0:12]
                if(status!="kill" and status!="die"):
                    if(status == "start"):
                        status = "running"
                    if(status == "attach"):
                        status = "running"
                    if(status == "stop"):
                        status = "exited"
                    if(status == "create"):
                        status = "created"
                    if(status == "restart"):
                        status = "restarting"
                    if(status == "destroy"):
                        status = "removing"
                    if(status == "exec_start: bash"):
                        status = "running"
                    try:
                        database.db_connector.update_container_status(id_container,status)
                        print("Updated!",id_container,status)
                    except:
                        print("nope")

        #update factor utilization values
        names_app = database.db_connector.select_all_names_app()
        #names = database.db_connector.select_all_names()
        for i in range(len(names_app)):

            status_containers,containers_id = database.db_connector.select_all_status(names_app[i][0])
            cont_rows = database.db_connector.select_container_rows(containers_id[0][0])
            print(status_containers)
            #Agrega las apps al supervision system
            if(len(cont_rows) == 1):
                print("se va a registrar")
                process = subprocess.Popen(['curl','-G','http://localhost:22000/replacesolution/'+names_app[i][1]+'.yml/3/1/0'], stdout=subprocess.PIPE)
                output, error = process.communicate()
                output = output.decode('utf-8')
                print(output)
                time.sleep(5)

            #curl -G http://localhost:22004/v2/aggregates/tps.yml/END/60/0/status-tps

            process = subprocess.Popen(['curl','-G','http://localhost:22004/v2/aggregates/'+names_app[i][1]+'.yml/END/60/0/status-'+names_app[i][1]], stdout=subprocess.PIPE)
            output, error = process.communicate()
            output = output.decode('utf-8')
            output_json = json.loads(output)
            #print(output_json)
            name_appli = names_app[i][1]
            if(output_json["msg"] == "documents found"):
                print("si se encontraron documentos")
                c1 = 3
                c2 = 5
                c3 = 0
                app_graph = database.db_connector.select_app_graph(name_appli)[0]
                output_json_str = json.dumps(output_json)
                """if(app_graph==0):
                    processG = subprocess.Popen(['curl','-G','http://localhost:22003/model/structure/'+name_appli+'.yml'], stdout=subprocess.PIPE)
                    output, error = processG.communicate()
                    output = output.decode('utf-8')
                    output_json_G = json.loads(output)
                    output_json_G_str = json.dumps(output_json_G)
                    database.db_connector.insert_app_graph(name_appli,output_json_G_str,output_json_str)
                else:
                    print("si hay registro")"""
                for i in range(0,len(containers_id)):
                    values = output_json["data"]["status"]["data_status"]["data"][c1]
                    levels = output_json["data"]["status"]["data_status"]["data"][c2]
                    index_cont = output_json["data"]["status"]["data_status"]["index"][c3]
                    print(levels)
                    c1 = c1 + 6
                    c2 = c2 + 6
                    c3 = c3 + 6
                    #positions supervision system cpu, fs, memory, net
                    if(levels[0] == "low"):
                        cpu_lvl = 1
                    if(levels[1] == "low"):
                        fs_lvl = 1
                    if(levels[2] == "low"):
                        mem_lvl = 1
                    if(levels[3] == "low"):
                        net_lvl = 1
                    if(levels[0] == "medium"):
                        cpu_lvl = 2
                    if(levels[1] == "medium"):
                        fs_lvl = 2
                    if(levels[2] == "medium"):
                        mem_lvl = 2
                    if(levels[3] == "medium"):
                        net_lvl = 2
                    if(levels[0] == "high"):
                        cpu_lvl = 3
                    if(levels[1] == "high"):
                        fs_lvl = 3
                    if(levels[2] == "high"):
                        mem_lvl = 3
                    if(levels[3] == "high"):
                        net_lvl = 3
                    container_id,container_id_long,stat = database.db_connector.select_container_id(index_cont)
                    utility = database.db_connector.select_containers_utility(container_id)
                    #print("utility:")
                    #print(utility)
                    #print("utility obtained:")
                    #print(values)
                    if(stat == "exited" or stat == "removing"):
                        cpu_lvl = 0
                        mem_lvl = 0
                        net_lvl = 0
                        fs_lvl = 0
                    if(utility[6] == 0 or utility[7] == 0 or utility[8] == 0 or utility[9] == 0):
                        datetime1 = str(datetime.datetime.now())
                        datetime1 = datetime1.split(".")
                        database.db_connector.insert_containers_utility(container_id,container_id_long,values[0],values[2],values[3],values[1],cpu_lvl,mem_lvl,net_lvl,fs_lvl,datetime1[0],utility[11])
                        database.db_connector.update_app_graph(name_appli,output_json_str)
                    else:
                        if(utility[6] != cpu_lvl or utility[7] != mem_lvl or utility[8] != net_lvl or utility[9] != fs_lvl):
                            datetime2 = str(datetime.datetime.now())
                            datetime2 = datetime2.split(".")
                            database.db_connector.insert_containers_utility(container_id,container_id_long,values[0],values[2],values[3],values[1],cpu_lvl,mem_lvl,net_lvl,fs_lvl,datetime2[0],utility[11])
                            database.db_connector.update_app_graph(name_appli,output_json_str)
                        else:
                            print("No han cambiado los niveles de utilizacion")
            else:
                print("no se encontraron documentos")
        
        print("")
        print("check http://localhost:8000/index.html to see your containers")
        print("you also can check your avatar in http://localhost:22005/solutions/")
        print("")
        time.sleep(3)
        
except KeyboardInterrupt:
    print('Interrupted!')

