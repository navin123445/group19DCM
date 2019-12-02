from tkinter import *

from tkinter import messagebox
import numpy as np
import serial
import serial.tools.list_ports as port_list
import os

dirname = os.path.dirname(__file__)
userfilename = os.path.join(dirname, 'login_info.txt')
paramfilename = os.path.join(dirname, 'user_param_data.txt')
ser = serial.Serial('COM5',115200,serial.EIGHTBITS,serial.PARITY_NONE,serial.STOPBITS_ONE)

#implement other dropdown menu modes
#start indexing modes at AOO=0 then ascend by one to DOOR
#add if statement to check for correct values with dropbox


class Window(Frame):


    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.master = master
        self.welcome_window()


    def welcome_window(self):


        self.master.title("Welcome")

        self.pack(fill=BOTH, expand=1)

        Guser = Label(self, text="Username:")
        Guser.place(x=50,y=50)

        Gpwrd = Label(self, text="Password:")
        Gpwrd.place(x=50,y=100)

        self.Username=Entry(self)
        self.Username.place(x=120,y=50)

        self.Password=Entry(self)
        self.Password.place(x=120,y=100)



        def OperatingParam(p):
            print("Chosen Option is: ", p.get())
            if p.get()=="AOO":
                AOOConfigApp=Toplevel(self)
                AOOConfigApp.title("Configuration for AOO")
                AOOConfigApp.geometry("400x650")
                LowerRateLimitlabel= Label(AOOConfigApp, text="Lower Rate Limit: ")
                LowerRateLimitlabel.place(x=10, y=10)
                LowerRateLimitEntry=Entry(AOOConfigApp)
                LowerRateLimitEntry.place(x=120,y=10)
                UpperRateLimitlabel= Label(AOOConfigApp, text="Upper Rate Limit: ")
                UpperRateLimitlabel.place(x=10, y=40)
                UpperRateLimitEntry=Entry(AOOConfigApp)
                UpperRateLimitEntry.place(x=120,y=40)
                AtrialAmplitudelabel= Label(AOOConfigApp, text="Atrial Amplitude: ")
                AtrialAmplitudelabel.place(x=10, y=70)
                AtrialAmplitudeEntry=Entry(AOOConfigApp)
                AtrialAmplitudeEntry.place(x=120,y=70)
                AtrialPulseWidthlabel= Label(AOOConfigApp, text="Atrial Pulse Width: ")
                AtrialPulseWidthlabel.place(x=10, y=100)
                AtrialPulseWidthEntry=Entry(AOOConfigApp)
                AtrialPulseWidthEntry.place(x=120,y=100)


                def clicked_AOOsend( ):
                    f=open(paramfilename,"a")
                    f.write("Pacing mode: AOO \n")
                    f.write("Lower Rate Limit: ")
                    f.write(LowerRateLimitEntry.get())
                    f.write("\n")

                    f.write("Upper Rate Limit: ")
                    f.write(UpperRateLimitEntry.get())
                    f.write("\n")

                    f.write("Atrial Amplitude: ")
                    f.write(AtrialAmplitudeEntry.get())
                    f.write("\n")

                    f.write("Atrial Pulse Width: ")
                    f.write(AtrialPulseWidthEntry.get())

                    f.write("\n")

                    f.close()

                    data_array = np.arange(26)
                    data_array[0]=np.uint8(0)
                    data_array[1]=np.uint16(LowerRateLimitEntry.get())
                    data_array[2]=np.uint16(UpperRateLimitEntry.get())
                    data_array[3]=np.uint16(0)
                    data_array[4]=np.uint16(0)
                    data_array[5]=np.uint16(0)
                    data_array[6]=np.uint16(0)
                    data_array[7]=np.uint16(0)
                    data_array[8]=np.uint16(AtrialAmplitudeEntry.get())
                    data_array[9]=np.uint16(AtrialPulseWidthEntry.get())
                    data_array[10]=np.uint16(0)
                    data_array[11]=np.uint16(0)
                    data_array[12]=np.uint16(0)
                    data_array[13]=np.uint16(0)
                    data_array[14]=np.uint16(0)
                    data_array[15]=np.uint16(0)
                    data_array[16]=np.uint16(0)
                    data_array[17]=np.uint16(0)
                    data_array[18]=np.uint16(0)
                    data_array[19]=np.uint16(0)
                    data_array[20]=np.uint16(0)
                    data_array[21]=np.uint16(0)
                    data_array[22]=np.uint16(0)
                    data_array[23]=np.uint16(0)
                    data_array[24]=np.uint16(0)
                    print(data_array)

                send=Button(AOOConfigApp,text='Register Parameters',command=clicked_AOOsend)
                send.place(x=50,y=130)

            if p.get()=="VOO":
                VOOConfigApp=Toplevel(self)
                VOOConfigApp.title("Configuration for VOO")
                VOOConfigApp.geometry("400x650")
                LowerRateLimitlabel= Label(VOOConfigApp, text="Lower Rate Limit: ")
                LowerRateLimitlabel.place(x=10, y=10)
                LowerRateLimitEntry=Entry(VOOConfigApp)
                LowerRateLimitEntry.place(x=150,y=10)
                UpperRateLimitlabel= Label(VOOConfigApp, text="Upper Rate Limit: ")
                UpperRateLimitlabel.place(x=10, y=40)
                UpperRateLimitEntry=Entry(VOOConfigApp)
                UpperRateLimitEntry.place(x=150,y=40)
                VentricularAmplitudelabel= Label(VOOConfigApp, text="Ventricular Amplitude: ")
                VentricularAmplitudelabel.place(x=10, y=70)
                VentricularAmplitudeEntry=Entry(VOOConfigApp)
                VentricularAmplitudeEntry.place(x=150,y=70)
                VentricularPulseWidthlabel= Label(VOOConfigApp, text="Ventricular Pulse Width: ")
                VentricularPulseWidthlabel.place(x=10, y=100)
                VentricularPulseWidthEntry=Entry(VOOConfigApp)
                VentricularPulseWidthEntry.place(x=150,y=100)

                def clicked_VOOsend( ):
                    #VOO array data
                    #
                    #


                    f=open(paramfilename,"a")
                    f.write("Pacing mode: VOO \n")
                    f.write("Lower Rate Limit: ")
                    f.write(LowerRateLimitEntry.get())
                    f.write("\n")

                    f.write("Upper Rate Limit: ")
                    f.write(UpperRateLimitEntry.get())
                    f.write("\n")

                    f.write("Ventricular Amplitude: ")
                    f.write(VentricularAmplitudeEntry.get())
                    f.write("\n")

                    f.write("Ventricular Pulse Width: ")
                    f.write(VentricularPulseWidthEntry.get())

                    f.write("\n")

                    f.close()

                    data_array = np.arange(25)
                    data_array[0]=np.uint16(5)
                    data_array[1]=np.uint16(LowerRateLimitEntry.get())
                    data_array[2]=np.uint16(UpperRateLimitEntry.get())
                    data_array[3]=np.uint16(0)
                    data_array[4]=np.uint16(0)
                    data_array[5]=np.uint16(0)
                    data_array[6]=np.uint16(0)
                    data_array[7]=np.uint16(0)
                    data_array[8]=np.uint16(VentricularAmplitudeEntry.get())
                    data_array[9]=np.uint16(VentricularPulseWidthEntry.get())
                    data_array[10]=np.uint16(0)
                    data_array[11]=np.uint16(0)
                    data_array[12]=np.uint16(0)
                    data_array[13]=np.uint16(0)
                    data_array[14]=np.uint16(0)
                    data_array[15]=np.uint16(0)
                    data_array[16]=np.uint16(0)
                    data_array[17]=np.uint16(0)
                    data_array[18]=np.uint16(0)
                    data_array[19]=np.uint16(0)
                    data_array[20]=np.uint16(0)
                    data_array[21]=np.uint16(0)
                    data_array[22]=np.uint16(0)
                    data_array[23]=np.uint16(0)
                    data_array[24]=np.uint16(0)


                    #data_array[]=np.uint16()
                    print(data_array)

                send=Button(VOOConfigApp,text='Register Parameters',command=clicked_VOOsend)
                send.place(x=50,y=130)


            if p.get()=="AAI":
                AAIConfigApp=Toplevel(self)
                AAIConfigApp.title("Configuration for AAI")
                AAIConfigApp.geometry("400x650")

                LowerRateLimitlabel= Label(AAIConfigApp, text="Lower Rate Limit: ")
                LowerRateLimitlabel.place(x=10, y=10)
                LowerRateLimitEntry=Entry(AAIConfigApp)
                LowerRateLimitEntry.place(x=130,y=10)
                UpperRateLimitlabel= Label(AAIConfigApp, text="Upper Rate Limit: ")
                UpperRateLimitlabel.place(x=10, y=40)
                UpperRateLimitEntry=Entry(AAIConfigApp)
                UpperRateLimitEntry.place(x=130,y=40)
                AtrialAmplitudelabel= Label(AAIConfigApp, text="Atrial Amplitude: ")
                AtrialAmplitudelabel.place(x=10, y=70)
                AtrialAmplitudeEntry=Entry(AAIConfigApp)
                AtrialAmplitudeEntry.place(x=130,y=70)
                AtrialPulseWidthlabel= Label(AAIConfigApp, text="Atrial Pulse Width: ")
                AtrialPulseWidthlabel.place(x=10, y=100)
                AtrialPulseWidthEntry=Entry(AAIConfigApp)
                AtrialPulseWidthEntry.place(x=130,y=100)
                AtrialSensitivitylabel= Label(AAIConfigApp, text="Atrial Sensitivity: ")
                AtrialSensitivitylabel.place(x=10, y=130)
                AtrialSensitivityEntry=Entry(AAIConfigApp)
                AtrialSensitivityEntry.place(x=130,y=130)
                ARPlabel= Label(AAIConfigApp, text="ARP: ")
                ARPlabel.place(x=10, y=160)
                ARPEntry=Entry(AAIConfigApp)
                ARPEntry.place(x=130,y=160)
                PVARPlabel= Label(AAIConfigApp, text="PVARP: ")
                PVARPlabel.place(x=10, y=190)
                PVARPEntry=Entry(AAIConfigApp)
                PVARPEntry.place(x=130,y=190)
                Hysteresislabel= Label(AAIConfigApp, text="Hysteresis: ")
                Hysteresislabel.place(x=10, y=220)
                HysteresisEntry=Entry(AAIConfigApp)
                HysteresisEntry.place(x=130,y=220)
                RateSmoothlabel= Label(AAIConfigApp, text="Rate Smoothing: ")
                RateSmoothlabel.place(x=10, y=250)
                RateSmoothEntry=Entry(AAIConfigApp)
                RateSmoothEntry.place(x=130,y=250)

                def clicked_AAIsend( ):

                    #
                    #
                    #
                    #
                    #

                    f=open(paramfilename,"a")
                    f.write("Pacing mode: AAI \n")
                    f.write("Lower Rate Limit: ")
                    f.write(LowerRateLimitEntry.get())
                    f.write("\n")

                    f.write("Upper Rate Limit: ")
                    f.write(UpperRateLimitEntry.get())
                    f.write("\n")

                    f.write("Atrial Amplitude: ")
                    f.write(AtrialAmplitudeEntry.get())
                    f.write("\n")

                    f.write("Atrial Pulse Width: ")
                    f.write(AtrialPulseWidthEntry.get())
                    f.write("\n")

                    f.write("Atrial Sensitivity: ")
                    f.write(AtrialSensitivityEntry.get())
                    f.write("\n")

                    f.write("ARP: ")
                    f.write(ARPEntry.get())
                    f.write("\n")

                    f.write("PVARP: ")
                    f.write(PVARPEntry.get())
                    f.write("\n")

                    f.write("Hysteresis: ")
                    f.write(HysteresisEntry.get())
                    f.write("\n")

                    f.write("Rate Smoothing: ")
                    f.write(RateSmoothEntry.get())

                    f.write("\n")
                    f.close()

                    data_array = np.arange(25)
                    data_array[0]=np.uint16(4)
                    data_array[1]=np.uint16(LowerRateLimitEntry.get())
                    data_array[2]=np.uint16(UpperRateLimitEntry.get())
                    data_array[3]=np.uint16(0)
                    data_array[4]=np.uint16(0)
                    data_array[5]=np.uint16(0)
                    data_array[6]=np.uint16(0)
                    data_array[7]=np.uint16(0)
                    data_array[8]=np.uint16(AtrialAmplitudeEntry.get())
                    data_array[9]=np.uint16(AtrialPulseWidthEntry.get())
                    data_array[10]=np.uint16(AtrialSensitivityEntry.get())
                    data_array[11]=np.uint16(0)
                    data_array[12]=np.uint16(ARPEntry.get())
                    data_array[13]=np.uint16(PVARPEntry.get())
                    data_array[14]=np.uint16(0)
                    data_array[15]=np.uint16(HysteresisEntry.get())
                    data_array[16]=np.uint16(RateSmoothEntry.get())
                    data_array[17]=np.uint16(0)
                    data_array[18]=np.uint16(0)
                    data_array[19]=np.uint16(0)
                    data_array[20]=np.uint16(0)
                    data_array[21]=np.uint16(0)
                    data_array[22]=np.uint16(0)
                    data_array[23]=np.uint16(0)
                    data_array[24]=np.uint16(0)


                    #data_array[]=np.uint16()
                    print(data_array)


                send=Button(AAIConfigApp,text='Register Parameters',command=clicked_AAIsend)
                send.place(x=50,y=280)


            if p.get()=="VVI":
                VVIConfigApp=Toplevel(self)
                VVIConfigApp.title("Configuration for VVI")
                VVIConfigApp.geometry("400x650")
                LowerRateLimitlabel= Label(VVIConfigApp, text="Lower Rate Limit: ")
                LowerRateLimitlabel.place(x=10, y=10)
                LowerRateLimitEntry=Entry(VVIConfigApp)
                LowerRateLimitEntry.place(x=150,y=10)
                UpperRateLimitlabel= Label(VVIConfigApp, text="Upper Rate Limit: ")
                UpperRateLimitlabel.place(x=10, y=40)
                UpperRateLimitEntry=Entry(VVIConfigApp)
                UpperRateLimitEntry.place(x=150,y=40)
                VentricularAmplitudelabel= Label(VVIConfigApp, text="Ventricular Amplitude: ")
                VentricularAmplitudelabel.place(x=10, y=70)
                VentricularAmplitudeEntry=Entry(VVIConfigApp)
                VentricularAmplitudeEntry.place(x=150,y=70)
                VentricularPulseWidthlabel= Label(VVIConfigApp, text="Ventricular Pulse Width: ")
                VentricularPulseWidthlabel.place(x=10, y=100)
                VentricularPulseWidthEntry=Entry(VVIConfigApp)
                VentricularPulseWidthEntry.place(x=150,y=100)
                VentricularSensitivitylabel= Label(VVIConfigApp, text="Ventricular Sensitivity: ")
                VentricularSensitivitylabel.place(x=10, y=130)
                VentricularSensitivityEntry=Entry(VVIConfigApp)
                VentricularSensitivityEntry.place(x=150,y=130)
                VRPlabel= Label(VVIConfigApp, text="VRP: ")
                VRPlabel.place(x=10, y=160)
                VRPEntry=Entry(VVIConfigApp)
                VRPEntry.place(x=150,y=160)
                Hysteresislabel= Label(VVIConfigApp, text="Hysteresis: ")
                Hysteresislabel.place(x=10, y=190)
                HysteresisEntry=Entry(VVIConfigApp)
                HysteresisEntry.place(x=150,y=190)
                RateSmoothlabel= Label(VVIConfigApp, text="Rate Smoothing: ")
                RateSmoothlabel.place(x=10, y=190)
                RateSmoothEntry=Entry(VVIConfigApp)
                RateSmoothEntry.place(x=150,y=190)

                def clicked_VVIsend( ):

                    f=open(paramfilename,"a")
                    f.write("Pacing mode: VVI \n")
                    f.write("Lower Rate Limit: ")
                    f.write(LowerRateLimitEntry.get())
                    f.write("\n")

                    f.write("Upper Rate Limit: ")
                    f.write(UpperRateLimitEntry.get())
                    f.write("\n")

                    f.write("Ventricular Amplitude: ")
                    f.write(VentricularAmplitudeEntry.get())
                    f.write("\n")

                    f.write("Ventricular Pulse Width: ")
                    f.write(VentricularPulseWidthEntry.get())
                    f.write("\n")

                    f.write("Ventricular Sensitivity: ")
                    f.write(VentricularSensitivityEntry.get())
                    f.write("\n")

                    f.write("VRP: ")
                    f.write(VRPEntry.get())
                    f.write("\n")

                    f.write("Hysteresis: ")
                    f.write(HysteresisEntry.get())
                    f.write("\n")

                    f.write("Rate Smoothing: ")
                    f.write(RateSmoothEntry.get())

                    f.write("\n")
                    f.close()

                    data_array = np.arange(25)
                    data_array[0]=np.uint16(6)
                    data_array[1]=np.uint16(LowerRateLimitEntry.get())
                    data_array[2]=np.uint16(UpperRateLimitEntry.get())
                    data_array[3]=np.uint16(0)
                    data_array[4]=np.uint16(0)
                    data_array[5]=np.uint16(0)
                    data_array[6]=np.uint16(0)
                    data_array[7]=np.uint16(0)
                    data_array[8]=np.uint16(VentricularAmplitudeEntry.get())
                    data_array[9]=np.uint16(VentricularPulseWidthEntry.get())
                    data_array[10]=np.uint16(VentricularSensitivityEntry.get())
                    data_array[11]=np.uint16(VRPEntry.get())
                    data_array[12]=np.uint16(0)
                    data_array[13]=np.uint16(0)
                    data_array[14]=np.uint16(0)
                    data_array[15]=np.uint16(HysteresisEntry.get())
                    data_array[16]=np.uint16(RateSmoothEntry.get())
                    data_array[17]=np.uint16(0)
                    data_array[18]=np.uint16(0)
                    data_array[19]=np.uint16(0)
                    data_array[20]=np.uint16(0)
                    data_array[21]=np.uint16(0)
                    data_array[22]=np.uint16(0)
                    data_array[23]=np.uint16(0)
                    data_array[24]=np.uint16(0)


                    #data_array[]=np.uint16()
                    print(data_array)


                send=Button(VVIConfigApp,text='Register Parameters',command=clicked_VVIsend)
                send.place(x=50,y=220)


        #def bytearray():


        def clicked_reg( ):
            f=open(userfilename,"a")

            f.write(self.Username.get())
            f.write("\t")
            f.write(self.Password.get())
            f.write("\n")
            f.close()
            messagebox.showinfo('Thank You!', 'You are now registered.')


        def clicked_log( ):
            file=open(userfilename,"r")
            RegisteredUser= False
            for line in file:
                line = line.strip().split("\t")
                if self.Username.get() == line[0]:
                    RegisteredUser = True
                    if self.Password.get() == line[1]:
                        messagebox.showinfo('Thank You.','You have now logged in')
                        freg=open(paramfilename,"a")
                        freg.write("\n")
                        freg.write("Pacemaker Configuration for User: ")
                        freg.write(self.Username.get())
                        freg.write("\n")
                        freg.close()

                        PacemakerConfigApp=Toplevel(self)
                        PacemakerConfigApp.title("PacemakerConfigApp")
                        PacemakerConfigApp.geometry("400x400")


                        BradycardiaOperatingMode = StringVar(PacemakerConfigApp)
                        BradycardiaOperatingMode.set("AOO")


                        OpMode = OptionMenu(PacemakerConfigApp, BradycardiaOperatingMode, "AOO","AAI","VOO","VVI","VDD","DOO","DDI","DDD","AOOR","AAIR","VOOR","VVIR","VDDR","DOOR")
                        OpMode.pack()
                        OpMode.place(x=100,y=20)
                        OpTag=Label(PacemakerConfigApp,text="Select mode:")
                        OpTag.place(x=10,y=20)
                        submit_button = Button(PacemakerConfigApp, text = "Submit", command=lambda: OperatingParam(BradycardiaOperatingMode))
                        submit_button.place(x=200, y=20)


                    elif self.Password.get() != line[1]:
                        messagebox.showinfo('NOTICE','Password is incorrect')

            if RegisteredUser==False:
                messagebox.showinfo('NOTICE','You are not registered')
            file.close()




        regButton = Button(self, text="Register",command=clicked_reg)
        regButton.place(x=30, y=200)


        logButton = Button(self, text="Log in",command=clicked_log)
        logButton.place(x=150, y=200)




root = Tk()


root.geometry("500x500")

app = Window(root)
root.mainloop()
