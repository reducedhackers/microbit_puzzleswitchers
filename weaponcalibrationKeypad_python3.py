#!/usr/bin/env python

from guizero import App,Text,PushButton,Box
from bluezero import microbit
from bluezero import async_tools


# https://ukbaz.github.io/howto/targetOne_workshop.html
# this App needs SUDO ..
# make sure to pair with microbits.
# Strings to send .. must begin with  #
# Strings to send .. must end with \n
# Expected Strings.
# ACTIVE ... BEGIN .. ACTIVE ... WAIT ... END .. 


ubitDeviceAddr=['C6:EF:44:78:2E:F4','FD:B4:42:E6:B6:56','DE:BB:08:3B:F2:08']
secretvalue="2741"
resetValue="0000"
targetactive = 0
counter=100
gameResult=""
targetHit = ['MISS','MISS','MISS']


eloop=async_tools.EventLoop()


ubitTargetZero = microbit.Microbit(adapter_addr='B8:27:EB:3A:C9:38',
                         device_addr='C6:EF:44:78:2E:F4',
                         accelerometer_service=False,
                         button_service=False,
                         led_service=False,
                         magnetometer_service=False,
                         pin_service=False,
                         temperature_service=False,
                         uart_service=True)

ubitTargetTwo = microbit.Microbit(adapter_addr='B8:27:EB:3A:C9:38',
                         device_addr='FD:B4:42:E6:B6:56',
                         accelerometer_service=False,
                         button_service=False,
                         led_service=False,
                         magnetometer_service=False,
                         pin_service=False,
                         temperature_service=False,
                         uart_service=True)


ubitTargetOne = microbit.Microbit(adapter_addr='B8:27:EB:3A:C9:38',
                         device_addr='DE:BB:08:3B:F2:08',
                         accelerometer_service=False,
                         button_service=False,
                         led_service=False,
                         magnetometer_service=False,
                         pin_service=False,
                         temperature_service=False,
                         uart_service=True)

def clearGame():
    global targetHit,counter,targetactive,gameResult
    gameResult=""
    counter=100
    targetactive=0
    targetHit = ['MISS','MISS','MISS']
    for targets in targetButton:
                targets.text="MISS"
                targets.visible=False
    uartSend('RESET\n')
    lcdScreen.value="----"
    return True
    

def threehits():
    global targetHit
    return (( targetHit[0]=='HIT' ) and (targetHit[1]=='HIT'  ) and (targetHit[2]=='HIT' )  )


def updateCountDown():
    global targetactive,counter,targetHit,gameResult
    lcdvalue=""
    if (((targetactive==1) ) and ( threehits() )):
        clearGame()
        gameResult="WIN"
        lcdScreen.value="RESOLVED"
    if((targetactive==1) and (counter<1)):
        clearGame()
    if ( (targetactive==1) and (gameResult=="")):
        counter-=1
        lcdvalue="{0:b}".format(counter)
        lcdScreen.value=lcdvalue
    return True


def uartReadzero(uartResult):
    global targetHit
    targetHit[0]=uartResult.rstrip()
    return True

def uartReadone(uartResult):
    global targetHit
    targetHit[1]=uartResult.rstrip()
    return True

def uartReadtwo(uartResult):
    global targetHit
    targetHit[2]=uartResult.rstrip()
    return True
    
def uartSend(uartCommand):
    ubitTargetZero.uart=uartCommand
    ubitTargetOne.uart=uartCommand
    ubitTargetTwo.uart=uartCommand
    return True



def connect_targets():
    global ubitTargetZero,ubitTargetOne,ubitTargetTwo
    ubitTargetZero.connect()
    ubitTargetOne.connect()
    ubitTargetTwo.connect()    
    ubitTargetZero.subscribe_uart(uartReadzero)
    ubitTargetOne.subscribe_uart(uartReadone)
    ubitTargetTwo.subscribe_uart(uartReadtwo)
    return True
        
        
