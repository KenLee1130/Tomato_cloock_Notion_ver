# -*- coding: utf-8 -*-
"""
Created on Wed Sep 20 17:37:37 2023

@author: User
"""
import requests
import tkinter as tk

class Notion_connection:
    def __init__(self, project_name):
        self.project_name = project_name
        
        self.token = 'secret_MwY2PiK14BgS4D3xi7PAej27pER3Ju5MOSRMi9lkjJp'
        self.database_id = "63c442d2-f770-4c03-91cd-946692889004"
        r = requests.post(
            url="https://api.notion.com/v1/databases/{}/query".format(self.database_id) ,
            headers={"Authorization": "Bearer " + self.token, "Notion-Version": "2021-05-13"})

        self.data = r.json()

    def Choose_project_number(self):
        def which_project(project_idx, project_name):
            if self.data['results'][project_idx]['properties']['Name']['title'][0]['text']['content'] == project_name:
                return project_idx
            
        project_number = 0
        for project_idx in range(len(self.data['results'])):
            project_number = which_project(project_idx, self.project_name)
            if project_number != None:
                break
        return project_number
    
    def Uncheck_project_info(self):
        uncheck_project_name = []
        tomato_remaining = []
        for project_idx in range(len(self.data['results'])):
            if self.data['results'][project_idx]['properties']['Check']['checkbox'] == False:
                uncheck_project_name.append(self.data['results'][project_idx]['properties']['Name']['title'][0]['text']['content'])
                tomato_remaining.append(self.data['results'][project_idx]['properties']['預估-實際']['formula']['number'])
        return {'Name list': uncheck_project_name, 'Tomato remaining': tomato_remaining}

    def clock_modification(self, modif):
        project_number = self.Choose_project_number()
        if modif == 'Tomato':
            n = self.data['results'][project_number]['properties']['實際番茄鐘數']['number']
            n += 1
    
            Data = {'parent': {'type': 'database_id', 'database_id': self.database_id}, 
                    'properties':{'實際番茄鐘數':{'id': 'z}}F', 'type': 'number', 'number': n}}}
        elif modif == 'checkbox':
            Data = {'parent': {'type': 'database_id', 'database_id': self.database_id}, 
                    'properties':{'Check': {'id': '|:uh', 'type': 'checkbox', 'checkbox': True}}}
        
        # Send the updated data back to Notion
        page_id_to_update = self.data['results'][project_number]['id']
        update_url = f"https://api.notion.com/v1/pages/{page_id_to_update}"

        response = requests.patch(
            url=update_url,
            json=Data,
            headers={"Authorization": "Bearer " + self.token, "Notion-Version": "2021-05-13"},
        )

        return response.status_code

