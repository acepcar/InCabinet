import wx
#from databases import Database
import sqlite3
import wx.lib.agw.aquabutton as AB
import wx.lib.agw.gradientbutton as GB

#NA PANELIMA SU GUMBOVI DISABLEANI (UMJESTO TEXTBOXOVA SU STAVLJENI ZBOG FERESH FUNKCIJE KOJU NISMO IMPLEMENTIRALI)
#mogu se svaki put hideati svi gumbi, ali nema potrebe zbog pasivnosti, i za tekst..
#pocetna NE ODLOGIRAVA, vise korisnika u istoj app,mogu napraviti i da odlogira


#funkcija za stvaranje baze podataka
def databaseFunction():
    global c
    global dic
    global connector
    global odsjeci
    #stvaranje connectora, cursora i povezivanje i stvaranje baze
    connector = sqlite3.connect('example.db')
    c= connector.cursor()
    #IF NOT EXISTS osigurava da se nova baza ne stvara svaki put pri pokretanju programa, create index osigurava jedinstvenost korisničkog imena (nema duplih unosa)
    c.execute('''CREATE TABLE IF NOT EXISTS DatabaseInCabinet(password INTEGER, username VARCHAR(100), titula VARCHAR(100), name VARCHAR(100), role INTEGER, odsjek VARCHAR(100), status VARCHAR(50))''')
    c.execute("CREATE  UNIQUE INDEX IF NOT EXISTS index_part_name ON DatabaseInCabinet(username)")
   
    values = [
        {"username": "bb1024", "password": 9221, "name": "Boris Bandurina", "titula": "izv.prof.dr.sc","role":1,"odsjek":"Odsjek za informatologiju","status":"P"},
        {"username": "sft3321", "password": 8754, "name": "Sanjica Faletar Tanacaković", "titula": "prof.dr.sc","role":1,"odsjek":"Odsjek za informatologiju","status":"P"},
        {"username": "dh3123", "password": 4322, "name": "Damir Hasenay", "titula": "prof.dr.sc","role":1,"odsjek":"Odsjek za informatologiju","status":"P"},
        {"username": "kf0918", "password": 2985, "name": "Kristina Feldvari", "titula": "doc.dr.sc","role":1,"odsjek":"Odsjek za informatologiju","status":"P"},
        
        {"username": "dv5076", "password": 4331, "name": "Danica Vladić", "titula": "prof.dr.sc","role":1,"odsjek":"Odsjek za psihologiju","status":"N"},
        {"username": "as1111", "password": 1001, "name": "Ana Šobot", "titula": "izv.prof.dr.sc","role":1,"odsjek":"Odsjek za psihologiju","status":"P"},
        {"username": "is2131", "password": 5479, "name": "Ivan Skorupan", "titula": "doc.dr.sc","role":1,"odsjek":"Odsjek za psihologiju","status":"N"},
        {"username": "pb7651", "password": 2008, "name": "Petar Bubica", "titula": "doc.dr.sc","role":1,"odsjek":"Odsjek za psihologiju","status":"P"},
        
        {"username": "df9129", "password": 2048, "name": "Dora Franjić", "titula": "izv.prof.dr.sc","role":1,"odsjek":"Odsjek za pedagogiju","status":"P"},
        {"username": "fd0201", "password": 1604, "name": "Filip Dutina", "titula": "prof.dr.sc","role":1,"odsjek":"Odsjek za pedagogiju","status":"N"},
        {"username": "ea0402", "password": 1805, "name": "Ena Aničić", "titula": "doc.dr.sc","role":1,"odsjek":"Odsjek za pedagogiju","status":"P"},
        {"username": "ik1405", "password": 1307, "name": "Ivana Kurelja", "titula": "doc.dr.sc","role":1,"odsjek":"Odsjek za pedagogiju","status":"P"},
        
        {"username": "ds2303", "password": 1806, "name": "Danijel Strbad", "titula": "izv.prof.dr.sc","role":1,"odsjek":"Odsjek za povijest","status":"N"},
        {"username": "kg1811", "password": 2309, "name": "Karla Gale", "titula": "prof.dr.sc","role":1,"odsjek":"Odsjek za povijest","status":"P"},
        {"username": "pg1412", "password": 1995, "name": "Patricia Gale", "titula": "izv.prof.dr.sc","role":1,"odsjek":"Odsjek za povijest","status":"P"},
        {"username": "iv2712", "password": 1609, "name": "Ivana Vladić", "titula": "doc.dr.sc","role":1,"odsjek":"Odsjek za povijest","status":"P"},

        {"username": "ft4865", "password": 1234, "name": "Filip Todorić", "titula": "student","role":0,"odsjek":"FFOS","status":"P"},
        {"username": "ds3190", "password": 9909, "name": "Dora Šegvić", "titula": "student","role":0,"odsjek":"FFOS","status":"P"},
        {"username": "ac6191", "password": 8808, "name": "Antonela Čepčar", "titula": "student","role":0,"odsjek":"FFOS","status":"P"},]
    #unošenje podataka u bazu podataka (IGNORE) za svako pokretanje programa
    c.executemany("INSERT OR IGNORE INTO DatabaseInCabinet(username, password, name, titula,role,odsjek,status) VALUES (:username, :password, :name, :titula,:role,:odsjek,:status)",values)
    dic = {"bb1024": ["P01","P02","P03","P04"], "ds2303": ["P01"],"sft3321":["P01","P02","P03","P04"],"dh3123":["P01","P02","P03"],"kf0918":["P01","P02","P03","P04"],
           "dv5076":["P01","P02"],"as1111":["P01","P03","P04"],"is2131":["P01","P02","P03","P04","P05","P06"],"pb7651":["P01","P02","P03","P04"],
           "df9129":["P01","P02","P03","P04"],"fd0201":["P01","P02","P03","P04"],"ea0402":["P01","P02","P03","P04"],"ik1405":["P01","P02","P03","P04"],
           "kg1811": ["P01","P02","P03","P04"], "pg1412":["P01","P02","P03","P04"],"iv2712":["P01","P02","P03","P04"]} #grupe kojima profesor predaje
    
    #c.execute("UPDATE DatabaseInCabinet SET name = ? WHERE username = ?", ("Sanjica Faletar","sft3321"))
    #connector.commit() - samo prvo prezime
    
    odsjeci = ["Odsjek za informatologiju", "Odsjek za psihologiju", "Odsjek za pedagogiju", "Odsjek za povijest"] #lista odsjeka
