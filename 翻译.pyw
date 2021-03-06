import requests
from bs4 import BeautifulSoup
import re
import tkinter


def UI():
    Ui = tkinter.Tk()
    Ui.title("X翻译")
    Ui.geometry("600x600")
    Label = tkinter.Label(Ui,text="输入你要翻译的词语或句子:",font="2px")
    Label.place(relx=0.1,rely=0.05)
    txt = tkinter.Text(Ui, bd=2,width=35,height=5,font="2px")
    txt.place(relx=0.1,rely=0.1)
    but = tkinter.Button(Ui,text="翻译",font="2px",command=lambda:interpret(txt,txt2))
    but.place(relx=0.82,rely=0.24)
    txt2 = tkinter.Text(Ui,bd=1,width=40,height=14,font="2px")
    txt2.place(relx=0.1,rely=0.4)
    Ui.mainloop()

def interpret(text,text2):
    message = text.get(0.0,tkinter.END)
    url = "http://dict.youdao.com/search?q="+message+"&keyfrom=new-fanyi.smartResult"
    html = html = GetHtml(url)
    GetMessage(html,text2)


def GetHtml(url):
    try:
        r = requests.get(url)
        r.raise_for_status()
        r.encoding = r.apparent_encoding
        return r.text
    except:
        print("error")
def GetMessage(html,text2):
    text2.delete(0.0,tkinter.END)
    try:
        soup = BeautifulSoup(html,"html.parser")
        div = soup.find("div",class_="trans-container")
        if(div.span==None and div.ul!=None):
            if (div.p == None):
                text2.insert(tkinter.END, div.ul.text)
            else:
                text2.insert(tkinter.END,div.ul.text+div.p.text.replace("\n","—").replace(" ","").strip("[]—"))
        elif(div.span!=None):
            for span in div.ul.p.find_all("span",class_="contentTitle"):
                text2.insert(tkinter.END,(span.a.text+"\n"))
        else:
            ps = div.find_all("p")
            text2.insert(tkinter.END,ps[1].string)
    except:
        try:
            div = soup.find("div",class_="error-typo")
            text2.insert(tkinter.END,(div.h4.text+"\n"))
            for p in div.find_all("p",class_="typo-rel"):
                text2.insert(tkinter.END,p.text.replace("\n","—").replace(" ","").strip("—")+"\n")
        except:
            try:
                div = soup.find("div",class_="trans-container tab-content")
                for p in div.find_all("p",class_="wordGroup"):
                    text2.insert(tkinter.END, re.sub(" +"," ",p.text.replace("\n", "—").strip(" — "))+"\n")
            except:
                text2.insert(tkinter.END,"未找到相关翻译！")
UI()