class GUI:
    def __init__(self):
        import pygetwindow as gw
        self.selection = 0
        self.window = tk.Tk()
        # Check for tkinter windows
        windows = gw.getWindowsWithTitle('Tk')
        if windows:
            print("Tkinter window is open")
        
        # Close the tkinter window
        self.window.destroy()
        self.window = tk.Tk()
        self.window.title('Tomato clock for Projects')
        self.window.geometry('600x400')
        self.window.configure(bg='white')
        self.window.resizable(False, False)

    def Select_project(self, frame):
        Info = Notion_connection('').Uncheck_project_info()
        def radiobutton_used():
            selection = Info['Name list'][radio_state.get()]
            self.selection = selection
            return selection
        radio_state = tk.IntVar()

        for i in range(len(Info['Name list'])):
            radiobutton = tk.Radiobutton(frame, bg="white", text=f"{Info['Name list'][i]}", variable=radio_state, 
                                         value=i, command=radiobutton_used)
            
            radiobutton.grid(row=i+7, column=0, sticky="w")
            mylabel = tk.Label(frame, bg="white", text=f"🍅 remaining: {Info['Tomato remaining'][i]}")  # 建立 label 標籤
            mylabel.grid(row=i+7, column=5, sticky="w")
             
    def window_project_select(self):
        ## Frame 1
        self.frame_projects = tk.Frame(self.window, bg="white")
        self.frame_projects.grid(row=0, column=3)
        title = tk.Label(self.frame_projects, bg="white", text="Projects", font=("Comic Sans MS", 20, "bold"))  # 建立 label 標籤
        title.grid(row=0, column=2, sticky="w")
        self.Select_project(self.frame_projects)
        
        ## Frame 2
        self.frame_button = tk.Frame(self.window, bg="white")
        self.frame_button.grid(row=150, column=3)
        def button_clicked():
            self.frame_projects.destroy()
            self.frame_button.destroy()
            self.window_clock(self.selection)
            
            return
        self.loadimage = tk.PhotoImage(file="C:/Users/User/Desktop/tomato_clock/pngwing.com (1).png")
        button = tk.Button(self.frame_button, image=self.loadimage, text="Start", font=("Arial", 14, "bold"), padx=5, pady=5, 
                           bg="white", fg="lawngreen", border='0', command=button_clicked)

        button.grid(row=80, column=6)
        # Icon of this GUI
        self.window.iconbitmap('C:/Users/User/Desktop/tomato_clock/tomato_vegetables.ico')
        
        # Let the GUI exist
        self.window.mainloop()
    
    def window_clock(self, project_selection):
        import time
        self.window.title(f'Tomato clock for {project_selection}')
        self.window.geometry('500x400')
        frame_title = tk.Frame(self.window, bg='white')
        frame_title.grid(row=0, column=3)
        frame_clock = tk.Frame(self.window, bg='white')
        frame_clock.grid(row=5, column=3)
        title = tk.Label(frame_title, text=f"{project_selection} 🍅", bg='white', font=("Comic Sans MS", 20, "bold"))  # 建立 label 標籤
        title.grid(row=0, column=1, sticky="w")
        
        def line_notify(msg):
            token = 'sTS3haKSxmxz5ZItVgi4q25dWUKB64nkdvB7JdPUxmi'  # 填入你的token
            url = 'https://notify-api.line.me/api/notify'
            headers = {
                'Authorization': 'Bearer ' + token
            }
            data = {
                'message': msg
            }
            requests.post(url, headers=headers, data=data)
        
        # Start tomato clock
        def tomato_clock(work_time=45):
            remain_time = work_time*60
            bb = time.strftime('/  %M:%S', time.gmtime(remain_time))
            lb2.configure(text=bb)
            lb3.configure(text='Remaining/Total time')
            for i in range(work_time*60):
                remain_time -= 1
                aa = time.strftime('%M:%S', time.gmtime(remain_time))
                lb.configure(text=aa)
                frame_title.update()
                time.sleep(1)
                if remain_time == 0:
                    Notion_connection(project_selection).clock_modification('Tomato')
                    line_notify('Finish one 🍅!')
                    relax()
                    
        
        # Rest time
        def relax(break_time=15):
            remain_time = break_time*60
            bbb = time.strftime('/  %M:%S', time.gmtime(remain_time))
            lb2.configure(text=bbb)
            lb3.configure(text='Remaining/Total time')
            for i in range(break_time*60):
                remain_time -= 1
                aaa = time.strftime('%M:%S', time.gmtime(remain_time))
                lb.configure(text=aaa)
                frame_title.update()
                time.sleep(1)
                if remain_time == 0:
                    line_notify('Time to work~')
                    frame_title.destroy()
                    frame_clock.destroy()
                    self.window_project_select()
        
        # Finish
        def finish():
            Notion_connection(project_selection).clock_modification('Tomato')
            Notion_connection(project_selection).clock_modification('checkbox')
            line_notify(f'{project_selection} is finished!')
            frame_title.destroy()
            frame_clock.destroy()
            self.window_project_select()

        # Timing
        lb = tk.Label(frame_clock, text=' ', bg='white', fg='black', font='Verdana 16 bold')
        lb.grid()
         
        # Fix time
        lb2 = tk.Label(frame_clock, text=' ', bg='white', fg='black', font='Verdana 16 bold')
        lb2.grid()
        
        # remain time/ total time
        lb3 = tk.Label(frame_clock, text=' ', bg='white', fg='black', font='Verdana 16 bold')
        lb3.grid()

        # Buttons 
        Button1 = tk.Button(frame_clock, text='Start', bg='orange', fg='black', font='Verdana 13 bold', 
                            width=15, height=1, command=tomato_clock)
        Button1.grid()

        Button2 = tk.Button(frame_clock, text='Finish', bg='cornflowerblue', fg='black', font='Verdana 13 bold', 
                            width=15, height=1, command=finish)
        Button2.grid()
    

        
if __name__ == "__main__":
    GUI().window_project_select()

    