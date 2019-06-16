

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
