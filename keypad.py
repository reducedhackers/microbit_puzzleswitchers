from guizero import App,Text,PushButton,Box

secretvalue="1001"

def update_lcd(keypress):
    global secretvalue
    lcdvalue = lcdScreen.value
    #  if keypress is clear then rest screen
    #  if keypress is enter then check against secret
    #     if keypres is enter and secret matches broadcast start game
    if (keypress =='clear'):
        lcdScreen.value='----'
        return
    #  if lcdvalue contains a minus sign add value to left of string
    #  if lcdvalye contains no minus sign ignore action
    if ( lcdvalue.find('-') != -1):
        lcdvalue+=keypress
        lcdvalue = lcdvalue[-4:]
    if (keypress == 'enter') :
        if( lcdScreen.value == secretvalue ):
            lcdvalue="open"
    lcdScreen.value=lcdvalue       
    
app = App(title="Weapons Calibration",bg="lightgrey")
lcd = Box(app,align="top",width="fill",border=True)
lcdScreen = Text(lcd, text="0000", width="fill",  font="Arial")
keypad = Box(app,layout="grid")
button1 = PushButton(keypad, text="1", grid=[0,1],args=["1"],command= update_lcd,width=8,height=3)
button2 = PushButton(keypad, text="2", grid=[1,1],args=["2"],command= update_lcd,width=8,height=3)
button3  = PushButton(keypad, text="3", grid=[2,1],args=["3"],command= update_lcd,width=8,height=3)
button4  = PushButton(keypad, text="4", grid=[0,2],args=["4"],command= update_lcd,width=8,height=3)
button5  = PushButton(keypad, text="5", grid=[1,2],args=["5"],command= update_lcd,width=8,height=3)
button6  = PushButton(keypad, text="6", grid=[2,2],args=["6"],command= update_lcd,width=8,height=3)
button7  = PushButton(keypad, text="7", grid=[0,3],args=["7"],command= update_lcd,width=8,height=3)
button8  = PushButton(keypad, text="8", grid=[1,3],args=["8"],command= update_lcd,width=8,height=3)
button9  = PushButton(keypad, text="9", grid=[2,3],args=["9"],command= update_lcd,width=8,height=3)
button_clear  = PushButton(keypad, text="clear", grid=[0,4],args=["clear"],command= update_lcd,width=8,height=3)
button0  = PushButton(keypad, text="0", grid=[1,4],args=["0"],command= update_lcd,width=8,height=3)
button_enter  = PushButton(keypad, text="enter", grid=[2,4],args=["enter"],command= update_lcd,width=8,height=3)
lcdScreen.bg="white"
lcdScreen.value="----"
lcdScreen.text_size=20

app.display()
