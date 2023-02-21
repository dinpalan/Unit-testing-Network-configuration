#! /usr/bin/env python3
#SHEBANG
#import modules with methods in this space
import csv
import os

#Objective 1 -File Parsing and Verification 
def Parse_file():
        try:     
                with open('sshInfo.csv', 'r') as f:                
                        reader = csv.reader(f)
                        the_whole_file = list(reader)
                        no = len(the_whole_file)
                        a=1
                        details=[]
                        iplist=[]
                        while a<int(no):
                        
                                column1 = 0
                                device = the_whole_file[a][column1]
                                column2 = 1
                                usernames = the_whole_file[a][column2]
                                column3 = 2
                                passwords = the_whole_file[a][column3]
                                column4 = 3
                                ips = the_whole_file[a][column4]
                                detail = {
                                        'device_type': device,
                                        'username': usernames,
                                        'password': passwords,
                                        'ip': ips,
                                        }
                                details.append(detail)
                                iplist.append(the_whole_file[a][column4])
                                a=int(a)+1;
                return details, iplist
                                                             
        except:                            
                return -1, -1
        
#Objectiv 2 - IP Address Validation
def IsValid():  
        n=len(Parse_file()[1])
        r=0
        val=[]
        while r<n:
                ip=Parse_file()[1][r]
                a=ip.split('.')
                if ( (len(a)==4) and ( 1<=int(a[0])<=223) and (int(a[0])!=127) and (int(a[0])!=169 or int (a[1])!=254) and (0<= int(a[1])<=255) and (0<=int(a[2]) <=255) and (0<=int(a[3])<=255)):
                        val.append(True)
                else:
                         val.append(False)
                r=r+1;
        return val
def Val_IP():
        n=len(IsValid())
        r=0
        val=[]
        while r<n:
                ip=Parse_file()[1][r]
                if IsValid()[r] == True:
                        val.append(ip)
                else:
                         continue
                r=r+1;
        return val

#Objective 3 - IP Address Connectivity
def Is_connected():
        n=len(Val_IP())
        r=0
        ping=[]
        while r<n:
                ip=Val_IP()[r]
                h = os.system(f"ping {ip} -c 2 >/dev/null")
                if h == 0:
                        ping.append(True)
                else:
                        ping.append(False)
                r=r+1;                
        return ping
def Connected_devices():
        n=len(Is_connected())
        r=0
        conn=[]
        while r<n:
                ip=Val_IP()[r]
                if Is_connected()[r] == True:
                        conn.append(ip)
                else:
                         continue
                r=r+1;
        return conn

#Objective 4 - iBGP Configuration
from netmiko import ConnectHandler
from prettytable import PrettyTable
def Bgp_config():
        with open('bgp.conf', 'r') as f:
                reader = csv.reader(f)
                z = list(reader)
                H=len(z)-1
                N=0;
                while N<H:
                        #comparing verified IPs with IPs which we are using for connectivity
                        if Connected_devices()[N] == Parse_file()[1][N]:
                                details = Parse_file()[0][N]
                                config_commands = [f'router bgp {z[N+1][1]}',f'neighbor {z[N+1][2]} remote-as {z[N+1][3]}',f'network {z[N+1][4]} mask {z[N+1][5]}',f'network {z[N+1][6]} mask {z[N+1][7]}'];
                                vty = ConnectHandler(**details)
                                vty.enable()
                                output1=vty.send_config_set(config_commands, delay_factor=5)
                                vty.disconnect()
                        else:
                                continue
                        N=N+1;
                N=0;
                #verification of configurations made
                while N<H:
                        if Connected_devices()[N] == Parse_file()[1][N]:
                                details = Parse_file()[0][N]
                                config_commands = [f'router bgp {z[N+1][1]}',f'neighbor {z[N+1][2]} remote-as {z[N+1][3]}',f'network {z[N+1][4]} mask {z[N+1][5]}',f'network {z[N+1][6]} mask {z[N+1][7]}'];
                                vty = ConnectHandler(**details)
                                output = vty.send_command("show ip bgp neighbors")
                                print(f"BGP is configured in R{N+1} - Verification is given below")
                                print(output)
                                output1 = vty.send_command(f"ping {z[N+1][4]}")
                                print(output1)
                                output2 = vty.send_command(f"ping {z[N+1][6]}")
                                print(output2)
                                vty.disconnect()
                        else:
                                continue
                        N=N+1;
                N=0;
                #Creating a Pretty Table output
                try:
                        x = PrettyTable()
                        x.field_names = [z[N]]
                        while N<H:                        
                                x.add_row([z[N+1]])
                                N=N+1;
                        return x
                except:
                        return -1
                
#write your main function here                
def main():        
    try:        
            Bgp_config()
    except KeyboardInterrupt:        
        print("Exiting because of program interpreted by user"); print("Thanks for using my application");       
              
if __name__=='__main__':
       main() 