#zadnji panel, ime profesora i aktivnost (kada je logiran student)    
class APanel(wx.Panel):
    
    def __init__(self,parent):
        wx.Panel.__init__(self,parent,pos=(0,0),size=(2000,2000))
        self.frame = parent
        
    def ShowActivity(self,status,name,user):
        #postavljanje gumbova
        name_button = GB.GradientButton(self, bitmap=None,pos=(90,30),size=(200,50),label=name)
        name_button.SetTopStartColour((105,105,105))
        name_button.SetTopEndColour((105,105,105))
        name_button.SetBottomStartColour((105,105,105))
        name_button.SetBottomEndColour((105,105,105))
        name_button.Disable()
        back_button = GB.GradientButton(self, bitmap=None,pos=(165,300),label="Back")
        back_button.Bind(wx.EVT_BUTTON,self.backP)
        poc_button = GB.GradientButton(self, bitmap=None,pos=(5,5),size=(50,30),label="Početna")
        poc_button.Bind(wx.EVT_BUTTON,self.pocetna)
        logout_button = GB.GradientButton(self, bitmap=None,pos=(300,300),label="Log out")
        logout_button.Bind(wx.EVT_BUTTON,lambda event: self.logout(event,user))
        activity = status[0][0]
        #postavljanje aktivnosti
        if activity == "A":
            a_button = GB.GradientButton(self, bitmap=None,pos=(90,150),size=(200,50),label="AKTIVAN(U KABINETU)")
            a_button.SetTopStartColour((127,255,0))
            a_button.SetTopEndColour((127,255,0))
            a_button.SetBottomStartColour((127,255,0))
            a_button.SetBottomEndColour((127,255,0))
            a_button.Disable()
        elif activity == "P":
            a_button = GB.GradientButton(self, bitmap=None,pos=(90,150),size=(200,50),label="NEAKTIVAN (NIJE U KABINETU)")
            a_button.SetTopStartColour((139,0,0))
            a_button.SetTopEndColour((139,0,0))
            a_button.SetBottomStartColour((139,0,0))
            a_button.SetBottomEndColour((139,0,0))
            a_button.Disable()
        else:
            a_button = GB.GradientButton(self, bitmap=None,pos=(90,150),size=(200,50),label="NE KORISTI APLIKACIJU")
            a_button.SetTopStartColour((255,255,0))
            a_button.SetTopEndColour((255,255,0))
            a_button.SetBottomStartColour((255,255,0))
            a_button.SetBottomEndColour((255,255,0))
            a_button.Disable()
            
            
    #funkcija za nazad   
    def backP(self,event):
        self.frame.panel_fifth.Hide()
        for i in l_buttons:
             i.Show()
        self.frame.panel_four.Show()
        self.Layout()
    #funkcija za početnu
    def pocetna(self,event):
        self.frame.panel_fifth.Hide()
        self.frame.panel.Show()
        self.Layout()
    #log out
    def logout(self,event,username):
        c.execute("UPDATE DatabaseInCabinet SET status = ? WHERE username = ?",("P",username))
        connector.commit()
        self.frame.panel_fifth.Hide()
        self.frame.panel.Show()
        self.Layout()
        
        
