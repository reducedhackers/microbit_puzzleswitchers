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

targetHit = ['MISS','MISS']

targetOne = microbit.Microbit(adapter_addr='B8:27:EB:3A:C9:38',
                         device_addr='C6:EF:44:78:2E:F4',
                         accelerometer_service=False,
                         button_service=False,
                         led_service=False,
                         magnetometer_service=False,
                         pin_service=False,
                         temperature_service=False,
                         uart_service=True)

targetTwo = microbit.Microbit(adapter_addr='B8:27:EB:3A:C9:38',
                         device_addr='FD:B4:42:E6:B6:56',
                         accelerometer_service=False,
                         button_service=False,
                         led_service=False,
                         magnetometer_service=False,
                         pin_service=False,
                         temperature_service=False,
                         uart_service=True)


eloop=async_tools.EventLoop()

def targetOneNotify(uartRead):
    global targetHit
    print('uart read targetone:', uartRead)
    targetHit[0]=uartRead
    return True

def targetTwoNotify(uartRead):
    global targetHit
    print('uart read targettwo:', uartRead)
    targetHit[1]=uartRead
    return True


def update_display():
    global app,targetHit
    print('update display')
    targetone_button.text=targetHit[0]
    targettwo_button.text=targetHit[1]
    app.update()
    return True

def connect_targets():
    global targetOne,targetTwo
    targetOne.connect()
    targetOne.subscribe_uart(targetOneNotify)
    targetTwo.connect()
    targetTwo.subscribe_uart(targetTwoNotify)
    label.value="CONNECT"

def disconnect_targets():
    global targetOne,targetTwo
    targetOne.uart='INFO\n'
    targetOne.quit_async()
    targetOne.disconnect()
    targetTwo.uart='INFO\n'
    targetTwo.quit_async()
    targetTwo.disconnect()
    label.value="DISCONNECT"


def quitAsync():
    global targetOne,targetTwo
    targetOne.uart='INFO\n'
    targetOne.quit_async()
    targetTwo.uart='INFO\n'
    targetTwo.quit_async()

def info_uart():
    global targetOne,targetTwo
    targetOne.uart='INFO\n'
    targetTwo.uart='INFO\n'
    label.value = 'INFO'

def send_uart(uartCommand=[]):
    global targetOne,targetTwo
    for aCommand in uartCommand:
        targetOne.uart = aCommand
        targetTwo.uart = aCommand
    return True

app = App(title="TEST",bg="lightgrey")
label = Text(app, text="UART RESPONSE", align="top",width="fill")
rangedata = Box(app,layout="grid")
connect_button = PushButton(rangedata,command=connect_targets,text="Connect",grid=[0,1])
disconnect_button = PushButton(rangedata,command=disconnect_targets,text="Disconnect",grid=[3,1])
active_button = PushButton(rangedata,command=send_uart,args=['ACTIVE\n'],text="ACTIVE",grid=[0,2])
begin_button = PushButton(rangedata,command=send_uart,args=['BEGIN\n'],text="BEGIN",grid=[1,2])
reset_button = PushButton(rangedata,command=send_uart,args=['RESET\n'],text="RESET",grid=[2,2])
info_button = PushButton(rangedata,command=send_uart,args=['INFO\n'],text="INFO",grid=[3,2])
targetone_button = PushButton(rangedata,text="----",grid=[0,3])
targettwo_button = PushButton(rangedata,text="----",grid=[1,3])
targetthree_button = PushButton(rangedata,text="----",grid=[2,3])
eloop.add_timer(500, update_display)
targetOne.run_async()
targetTwo.run_async()