def disconnect_targets():
    global ubitTargetZero,ubitTargetOne,ubitTargetTwo
    uartSend('RESET\n')
    ubitTargetZero.disconnect()
    ubitTargetOne.disconnect()
    ubitTargetTwo.disconnect()
    return True
    

def update_Display():
    global app,targetHit,targetactive,gameResult
    updateCountDown()
    targetIndex=0
    if ( (targetactive== 1)  and ( gameResult=="") ):
            for targets in targetButton:
                targets.text=targetHit[targetIndex].rstrip()
                targetIndex+=1
    app.update()
    return True
    


def update_lcd(keypress):
    global secretvalue,targetactive
    lcdvalue = lcdScreen.value
    #  if keypress is clear then rest screen
    #  if keypress is enter then check against secret
    #     if keypres is enter and secret matches broadcast start game
    if (keypress =='clear'):
        lcdScreen.value='----'
        return
    #  if lcdvalue contains a minus sign add value to left of string
    #  if lcdvalue contains no minus sign ignore action    
    if (keypress == 'enter') :
        if( lcdScreen.value == resetValue ):
            clearGame()
            lcdvalue="----"
        if( lcdScreen.value == secretvalue ):
            for targets in targetButton:
                targets.visible=True
            connect_targets()
            uartSend('ACTIVE\n')
            uartSend('BEGIN\n')
            counter=300
            targetactive=1
    else:
        if ( lcdvalue.find('-') != -1):
            lcdvalue+=keypress
            lcdvalue = lcdvalue[-4:]
    lcdScreen.value=lcdvalue
    return True
    
targetButton=[]
app = App(title="Weapons Calibration",bg="lightgrey")
lcd = Box(app,align="top",width="fill",border=True)
lcdScreen = Text(lcd, text="0000", width="fill",  font="Arial")
keypad = Box(app,layout="grid")
button1 = PushButton(keypad, text="1", grid=[0,1],args=["1"],command= update_lcd,width=8,height=3)
button2 = PushButton(keypad, text="2", grid=[1,1],args=["2"],command= update_lcd,width=8,height=3)
button3  = PushButton(keypad, text="3", grid=[2,1],args=["3"],command= update_lcd,width=8,height=3)
targetButton.append(PushButton(keypad, text="MISS", grid=[3,1],width=8,height=3,visible=False))
button4  = PushButton(keypad, text="4", grid=[0,2],args=["4"],command= update_lcd,width=8,height=3)
button5  = PushButton(keypad, text="5", grid=[1,2],args=["5"],command= update_lcd,width=8,height=3)
button6  = PushButton(keypad, text="6", grid=[2,2],args=["6"],command= update_lcd,width=8,height=3)
targetButton.append(PushButton(keypad, text="MISS", grid=[3,2],width=8,height=3,visible=False))
button7  = PushButton(keypad, text="7", grid=[0,3],args=["7"],command= update_lcd,width=8,height=3)
button8  = PushButton(keypad, text="8", grid=[1,3],args=["8"],command= update_lcd,width=8,height=3)
button9  = PushButton(keypad, text="9", grid=[2,3],args=["9"],command= update_lcd,width=8,height=3)
targetButton.append(PushButton(keypad, text="MISS", grid=[3,3],width=8,height=3,visible=False))
button_clear  = PushButton(keypad, text="clear", grid=[0,4],args=["clear"],command= update_lcd,width=8,height=3)
button0  = PushButton(keypad, text="0", grid=[1,4],args=["0"],command= update_lcd,width=8,height=3)
button_enter  = PushButton(keypad, text="enter", grid=[2,4],args=["enter"],command= update_lcd,width=8,height=3)
lcdScreen.bg="white"
lcdScreen.value="----"
lcdScreen.text_size=20
app.set_full_screen('ESC')
eloop.add_timer(500,update_Display)
connect_targets()
uartSend('RESET\n')
ubitTargetZero.run_async()
ubitTargetOne.run_async()
ubitTargetTwo.run_async()