#panel za odsjeke   
class PanelOdsjek(wx.Panel):
     def __init__(self,parent):
        wx.Panel.__init__(self,parent,pos=(0,0),size=(2000,2000))
        self.frame = parent
        
     def addToOdsjek(self,odsjek):
         global l_buttons
         self.Refresh()
         odsjek_button = GB.GradientButton(self, bitmap=None,pos=(120,30),size=(150,50),label=odsjek)
         odsjek_button.SetTopStartColour((105,105,105))
         odsjek_button.SetTopEndColour((105,105,105))
         odsjek_button.SetBottomStartColour((105,105,105))
         odsjek_button.SetBottomEndColour((105,105,105))
         odsjek_button.Disable()
         back_button = GB.GradientButton(self, bitmap=None,pos=(165,300),label="Back")
         back_button.Bind(wx.EVT_BUTTON,self.back)
         poc_button = GB.GradientButton(self, bitmap=None,pos=(5,5),size=(50,30),label="Početna")
         poc_button.Bind(wx.EVT_BUTTON,self.pocetna)
         c.execute("SELECT titula,name,username,status FROM DatabaseInCabinet WHERE odsjek = ?",(odsjek,))
         fetched = c.fetchall()
         #ovo bi se moglo ubaciti u funkciju
         x=0
         y=-100
         brojac=0
         l_buttons=[]
         #postavljanje profesora na odsjecima
         for i in range(len(fetched)):
             if i%2==0 and i!=0:
                 x=0
             if brojac%2==0:
                 y+=100
             prof_info = GB.GradientButton(self, bitmap=None,pos=(13+x,100+y),size=(180,50),label=fetched[i][0]+ " " + fetched[i][1],align=wx.CENTER)
             if fetched[i][3]=="A":
                 prof_info.SetForegroundColour((76,187,23))
             elif fetched[i][3]=="P":
                 prof_info.SetForegroundColour((255,0,0))
             else:
                 prof_info.SetForegroundColour((255,255,0))
                 
             l_buttons.append(prof_info)
             x+=183
             brojac+=1
         for j in range(len(l_buttons)):
             string = fetched[j][0]+ " " + fetched[j][1]
             self.bindButtonsProf(l_buttons[j],string,fetched[j][2])
             
     def back(self,event):
         self.frame.panel_three.Show()
         for i in l_buttons:
             i.Hide()
         self.frame.panel_four.Hide()
         self.Layout()
         
     def bindButtonsProf(self,button,string,user):
         button.Bind(wx.EVT_BUTTON,lambda event: self.ActivityProf(event,string,user))
        
     def ActivityProf(self,event,string,user):
         c.execute("SELECT status FROM DatabaseInCabinet WHERE username = ?",(user,))
         fetched_status = c.fetchall()
         self.frame.panel_four.Hide()
         for i in l_buttons:
             i.Hide()
         self.frame.panel_fifth.Show()
         self.Layout()
         self.frame.panel_fifth.ShowActivity(fetched_status,string,user)
     def pocetna(self,event):
         self.frame.panel.Show()
         for i in l_buttons:
             i.Hide()
         self.frame.panel_four.Hide()
         self.Layout()
        
        
        
         
    


# application for Professors/Students
class MyPanelStudent(wx.Panel):
    
    def __init__(self,parent):
        wx.Panel.__init__(self,parent,pos=(0,0),size=(2000,2000))
        self.frame = parent
    def addToSPanel(self,value):
        status_p = wx.StaticBox(self,-1)
        sSizer = wx.StaticBoxSizer(status_p,wx.VERTICAL)
        s1 = wx.BoxSizer(wx.HORIZONTAL)
        text_g = wx.StaticText(self,-1,"Odsjeci:",pos=(150,30),size=(60,20),style=wx.ALIGN_CENTRE_HORIZONTAL)
        s1.Add(text_g,0,wx.ALL | wx.CENTER, 100)
        text_g.SetBackgroundColour((192,192,192))
        poc_button = GB.GradientButton(self, bitmap=None,pos=(5,5),size=(50,30),label="Početna")
        poc_button.Bind(wx.EVT_BUTTON,self.pocetna)
        back_button = GB.GradientButton(self, bitmap=None,pos=(150,300),label="Log out")
        
        x=0
        y=-100
        brojac = 0
        l = []
        for i in range(len(odsjeci)):
            if i%2==0 and i!=0:
                x=0
            if brojac%2==0:
                y+=100
            odsjek_info = GB.GradientButton(self, bitmap=None,pos=(33+x,100+y),size=(150,50),label=odsjeci[i])
            l.append(odsjek_info)
            x+=183
            brojac+=1

        for j in range(len(l)):
            self.bindButtons(l[j],odsjeci[j])
        back_button.Bind(wx.EVT_BUTTON,lambda event: self.backMainS(event,value))
       
        
    def backMainS(self,event,value):
        c.execute("UPDATE DatabaseInCabinet SET status = ? WHERE username = ?",("P",value))
        connector.commit()
        self.frame.panel_three.Hide()
        self.frame.panel.Show()
        self.Layout()
    def pocetna(self,event):
        self.frame.panel_three.Hide()
        self.frame.panel.Show()
        self.Layout()
        
    def bindButtons(self,button,odsjek):
         button.Bind(wx.EVT_BUTTON,lambda event: self.listaProfOdsjek(event,odsjek))
        
    def listaProfOdsjek(self,event,odsjek):
        self.frame.panel_three.Hide()
        self.frame.panel_four.Show()
        self.Layout()
        self.frame.panel_four.addToOdsjek(odsjek)
#panel za prof sucelje        
class MyPanel(wx.Panel):
    def __init__(self,parent):
        wx.Panel.__init__(self,parent,pos=(0,0),size=(2000,2000))
        self.frame = parent
        
    def addToPanel(self,status,name,value,titula):
        string = titula + " " + name + " - " + "aktivnost" + " :"
        status_p = wx.StaticBox(self,-1,'Name')
        sSizer = wx.StaticBoxSizer(status_p,wx.VERTICAL)
        s1 = wx.BoxSizer(wx.HORIZONTAL)
        #Može i text, static text, itd..
        ac_button = GB.GradientButton(self, bitmap=None,pos=(100,100),size=(200,50),label="AKTIVAN(U KABINETU)")
        ac_button.SetTopStartColour((127,255,0))
        ac_button.SetTopEndColour((127,255,0))
        ac_button.SetBottomStartColour((127,255,0))
        ac_button.SetBottomEndColour((127,255,0))
        ac_button.Disable()
        ac_button = GB.GradientButton(self, bitmap=None,pos=(40,40),size=(300,50),label=string)
        ac_button.SetTopStartColour((169,169,169))
        ac_button.SetTopEndColour((169,169,169))
        ac_button.SetBottomStartColour((169,169,169))
        ac_button.SetBottomEndColour((169,169,169))
        ac_button.Disable()
        poc_button = GB.GradientButton(self, bitmap=None,pos=(5,5),size=(50,30),label="Početna")
        poc_button.Bind(wx.EVT_BUTTON,self.pocetna)
        #text_name = wx.StaticText(self,-1,string,pos=(40,40),size=(150,50),style=wx.ALIGN_CENTRE_HORIZONTAL)
        #s1.Add(text_name,0,wx.ALL | wx.CENTER, 100)
        text_g = wx.StaticText(self,-1,"Grupe :",pos=(50,170),size=(60,20),style=wx.ALIGN_CENTRE_HORIZONTAL)
        s1.Add(text_g,0,wx.ALL | wx.CENTER, 100)

        back_button = GB.GradientButton(self, bitmap=None,pos=(165,280),label="Log out")
        self.SetBackgroundColour((211,211,211))

        #back_button = wx.Button(self,label='Back',pos=(165, 280),size=(50,25))
        back_button.Bind(wx.EVT_BUTTON,lambda event: self.backMain(event,value))

        string_for_g = ""
        for i in dic[value]:
            string_for_g+=i + " "
        text_ctrl_groups = wx.TextCtrl(self,value=string_for_g,pos=(60, 200),style=wx.TE_READONLY | wx.TE_MULTILINE,name="Groups",size=(100,40))
        s1.Add(text_ctrl_groups,0,wx.ALL | wx.CENTER | wx.EXPAND, 100)
        
    def backMain(self,event,value):
        c.execute("UPDATE DatabaseInCabinet SET status =? WHERE username = ?",("P",value))
        connector.commit()
        self.frame.panel_two.Hide()
        self.frame.panel.Show()
        self.Layout()
        
    def pocetna(self,event):
        self.frame.panel_two.Hide()
        self.frame.panel.Show()
        self.Layout()
        
        
     

class MainPanel(wx.Panel):
    def __init__(self,parent):
        wx.Panel.__init__(self,parent)
        #self.frame = parent


class MyApp(wx.Frame):
    
    def __init__(self):
        super().__init__(parent=None, title='InCabinet',style=wx.DEFAULT_DIALOG_STYLE | wx.MINIMIZE_BOX)
        #panel = wx.Panel(self)
        
        sizer = wx.BoxSizer()
        self.SetSizer(sizer)
        
        panel = MainPanel(self)
        panel.SetBackgroundColour((211,211,211))
        self.panel = panel
        sizer.Add(self.panel, 1, wx.EXPAND)
        self.panel_two = MyPanel(self)
        self.panel_two.SetBackgroundColour((211,211,211))
        sizer.Add(self.panel_two, 1, wx.EXPAND)
        self.panel_two.Hide()
        self.panel_three = MyPanelStudent(self)
        self.panel_three.SetBackgroundColour((211,211,211))
        sizer.Add(self.panel_three, 1, wx.EXPAND)
        self.panel_three.Hide()
        self.panel_four = PanelOdsjek(self)
        self.panel_four.SetBackgroundColour((211,211,211))
        sizer.Add(self.panel_four, 1, wx.EXPAND)
        self.panel_four.Hide()
        self.panel_fifth = APanel(self)
        self.panel_fifth.SetBackgroundColour((211,211,211))
        sizer.Add(self.panel_fifth, 1, wx.EXPAND)
        self.panel_fifth.Hide()
        self.SetSize((400, 400))
        self.Centre()

        self.text_ctrl_usernamefield = wx.TextCtrl(panel, pos=(140, 100))
        self.text_ctrl_passwordfield = wx.TextCtrl(panel, pos=(140, 150),style=wx.TE_PASSWORD)
        self.text_ctrl_usernamefield.SetBackgroundColour((229,229,229))
        self.text_ctrl_passwordfield.SetBackgroundColour((229,229,229))
        
        my_btn_student = GB.GradientButton(panel, label='Login student', pos=(150, 200))
        my_btn_student.Bind(wx.EVT_BUTTON, self.on_press_student)

        my_btn_prof = GB.GradientButton(panel, label='Login professor', pos=(142, 250))
        my_btn_prof.Bind(wx.EVT_BUTTON, self.on_press)

        close_btn = GB.GradientButton(panel, label='Kraj', pos=(320, 320), size=(50,30))
        close_btn.Bind(wx.EVT_BUTTON, self.close)

        
        username_text = wx.StaticText(panel, -1, label="Username:", pos=(80,105), style = wx.ALIGN_CENTER)
        password_text = wx.StaticText(panel, -1, label="Password:", pos=(80,155), style = wx.ALIGN_CENTER)
        
        self.Show()
    
    def newPanel(self):
        self.panel_two.Show()
        #self.panel_three.Hide()
        self.panel.Hide()
        self.Layout()
        
    def newSPanel(self):
        self.panel_three.Show()
        #self.panel_two.Hide()
        self.panel.Hide()
        self.Layout()
    def close(self,event):
        self.Close()

    def on_press(self, event):
        value = self.text_ctrl_usernamefield.GetValue()
        second_value = self.text_ctrl_passwordfield.GetValue()
        self.text_ctrl_usernamefield.Clear()
        self.text_ctrl_passwordfield.Clear()
        if not (value and second_value):
            msg = wx.MessageBox(message="Try again",
                          caption='You did not enter anything',
                          style=wx.OK | wx.ICON_INFORMATION)
        else:
            c.execute("SELECT username FROM DatabaseInCabinet WHERE username = ? AND password = ? AND role = ?",(value,second_value,1))
            if len(c.fetchall())>0:
                c.execute("UPDATE DatabaseInCabinet SET status = ? WHERE username = ?",("A",value))
                connector.commit()
                c.execute("SELECT username,name,titula FROM DatabaseInCabinet WHERE username = ?",(value,))
                lista = c.fetchall()
                name = lista[0][1]
                titula = lista[0][2]
                self.newPanel()
                self.panel_two.addToPanel("AKTIVAN   (U KABINETU)",name,value,titula)
            else:
                 msg = wx.MessageBox(message="Try again",
                          caption='Wrong arguments - Username/Password not correct',
                          style=wx.OK | wx.ICON_INFORMATION)
                
                
    def on_press_student(self, event):
        value = self.text_ctrl_usernamefield.GetValue()
        second_value = self.text_ctrl_passwordfield.GetValue()
        self.text_ctrl_usernamefield.Clear()
        self.text_ctrl_passwordfield.Clear()
        if not (value and second_value):
            msg = wx.MessageBox(message="Try again",
                          caption='You did not enter all information',
                          style=wx.OK | wx.ICON_INFORMATION)

        else:
            c.execute("SELECT username FROM DatabaseInCabinet WHERE username = ? AND password = ? AND role = ?",(value,second_value,0))
            if len(c.fetchall())>0:
                c.execute("UPDATE DatabaseInCabinet SET status = ? WHERE username = ?",("A",value))
                connector.commit()
                self.newSPanel()
                self.panel_three.addToSPanel(value)
            else:
                msg = wx.MessageBox(message="Try again",
                          caption='Wrong arguments - Username/Password not correct',
                          style=wx.OK | wx.ICON_INFORMATION)
                
    
#Main funkcija - u njoj se kreira baza podataka, stvara Frame i otvara se aplikacija
def main():
    databaseFunction();
    app = wx.App()
    frame = MyApp()
    app.MainLoop()
if __name__ == '__main__':
    main()
