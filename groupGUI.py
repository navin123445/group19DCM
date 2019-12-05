from tkinter import *

from tkinter import messagebox
import numpy as np
import serial
import serial.tools.list_ports as port_list
import os
import struct
import time

dirname = os.path.dirname(__file__)
userfilename = os.path.join(dirname, 'login_info.txt')
paramfilename = os.path.join(dirname, 'user_param_data.txt')
ser = serial.Serial('COM5',115200)

#AOO index = 0, up to DOOR index=13
#Activity threshold index 23 in array takes values 0-7 corresponding to 0 for off up to 7 for very high

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
                LowerRateLimitlabel= Label(AOOConfigApp, text="Lower Rate Limit[ppm]: ")
                LowerRateLimitlabel.place(x=10, y=10)
                LowerRateLimitEntry=Entry(AOOConfigApp)
                LowerRateLimitEntry.place(x=200,y=10)
                UpperRateLimitlabel= Label(AOOConfigApp, text="Upper Rate Limit[ppm]: ")
                UpperRateLimitlabel.place(x=10, y=40)
                UpperRateLimitEntry=Entry(AOOConfigApp)
                UpperRateLimitEntry.place(x=200,y=40)
                AtrialAmplitudelabel= Label(AOOConfigApp, text="Atrial Amplitude[V]: ")
                AtrialAmplitudelabel.place(x=10, y=70)
                AtrialAmplitudeEntry=Entry(AOOConfigApp)
                AtrialAmplitudeEntry.place(x=200,y=70)
                AtrialPulseWidthlabel= Label(AOOConfigApp, text="Atrial Pulse Width[ms]: ")
                AtrialPulseWidthlabel.place(x=10, y=100)
                AtrialPulseWidthEntry=Entry(AOOConfigApp)
                AtrialPulseWidthEntry.place(x=200,y=100)


                def clicked_AOOsend( ):
                    if int(LowerRateLimitEntry.get())>175 or int(LowerRateLimitEntry.get())<30:
                        messagebox.showinfo('Message','Invalid Input for Lower Rate Limit\nMust be within 30-175ppm')
                        return
                    if int(UpperRateLimitEntry.get())>175 or int(UpperRateLimitEntry.get())<50:
                        messagebox.showinfo('Message','Invalid input for Upper Rate Limit\nMust be within 50-175ppm')
                        return
                    if int(UpperRateLimitEntry.get())<int(LowerRateLimitEntry.get()):
                        messagebox.showinfo('Message', 'Invalid input, Upper Rate limit must be greater than Lower Rate limit')
                        return
                    if (float(AtrialAmplitudeEntry.get()))>6.2 or (float(AtrialAmplitudeEntry.get()))<0.5:
                        messagebox.showinfo('Message','Invalid Input for Atrial Amplitude\nMust be within 0.5-3.2V (<6V for testing purposes)') # regulated
                        return
                    if float(AtrialPulseWidthEntry.get())>20.0 or float(AtrialPulseWidthEntry.get())<0.1:
                        messagebox.showinfo('Message','Invalid Input for Atrial Pulse Width\nMust be within 0.1-1.9ms (20ms max for testing purposes)')
                        return

                    f=open(paramfilename,"a")
                    f.write("Pacing mode: AOO \n")
                    f.write("Lower Rate Limit[ppm]: ")
                    f.write(LowerRateLimitEntry.get())
                    f.write("\n")

                    f.write("Upper Rate Limit[ppm]: ")
                    f.write(UpperRateLimitEntry.get())
                    f.write("\n")

                    f.write("Atrial Amplitude[V]: ")
                    f.write(AtrialAmplitudeEntry.get())
                    f.write("\n")

                    f.write("Atrial Pulse Width[ms]: ")
                    f.write(AtrialPulseWidthEntry.get())

                    f.write("\n")

                    f.close()
                    #stemp=struct.pack('<H',np.uint16(LowerRateLimitEntry.get()))
                    #print(stemp)
                    #print(struct.unpack('<H', stemp))
                    data_array = np.arange(27)
                    data_array[0]=np.uint16(16)
                    data_array[1]=np.uint8(0)
                    data_array[2]=np.uint16(LowerRateLimitEntry.get())
                    data_array[3]=np.uint16(UpperRateLimitEntry.get())
                    data_array[4]=np.uint16(0)
                    data_array[5]=np.uint16(0)
                    data_array[6]=np.uint16(0)
                    data_array[7]=np.uint16(0)
                    data_array[8]=np.uint16(1000*float(AtrialAmplitudeEntry.get()))
                    data_array[9]=np.uint16(0)
                    data_array[10]=np.uint16(100*float(AtrialPulseWidthEntry.get()))
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
                    data_array[25]=np.uint16(0)
                    data_array[26]=np.uint16(0)

                    print(data_array)

                    byte_array=struct.pack('<H', 16)
                    byte_array+=struct.pack('<H', 0)
                    byte_array+=struct.pack('<H',np.uint16(LowerRateLimitEntry.get()))
                    byte_array+=struct.pack('<H',np.uint16(UpperRateLimitEntry.get()))
                    byte_array+=struct.pack('<H', 0)
                    byte_array+=struct.pack('<H', 0)
                    byte_array+=struct.pack('<H', 0)
                    byte_array+=struct.pack('<H', 0)
                    byte_array+=struct.pack('<H', np.uint16(1000*float(AtrialAmplitudeEntry.get())))
                    byte_array+=struct.pack('<H', 0)
                    byte_array+=struct.pack('<H', np.uint16(10*float(AtrialPulseWidthEntry.get())))
                    byte_array+=struct.pack('<H', 0)
                    byte_array+=struct.pack('<H', 0)
                    byte_array+=struct.pack('<H', 0)
                    byte_array+=struct.pack('<H', 0)
                    byte_array+=struct.pack('<H', 0)
                    byte_array+=struct.pack('<H', 0)
                    byte_array+=struct.pack('<H', 0)
                    byte_array+=struct.pack('<H', 0)
                    byte_array+=struct.pack('<H', 0)
                    byte_array+=struct.pack('<H', 0)
                    byte_array+=struct.pack('<H', 0)
                    byte_array+=struct.pack('<H', 0)
                    byte_array+=struct.pack('<H', 0)
                    byte_array+=struct.pack('<H', 0)
                    byte_array+=struct.pack('<H', 0)
                    byte_array+=struct.pack('<H', 0)


                    ser.write(byte_array)
                    print(byte_array)
                    time.sleep(2)
                    #print(ser.read(1))

                send=Button(AOOConfigApp,text='Register Parameters',command=clicked_AOOsend)
                send.place(x=50,y=130)

            if p.get()=="VOO":
                VOOConfigApp=Toplevel(self)
                VOOConfigApp.title("Configuration for VOO")
                VOOConfigApp.geometry("400x650")
                LowerRateLimitlabel= Label(VOOConfigApp, text="Lower Rate Limit[ppm]: ")
                LowerRateLimitlabel.place(x=10, y=10)
                LowerRateLimitEntry=Entry(VOOConfigApp)
                LowerRateLimitEntry.place(x=200,y=10)
                UpperRateLimitlabel= Label(VOOConfigApp, text="Upper Rate Limit[ppm]: ")
                UpperRateLimitlabel.place(x=10, y=40)
                UpperRateLimitEntry=Entry(VOOConfigApp)
                UpperRateLimitEntry.place(x=200,y=40)
                VentricularAmplitudelabel= Label(VOOConfigApp, text="Ventricular Amplitude[V]: ")
                VentricularAmplitudelabel.place(x=10, y=70)
                VentricularAmplitudeEntry=Entry(VOOConfigApp)
                VentricularAmplitudeEntry.place(x=200,y=70)
                VentricularPulseWidthlabel= Label(VOOConfigApp, text="Ventricular Pulse Width[ms]: ")
                VentricularPulseWidthlabel.place(x=10, y=100)
                VentricularPulseWidthEntry=Entry(VOOConfigApp)
                VentricularPulseWidthEntry.place(x=200,y=100)

                def clicked_VOOsend( ):
                    if int(LowerRateLimitEntry.get())>175 or int(LowerRateLimitEntry.get())<30:
                        messagebox.showinfo('Message','Invalid Input for Lower Rate Limit\nMust be within 30-175ppm')
                        return
                    if int(UpperRateLimitEntry.get())>175 or int(UpperRateLimitEntry.get())<50:
                        messagebox.showinfo('Message','Invalid input for Upper Rate Limit\nMust be within 50-175ppm')
                        return
                    if float(VentricularAmplitudeEntry.get())>7.0 or float(VentricularAmplitudeEntry.get())<0.5:
                        messagebox.showinfo('Message','Invalid Input for Ventricular Amplitude\nMust be within 3.5-7.0V')
                        return
                    if float(VentricularPulseWidthEntry.get())>20.0 or float(VentricularPulseWidthEntry.get())<0.1:
                        messagebox.showinfo('Message','Invalid Input for Ventricular Pulse Width\nMust be within 0.1-1.9ms(20ms max for testing purposes)')
                        return
                    if int(UpperRateLimitEntry.get())<int(LowerRateLimitEntry.get()):
                        messagebox.showinfo('Message', 'Invalid input, Upper Rate limit must be greater than Lower Rate limit')
                        return


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

                    data_array = np.arange(27)
                    data_array[0]=np.uint16(16)
                    data_array[1]=np.uint16(2)
                    data_array[2]=np.uint16(LowerRateLimitEntry.get())
                    data_array[3]=np.uint16(UpperRateLimitEntry.get())
                    data_array[4]=np.uint16(0)
                    data_array[5]=np.uint16(0)
                    data_array[6]=np.uint16(0)
                    data_array[7]=np.uint16(0)
                    data_array[8]=np.uint16(0)
                    data_array[9]=np.uint16(1000*float(VentricularAmplitudeEntry.get()))
                    data_array[10]=np.uint16(0)
                    data_array[11]=np.uint16(10*float(VentricularPulseWidthEntry.get()))
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
                    data_array[25]=np.uint16(0)
                    data_array[26]=np.uint16(0)


                    print(data_array)

                    byte_array=struct.pack('<H', 16)

                    byte_array+=struct.pack('<H', 2)
                    byte_array+=struct.pack('<H',np.uint16(LowerRateLimitEntry.get()))
                    byte_array+=struct.pack('<H',np.uint16(UpperRateLimitEntry.get()))
                    byte_array+=struct.pack('<H', 0)
                    byte_array+=struct.pack('<H', 0)
                    byte_array+=struct.pack('<H', 0)
                    byte_array+=struct.pack('<H', 0)
                    byte_array+=struct.pack('<H', 0)
                    byte_array+=struct.pack('<H', np.uint16(1000*float(VentricularAmplitudeEntry.get())))
                    byte_array+=struct.pack('<H', 0)
                    byte_array+=struct.pack('<H', np.uint16(10*float(VentricularPulseWidthEntry.get())))
                    byte_array+=struct.pack('<H', 0)
                    byte_array+=struct.pack('<H', 0)
                    byte_array+=struct.pack('<H', 0)
                    byte_array+=struct.pack('<H', 0)
                    byte_array+=struct.pack('<H', 0)
                    byte_array+=struct.pack('<H', 0)
                    byte_array+=struct.pack('<H', 0)
                    byte_array+=struct.pack('<H', 0)
                    byte_array+=struct.pack('<H', 0)
                    byte_array+=struct.pack('<H', 0)
                    byte_array+=struct.pack('<H', 0)
                    byte_array+=struct.pack('<H', 0)
                    byte_array+=struct.pack('<H', 0)
                    byte_array+=struct.pack('<H', 0)
                    byte_array+=struct.pack('<H', 0)

                    
                    ser.write(byte_array)
                    print(byte_array)
                    time.sleep(2)
                    #print(ser.read(1))

                send=Button(VOOConfigApp,text='Register Parameters',command=clicked_VOOsend)
                send.place(x=50,y=130)


            if p.get()=="AAI":
                AAIConfigApp=Toplevel(self)
                AAIConfigApp.title("Configuration for AAI")
                AAIConfigApp.geometry("400x650")

                LowerRateLimitlabel= Label(AAIConfigApp, text="Lower Rate Limit[ppm]: ")
                LowerRateLimitlabel.place(x=10, y=10)
                LowerRateLimitEntry=Entry(AAIConfigApp)
                LowerRateLimitEntry.place(x=200,y=10)
                UpperRateLimitlabel= Label(AAIConfigApp, text="Upper Rate Limit[ppm]: ")
                UpperRateLimitlabel.place(x=10, y=40)
                UpperRateLimitEntry=Entry(AAIConfigApp)
                UpperRateLimitEntry.place(x=200,y=40)
                AtrialAmplitudelabel= Label(AAIConfigApp, text="Atrial Amplitude[V]: ")
                AtrialAmplitudelabel.place(x=10, y=70)
                AtrialAmplitudeEntry=Entry(AAIConfigApp)
                AtrialAmplitudeEntry.place(x=200,y=70)
                AtrialPulseWidthlabel= Label(AAIConfigApp, text="Atrial Pulse Width[ms]: ")
                AtrialPulseWidthlabel.place(x=10, y=100)
                AtrialPulseWidthEntry=Entry(AAIConfigApp)
                AtrialPulseWidthEntry.place(x=200,y=100)
                AtrialSensitivitylabel= Label(AAIConfigApp, text="Atrial Sensitivity[mV]: ")
                AtrialSensitivitylabel.place(x=10, y=130)
                AtrialSensitivityEntry=Entry(AAIConfigApp)
                AtrialSensitivityEntry.place(x=200,y=130)
                ARPlabel= Label(AAIConfigApp, text="ARP[ms]: ")
                ARPlabel.place(x=10, y=160)
                ARPEntry=Entry(AAIConfigApp)
                ARPEntry.place(x=200,y=160)
                PVARPlabel= Label(AAIConfigApp, text="PVARP[ms]: ")
                PVARPlabel.place(x=10, y=190)
                PVARPEntry=Entry(AAIConfigApp)
                PVARPEntry.place(x=200,y=190)
                Hysteresislabel= Label(AAIConfigApp, text="Hysteresis: ")
                Hysteresislabel.place(x=10, y=220)
                HysteresisEntry=Entry(AAIConfigApp)
                HysteresisEntry.place(x=200,y=220)
                RateSmoothlabel= Label(AAIConfigApp, text="Rate Smoothing: ")
                RateSmoothlabel.place(x=10, y=250)
                RateSmoothEntry=Entry(AAIConfigApp)
                RateSmoothEntry.place(x=200,y=250)



                def clicked_AAIsend( ):
                    if int(LowerRateLimitEntry.get())>175 or int(LowerRateLimitEntry.get())<30:
                        messagebox.showinfo('Message','Invalid Input for Lower Rate Limit\nMust be within 30-175ppm')
                        return
                    if int(UpperRateLimitEntry.get())>175 or int(UpperRateLimitEntry.get())<50:
                        messagebox.showinfo('Message','Invalid input for Upper Rate Limit\nMust be within 50-175ppm')
                        return
                    if float(AtrialAmplitudeEntry.get())>6.2 or float(AtrialAmplitudeEntry.get())<0.5:
                        messagebox.showinfo('Message','Invalid Input for Atrial Amplitude\nMust be within 0.5-3.2V (<6v for testing purposes) ') # regulated
                        return
                    if float(AtrialPulseWidthEntry.get())>20 or float(AtrialPulseWidthEntry.get())<0.1:
                        messagebox.showinfo('Message','Invalid Input for Atrial Pulse Width\nMust be within 0.1-1.9ms (20ms max for testing purposes)')
                        return
                    if float(AtrialSensitivityEntry.get())>10.0 or float(AtrialSensitivityEntry.get())<1.0:
                        messagebox.showinfo('Message','Invalid input for Atrial Sensitivity\nMust be within 1.0-10.0mV')
                        return
                    if int(ARPEntry.get())>500 or int(ARPEntry.get())<150:
                        messagebox.showinfo('Message','Invalid Input for ARP\nMust be within 150-500ms')
                        return
                    if int(PVARPEntry.get())>500 or int(PVARPEntry.get())<150:
                        messagebox.showinfo('Message','Invalid Input for PVARP\nMust be within 150-500ms')
                        return
                    if int(HysteresisEntry.get())!=int(LowerRateLimitEntry.get()):
                        messagebox.showinfo('Message','Invalid input for Hysteresis\nMust match Lower Rate Limit')
                        return
                    if int(RateSmoothEntry.get())!=0 and int(RateSmoothEntry.get())!=3 and int(RateSmoothEntry.get())!=6 and int(RateSmoothEntry.get())!=9 and int(RateSmoothEntry.get())!=12 and int(RateSmoothEntry.get())!=15 and int(RateSmoothEntry.get())!=18 and int(RateSmoothEntry.get())!=21:
                        messagebox.showinfo('Message',"Invalid input for Rate Smoothing\n Values include:0, 3, 6, 9, 12, 15, 18, 21")
                        return
                    if int(UpperRateLimitEntry.get())<int(LowerRateLimitEntry.get()):
                        messagebox.showinfo('Message', 'Invalid input, Upper Rate limit must be greater than Lower Rate limit')
                        return
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

                    data_array = np.arange(27)
                    data_array[0]=np.uint16(16)
                    data_array[1]=np.uint16(1)
                    data_array[2]=np.uint16(LowerRateLimitEntry.get())
                    data_array[3]=np.uint16(UpperRateLimitEntry.get())
                    data_array[4]=np.uint16(0)
                    data_array[5]=np.uint16(0)
                    data_array[6]=np.uint16(0)
                    data_array[7]=np.uint16(0)
                    data_array[8]=np.uint16(1000*float(AtrialAmplitudeEntry.get()))
                    data_array[9]=np.uint16(0)
                    data_array[10]=np.uint16(10*float(AtrialPulseWidthEntry.get()))
                    data_array[11]=np.uint16(0)
                    data_array[12]=np.uint16(1000*float(AtrialSensitivityEntry.get()))
                    data_array[13]=np.uint16(0)
                    data_array[14]=np.uint16(0)
                    data_array[15]=np.uint16(ARPEntry.get())
                    data_array[16]=np.uint16(PVARPEntry.get())
                    data_array[17]=np.uint16(0)
                    data_array[18]=np.uint16(HysteresisEntry.get())
                    data_array[19]=np.uint16(RateSmoothEntry.get())
                    data_array[20]=np.uint16(0)
                    data_array[21]=np.uint16(0)
                    data_array[22]=np.uint16(0)
                    data_array[23]=np.uint16(0)
                    data_array[24]=np.uint16(0)
                    data_array[25]=np.uint16(0)
                    data_array[26]=np.uint16(0)

                    print(data_array)

                    byte_array=struct.pack('<H', 16)
                    byte_array+=struct.pack('<H',1)
                    byte_array+=struct.pack('<H',np.uint16(LowerRateLimitEntry.get()))
                    byte_array+=struct.pack('<H',np.uint16(UpperRateLimitEntry.get()))
                    byte_array+=struct.pack('<H',0)
                    byte_array+=struct.pack('<H',0)
                    byte_array+=struct.pack('<H',0)
                    byte_array+=struct.pack('<H',0)
                    byte_array+=struct.pack('<H', np.uint16(1000*float(AtrialAmplitudeEntry.get())))
                    byte_array+=struct.pack('<H',0)
                    byte_array+=struct.pack('<H', np.uint16(10*float(AtrialPulseWidthEntry.get())))
                    byte_array+=struct.pack('<H',0)
                    byte_array+=struct.pack('<H', np.uint16(1000*float(AtrialSensitivityEntry.get())))
                    byte_array+=struct.pack('<H',0)
                    byte_array+=struct.pack('<H',0)
                    byte_array+=struct.pack('<H', np.uint16(ARPEntry.get()))
                    byte_array+=struct.pack('<H', np.uint16(PVARPEntry.get()))
                    byte_array+=struct.pack('<H',0)
                    byte_array+=struct.pack('<H', np.uint16(HysteresisEntry.get()))
                    byte_array+=struct.pack('<H', np.uint16(RateSmoothEntry.get()))
                    byte_array+=struct.pack('<H', 0)
                    byte_array+=struct.pack('<H', 0)
                    byte_array+=struct.pack('<H', 0)
                    byte_array+=struct.pack('<H', 0)
                    byte_array+=struct.pack('<H', 0)
                    byte_array+=struct.pack('<H', 0)
                    byte_array+=struct.pack('<H', 0)



                    #for k in range(2):
                    
                    ser.write(byte_array)
                    print(byte_array)
                    time.sleep(2)
                    ##print(ser.read(1))



                send=Button(AAIConfigApp,text='Register Parameters',command=clicked_AAIsend)
                send.place(x=50,y=280)


            if p.get()=="VVI":
                VVIConfigApp=Toplevel(self)
                VVIConfigApp.title("Configuration for VVI")
                VVIConfigApp.geometry("400x650")
                LowerRateLimitlabel= Label(VVIConfigApp, text="Lower Rate Limit[ppm]: ")
                LowerRateLimitlabel.place(x=10, y=10)
                LowerRateLimitEntry=Entry(VVIConfigApp)
                LowerRateLimitEntry.place(x=200,y=10)
                UpperRateLimitlabel= Label(VVIConfigApp, text="Upper Rate Limit[ppm]: ")
                UpperRateLimitlabel.place(x=10, y=40)
                UpperRateLimitEntry=Entry(VVIConfigApp)
                UpperRateLimitEntry.place(x=200,y=40)
                VentricularAmplitudelabel= Label(VVIConfigApp, text="Ventricular Amplitude[V]: ")
                VentricularAmplitudelabel.place(x=10, y=70)
                VentricularAmplitudeEntry=Entry(VVIConfigApp)
                VentricularAmplitudeEntry.place(x=200,y=70)
                VentricularPulseWidthlabel= Label(VVIConfigApp, text="Ventricular Pulse Width[ms]: ")
                VentricularPulseWidthlabel.place(x=10, y=100)
                VentricularPulseWidthEntry=Entry(VVIConfigApp)
                VentricularPulseWidthEntry.place(x=200,y=100)
                VentricularSensitivitylabel= Label(VVIConfigApp, text="Ventricular Sensitivity[mV]: ")
                VentricularSensitivitylabel.place(x=10, y=130)
                VentricularSensitivityEntry=Entry(VVIConfigApp)
                VentricularSensitivityEntry.place(x=200,y=130)
                VRPlabel= Label(VVIConfigApp, text="VRP[ms]: ")
                VRPlabel.place(x=10, y=160)
                VRPEntry=Entry(VVIConfigApp)
                VRPEntry.place(x=200,y=160)
                Hysteresislabel= Label(VVIConfigApp, text="Hysteresis: ")
                Hysteresislabel.place(x=10, y=190)
                HysteresisEntry=Entry(VVIConfigApp)
                HysteresisEntry.place(x=200,y=190)
                RateSmoothlabel= Label(VVIConfigApp, text="Rate Smoothing: ")
                RateSmoothlabel.place(x=10, y=220)
                RateSmoothEntry=Entry(VVIConfigApp)
                RateSmoothEntry.place(x=200,y=220)

                def clicked_VVIsend( ):
                    if int(UpperRateLimitEntry.get())<int(LowerRateLimitEntry.get()):
                        messagebox.showinfo('Message', 'Invalid input, Upper Rate limit must be greater than Lower Rate limit')
                        return
                    if int(LowerRateLimitEntry.get())>175 or int(LowerRateLimitEntry.get())<30:
                        messagebox.showinfo('Message','Invalid Input for Lower Rate Limit\nMust be within 30-175ppm')
                        return
                    if int(UpperRateLimitEntry.get())>175 or int(UpperRateLimitEntry.get())<50:
                        messagebox.showinfo('Message','Invalid input for Upper Rate Limit\nMust be within 50-175ppm')
                        return
                    if float(VentricularAmplitudeEntry.get())>7.0 or float(VentricularAmplitudeEntry.get())<0.5:
                        messagebox.showinfo('Message','Invalid Input for Ventricular Amplitude\nMust be within 3.5-7.0V')
                        return
                    if float(VentricularPulseWidthEntry)>20.0 or float(VentricularPulseWidthEntry)<0.1:
                        messagebox.showinfo('Message','Invalid Input for Ventricular Pulse Width\nMust be within 0.1-1.9ms (20ms max for testing purposes)')
                        return
                    if float(VentricularSensitivityEntry.get())>10.0 or float(VentricularSensitivityEntry.get())<1.0:
                        messagebox.showinfo('Message','Invalid input for Ventricular Sensitivity\nMust be within 1.0-10.0mV')
                        return
                    if int(VRPEntry.get())>500 or int(VRPEntry.get())<150:
                        messagebox.showinfo('Message','Invalid Input for VRP\nMust be within 150-500ms')
                        return
                    if int(HysteresisEntry.get())!=int(LowerRateLimitEntry.get()):
                        messagebox.showinfo('Message','Invalid input for Hysteresis\nMust match Lower Rate Limit')
                        return
                    if int(RateSmoothEntry.get())!=0 and int(RateSmoothEntry.get())!=3 and int(RateSmoothEntry.get())!=6 and int(RateSmoothEntry.get())!=9 and int(RateSmoothEntry.get())!=12 and int(RateSmoothEntry.get())!=15 and int(RateSmoothEntry.get())!=18 and int(RateSmoothEntry.get())!=21:
                        messagebox.showinfo('Message',"Invalid input for Rate Smoothing\n Values include:0, 3, 6, 9, 12, 15, 18, 21")
                        return

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

                    data_array = np.arange(27)
                    data_array[0]=np.uint16(16)
                    data_array[1]=np.uint16(3)
                    data_array[2]=np.uint16(LowerRateLimitEntry.get())
                    data_array[3]=np.uint16(UpperRateLimitEntry.get())
                    data_array[4]=np.uint16(0)
                    data_array[5]=np.uint16(0)
                    data_array[6]=np.uint16(0)
                    data_array[7]=np.uint16(0)
                    data_array[8]=np.uint16(0)
                    data_array[9]=np.uint16(1000*float(VentricularAmplitudeEntry.get()))
                    data_array[10]=np.uint16(0)
                    data_array[11]=np.uint16(10*float(VentricularPulseWidthEntry.get()))
                    data_array[12]=np.uint16(0)
                    data_array[13]=np.uint16(1000*float(VentricularSensitivityEntry.get()))
                    data_array[14]=np.uint16(VRPEntry.get())
                    data_array[15]=np.uint16(0)
                    data_array[16]=np.uint16(0)
                    data_array[17]=np.uint16(0)
                    data_array[18]=np.uint16(HysteresisEntry.get())
                    data_array[19]=np.uint16(RateSmoothEntry.get())
                    data_array[20]=np.uint16(0)
                    data_array[21]=np.uint16(0)
                    data_array[22]=np.uint16(0)
                    data_array[23]=np.uint16(0)
                    data_array[24]=np.uint16(0)
                    data_array[25]=np.uint16(0)
                    data_array[26]=np.uint16(0)

                    print(data_array)


                    byte_array=struct.pack('<H', 16)
                    byte_array+=struct.pack('<H',3)
                    byte_array+=struct.pack('<H',np.uint16(LowerRateLimitEntry.get()))
                    byte_array+=struct.pack('<H',np.uint16(UpperRateLimitEntry.get()))
                    byte_array+=struct.pack('<H',0)
                    byte_array+=struct.pack('<H',0)
                    byte_array+=struct.pack('<H',0)
                    byte_array+=struct.pack('<H',0)
                    byte_array+=struct.pack('<H', 0)
                    byte_array+=struct.pack('<H', np.uint16(1000*float(VentricularAmplitudeEntry.get())))
                    byte_array+=struct.pack('<H', 0)
                    byte_array+=struct.pack('<H',np.uint16(10*float(VentricularPulseWidthEntry.get())))
                    byte_array+=struct.pack('<H', 0)
                    byte_array+=struct.pack('<H',1000*float(VentricularSensitivityEntry.get()))
                    byte_array+=struct.pack('<H',np.uint16(VRPEntry.get()))
                    byte_array+=struct.pack('<H', 0)
                    byte_array+=struct.pack('<H', 0)
                    byte_array+=struct.pack('<H',0)
                    byte_array+=struct.pack('<H', np.uint16(HysteresisEntry.get()))
                    byte_array+=struct.pack('<H', np.uint16(RateSmoothEntry.get()))
                    byte_array+=struct.pack('<H', 0)
                    byte_array+=struct.pack('<H', 0)
                    byte_array+=struct.pack('<H', 0)
                    byte_array+=struct.pack('<H', 0)
                    byte_array+=struct.pack('<H', 0)
                    byte_array+=struct.pack('<H', 0)
                    byte_array+=struct.pack('<H', 0)




                    #for k in range(2):
                    ser.write(byte_array)
                    print(byte_array)
                    time.sleep(2)
                    #print(ser.read(1))


                send=Button(VVIConfigApp,text='Register Parameters',command=clicked_VVIsend)
                send.place(x=50,y=250)

            if p.get()=="VDD":
                VDDConfigApp=Toplevel(self)
                VDDConfigApp.title("Configuration for VDD")
                VDDConfigApp.geometry("400x650")
                LowerRateLimitlabel= Label(VDDConfigApp, text="Lower Rate Limit[ppm]: ")
                LowerRateLimitlabel.place(x=10, y=10)
                LowerRateLimitEntry=Entry(VDDConfigApp)
                LowerRateLimitEntry.place(x=200,y=10)
                UpperRateLimitlabel= Label(VDDConfigApp, text="Upper Rate Limit[ppm]: ")
                UpperRateLimitlabel.place(x=10, y=40)
                UpperRateLimitEntry=Entry(VDDConfigApp)
                UpperRateLimitEntry.place(x=200,y=40)
                VentricularAmplitudelabel= Label(VDDConfigApp, text="Ventricular Amplitude[V]: ")
                VentricularAmplitudelabel.place(x=10, y=70)
                VentricularAmplitudeEntry=Entry(VDDConfigApp)
                VentricularAmplitudeEntry.place(x=200,y=70)
                VentricularPulseWidthlabel= Label(VDDConfigApp, text="Ventricular Pulse Width[ms]: ")
                VentricularPulseWidthlabel.place(x=10, y=100)
                VentricularPulseWidthEntry=Entry(VDDConfigApp)
                VentricularPulseWidthEntry.place(x=200,y=100)
                VentricularSensitivitylabel= Label(VDDConfigApp, text="Ventricular Sensitivity[mV]: ")
                VentricularSensitivitylabel.place(x=10, y=130)
                VentricularSensitivityEntry=Entry(VDDConfigApp)
                VentricularSensitivityEntry.place(x=200,y=130)
                VRPlabel= Label(VDDConfigApp, text="VRP[ms]: ")
                VRPlabel.place(x=10, y=160)
                VRPEntry=Entry(VDDConfigApp)
                VRPEntry.place(x=200,y=160)
                PVARPExtensionlabel= Label(VDDConfigApp, text="PVARP Extension[ms]: ")
                PVARPExtensionlabel.place(x=10, y=190)
                PVARPExtensionEntry=Entry(VDDConfigApp)
                PVARPExtensionEntry.place(x=200,y=190)
                RateSmoothlabel= Label(VDDConfigApp, text="Rate Smoothing: ")
                RateSmoothlabel.place(x=10, y=220)
                RateSmoothEntry=Entry(VDDConfigApp)
                RateSmoothEntry.place(x=200,y=220)
                FixedAVDelaylabel= Label(VDDConfigApp, text="Fixed AV Delay[ms]: ")
                FixedAVDelaylabel.place(x=10, y=250)
                FixedAVDelayEntry= Entry(VDDConfigApp)
                FixedAVDelayEntry.place(x=200,y=250)
                DynamicAVDelaylabel= Label(VDDConfigApp, text="Dynamic AV Delay[ms]: ")
                DynamicAVDelaylabel.place(x=10, y=280)
                DynamicAVDelayEntry= Entry(VDDConfigApp)
                DynamicAVDelayEntry.place(x=200,y=280)
                ATRDurationlabel= Label(VDDConfigApp, text="ATR Duration[Cardiac Cycles]: ")
                ATRDurationlabel.place(x=10, y=310)
                ATRDurationEntry= Entry(VDDConfigApp)
                ATRDurationEntry.place(x=200,y=310)
                ATRFallbackMlabel= Label(VDDConfigApp, text="ATR fallback mode: ")
                ATRFallbackMlabel.place(x=10, y=340)
                ATRFallbackMEntry= Entry(VDDConfigApp)
                ATRFallbackMEntry.place(x=200,y=340)
                ATRFallbackTlabel= Label(VDDConfigApp, text="ATR fallback time:[min] ")
                ATRFallbackTlabel.place(x=10, y=370)
                ATRFallbackTEntry= Entry(VDDConfigApp)
                ATRFallbackTEntry.place(x=200,y=370)

                def clicked_VDDsend( ):
                    if int(LowerRateLimitEntry.get())>175 or int(LowerRateLimitEntry.get())<30:
                        messagebox.showinfo('Message','Invalid Input for Lower Rate Limit\nMust be within 30-175ppm')
                        return
                    if int(UpperRateLimitEntry.get())>175 or int(UpperRateLimitEntry.get())<50:
                        messagebox.showinfo('Message','Invalid input for Upper Rate Limit\nMust be within 50-175ppm')
                        return
                    if float(VentricularAmplitudeEntry.get())>7.0 or float(VentricularAmplitudeEntry.get())<0.5:
                        messagebox.showinfo('Message','Invalid Input for Ventricular Amplitude\nMust be within 3.5-7.0V')
                        return
                    if float(VentricularPulseWidthEntry)>20.0 or float(VentricularPulseWidthEntry)<0.1:
                        messagebox.showinfo('Message','Invalid Input for Ventricular Pulse Width\nMust be within 0.1-1.9ms (20ms max for testing purposes)')
                        return
                    if float(VentricularSensitivityEntry.get())>10.0 or float(VentricularSensitivityEntry.get())<1.0:
                        messagebox.showinfo('Message','Invalid input for Ventricular Sensitivity\nMust be within 1.0-10.0mV')
                        return
                    if int(VRPEntry.get())>500 or int(VRPEntry.get())<150:
                        messagebox.showinfo('Message','Invalid Input for VRP\nMust be within 150-500ms')
                        return
                    if int(RateSmoothEntry.get())!=0 and int(RateSmoothEntry.get())!=3 and int(RateSmoothEntry.get())!=6 and int(RateSmoothEntry.get())!=9 and int(RateSmoothEntry.get())!=12 and int(RateSmoothEntry.get())!=15 and int(RateSmoothEntry.get())!=18 and int(RateSmoothEntry.get())!=21:
                        messagebox.showinfo('Message',"Invalid input for Rate Smoothing\n Values include:0, 3, 6, 9, 12, 15, 18, 21")
                        return
                    if int(ATRDurationEntry.get())>2000 or int(ATRDurationEntry.get())<10:
                            messagebox.showinfo('Message','Invalid Input for ATR Duration\nMust be Off or within 10-2000 cardiac cycles')
                            return
                    if int(ATRFallbackTEntry.get())>5 or int(ATRFallbackTEntry.get())<1:
                            messagebox.showinfo('Message','Invalid Input for ATR Fallback\nMust be Off or within 1-5 minutes')
                            return
                    if int(PVARPExtensionEntry.get())>400 or int(PVARPExtensionEntry.get())<50:
                            messagebox.showinfo('Message','Invalid Input for PVARP Extension\nMust be Off or within 50-400ms')
                            return
                    if int(FixedAVDelayEntry.get())>300 or int(UpperRateLimitEntry.get())<70:
                        messagebox.showinfo('Message','Invalid input for Fixed AV Delay\nMust be within 70-300ms')
                        return
                    if int(DynamicAVDelayEntry.get())!=0 or int(DynamicAVDelayEntry.get())!=1: # should we do min dynamic av delay with 30-100?
                        messagebox.showinfo('Message','Invalid Input for Dynamic AV Delay\nMust be 0 or 1')
                        return
                    if int(UpperRateLimitEntry.get())<int(LowerRateLimitEntry.get()):
                        messagebox.showinfo('Message', 'Invalid input, Upper Rate limit must be greater than Lower Rate limit')
                        return
                    f=open(paramfilename,"a")
                    f.write("Pacing mode: VDD \n")
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

                    f.write("PVARPExtension: ")
                    f.write(PVARPExtensionEntry.get())
                    f.write("\n")

                    f.write("Rate Smoothing: ")
                    f.write(RateSmoothEntry.get())

                    f.write("Fixed Delay: ")
                    f.write(FixedAVDelayEntry.get())
                    f.write("\n")

                    f.write("Dynamic Delay: ")
                    f.write(DynamicAVDelayEntry.get())
                    f.write("\n")

                    f.close()

                    data_array = np.arange(27)
                    data_array[0]=np.uint16(16)
                    data_array[1]=np.uint16(4)
                    data_array[2]=np.uint16(LowerRateLimitEntry.get())
                    data_array[3]=np.uint16(UpperRateLimitEntry.get())
                    data_array[4]=np.uint16(0)
                    data_array[5]=np.uint16(FixedAVDelayEntry.get())
                    data_array[6]=np.uint16(DynamicAVDelayEntry.get())
                    data_array[7]=np.uint16(0)
                    data_array[8]=np.uint16(0)
                    data_array[9]=np.uint16(1000*float(VentricularAmplitudeEntry.get()))
                    data_array[10]=np.uint16(0)
                    data_array[11]=np.uint16(10*float(VentricularPulseWidthEntry.get()))
                    data_array[12]=np.uint16(0)
                    data_array[13]=np.uint16(1000*float(VentricularSensitivityEntry.get()))
                    data_array[14]=np.uint16(VRPEntry.get())
                    data_array[15]=np.uint16(0)
                    data_array[16]=np.uint16(0)
                    data_array[17]=np.uint16(PVARPExtension.get())
                    data_array[18]=np.uint16(0)
                    data_array[19]=np.uint16(RateSmoothEntry.get())
                    data_array[20]=np.uint16(ATRDurationEntry.get())
                    data_array[21]=np.uint16(ATRFallbackMEntry.get())
                    data_array[22]=np.uint16(ATRFallbackTEntry.get())
                    data_array[23]=np.uint16(0)
                    data_array[24]=np.uint16(0)
                    data_array[25]=np.uint16(0)
                    data_array[26]=np.uint16(0)


                    print(data_array)

                    byte_array=struct.pack('<H', 16)
                    byte_array+=struct.pack('<H',4)
                    byte_array+=struct.pack('<H',np.uint16(LowerRateLimitEntry.get()))
                    byte_array+=struct.pack('<H',np.uint16(UpperRateLimitEntry.get()))
                    byte_array+=struct.pack('<H',0)
                    byte_array+=struct.pack('<H',np.uint16(FixedAVDelayEntry.get()))
                    byte_array+=struct.pack('<H',np.uint16(DynamicAVDelayEntry.get()))
                    byte_array+=struct.pack('<H',0)
                    byte_array+=struct.pack('<H', 0)
                    byte_array+=struct.pack('<H', np.uint16(1000*float(VentricularAmplitudeEntry.get())))
                    byte_array+=struct.pack('<H', 0)
                    byte_array+=struct.pack('<H',np.uint16(10*float(VentricularPulseWidthEntry.get())))
                    byte_array+=struct.pack('<H', 0)
                    byte_array+=struct.pack('<H',1000*float(VentricularSensitivityEntry.get()))
                    byte_array+=struct.pack('<H',np.uint16(VRPEntry.get()))
                    byte_array+=struct.pack('<H', 0)
                    byte_array+=struct.pack('<H', 0)
                    byte_array+=struct.pack('<H',np.uint16(PVARPExtension.get()))
                    byte_array+=struct.pack('<H', 0)
                    byte_array+=struct.pack('<H', np.uint16(RateSmoothEntry.get()))
                    byte_array+=struct.pack('<H', np.uint16(ATRDurationEntry.get()))
                    byte_array+=struct.pack('<H', np.uint16(ATRFallbackMEntry.get()))
                    byte_array+=struct.pack('<H', np.uint16(ATRFallbackTEntry.get()))
                    byte_array+=struct.pack('<H', 0)
                    byte_array+=struct.pack('<H', 0)
                    byte_array+=struct.pack('<H', 0)
                    byte_array+=struct.pack('<H', 0)




                    for k in range(2):
                        ser.write(byte_array)
                    print(byte_array)
                    time.sleep(2)
                    #print(ser.read(1))


                send=Button(VDDConfigApp,text='Register Parameters',command=clicked_VDDsend)
                send.place(x=50,y=400)


            if p.get()=="DOO":
                DOOConfigApp=Toplevel(self)
                DOOConfigApp.title("Configuration for DOO")
                DOOConfigApp.geometry("400x650")
                LowerRateLimitlabel= Label(DOOConfigApp, text="Lower Rate Limit[ppm]: ")
                LowerRateLimitlabel.place(x=10, y=10)
                LowerRateLimitEntry=Entry(DOOConfigApp)
                LowerRateLimitEntry.place(x=200,y=10)
                
                UpperRateLimitlabel= Label(DOOConfigApp, text="Upper Rate Limit[ppm]: ")
                UpperRateLimitlabel.place(x=10, y=40)
                UpperRateLimitEntry=Entry(DOOConfigApp)
                UpperRateLimitEntry.place(x=200,y=40)
                VentricularAmplitudelabel= Label(DOOConfigApp, text="Ventricular Amplitude[V]: ")
                VentricularAmplitudelabel.place(x=10, y=70)
                VentricularAmplitudeEntry=Entry(DOOConfigApp)
                VentricularAmplitudeEntry.place(x=200,y=70)
                VentricularPulseWidthlabel= Label(DOOConfigApp, text="Ventricular Pulse Width[ms]: ")
                VentricularPulseWidthlabel.place(x=10, y=100)
                VentricularPulseWidthEntry=Entry(DOOConfigApp)
                VentricularPulseWidthEntry.place(x=200,y=100)
                AtrialAmplitudelabel= Label(DOOConfigApp, text="Atrial Amplitude[V]: ")
                AtrialAmplitudelabel.place(x=10, y=130)
                AtrialAmplitudeEntry=Entry(DOOConfigApp)
                AtrialAmplitudeEntry.place(x=200,y=130)
                AtrialPulseWidthlabel= Label(DOOConfigApp, text="Atrial Pulse Width[ms]: ")
                AtrialPulseWidthlabel.place(x=10, y=160)
                AtrialPulseWidthEntry=Entry(DOOConfigApp)
                AtrialPulseWidthEntry.place(x=200,y=160)
                FixedAVDelaylabel= Label(DOOConfigApp, text="Fixed AV Delay[ms]: ")
                FixedAVDelaylabel.place(x=10, y=190)
                FixedAVDelayEntry= Entry(DOOConfigApp)
                FixedAVDelayEntry.place(x=200,y=190)


                def clicked_DOOsend( ):
                    if int(UpperRateLimitEntry.get())<int(LowerRateLimitEntry.get()):
                        messagebox.showinfo('Message', 'Invalid input, Upper Rate limit must be greater than Lower Rate limit')
                        return
                    if int(LowerRateLimitEntry.get())>175 or int(LowerRateLimitEntry.get())<30:
                        messagebox.showinfo('Message','Invalid Input for Lower Rate Limit\nMust be within 30-175ppm')
                        return
                    if int(UpperRateLimitEntry.get())>175 or int(UpperRateLimitEntry.get())<50:
                        messagebox.showinfo('Message','Invalid input for Upper Rate Limit\nMust be within 50-175ppm')
                        return
                    if (float(AtrialAmplitudeEntry.get()))>6.2 or (float(AtrialAmplitudeEntry.get()))<0.5:
                        messagebox.showinfo('Message','Invalid Input for Atrial Amplitude\nMust be within 0.5-3.2V (<6V for testing purposes)') # regulated
                        return
                    if float(AtrialPulseWidthEntry.get())>20.0 or float(AtrialPulseWidthEntry.get())<0.1:
                        messagebox.showinfo('Message','Invalid Input for Atrial Pulse Width\nMust be within 0.1-1.9ms (20ms max for testing purposes)')
                        return
                    if float(VentricularAmplitudeEntry.get())>7.0 or float(VentricularAmplitudeEntry.get())<0.5:
                        messagebox.showinfo('Message','Invalid Input for Ventricular Amplitude\nMust be within 3.5-7.0V')
                        return
                    if float(VentricularPulseWidthEntry.get())>20.0 or float(VentricularPulseWidthEntry.get())<0.1:
                        messagebox.showinfo('Message','Invalid Input for Ventricular Pulse Width\nMust be within 0.1-1.9ms(20ms max for testing purposes)')
                        return
                    if int(FixedAVDelayEntry.get())>300 or int(FixedAVDelayEntry.get())<70:
                        messagebox.showinfo('Message','Invalid input for Fixed AV Delay\nMust be within 70-300ms')
                        return


                    f=open(paramfilename,"a")
                    f.write("Pacing mode: DOO \n")
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

                    f.write("Atrial Amplitude: ")
                    f.write(AtrialAmplitudeEntry.get())
                    f.write("\n")

                    f.write("Atrial Pulse Width: ")
                    f.write(AtrialPulseWidthEntry.get())

                    f.write("Fixed Delay: ")
                    f.write(FixedAVDelayEntry.get())

                    f.write("\n")

                    f.close()

                    data_array = np.arange(27)
                    data_array[0]=np.uint16(16)
                    data_array[1]=np.uint16(5)
                    data_array[2]=np.uint16(LowerRateLimitEntry.get())
                    data_array[3]=np.uint16(UpperRateLimitEntry.get())
                    data_array[4]=np.uint16(0)
                    data_array[5]=np.uint16(FixedAVDelayEntry.get())
                    data_array[6]=np.uint16(0)
                    data_array[7]=np.uint16(0)
                    data_array[8]=np.uint16(1000*float(AtrialAmplitudeEntry.get()))
                    data_array[9]=np.uint16(1000*float(VentricularAmplitudeEntry.get()))
                    data_array[10]=np.uint16(10*float(AtrialPulseWidthEntry.get()))
                    data_array[11]=np.uint16(10*float(VentricularPulseWidthEntry.get()))
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
                    data_array[25]=np.uint16(0)
                    data_array[26]=np.uint16(0)

                    print(data_array)

                    byte_array=struct.pack('<H', 16)
                    byte_array+=struct.pack('<H', 5)
                    byte_array+=struct.pack('<H',np.uint16(LowerRateLimitEntry.get()))
                    byte_array+=struct.pack('<H',np.uint16(UpperRateLimitEntry.get()))
                    byte_array+=struct.pack('<H', 0)
                    byte_array+=struct.pack('<H', np.uint16(FixedAVDelayEntry.get()))
                    byte_array+=struct.pack('<H', 0)
                    byte_array+=struct.pack('<H', 0)
                    byte_array+=struct.pack('<H', np.uint16(1000*float(AtrialAmplitudeEntry.get())))
                    byte_array+=struct.pack('<H', np.uint16(1000*float(VentricularAmplitudeEntry.get())))
                    byte_array+=struct.pack('<H', np.uint16(10*float(AtrialPulseWidthEntry.get())))
                    byte_array+=struct.pack('<H', np.uint16(10*float(VentricularPulseWidthEntry.get())))
                    byte_array+=struct.pack('<H', 0)
                    byte_array+=struct.pack('<H', 0)
                    byte_array+=struct.pack('<H', 0)
                    byte_array+=struct.pack('<H', 0)
                    byte_array+=struct.pack('<H', 0)
                    byte_array+=struct.pack('<H', 0)
                    byte_array+=struct.pack('<H', 0)
                    byte_array+=struct.pack('<H', 0)
                    byte_array+=struct.pack('<H', 0)
                    byte_array+=struct.pack('<H', 0)
                    byte_array+=struct.pack('<H', 0)
                    byte_array+=struct.pack('<H', 0)
                    byte_array+=struct.pack('<H', 0)
                    byte_array+=struct.pack('<H', 0)
                    byte_array+=struct.pack('<H', 0)

                    for k in range(2):
                        ser.write(byte_array)
                    print(byte_array)
                    time.sleep(2)
                    #print(ser.read(1))

                send=Button(DOOConfigApp,text='Register Parameters',command=clicked_DOOsend)
                send.place(x=50,y=220)

            if p.get()=="DDI":
                DDIConfigApp=Toplevel(self)
                DDIConfigApp.title("Configuration for DDI")
                DDIConfigApp.geometry("400x650")
                LowerRateLimitlabel= Label(DDIConfigApp, text="Lower Rate Limit[ppm]: ")
                LowerRateLimitlabel.place(x=10, y=10)
                LowerRateLimitEntry=Entry(DDIConfigApp)
                LowerRateLimitEntry.place(x=200,y=10)
                UpperRateLimitlabel= Label(DDIConfigApp, text="Upper Rate Limit[ppm]: ")
                UpperRateLimitlabel.place(x=10, y=40)
                UpperRateLimitEntry=Entry(DDIConfigApp)
                UpperRateLimitEntry.place(x=200,y=40)
                VentricularAmplitudelabel= Label(DDIConfigApp, text="Ventricular Amplitude[V]: ")
                VentricularAmplitudelabel.place(x=10, y=70)
                VentricularAmplitudeEntry=Entry(DDIConfigApp)
                VentricularAmplitudeEntry.place(x=200,y=70)
                VentricularPulseWidthlabel= Label(DDIConfigApp, text="Ventricular Pulse Width[ms]: ")
                VentricularPulseWidthlabel.place(x=10, y=100)
                VentricularPulseWidthEntry=Entry(DDIConfigApp)
                VentricularPulseWidthEntry.place(x=200,y=100)
                VentricularSensitivitylabel= Label(DDIConfigApp, text="Ventricular Sensitivity[mV]: ")
                VentricularSensitivitylabel.place(x=10, y=130)
                VentricularSensitivityEntry=Entry(DDIConfigApp)
                VentricularSensitivityEntry.place(x=200,y=130)
                AtrialAmplitudelabel= Label(DDIConfigApp, text="Atrial Amplitude[V]: ")
                AtrialAmplitudelabel.place(x=10, y=160)
                AtrialAmplitudeEntry=Entry(DDIConfigApp)
                AtrialAmplitudeEntry.place(x=200,y=160)
                AtrialPulseWidthlabel= Label(DDIConfigApp, text="Atrial Pulse Width[ms]: ")
                AtrialPulseWidthlabel.place(x=10, y=190)
                AtrialPulseWidthEntry=Entry(DDIConfigApp)
                AtrialPulseWidthEntry.place(x=200,y=190)
                AtrialSensitivitylabel= Label(DDIConfigApp, text="Atrial Sensitivity[mV]: ")
                AtrialSensitivitylabel.place(x=10, y=220)
                AtrialSensitivityEntry=Entry(DDIConfigApp)
                AtrialSensitivityEntry.place(x=200,y=220)
                FixedAVDelaylabel= Label(DDIConfigApp, text="Fixed AV Delay[ms]: ")
                FixedAVDelaylabel.place(x=10, y=250)
                FixedAVDelayEntry= Entry(DDIConfigApp)
                FixedAVDelayEntry.place(x=200,y=250)
                VRPlabel= Label(DDIConfigApp, text="VRP[ms]: ")
                VRPlabel.place(x=10, y=280)
                VRPEntry=Entry(DDIConfigApp)
                VRPEntry.place(x=200,y=280)
                ARPlabel= Label(DDIConfigApp, text="ARP[ms]: ")
                ARPlabel.place(x=10, y=310)
                ARPEntry=Entry(DDIConfigApp)
                ARPEntry.place(x=200,y=310)
                PVARPlabel= Label(DDIConfigApp, text="PVARP[ms]: ")
                PVARPlabel.place(x=10, y=340)
                PVARPEntry=Entry(DDIConfigApp)
                PVARPEntry.place(x=200,y=340)

                def clicked_DDIsend( ):
                    if int(UpperRateLimitEntry.get())<int(LowerRateLimitEntry.get()):
                        messagebox.showinfo('Message', 'Invalid input, Upper Rate limit must be greater than Lower Rate limit')
                        return
                    if int(LowerRateLimitEntry.get())>175 or int(LowerRateLimitEntry.get())<30:
                        messagebox.showinfo('Message','Invalid Input for Lower Rate Limit\nMust be within 30-175ppm')
                        return
                    if int(UpperRateLimitEntry.get())>175 or int(UpperRateLimitEntry.get())<50:
                        messagebox.showinfo('Message','Invalid input for Upper Rate Limit\nMust be within 50-175ppm')
                        return
                    if int(FixedAVDelayEntry.get())>300 or int(FixedAVDelayEntry.get())<70:
                        messagebox.showinfo('Message','Invalid input for Fixed AV Delay\nMust be within 70-300ms')
                        return
                    if (float(AtrialAmplitudeEntry.get()))>6.2 or (float(AtrialAmplitudeEntry.get()))<0.5:
                        messagebox.showinfo('Message','Invalid Input for Atrial Amplitude\nMust be within 0.5-3.2V (<6V for testing purposes)') # regulated
                        return
                    if (float(VentricularAmplitudeEntry.get()))>7.0 or (float(VentricularAmplitudeEntry.get()))<3.5:
                        messagebox.showinfo('Message','Invalid Input for Ventricular Amplitude\nMust be within 3.5-7.0V')
                        return
                    if float(AtrialPulseWidthEntry.get())>20.0 or float(AtrialPulseWidthEntry.get())<0.1:
                            messagebox.showinfo('Message','Invalid Input for Atrial Pulse Width\nMust be within 0.1-1.9ms (20ms max for testing purposes)')
                            return
                    if float(VentricularPulseWidthEntry.get())>20.0 or float(VentricularPulseWidthEntry.get())<0.1:
                            messagebox.showinfo('Message','Invalid Input for Ventricular Pulse Width\nMust be within 0.1-1.9ms(20ms max for testing purposes)')
                            return
                    if float(AtrialSensitivityEntry.get())>10.0 or float(AtrialSensitivityEntry.get())<1.0:
                            messagebox.showinfo('Message','Invalid input for Atrial Sensitivity\nMust be within 1.0-10.0mV')
                            return
                    if int(VentricularSensitivityEntry.get())>10 or int(VentricularSensitivityEntry.get())<1:
                        messagebox.showinfo('Message','Invalid input for Ventricular Sensitivity\nMust be within 1.0-10.0mV')
                        return
                    if int(VRPEntry.get())>500 or int(VRPEntry.get())<150:
                        messagebox.showinfo('Message','Invalid Input for VRP\nMust be within 150-500ms')
                        return
                    if int(ARPEntry.get())>500 or int(ARPEntry.get())<150:
                            messagebox.showinfo('Message','Invalid Input for ARP\nMust be within 150-500ms')
                            return
                    if int(PVARPEntry.get())>500 or int(PVARPEntry.get())<150:
                            messagebox.showinfo('Message','Invalid Input for PVARP\nMust be within 150-500ms')
                            return


                    f=open(paramfilename,"a")
                    f.write("Pacing mode: DDI \n")
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

                    f.write("Atrial Amplitude: ")
                    f.write(AtrialAmplitudeEntry.get())
                    f.write("\n")

                    f.write("Atrial Pulse Width: ")
                    f.write(AtrialPulseWidthEntry.get())


                    f.write("\n")

                    f.close()

                    data_array = np.arange(27)
                    data_array[0]=np.uint16(16)
                    data_array[1]=np.uint16(6)
                    data_array[2]=np.uint16(LowerRateLimitEntry.get())
                    data_array[3]=np.uint16(UpperRateLimitEntry.get())
                    data_array[4]=np.uint16(0)
                    data_array[5]=np.uint16(FixedAVDelayEntry.get())
                    data_array[6]=np.uint16(0)
                    data_array[7]=np.uint16(0)
                    data_array[8]=np.uint16(1000*float(AtrialAmplitudeEntry.get()))
                    data_array[9]=np.uint16(1000*float(VentricularAmplitudeEntry.get()))
                    data_array[10]=np.uint16(10*float(AtrialPulseWidthEntry.get()))
                    data_array[11]=np.uint16(10*float(VentricularPulseWidthEntry.get()))
                    data_array[12]=np.uint16(1000*float(AtrialSensitivityEntry.get()))
                    data_array[13]=np.uint16(1000*float(VentricularSensitivityEntry.get()))
                    data_array[14]=np.uint16(VRPEntry.get())
                    data_array[15]=np.uint16(ARPEntry.get())
                    data_array[16]=np.uint16(PVARPEntry.get())
                    data_array[17]=np.uint16(0)
                    data_array[18]=np.uint16(0)
                    data_array[19]=np.uint16(0)
                    data_array[20]=np.uint16(0)
                    data_array[21]=np.uint16(0)
                    data_array[22]=np.uint16(0)
                    data_array[23]=np.uint16(0)
                    data_array[24]=np.uint16(0)
                    data_array[25]=np.uint16(0)
                    data_array[26]=np.uint16(0)


                    print(data_array)

                    byte_array=struct.pack('<H', 16)
                    byte_array+=struct.pack('<H',6)
                    byte_array+=struct.pack('<H',np.uint16(LowerRateLimitEntry.get()))
                    byte_array+=struct.pack('<H',np.uint16(UpperRateLimitEntry.get()))
                    byte_array+=struct.pack('<H',0)
                    byte_array+=struct.pack('<H',np.uint16(FixedAVDelayEntry.get()))
                    byte_array+=struct.pack('<H',0)
                    byte_array+=struct.pack('<H',0)
                    byte_array+=struct.pack('<H', np.uint16(1000*float(AtrialAmplitudeEntry.get())))
                    byte_array+=struct.pack('<H', np.uint16(1000*float(VentricularAmplitudeEntry.get())))
                    byte_array+=struct.pack('<H', np.uint16(10*float(AtrialPulseWidthEntry.get())))
                    byte_array+=struct.pack('<H', np.uint16(10*float(VentricularPulseWidthEntry.get())))
                    byte_array+=struct.pack('<H', np.uint16(1000*float(AtrialSensitivityEntry.get())))
                    byte_array+=struct.pack('<H',1000*float(VentricularSensitivityEntry.get()))
                    byte_array+=struct.pack('<H',np.uint16(VRPEntry.get()))
                    byte_array+=struct.pack('<H',np.uint16(ARPEntry.get()))
                    byte_array+=struct.pack('<H', np.uint16(PVARPEntry.get()))
                    byte_array+=struct.pack('<H', 0)
                    byte_array+=struct.pack('<H', 0)
                    byte_array+=struct.pack('<H', 0)
                    byte_array+=struct.pack('<H', 0)
                    byte_array+=struct.pack('<H', 0)
                    byte_array+=struct.pack('<H', 0)
                    byte_array+=struct.pack('<H', 0)
                    byte_array+=struct.pack('<H', 0)
                    byte_array+=struct.pack('<H', 0)
                    byte_array+=struct.pack('<H', 0)




                    for k in range(2):
                        ser.write(byte_array)
                    print(byte_array)
                    time.sleep(2)
                    #print(ser.read(1))


                send=Button(DDIConfigApp,text='Register Parameters',command=clicked_DDIsend)
                send.place(x=50,y=370)

            if p.get()=="DDD":
                DDDConfigApp=Toplevel(self)
                DDDConfigApp.title("Configuration for DDD")
                DDDConfigApp.geometry("400x650")
                LowerRateLimitlabel= Label(DDDConfigApp, text="Lower Rate Limit[ppm]: ")
                LowerRateLimitlabel.place(x=10, y=10)
                LowerRateLimitEntry=Entry(DDDConfigApp)
                LowerRateLimitEntry.place(x=200,y=10)
                UpperRateLimitlabel= Label(DDDConfigApp, text="Upper Rate Limit[ppm]: ")
                UpperRateLimitlabel.place(x=10, y=40)
                UpperRateLimitEntry=Entry(DDDConfigApp)
                UpperRateLimitEntry.place(x=200,y=40)
                VentricularAmplitudelabel= Label(DDDConfigApp, text="Ventricular Amplitude[V]: ")
                VentricularAmplitudelabel.place(x=10, y=70)
                VentricularAmplitudeEntry=Entry(DDDConfigApp)
                VentricularAmplitudeEntry.place(x=200,y=70)
                VentricularPulseWidthlabel= Label(DDDConfigApp, text="Ventricular Pulse Width[ms]: ")
                VentricularPulseWidthlabel.place(x=10, y=100)
                VentricularPulseWidthEntry=Entry(DDDConfigApp)
                VentricularPulseWidthEntry.place(x=200,y=100)
                VentricularSensitivitylabel= Label(DDDConfigApp, text="Ventricular Sensitivity[mV]: ")
                VentricularSensitivitylabel.place(x=10, y=130)
                VentricularSensitivityEntry=Entry(DDDConfigApp)
                VentricularSensitivityEntry.place(x=200,y=130)
                AtrialAmplitudelabel= Label(DDDConfigApp, text="Atrial Amplitude[V]: ")
                AtrialAmplitudelabel.place(x=10, y=160)
                AtrialAmplitudeEntry=Entry(DDDConfigApp)
                AtrialAmplitudeEntry.place(x=200,y=160)
                AtrialPulseWidthlabel= Label(DDDConfigApp, text="Atrial Pulse Width[ms]: ")
                AtrialPulseWidthlabel.place(x=10, y=190)
                AtrialPulseWidthEntry=Entry(DDDConfigApp)
                AtrialPulseWidthEntry.place(x=200,y=190)
                AtrialSensitivitylabel= Label(DDDConfigApp, text="Atrial Sensitivity[mV]: ")
                AtrialSensitivitylabel.place(x=10, y=220)
                AtrialSensitivityEntry=Entry(DDDConfigApp)
                AtrialSensitivityEntry.place(x=200,y=220)
                FixedAVDelaylabel= Label(DDDConfigApp, text="Fixed AV Delay[ms]: ")
                FixedAVDelaylabel.place(x=10, y=250)
                FixedAVDelayEntry= Entry(DDDConfigApp)
                FixedAVDelayEntry.place(x=200,y=250)
                DynamicAVDelaylabel= Label(DDDConfigApp, text="Dynamic AV Delay: ")
                DynamicAVDelaylabel.place(x=10, y=280)
                DynamicAVDelayEntry= Entry(DDDConfigApp)
                DynamicAVDelayEntry.place(x=200,y=280)
                SensedAVDelaylabel= Label(DDDConfigApp, text="Sensed AV Delay Offset[ms]: ")
                SensedAVDelaylabel.place(x=10, y=310)
                SensedAVDelayEntry= Entry(DDDConfigApp)
                SensedAVDelayEntry.place(x=200,y=310)
                VRPlabel= Label(DDDConfigApp, text="VRP[ms]: ")
                VRPlabel.place(x=10, y=340)
                VRPEntry=Entry(DDDConfigApp)
                VRPEntry.place(x=200,y=340)
                ARPlabel= Label(DDDConfigApp, text="ARP[ms]: ")
                ARPlabel.place(x=10, y=370)
                ARPEntry=Entry(DDDConfigApp)
                ARPEntry.place(x=200,y=370)
                PVARPlabel= Label(DDDConfigApp, text="PVARP[ms]: ")
                PVARPlabel.place(x=10, y=400)
                PVARPEntry=Entry(DDDConfigApp)
                PVARPEntry.place(x=200,y=400)
                PVARPExtensionlabel= Label(DDDConfigApp, text="PVARP Extension[ms]: ")
                PVARPExtensionlabel.place(x=10, y=430)
                PVARPExtensionEntry=Entry(DDDConfigApp)
                PVARPExtensionEntry.place(x=200,y=430)
                RateSmoothlabel= Label(DDDConfigApp, text="Rate Smoothing: ")
                RateSmoothlabel.place(x=10, y=460)
                RateSmoothEntry=Entry(DDDConfigApp)
                RateSmoothEntry.place(x=200,y=460)
                Hysteresislabel= Label(DDDConfigApp, text="Hysteresis: ")
                Hysteresislabel.place(x=10, y=490)
                HysteresisEntry=Entry(DDDConfigApp)
                HysteresisEntry.place(x=200,y=490)
                ATRDurationlabel= Label(DDDConfigApp, text="ATR Duration[Cardiac Cycles]: ")
                ATRDurationlabel.place(x=10, y=520)
                ATRDurationEntry= Entry(DDDConfigApp)
                ATRDurationEntry.place(x=200,y=520)
                ATRFallbackMlabel= Label(DDDConfigApp, text="ATR fallback mode: ")
                ATRFallbackMlabel.place(x=10, y=550)
                ATRFallbackMEntry= Entry(DDDConfigApp)
                ATRFallbackMEntry.place(x=200,y=550)
                ATRFallbackTlabel= Label(DDDConfigApp, text="ATR fallback time[min]: ")
                ATRFallbackTlabel.place(x=10, y=580)
                ATRFallbackTEntry= Entry(DDDConfigApp)
                ATRFallbackTEntry.place(x=200,y=580)

                def clicked_DDDsend( ):
                    if int(UpperRateLimitEntry.get())<int(LowerRateLimitEntry.get()):
                        messagebox.showinfo('Message', 'Invalid input, Upper Rate limit must be greater than Lower Rate limit')
                        return
                    if int(LowerRateLimitEntry.get())>175 or int(LowerRateLimitEntry.get())<30:
                        messagebox.showinfo('Message','Invalid Input for Lower Rate Limit\nMust be within 30-175ppm')
                        return
                    if int(UpperRateLimitEntry.get())>175 or int(UpperRateLimitEntry.get())<50:
                        messagebox.showinfo('Message','Invalid input for Upper Rate Limit\nMust be within 50-175ppm')
                        return
                    if int(FixedAVDelayEntry.get())>300 or int(UpperRateLimitEntry.get())<70:
                        messagebox.showinfo('Message','Invalid input for Fixed AV Delay\nMust be within 70-300ms')
                        return
                    if int(DynamicAVDelayEntry.get())!=0 or int(DynamicAVDelayEntry.get())!=1: # should we do min dynamic av delay with 30-100?
                        messagebox.showinfo('Message','Invalid Input for Dynamic AV Delay\nMust be 0 or 1')
                        return
                    if int(SensedAVDelayEntry.get())!=0 and int(SensedAVDelayEntry.get())>-100 or int(SensedAVDelayEntry.get())<-10:
                        messagebox.showinfo('Message','Invalid Input for Dynamic AV Delay\nMust be Off or within -10 - -100ms')
                        return
                    if (float(AtrialAmplitudeEntry.get()))>6.2 or (float(AtrialAmplitudeEntry.get()))<0.5:
                        messagebox.showinfo('Message','Invalid Input for Atrial Amplitude\nMust be within 0.5-3.2V (<6V for testing purposes)') # regulated
                        return
                    if (float(VentricularAmplitudeEntry.get()))>7.0 or (float(VentricularAmplitudeEntry.get()))<3.5:
                        messagebox.showinfo('Message','Invalid Input for Ventricular Amplitude\nMust be within 3.5-7.0V')
                        return
                    if float(AtrialPulseWidthEntry.get())>20.0 or float(AtrialPulseWidthEntry.get())<0.1:
                            messagebox.showinfo('Message','Invalid Input for Atrial Pulse Width\nMust be within 0.1-1.9ms (20ms max for testing purposes)')
                            return
                    if float(VentricularPulseWidthEntry.get())>20.0 or float(VentricularPulseWidthEntry.get())<0.1:
                            messagebox.showinfo('Message','Invalid Input for Ventricular Pulse Width\nMust be within 0.1-1.9ms(20ms max for testing purposes)')
                            return
                    if float(AtrialSensitivityEntry.get())>10.0 or float(AtrialSensitivityEntry.get())<1.0:
                            messagebox.showinfo('Message','Invalid input for Atrial Sensitivity\nMust be within 1.0-10.0mV')
                            return
                    if int(VentricularSensitivityEntry.get())>10 or int(VentricularSensitivityEntry.get())<1:
                        messagebox.showinfo('Message','Invalid input for Ventricular Sensitivity\nMust be within 1.0-10.0mV')
                        return
                    if int(VRPEntry.get())>500 or int(VRPEntry.get())<150:
                        messagebox.showinfo('Message','Invalid Input for VRP\nMust be within 150-500ms')
                        return
                    if int(ARPEntry.get())>500 or int(ARPEntry.get())<150:
                            messagebox.showinfo('Message','Invalid Input for ARP\nMust be within 150-500ms')
                            return
                    if int(PVARPEntry.get())>500 or int(PVARPEntry.get())<150:
                            messagebox.showinfo('Message','Invalid Input for PVARP\nMust be within 150-500ms')
                            return
                    if int(PVARPExtensionEntry.get())>400 or int(PVARPExtensionEntry.get())<50:
                            messagebox.showinfo('Message','Invalid Input for PVARP Extension\nMust be Off or within 50-400ms')
                            return
                    if int(HysteresisEntry.get())!=int(LowerRateLimitEntry.get()):
                        messagebox.showinfo('Message','Invalid input for Hysteresis\nMust match Lower Rate Limit')
                        return
                    if int(RateSmoothEntry.get())!=0 and int(RateSmoothEntry.get())!=3 and int(RateSmoothEntry.get())!=6 and int(RateSmoothEntry.get())!=9 and int(RateSmoothEntry.get())!=12 and int(RateSmoothEntry.get())!=15 and int(RateSmoothEntry.get())!=18 and int(RateSmoothEntry.get())!=21:
                            messagebox.showinfo('Message',"Invalid input for Rate Smoothing\n Values include:0, 3, 6, 9, 12, 15, 18, 21")
                            return
                    if int(ATRDurationEntry.get())>2000 or int(ATRDurationEntry.get())<10:
                            messagebox.showinfo('Message','Invalid Input for ATR Duration\nMust be Off or within 10-2000 cardiac cycles')
                            return
                    if int(ATRFallbackTEntry.get())>5 or int(ATRFallbackTEntry.get())<1:
                            messagebox.showinfo('Message','Invalid Input for ATR Fallback\nMust be Off or within 1-5 minutes')
                            return
                    if int(ReactionTimeEntry.get())<10 or int(ReactionTimeEntry.get())>50:
                        messagebox.showinfo('Message','Invalid Input for Reaction Time \nMust be within 10-50 seconds')
                        return
                    if int(ResponseFactorEntry.get())<1 or int(ResponseFactorEntry.get())>16:
                        messagebox.showinfo('Message','Invalid Input for the response factor\nMust be within 1-16')
                        return
                    if int(RecoveryTimeEntry.get())<2 or int(RecoveryTimeEntry.get())>16:
                        messagebox.showinfo('Message','Invalid Input for Recovery Time \nMust be within 1-5 minutes')
                        return
                    if int(ActivityThresholdEntry.get())<0 or int(ActivityThresholdEntry.get())>7:
                        messagebox.showinfo('Message','Invalid Input for Activity Threshold \nMust be within 0-7 corresponding to 0 for off up to 7 for very high')
                        return
                    #


                    f=open(paramfilename,"a")
                    f.write("Pacing mode: DDD \n")
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

                    f.write("Atrial Amplitude: ")
                    f.write(AtrialAmplitudeEntry.get())
                    f.write("\n")

                    f.write("Atrial Pulse Width: ")
                    f.write(AtrialPulseWidthEntry.get())


                    f.write("\n")

                    f.close()

                    data_array = np.arange(27)
                    data_array[0]=np.uint16(16)
                    data_array[1]=np.uint16(7)
                    data_array[2]=np.uint16(LowerRateLimitEntry.get())
                    data_array[3]=np.uint16(UpperRateLimitEntry.get())
                    data_array[4]=np.uint16(0)
                    data_array[5]=np.uint16(FixedAVDelayEntry.get())
                    data_array[6]=np.uint16(DynamicAVDelayEntry.get())
                    data_array[7]=np.uint16(SensedAVDelayEntry.get())
                    data_array[8]=np.uint16(1000*float(AtrialAmplitudeEntry.get()))
                    data_array[9]=np.uint16(1000*float(VentricularAmplitudeEntry.get()))
                    data_array[10]=np.uint16(10*float(AtrialPulseWidthEntry.get()))
                    data_array[11]=np.uint16(10*float(VentricularPulseWidthEntry.get()))
                    data_array[12]=np.uint16(1000*float(AtrialSensitivityEntry.get()))
                    data_array[13]=np.uint16(1000*float(VentricularSensitivityEntry.get()))
                    data_array[14]=np.uint16(VRPEntry.get())
                    data_array[15]=np.uint16(ARPEntry.get())
                    data_array[16]=np.uint16(PVARPEntry.get())
                    data_array[17]=np.uint16(PVARPExtensionEntry.get())
                    data_array[18]=np.uint16(HysteresisEntry.get())
                    data_array[19]=np.uint16(RateSmoothEntry.get())
                    data_array[20]=np.uint16(ATRDurationEntry.get())
                    data_array[21]=np.uint16(ATRFallbackMEntry.get())
                    data_array[22]=np.uint16(ATRFallbackTEntry.get())
                    data_array[23]=np.uint16(0)
                    data_array[24]=np.uint16(0)
                    data_array[25]=np.uint16(0)
                    data_array[26]=np.uint16(0)

                    print(data_array)

                    byte_array=struct.pack('<H', 16)
                    byte_array+=struct.pack('<H',7)
                    byte_array+=struct.pack('<H',np.uint16(LowerRateLimitEntry.get()))
                    byte_array+=struct.pack('<H',np.uint16(UpperRateLimitEntry.get()))
                    byte_array+=struct.pack('<H',0)
                    byte_array+=struct.pack('<H',np.uint16(FixedAVDelayEntry.get()))
                    byte_array+=struct.pack('<H',np.uint16(DynamicAVDelayEntry.get()))
                    byte_array+=struct.pack('<H',np.uint16(SensedAVDelayEntry.get()))
                    byte_array+=struct.pack('<H', np.uint16(1000*float(AtrialAmplitudeEntry.get())))
                    byte_array+=struct.pack('<H', np.uint16(1000*float(VentricularAmplitudeEntry.get())))
                    byte_array+=struct.pack('<H', np.uint16(10*float(AtrialPulseWidthEntry.get())))
                    byte_array+=struct.pack('<H', np.uint16(10*float(VentricularPulseWidthEntry.get())))
                    byte_array+=struct.pack('<H', np.uint16(1000*float(AtrialSensitivityEntry.get())))
                    byte_array+=struct.pack('<H',1000*float(VentricularSensitivityEntry.get()))
                    byte_array+=struct.pack('<H',np.uint16(VRPEntry.get()))
                    byte_array+=struct.pack('<H',np.uint16(ARPEntry.get()))
                    byte_array+=struct.pack('<H', np.uint16(PVARPEntry.get()))
                    byte_array+=struct.pack('<H', np.uint16(PVARPExtensionEntry.get()))
                    byte_array+=struct.pack('<H', np.uint16(HysteresisEntry.get()))
                    byte_array+=struct.pack('<H', np.uint16(RateSmoothEntry.get()))
                    byte_array+=struct.pack('<H', np.uint16(ATRDurationEntry.get()))
                    byte_array+=struct.pack('<H', np.uint16(ATRFallbackMEntry.get()))
                    byte_array+=struct.pack('<H', np.uint16(ATRFallbackTEntry.get()))
                    byte_array+=struct.pack('<H', 0)
                    byte_array+=struct.pack('<H', 0)
                    byte_array+=struct.pack('<H', 0)
                    byte_array+=struct.pack('<H', 0)




                    for k in range(2):
                        ser.write(byte_array)
                    print(byte_array)
                    time.sleep(2)
                    #print(ser.read(1))

                send=Button(DDDConfigApp,text='Register Parameters',command=clicked_DDDsend)
                send.place(x=50,y=610)

            if p.get()=="AOOR":
                AOORConfigApp=Toplevel(self)
                AOORConfigApp.title("Configuration for AOOR")
                AOORConfigApp.geometry("400x650")
                LowerRateLimitlabel= Label(AOORConfigApp, text="Lower Rate Limit[ppm]: ")
                LowerRateLimitlabel.place(x=10, y=10)
                LowerRateLimitEntry=Entry(AOORConfigApp)
                LowerRateLimitEntry.place(x=200,y=10)
                UpperRateLimitlabel= Label(AOORConfigApp, text="Upper Rate Limit[ppm]: ")
                UpperRateLimitlabel.place(x=10, y=40)
                UpperRateLimitEntry=Entry(AOORConfigApp)
                UpperRateLimitEntry.place(x=200,y=40)
                AtrialAmplitudelabel= Label(AOORConfigApp, text="Atrial Amplitude[V]: ")
                AtrialAmplitudelabel.place(x=10, y=70)
                AtrialAmplitudeEntry=Entry(AOORConfigApp)
                AtrialAmplitudeEntry.place(x=200,y=70)
                AtrialPulseWidthlabel= Label(AOORConfigApp, text="Atrial Pulse Width[ms]: ")
                AtrialPulseWidthlabel.place(x=10, y=100)
                AtrialPulseWidthEntry=Entry(AOORConfigApp)
                AtrialPulseWidthEntry.place(x=200,y=100)
                MaxRateLimitlabel= Label(AOORConfigApp, text="Max Sensor Rate[ppm]: ")
                MaxRateLimitlabel.place(x=10, y=130)
                MaxRateLimitEntry=Entry(AOORConfigApp)
                MaxRateLimitEntry.place(x=200,y=130)
                ActivityThresholdlabel= Label(AOORConfigApp, text="Activity Threshold: ")
                ActivityThresholdlabel.place(x=10, y=160)
                ActivityThresholdEntry=Entry(AOORConfigApp)
                ActivityThresholdEntry.place(x=200,y=160)
                ReactionTimelabel= Label(AOORConfigApp, text="Reaction Time[s]: ")
                ReactionTimelabel.place(x=10, y=190)
                ReactionTimeEntry=Entry(AOORConfigApp)
                ReactionTimeEntry.place(x=200,y=190)
                ResponseFactorlabel= Label(AOORConfigApp, text="Response Factor: ")
                ResponseFactorlabel.place(x=10, y=220)
                ResponseFactorEntry=Entry(AOORConfigApp)
                ResponseFactorEntry.place(x=200,y=220)
                RecoveryTimelabel= Label(AOORConfigApp, text="Recovery Time[min]: ")
                RecoveryTimelabel.place(x=10, y=250)
                RecoveryTimeEntry=Entry(AOORConfigApp)
                RecoveryTimeEntry.place(x=200,y=250)

                def clicked_AOORsend( ):
                    if int(UpperRateLimitEntry.get())<int(LowerRateLimitEntry.get()):
                        messagebox.showinfo('Message', 'Invalid input, Upper Rate limit must be greater than Lower Rate limit')
                        return
                    if int(LowerRateLimitEntry.get())>175 or int(LowerRateLimitEntry.get())<30:
                        messagebox.showinfo('Message','Invalid Input for Lower Rate Limit\nMust be within 30-175ppm')
                        return
                    if int(UpperRateLimitEntry.get())>175 or int(UpperRateLimitEntry.get())<50:
                        messagebox.showinfo('Message','Invalid input for Upper Rate Limit\nMust be within 50-175ppm')
                        return
                    if (float(AtrialAmplitudeEntry.get()))>6.2 or (float(AtrialAmplitudeEntry.get()))<0.5:
                        messagebox.showinfo('Message','Invalid Input for Atrial Amplitude\nMust be within 0.5-3.2V (<6V for testing purposes)') # regulated
                        return
                    if float(AtrialPulseWidthEntry.get())>20.0 or float(AtrialPulseWidthEntry.get())<0.1:
                        messagebox.showinfo('Message','Invalid Input for Atrial Pulse Width\nMust be within 0.1-1.9ms (20ms max for testing purposes)')
                        return
                    if int(ReactionTimeEntry.get())<10 or int(ReactionTimeEntry.get())>50:
                        messagebox.showinfo('Message','Invalid Input for Reaction Time \nMust be within 10-50 seconds')
                        return
                    if int(ResponseFactorEntry.get())<1 or int(ResponseFactorEntry.get())>16:
                        messagebox.showinfo('Message','Invalid Input for the response factor\nMust be within 1-16')
                        return
                    if int(RecoveryTimeEntry.get())<2 or int(RecoveryTimeEntry.get())>16:
                        messagebox.showinfo('Message','Invalid Input for Recovery Time \nMust be within 1-5 minutes')
                        return
                    if int(ActivityThresholdEntry.get())<0 or int(ActivityThresholdEntry.get())>7:
                        messagebox.showinfo('Message','Invalid Input for Activity Threshold \nMust be within 0-7 corresponding to 0 for off up to 7 for very high')
                        return
                    f=open(paramfilename,"a")
                    f.write("Pacing mode: AOOR \n")
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

                    data_array = np.arange(27)
                    data_array[0]=np.uint16(16)
                    data_array[1]=np.uint8(8)
                    data_array[2]=np.uint16(LowerRateLimitEntry.get())
                    data_array[3]=np.uint16(UpperRateLimitEntry.get())
                    data_array[4]=np.uint16(0)
                    data_array[5]=np.uint16(0)
                    data_array[6]=np.uint16(0)
                    data_array[7]=np.uint16(0)
                    data_array[8]=np.uint16(1000*float(AtrialAmplitudeEntry.get()))
                    data_array[9]=np.uint16(0)
                    data_array[10]=np.uint16(10*float(AtrialPulseWidthEntry.get()))
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
                    data_array[23]=np.uint16(ActivityThresholdEntry.get())
                    data_array[24]=np.uint16(ReactionTimeEntry.get())
                    data_array[25]=np.uint16(ResponseFactorEntry.get())
                    data_array[26]=np.uint16(RecoveryTimeEntry.get())

                    print(data_array)

                    byte_array=struct.pack('<H', 16)
                    byte_array+=struct.pack('<H', 8)
                    byte_array+=struct.pack('<H',np.uint16(LowerRateLimitEntry.get()))
                    byte_array+=struct.pack('<H',np.uint16(UpperRateLimitEntry.get()))
                    byte_array+=struct.pack('<H', 0)
                    byte_array+=struct.pack('<H', 0)
                    byte_array+=struct.pack('<H', 0)
                    byte_array+=struct.pack('<H', 0)
                    byte_array+=struct.pack('<H', np.uint16(1000*float(AtrialAmplitudeEntry.get())))
                    byte_array+=struct.pack('<H', 0)
                    byte_array+=struct.pack('<H', np.uint16(10*float(AtrialPulseWidthEntry.get())))
                    byte_array+=struct.pack('<H', 0)
                    byte_array+=struct.pack('<H', 0)
                    byte_array+=struct.pack('<H', 0)
                    byte_array+=struct.pack('<H', 0)
                    byte_array+=struct.pack('<H', 0)
                    byte_array+=struct.pack('<H', 0)
                    byte_array+=struct.pack('<H', 0)
                    byte_array+=struct.pack('<H', 0)
                    byte_array+=struct.pack('<H', 0)
                    byte_array+=struct.pack('<H', 0)
                    byte_array+=struct.pack('<H', 0)
                    byte_array+=struct.pack('<H', 0)
                    byte_array+=struct.pack('<H', np.uint16(ActivityThresholdEntry.get()))
                    byte_array+=struct.pack('<H', np.uint16(ReactionTimeEntry.get()))
                    byte_array+=struct.pack('<H', np.uint16(ResponseFactorEntry.get()))
                    byte_array+=struct.pack('<H', np.uint16(RecoveryTimeEntry.get()))

                    for k in range(2):
                        ser.write(byte_array)
                    print(byte_array)
                    time.sleep(2)
                    #print(ser.read(1))

                send=Button(AOORConfigApp,text='Register Parameters',command=clicked_AOORsend)
                send.place(x=50,y=280)

            if p.get()=="AAIR":
                AAIRConfigApp=Toplevel(self)
                AAIRConfigApp.title("Configuration for AAIR")
                AAIRConfigApp.geometry("400x650")

                LowerRateLimitlabel= Label(AAIRConfigApp, text="Lower Rate Limit[ppm]: ")
                LowerRateLimitlabel.place(x=10, y=10)
                LowerRateLimitEntry=Entry(AAIRConfigApp)
                LowerRateLimitEntry.place(x=200,y=10)
                UpperRateLimitlabel= Label(AAIRConfigApp, text="Upper Rate Limit[ppm]: ")
                UpperRateLimitlabel.place(x=10, y=40)
                UpperRateLimitEntry=Entry(AAIRConfigApp)
                UpperRateLimitEntry.place(x=200,y=40)
                AtrialAmplitudelabel= Label(AAIRConfigApp, text="Atrial Amplitude[V]: ")
                AtrialAmplitudelabel.place(x=10, y=70)
                AtrialAmplitudeEntry=Entry(AAIRConfigApp)
                AtrialAmplitudeEntry.place(x=200,y=70)
                AtrialPulseWidthlabel= Label(AAIRConfigApp, text="Atrial Pulse Width[ms]: ")
                AtrialPulseWidthlabel.place(x=10, y=100)
                AtrialPulseWidthEntry=Entry(AAIRConfigApp)
                AtrialPulseWidthEntry.place(x=200,y=100)
                AtrialSensitivitylabel= Label(AAIRConfigApp, text="Atrial Sensitivity[mV]: ")
                AtrialSensitivitylabel.place(x=10, y=130)
                AtrialSensitivityEntry=Entry(AAIRConfigApp)
                AtrialSensitivityEntry.place(x=200,y=130)
                ARPlabel= Label(AAIRConfigApp, text="ARP[ms]: ")
                ARPlabel.place(x=10, y=160)
                ARPEntry=Entry(AAIRConfigApp)
                ARPEntry.place(x=200,y=160)
                PVARPlabel= Label(AAIRConfigApp, text="PVARP[ms]: ")
                PVARPlabel.place(x=10, y=190)
                PVARPEntry=Entry(AAIRConfigApp)
                PVARPEntry.place(x=200,y=190)
                Hysteresislabel= Label(AAIRConfigApp, text="Hysteresis: ")
                Hysteresislabel.place(x=10, y=220)
                HysteresisEntry=Entry(AAIRConfigApp)
                HysteresisEntry.place(x=200,y=220)
                RateSmoothlabel= Label(AAIRConfigApp, text="Rate Smoothing: ")
                RateSmoothlabel.place(x=10, y=250)
                RateSmoothEntry=Entry(AAIRConfigApp)
                RateSmoothEntry.place(x=200,y=250)
                MaxRateLimitlabel= Label(AAIRConfigApp, text="Max Sensor Rate[ppm]: ")
                MaxRateLimitlabel.place(x=10, y=280)
                MaxRateLimitEntry=Entry(AAIRConfigApp)
                MaxRateLimitEntry.place(x=200,y=280)
                ActivityThresholdlabel= Label(AAIRConfigApp, text="Activity Threshold: ")
                ActivityThresholdlabel.place(x=10, y=310)
                ActivityThresholdEntry=Entry(AAIRConfigApp)
                ActivityThresholdEntry.place(x=200,y=310)
                ReactionTimelabel= Label(AAIRConfigApp, text="Reaction Time[s]: ")
                ReactionTimelabel.place(x=10, y=340)
                ReactionTimeEntry=Entry(AAIRConfigApp)
                ReactionTimeEntry.place(x=200,y=340)
                ResponseFactorlabel= Label(AAIRConfigApp, text="Response Factor: ")
                ResponseFactorlabel.place(x=10, y=370)
                ResponseFactorEntry=Entry(AAIRConfigApp)
                ResponseFactorEntry.place(x=200,y=370)
                RecoveryTimelabel= Label(AAIRConfigApp, text="Recovery Time[min]: ")
                RecoveryTimelabel.place(x=10, y=400)
                RecoveryTimeEntry=Entry(AAIRConfigApp)
                RecoveryTimeEntry.place(x=200,y=400)


                def clicked_AAIRsend( ):
                    if int(UpperRateLimitEntry.get())<int(LowerRateLimitEntry.get()):
                        messagebox.showinfo('Message', 'Invalid input, Upper Rate limit must be greater than Lower Rate limit')
                        return
                    if int(LowerRateLimitEntry.get())>175 or int(LowerRateLimitEntry.get())<30:
                        messagebox.showinfo('Message','Invalid Input for Lower Rate Limit\nMust be within 30-175ppm')
                        return
                    if int(UpperRateLimitEntry.get())>175 or int(UpperRateLimitEntry.get())<50:
                        messagebox.showinfo('Message','Invalid input for Upper Rate Limit\nMust be within 50-175ppm')
                        return
                    if (float(AtrialAmplitudeEntry.get()))>6.2 or (float(AtrialAmplitudeEntry.get()))<0.5:
                        messagebox.showinfo('Message','Invalid Input for Atrial Amplitude\nMust be within 0.5-3.2V (<6V for testing purposes)') # regulated
                        return
                    if float(AtrialPulseWidthEntry.get())>20 or float(AtrialPulseWidthEntry.get())<0.1:
                        messagebox.showinfo('Message','Invalid Input for Ventricular Pulse Width\nMust be within 0.1-1.9ms (20ms max for testing purposes)')
                        return
                    if float(AtrialSensitivityEntry.get())>10.0 or float(AtrialSensitivityEntry.get())<1.0:
                        messagebox.showinfo('Message','Invalid input for Atrial Sensitivity\nMust be within 1.0-10.0mV')
                        return
                    if int(ARPEntry.get())>500 or int(ARPEntry.get())<150:
                        messagebox.showinfo('Message','Invalid Input for ARP\nMust be within 150-500ms')
                        return
                    if int(PVARPEntry.get())>500 or int(PVARPEntry.get())<150:
                        messagebox.showinfo('Message','Invalid Input for PVARP\nMust be within 150-500ms')
                        return
                    if int(HysteresisEntry.get())!=int(LowerRateLimitEntry.get()):
                        messagebox.showinfo('Message','Invalid input for Hysteresis\nMust match Lower Rate Limit')
                        return
                    if int(RateSmoothEntry.get())!=0 and int(RateSmoothEntry.get())!=3 and int(RateSmoothEntry.get())!=6 and int(RateSmoothEntry.get())!=9 and int(RateSmoothEntry.get())!=12 and int(RateSmoothEntry.get())!=15 and int(RateSmoothEntry.get())!=18 and int(RateSmoothEntry.get())!=21:
                        messagebox.showinfo('Message',"Invalid input for Rate Smoothing\n Values include:0, 3, 6, 9, 12, 15, 18, 21")
                        return
                    if int(ReactionTimeEntry.get())<10 or int(ReactionTimeEntry.get())>50:
                        messagebox.showinfo('Message','Invalid Input for Reaction Time \nMust be within 10-50 seconds')
                        return
                    if int(ResponseFactorEntry.get())<1 or int(ResponseFactorEntry.get())>16:
                        messagebox.showinfo('Message','Invalid Input for the response factor\nMust be within 1-16')
                        return
                    if int(RecoveryTimeEntry.get())<2 or int(RecoveryTimeEntry.get())>16:
                        messagebox.showinfo('Message','Invalid Input for Recovery Time \nMust be within 1-5 minutes')
                        return
                    if int(ActivityThresholdEntry.get())<0 or int(ActivityThresholdEntry.get())>7:
                        messagebox.showinfo('Message','Invalid Input for Activity Threshold \nMust be within 0-7 corresponding to 0 for off up to 7 for very high')
                        return

                    f=open(paramfilename,"a")
                    f.write("Pacing mode: AAIR \n")
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

                    data_array = np.arange(27)
                    data_array[0]=np.uint16(16)
                    data_array[1]=np.uint16(9)
                    data_array[2]=np.uint16(LowerRateLimitEntry.get())
                    data_array[3]=np.uint16(UpperRateLimitEntry.get())
                    data_array[4]=np.uint16(0)
                    data_array[5]=np.uint16(0)
                    data_array[6]=np.uint16(0)
                    data_array[7]=np.uint16(0)
                    data_array[8]=np.uint16(1000*float(AtrialAmplitudeEntry.get()))
                    data_array[9]=np.uint16(0)
                    data_array[10]=np.uint16(10*float(AtrialPulseWidthEntry.get()))
                    data_array[11]=np.uint16(0)
                    data_array[12]=np.uint16(1000*float(AtrialSensitivityEntry.get()))
                    data_array[13]=np.uint16(0)
                    data_array[14]=np.uint16(0)
                    data_array[15]=np.uint16(ARPEntry.get())
                    data_array[16]=np.uint16(PVARPEntry.get())
                    data_array[17]=np.uint16(0)
                    data_array[18]=np.uint16(HysteresisEntry.get())
                    data_array[19]=np.uint16(RateSmoothEntry.get())
                    data_array[20]=np.uint16(0)
                    data_array[21]=np.uint16(0)
                    data_array[22]=np.uint16(0)
                    data_array[23]=np.uint16(ActivityThresholdEntry.get())
                    data_array[24]=np.uint16(ReactionTimeEntry.get())
                    data_array[25]=np.uint16(ResponseFactorEntry.get())
                    data_array[26]=np.uint16(RecoveryTimeEntry.get())

                    print(data_array)

                    byte_array=struct.pack('<H', 16)
                    byte_array+=struct.pack('<H',9)
                    byte_array+=struct.pack('<H',np.uint16(LowerRateLimitEntry.get()))
                    byte_array+=struct.pack('<H',np.uint16(UpperRateLimitEntry.get()))
                    byte_array+=struct.pack('<H',0)
                    byte_array+=struct.pack('<H',0)
                    byte_array+=struct.pack('<H',0)
                    byte_array+=struct.pack('<H',0)
                    byte_array+=struct.pack('<H', np.uint16(1000*float(AtrialAmplitudeEntry.get())))
                    byte_array+=struct.pack('<H',0)
                    byte_array+=struct.pack('<H', np.uint16(10*float(AtrialPulseWidthEntry.get())))
                    byte_array+=struct.pack('<H',0)
                    byte_array+=struct.pack('<H', np.uint16(1000*float(AtrialSensitivityEntry.get())))
                    byte_array+=struct.pack('<H',0)
                    byte_array+=struct.pack('<H',0)
                    byte_array+=struct.pack('<H', np.uint16(ARPEntry.get()))
                    byte_array+=struct.pack('<H', np.uint16(PVARPEntry.get()))
                    byte_array+=struct.pack('<H',0)
                    byte_array+=struct.pack('<H', np.uint16(HysteresisEntry.get()))
                    byte_array+=struct.pack('<H', np.uint16(RateSmoothEntry.get()))
                    byte_array+=struct.pack('<H', 0)
                    byte_array+=struct.pack('<H', 0)
                    byte_array+=struct.pack('<H', 0)
                    byte_array+=struct.pack('<H', np.uint16(ActivityThresholdEntry.get()))
                    byte_array+=struct.pack('<H', np.uint16(ReactionTimeEntry.get()))
                    byte_array+=struct.pack('<H', np.uint16(ResponseFactorEntry.get()))
                    byte_array+=struct.pack('<H', np.uint16(RecoveryTimeEntry.get()))



                    for k in range(2):
                        ser.write(byte_array)
                    print(byte_array)
                    time.sleep(2)
                    #print(ser.read(1))


                send=Button(AAIRConfigApp,text='Register Parameters',command=clicked_AAIRsend)
                send.place(x=50,y=430)

            if p.get()=="VOOR":
                VOORConfigApp=Toplevel(self)
                VOORConfigApp.title("Configuration for VOOR")
                VOORConfigApp.geometry("400x650")
                LowerRateLimitlabel= Label(VOORConfigApp, text="Lower Rate Limit[ppm]: ")
                LowerRateLimitlabel.place(x=10, y=10)
                LowerRateLimitEntry=Entry(VOORConfigApp)
                LowerRateLimitEntry.place(x=200,y=10)
                UpperRateLimitlabel= Label(VOORConfigApp, text="Upper Rate Limit[ppm]: ")
                UpperRateLimitlabel.place(x=10, y=40)
                UpperRateLimitEntry=Entry(VOORConfigApp)
                UpperRateLimitEntry.place(x=200,y=40)
                VentricularAmplitudelabel= Label(VOORConfigApp, text="Ventricular Amplitude[V]: ")
                VentricularAmplitudelabel.place(x=10, y=70)
                VentricularAmplitudeEntry=Entry(VOORConfigApp)
                VentricularAmplitudeEntry.place(x=200,y=70)
                VentricularPulseWidthlabel= Label(VOORConfigApp, text="Ventricular Pulse Width[ms]: ")
                VentricularPulseWidthlabel.place(x=10, y=100)
                VentricularPulseWidthEntry=Entry(VOORConfigApp)
                VentricularPulseWidthEntry.place(x=200,y=100)
                MaxRateLimitlabel= Label(VOORConfigApp, text="Max Sensor Rate[ppm]: ")
                MaxRateLimitlabel.place(x=10, y=130)
                MaxRateLimitEntry=Entry(VOORConfigApp)
                MaxRateLimitEntry.place(x=200,y=130)
                ActivityThresholdlabel= Label(VOORConfigApp, text="Activity Threshold: ")
                ActivityThresholdlabel.place(x=10, y=160)
                ActivityThresholdEntry=Entry(VOORConfigApp)
                ActivityThresholdEntry.place(x=200,y=160)
                ReactionTimelabel= Label(VOORConfigApp, text="Reaction Time[s]: ")
                ReactionTimelabel.place(x=10, y=190)
                ReactionTimeEntry=Entry(VOORConfigApp)
                ReactionTimeEntry.place(x=200,y=190)
                ResponseFactorlabel= Label(VOORConfigApp, text="Response Factor: ")
                ResponseFactorlabel.place(x=10, y=220)
                ResponseFactorEntry=Entry(VOORConfigApp)
                ResponseFactorEntry.place(x=200,y=220)
                RecoveryTimelabel= Label(VOORConfigApp, text="Recovery Time[min]: ")
                RecoveryTimelabel.place(x=10, y=250)
                RecoveryTimeEntry=Entry(VOORConfigApp)
                RecoveryTimeEntry.place(x=200,y=250)

                def clicked_VOORsend( ):
                    if int(UpperRateLimitEntry.get())<int(LowerRateLimitEntry.get()):
                        messagebox.showinfo('Message', 'Invalid input, Upper Rate limit must be greater than Lower Rate limit')
                        return
                    if int(ReactionTimeEntry.get())<10 or int(ReactionTimeEntry.get())>50:
                        messagebox.showinfo('Message','Invalid Input for Reaction Time \nMust be within 10-50 seconds')
                        return
                    if int(ResponseFactorEntry.get())<1 or int(ResponseFactorEntry.get())>16:
                        messagebox.showinfo('Message','Invalid Input for the response factor\nMust be within 1-16')
                        return
                    if int(RecoveryTimeEntry.get())<2 or int(RecoveryTimeEntry.get())>16:
                        messagebox.showinfo('Message','Invalid Input for Recovery Time \nMust be within 1-5 minutes')
                        return
                    if int(ActivityThresholdEntry.get())<0 or int(ActivityThresholdEntry.get())>7:
                        messagebox.showinfo('Message','Invalid Input for Activity Threshold \nMust be within 0-7 corresponding to 0 for off up to 7 for very high')
                        return
                    if int(LowerRateLimitEntry.get())>175 or int(LowerRateLimitEntry.get())<30:
                        messagebox.showinfo('Message','Invalid Input for Lower Rate Limit\nMust be within 30-175ppm')
                        return
                    if int(UpperRateLimitEntry.get())>175 or int(UpperRateLimitEntry.get())<50:
                        messagebox.showinfo('Message','Invalid input for Upper Rate Limit\nMust be within 50-175ppm')
                        return
                    if float(VentricularAmplitudeEntry.get())>7.0 or float(VentricularAmplitudeEntry.get())<0.5:
                        messagebox.showinfo('Message','Invalid Input for Ventricular Amplitude\nMust be within 3.5-7.0V')
                        return
                    if float(VentricularPulseWidthEntry.get())>20.0 or float(VentricularPulseWidthEntry.get())<0.1:
                        messagebox.showinfo('Message','Invalid Input for Ventricular Pulse Width\nMust be within 0.1-1.9ms(20ms max for testing purposes)')
                        return

                    f=open(paramfilename,"a")
                    f.write("Pacing mode: VOOR \n")
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

                    data_array = np.arange(27)
                    data_array[0]=np.uint16(16)
                    data_array[1]=np.uint16(10)
                    data_array[2]=np.uint16(LowerRateLimitEntry.get())
                    data_array[3]=np.uint16(UpperRateLimitEntry.get())
                    data_array[4]=np.uint16(0)
                    data_array[5]=np.uint16(0)
                    data_array[6]=np.uint16(0)
                    data_array[7]=np.uint16(0)
                    data_array[8]=np.uint16(0)
                    data_array[9]=np.uint16(1000*float(VentricularAmplitudeEntry.get()))
                    data_array[10]=np.uint16(0)
                    data_array[11]=np.uint16(10*float(VentricularPulseWidthEntry.get()))
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
                    data_array[23]=np.uint16(ActivityThresholdEntry.get())
                    data_array[24]=np.uint16(ReactionTimeEntry.get())
                    data_array[25]=np.uint16(ResponseFactorEntry.get())
                    data_array[26]=np.uint16(RecoveryTimeEntry.get())

                    print(data_array)

                    byte_array=struct.pack('<H', 16)

                    byte_array+=struct.pack('<H', 10)
                    byte_array+=struct.pack('<H',np.uint16(LowerRateLimitEntry.get()))
                    byte_array+=struct.pack('<H',np.uint16(UpperRateLimitEntry.get()))
                    byte_array+=struct.pack('<H', 0)
                    byte_array+=struct.pack('<H', 0)
                    byte_array+=struct.pack('<H', 0)
                    byte_array+=struct.pack('<H', 0)
                    byte_array+=struct.pack('<H', 0)
                    byte_array+=struct.pack('<H', np.uint16(1000*float(VentricularAmplitudeEntry.get())))
                    byte_array+=struct.pack('<H', 0)
                    byte_array+=struct.pack('<H', np.uint16(10*float(VentricularPulseWidthEntry.get())))
                    byte_array+=struct.pack('<H', 0)
                    byte_array+=struct.pack('<H', 0)
                    byte_array+=struct.pack('<H', 0)
                    byte_array+=struct.pack('<H', 0)
                    byte_array+=struct.pack('<H', 0)
                    byte_array+=struct.pack('<H', 0)
                    byte_array+=struct.pack('<H', 0)
                    byte_array+=struct.pack('<H', 0)
                    byte_array+=struct.pack('<H', 0)
                    byte_array+=struct.pack('<H', 0)
                    byte_array+=struct.pack('<H', 0)
                    byte_array+=struct.pack('<H', np.uint16(ActivityThresholdEntry.get()))
                    byte_array+=struct.pack('<H', np.uint16(ReactionTimeEntry.get()))
                    byte_array+=struct.pack('<H', np.uint16(ResponseFactorEntry.get()))
                    byte_array+=struct.pack('<H', np.uint16(RecoveryTimeEntry.get()))

                    for k in range(2):
                        ser.write(byte_array)
                    print(byte_array)
                    time.sleep(2)
                    #print(ser.read(1))


                send=Button(VOORConfigApp,text='Register Parameters',command=clicked_VOORsend)
                send.place(x=50,y=280)

            if p.get()=="VVIR":
                VVIRConfigApp=Toplevel(self)
                VVIRConfigApp.title("Configuration for VVIR")
                VVIRConfigApp.geometry("400x650")
                LowerRateLimitlabel= Label(VVIRConfigApp, text="Lower Rate Limit[ppm]: ")
                LowerRateLimitlabel.place(x=10, y=10)
                LowerRateLimitEntry=Entry(VVIRConfigApp)
                LowerRateLimitEntry.place(x=200,y=10)
                UpperRateLimitlabel= Label(VVIRConfigApp, text="Upper Rate Limit[ppm]: ")
                UpperRateLimitlabel.place(x=10, y=40)
                UpperRateLimitEntry=Entry(VVIRConfigApp)
                UpperRateLimitEntry.place(x=200,y=40)
                VentricularAmplitudelabel= Label(VVIRConfigApp, text="Ventricular Amplitude[V]: ")
                VentricularAmplitudelabel.place(x=10, y=70)
                VentricularAmplitudeEntry=Entry(VVIRConfigApp)
                VentricularAmplitudeEntry.place(x=200,y=70)
                VentricularPulseWidthlabel= Label(VVIRConfigApp, text="Ventricular Pulse Width[ms]: ")
                VentricularPulseWidthlabel.place(x=10, y=100)
                VentricularPulseWidthEntry=Entry(VVIRConfigApp)
                VentricularPulseWidthEntry.place(x=200,y=100)
                VentricularSensitivitylabel= Label(VVIRConfigApp, text="Ventricular Sensitivity[mV]: ")
                VentricularSensitivitylabel.place(x=10, y=130)
                VentricularSensitivityEntry=Entry(VVIRConfigApp)
                VentricularSensitivityEntry.place(x=200,y=130)
                VRPlabel= Label(VVIRConfigApp, text="VRP[ms]: ")
                VRPlabel.place(x=10, y=160)
                VRPEntry=Entry(VVIRConfigApp)
                VRPEntry.place(x=200,y=160)
                Hysteresislabel= Label(VVIRConfigApp, text="Hysteresis: ")
                Hysteresislabel.place(x=10, y=190)
                HysteresisEntry=Entry(VVIRConfigApp)
                HysteresisEntry.place(x=200,y=190)
                RateSmoothlabel= Label(VVIRConfigApp, text="Rate Smoothing: ")
                RateSmoothlabel.place(x=10, y=220)
                RateSmoothEntry=Entry(VVIRConfigApp)
                RateSmoothEntry.place(x=200,y=220)
                MaxRateLimitlabel= Label(VVIRConfigApp, text="Max Sensor Rate[ppm]: ")
                MaxRateLimitlabel.place(x=10, y=250)
                MaxRateLimitEntry=Entry(VVIRConfigApp)
                MaxRateLimitEntry.place(x=200,y=250)
                ActivityThresholdlabel= Label(VVIRConfigApp, text="Activity Threshold: ")
                ActivityThresholdlabel.place(x=10, y=280)
                ActivityThresholdEntry=Entry(VVIRConfigApp)
                ActivityThresholdEntry.place(x=200,y=280)
                ReactionTimelabel= Label(VVIRConfigApp, text="Reaction Time[s]: ")
                ReactionTimelabel.place(x=10, y=310)
                ReactionTimeEntry=Entry(VVIRConfigApp)
                ReactionTimeEntry.place(x=200,y=310)
                ResponseFactorlabel= Label(VVIRConfigApp, text="Response Factor: ")
                ResponseFactorlabel.place(x=10, y=340)
                ResponseFactorEntry=Entry(VVIRConfigApp)
                ResponseFactorEntry.place(x=200,y=340)
                RecoveryTimelabel= Label(VVIRConfigApp, text="Recovery Time[min]: ")
                RecoveryTimelabel.place(x=10, y=370)
                RecoveryTimeEntry=Entry(VVIRConfigApp)
                RecoveryTimeEntry.place(x=200,y=370)

                def clicked_VVIRsend( ):
                    if int(UpperRateLimitEntry.get())<int(LowerRateLimitEntry.get()):
                        messagebox.showinfo('Message', 'Invalid input, Upper Rate limit must be greater than Lower Rate limit')
                        return
                    if int(LowerRateLimitEntry.get())>175 or int(LowerRateLimitEntry.get())<30:
                        messagebox.showinfo('Message','Invalid Input for Lower Rate Limit\nMust be within 30-175ppm')
                        return
                    if int(UpperRateLimitEntry.get())>175 or int(UpperRateLimitEntry.get())<50:
                        messagebox.showinfo('Message','Invalid input for Upper Rate Limit\nMust be within 50-175ppm')
                        return
                    if float(VentricularAmplitudeEntry.get())>7.0 or float(VentricularAmplitudeEntry.get())<0.5:
                        messagebox.showinfo('Message','Invalid Input for Ventricular Amplitude\nMust be within 3.5-7.0V')
                        return
                    if float(VentricularPulseWidthEntry)>20.0 or float(VentricularPulseWidthEntry)<0.1:
                        messagebox.showinfo('Message','Invalid Input for Ventricular Pulse Width\nMust be within 0.1-1.9ms (20ms max for testing purposes)')
                        return
                    if float(VentricularSensitivityEntry.get())>10.0 or float(VentricularSensitivityEntry.get())<1.0:
                        messagebox.showinfo('Message','Invalid input for Ventricular Sensitivity\nMust be within 1.0-10.0mV')
                        return
                    if int(VRPEntry.get())>500 or int(VRPEntry.get())<150:
                        messagebox.showinfo('Message','Invalid Input for VRP\nMust be within 150-500ms')
                        return
                    if int(HysteresisEntry.get())!=int(LowerRateLimitEntry.get()):
                        messagebox.showinfo('Message','Invalid input for Hysteresis\nMust match Lower Rate Limit')
                        return
                    if int(RateSmoothEntry.get())!=0 and int(RateSmoothEntry.get())!=3 and int(RateSmoothEntry.get())!=6 and int(RateSmoothEntry.get())!=9 and int(RateSmoothEntry.get())!=12 and int(RateSmoothEntry.get())!=15 and int(RateSmoothEntry.get())!=18 and int(RateSmoothEntry.get())!=21:
                        messagebox.showinfo('Message',"Invalid input for Rate Smoothing\n Values include:0, 3, 6, 9, 12, 15, 18, 21")
                        return
                    if int(ReactionTimeEntry.get())<10 or int(ReactionTimeEntry.get())>50:
                        messagebox.showinfo('Message','Invalid Input for Reaction Time \nMust be within 10-50 seconds')
                        return
                    if int(ResponseFactorEntry.get())<1 or int(ResponseFactorEntry.get())>16:
                        messagebox.showinfo('Message','Invalid Input for the response factor\nMust be within 1-16')
                        return
                    if int(RecoveryTimeEntry.get())<2 or int(RecoveryTimeEntry.get())>16:
                        messagebox.showinfo('Message','Invalid Input for Recovery Time \nMust be within 1-5 minutes')
                        return
                    if int(ActivityThresholdEntry.get())<0 or int(ActivityThresholdEntry.get())>7:
                        messagebox.showinfo('Message','Invalid Input for Activity Threshold \nMust be within 0-7 corresponding to 0 for off up to 7 for very high')
                        return
                    f=open(paramfilename,"a")
                    f.write("Pacing mode: VVIR \n")
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

                    data_array = np.arange(27)
                    data_array[0]=np.uint16(16)
                    data_array[1]=np.uint16(11)
                    data_array[2]=np.uint16(LowerRateLimitEntry.get())
                    data_array[3]=np.uint16(UpperRateLimitEntry.get())
                    data_array[4]=np.uint16(0)
                    data_array[5]=np.uint16(0)
                    data_array[6]=np.uint16(0)
                    data_array[7]=np.uint16(0)
                    data_array[8]=np.uint16(0)
                    data_array[9]=np.uint16(1000*float(VentricularAmplitudeEntry.get()))
                    data_array[10]=np.uint16(0)
                    data_array[11]=np.uint16(10*float(VentricularPulseWidthEntry.get()))
                    data_array[12]=np.uint16(0)
                    data_array[13]=np.uint16(1000*float(VentricularSensitivityEntry.get()))
                    data_array[14]=np.uint16(VRPEntry.get())
                    data_array[15]=np.uint16(0)
                    data_array[16]=np.uint16(0)
                    data_array[17]=np.uint16(0)
                    data_array[18]=np.uint16(HysteresisEntry.get())
                    data_array[19]=np.uint16(RateSmoothEntry.get())
                    data_array[20]=np.uint16(0)
                    data_array[21]=np.uint16(0)
                    data_array[22]=np.uint16(0)
                    data_array[23]=np.uint16(ActivityThresholdEntry.get())
                    data_array[24]=np.uint16(ReactionTimeEntry.get())
                    data_array[25]=np.uint16(ResponseFactorEntry.get())
                    data_array[26]=np.uint16(RecoveryTimeEntry.get())



                    print(data_array)

                    byte_array=struct.pack('<H', 16)
                    byte_array+=struct.pack('<H',11)
                    byte_array+=struct.pack('<H',np.uint16(LowerRateLimitEntry.get()))
                    byte_array+=struct.pack('<H',np.uint16(UpperRateLimitEntry.get()))
                    byte_array+=struct.pack('<H',0)
                    byte_array+=struct.pack('<H',0)
                    byte_array+=struct.pack('<H',0)
                    byte_array+=struct.pack('<H',0)
                    byte_array+=struct.pack('<H', 0)
                    byte_array+=struct.pack('<H', np.uint16(1000*float(VentricularAmplitudeEntry.get())))
                    byte_array+=struct.pack('<H', 0)
                    byte_array+=struct.pack('<H',np.uint16(10*float(VentricularPulseWidthEntry.get())))
                    byte_array+=struct.pack('<H', 0)
                    byte_array+=struct.pack('<H',1000*float(VentricularSensitivityEntry.get()))
                    byte_array+=struct.pack('<H',np.uint16(VRPEntry.get()))
                    byte_array+=struct.pack('<H', 0)
                    byte_array+=struct.pack('<H', 0)
                    byte_array+=struct.pack('<H',0)
                    byte_array+=struct.pack('<H', np.uint16(HysteresisEntry.get()))
                    byte_array+=struct.pack('<H', np.uint16(RateSmoothEntry.get()))
                    byte_array+=struct.pack('<H', 0)
                    byte_array+=struct.pack('<H', 0)
                    byte_array+=struct.pack('<H', 0)
                    byte_array+=struct.pack('<H', np.uint16(ActivityThresholdEntry.get()))
                    byte_array+=struct.pack('<H', np.uint16(ReactionTimeEntry.get()))
                    byte_array+=struct.pack('<H', np.uint16(ResponseFactorEntry.get()))
                    byte_array+=struct.pack('<H', np.uint16(RecoveryTimeEntry.get()))



                    for k in range(2):
                        ser.write(byte_array)
                    print(byte_array)
                    time.sleep(2)
                    #print(ser.read(1))

                send=Button(VVIRConfigApp,text='Register Parameters',command=clicked_VVIRsend)
                send.place(x=50,y=400)


            if p.get()=="VDDR":
                VDDRConfigApp=Toplevel(self)
                VDDRConfigApp.title("Configuration for VDDR")
                VDDRConfigApp.geometry("400x650")
                LowerRateLimitlabel= Label(VDDRConfigApp, text="Lower Rate Limit[ppm]: ")
                LowerRateLimitlabel.place(x=10, y=10)
                LowerRateLimitEntry=Entry(VDDRConfigApp)
                LowerRateLimitEntry.place(x=200,y=10)
                UpperRateLimitlabel= Label(VDDRConfigApp, text="Upper Rate Limit[ppm]: ")
                UpperRateLimitlabel.place(x=10, y=40)
                UpperRateLimitEntry=Entry(VDDRConfigApp)
                UpperRateLimitEntry.place(x=200,y=40)
                VentricularAmplitudelabel= Label(VDDRConfigApp, text="Ventricular Amplitude[V]: ")
                VentricularAmplitudelabel.place(x=10, y=70)
                VentricularAmplitudeEntry=Entry(VDDRConfigApp)
                VentricularAmplitudeEntry.place(x=200,y=70)
                VentricularPulseWidthlabel= Label(VDDRConfigApp, text="Ventricular Pulse Width[ms]: ")
                VentricularPulseWidthlabel.place(x=10, y=100)
                VentricularPulseWidthEntry=Entry(VDDRConfigApp)
                VentricularPulseWidthEntry.place(x=200,y=100)
                VentricularSensitivitylabel= Label(VDDRConfigApp, text="Ventricular Sensitivity[mV]: ")
                VentricularSensitivitylabel.place(x=10, y=130)
                VentricularSensitivityEntry=Entry(VDDRConfigApp)
                VentricularSensitivityEntry.place(x=200,y=130)
                VRPlabel= Label(VDDRConfigApp, text="VRP[ms]: ")
                VRPlabel.place(x=10, y=160)
                VRPEntry=Entry(VDDRConfigApp)
                VRPEntry.place(x=200,y=160)
                PVARPExtensionlabel= Label(VDDRConfigApp, text="PVARP Extension[ms]: ")
                PVARPExtensionlabel.place(x=10, y=190)
                PVARPExtensionEntry=Entry(VDDRConfigApp)
                PVARPExtensionEntry.place(x=200,y=190)
                RateSmoothlabel= Label(VDDRConfigApp, text="Rate Smoothing: ")
                RateSmoothlabel.place(x=10, y=220)
                RateSmoothEntry=Entry(VDDRConfigApp)
                RateSmoothEntry.place(x=200,y=220)
                FixedAVDelaylabel= Label(VDDRConfigApp, text="Fixed AV Delay[ms]: ")
                FixedAVDelaylabel.place(x=10, y=250)
                FixedAVDelayEntry= Entry(VDDRConfigApp)
                FixedAVDelayEntry.place(x=200,y=250)
                DynamicAVDelaylabel= Label(VDDRConfigApp, text="Dynamic AV Delay: ")
                DynamicAVDelaylabel.place(x=10, y=280)
                DynamicAVDelayEntry= Entry(VDDRConfigApp)
                DynamicAVDelayEntry.place(x=200,y=280)
                ATRDurationlabel= Label(VDDRConfigApp, text="ATR Duration[Cardiac Cycles]: ")
                ATRDurationlabel.place(x=10, y=310)
                ATRDurationEntry= Entry(VDDRConfigApp)
                ATRDurationEntry.place(x=200,y=310)
                ATRFallbackMlabel= Label(VDDRConfigApp, text="ATR fallback mode: ")
                ATRFallbackMlabel.place(x=10, y=340)
                ATRFallbackMEntry= Entry(VDDRConfigApp)
                ATRFallbackMEntry.place(x=200,y=340)
                ATRFallbackTlabel= Label(VDDRConfigApp, text="ATR fallback time[min]: ")
                ATRFallbackTlabel.place(x=10, y=370)
                ATRFallbackTEntry= Entry(VDDRConfigApp)
                ATRFallbackTEntry.place(x=200,y=370)
                MaxRateLimitlabel= Label(VDDRConfigApp, text="Max Sensor Rate[ppm]: ")
                MaxRateLimitlabel.place(x=10, y=400)
                MaxRateLimitEntry=Entry(VDDRConfigApp)
                MaxRateLimitEntry.place(x=200,y=400)
                ActivityThresholdlabel= Label(VDDRConfigApp, text="Activity Threshold: ")
                ActivityThresholdlabel.place(x=10, y=430)
                ActivityThresholdEntry=Entry(VDDRConfigApp)
                ActivityThresholdEntry.place(x=200,y=430)
                ReactionTimelabel= Label(VDDRConfigApp, text="Reaction Time[s]: ")
                ReactionTimelabel.place(x=10, y=460)
                ReactionTimeEntry=Entry(VDDRConfigApp)
                ReactionTimeEntry.place(x=200,y=460)
                ResponseFactorlabel= Label(VDDRConfigApp, text="Response Factor: ")
                ResponseFactorlabel.place(x=10, y=490)
                ResponseFactorEntry=Entry(VDDRConfigApp)
                ResponseFactorEntry.place(x=200,y=490)
                RecoveryTimelabel= Label(VDDRConfigApp, text="Recovery Time[min]: ")
                RecoveryTimelabel.place(x=10, y=520)
                RecoveryTimeEntry=Entry(VDDRConfigApp)
                RecoveryTimeEntry.place(x=200,y=520)

                def clicked_VDDRsend( ):
                    if int(UpperRateLimitEntry.get())<int(LowerRateLimitEntry.get()):
                        messagebox.showinfo('Message', 'Invalid input, Upper Rate limit must be greater than Lower Rate limit')
                        return
                    if int(LowerRateLimitEntry.get())>175 or int(LowerRateLimitEntry.get())<30:
                        messagebox.showinfo('Message','Invalid Input for Lower Rate Limit\nMust be within 30-175ppm')
                        return
                    if int(UpperRateLimitEntry.get())>175 or int(UpperRateLimitEntry.get())<50:
                        messagebox.showinfo('Message','Invalid input for Upper Rate Limit\nMust be within 50-175ppm')
                        return
                    if float(VentricularAmplitudeEntry.get())>7.0 or float(VentricularAmplitudeEntry.get())<0.5:
                        messagebox.showinfo('Message','Invalid Input for Ventricular Amplitude\nMust be within 3.5-7.0V')
                        return
                    if float(VentricularPulseWidthEntry)>20.0 or float(VentricularPulseWidthEntry)<0.1:
                        messagebox.showinfo('Message','Invalid Input for Ventricular Pulse Width\nMust be within 0.1-1.9ms (20ms max for testing purposes)')
                        return
                    if float(VentricularSensitivityEntry.get())>10.0 or float(VentricularSensitivityEntry.get())<1.0:
                        messagebox.showinfo('Message','Invalid input for Ventricular Sensitivity\nMust be within 1.0-10.0mV')
                        return
                    if int(VRPEntry.get())>500 or int(VRPEntry.get())<150:
                        messagebox.showinfo('Message','Invalid Input for VRP\nMust be within 150-500ms')
                        return
                    if int(RateSmoothEntry.get())!=0 and int(RateSmoothEntry.get())!=3 and int(RateSmoothEntry.get())!=6 and int(RateSmoothEntry.get())!=9 and int(RateSmoothEntry.get())!=12 and int(RateSmoothEntry.get())!=15 and int(RateSmoothEntry.get())!=18 and int(RateSmoothEntry.get())!=21:
                        messagebox.showinfo('Message',"Invalid input for Rate Smoothing\n Values include:0, 3, 6, 9, 12, 15, 18, 21")
                        return
                    if int(ATRDurationEntry.get())>2000 or int(ATRDurationEntry.get())<10:
                            messagebox.showinfo('Message','Invalid Input for ATR Duration\nMust be Off or within 10-2000 cardiac cycles')
                            return
                    if int(ATRFallbackTEntry.get())>5 or int(ATRFallbackTEntry.get())<1:
                            messagebox.showinfo('Message','Invalid Input for ATR Fallback\nMust be Off or within 1-5 minutes')
                            return
                    if int(PVARPExtensionEntry.get())>400 or int(PVARPExtensionEntry.get())<50:
                            messagebox.showinfo('Message','Invalid Input for PVARP Extension\nMust be Off or within 50-400ms')
                            return
                    if int(FixedAVDelayEntry.get())>300 or int(FixedAVDelayEntry.get())<70:
                        messagebox.showinfo('Message','Invalid input for Fixed AV Delay\nMust be within 70-300ms')
                        return
                    if int(DynamicAVDelayEntry.get())!=0 or int(DynamicAVDelayEntry.get())!=1: # should we do min dynamic av delay with 30-100?
                        messagebox.showinfo('Message','Invalid Input for Dynamic AV Delay\nMust be 0 or 1')
                        return
                    if int(ReactionTimeEntry.get())<10 or int(ReactionTimeEntry.get())>50:
                        messagebox.showinfo('Message','Invalid Input for Reaction Time \nMust be within 10-50 seconds')
                        return
                    if int(ResponseFactorEntry.get())<1 or int(ResponseFactorEntry.get())>16:
                        messagebox.showinfo('Message','Invalid Input for the response factor\nMust be within 1-16')
                        return
                    if int(RecoveryTimeEntry.get())<2 or int(RecoveryTimeEntry.get())>16:
                        messagebox.showinfo('Message','Invalid Input for Recovery Time \nMust be within 1-5 minutes')
                        return
                    if int(ActivityThresholdEntry.get())<0 or int(ActivityThresholdEntry.get())>7:
                        messagebox.showinfo('Message','Invalid Input for Activity Threshold \nMust be within 0-7 corresponding to 0 for off up to 7 for very high')
                        return
                    f=open(paramfilename,"a")
                    f.write("Pacing mode: VDDR \n")
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

                    f.write("PVARPExtension: ")
                    f.write(PVARPExtensionEntry.get())
                    f.write("\n")

                    f.write("Rate Smoothing: ")
                    f.write(RateSmoothEntry.get())

                    f.write("Fixed Delay: ")
                    f.write(FixedAVDelayEntry.get())
                    f.write("\n")

                    f.write("Dynamic Delay: ")
                    f.write(DynamicAVDelayEntry.get())
                    f.write("\n")

                    f.close()

                    data_array = np.arange(27)
                    data_array[0]=np.uint16(16)
                    data_array[1]=np.uint16(12)
                    data_array[2]=np.uint16(LowerRateLimitEntry.get())
                    data_array[3]=np.uint16(UpperRateLimitEntry.get())
                    data_array[4]=np.uint16(0)
                    data_array[5]=np.uint16(FixedAVDelayEntry.get())
                    data_array[6]=np.uint16(DynamicAVDelayEntry.get())
                    data_array[7]=np.uint16(0)
                    data_array[8]=np.uint16(0)
                    data_array[9]=np.uint16(1000*float(VentricularAmplitudeEntry.get()))
                    data_array[10]=np.uint16(0)
                    data_array[11]=np.uint16(10*float(VentricularPulseWidthEntry.get()))
                    data_array[12]=np.uint16(0)
                    data_array[13]=np.uint16(1000*float(VentricularSensitivityEntry.get()))
                    data_array[14]=np.uint16(VRPEntry.get())
                    data_array[15]=np.uint16(0)
                    data_array[16]=np.uint16(0)
                    data_array[17]=np.uint16(PVARPExtension.get())
                    data_array[18]=np.uint16(0)
                    data_array[19]=np.uint16(RateSmoothEntry.get())
                    data_array[20]=np.uint16(ATRDurationEntry.get())
                    data_array[21]=np.uint16(ATRFallbackMEntry.get())
                    data_array[22]=np.uint16(ATRFallbackTEntry.get())
                    data_array[23]=np.uint16(ActivityThresholdEntry.get())
                    data_array[24]=np.uint16(ReactionTimeEntry.get())
                    data_array[25]=np.uint16(ResponseFactorEntry.get())
                    data_array[26]=np.uint16(RecoveryTimeEntry.get())


                    print(data_array)

                    byte_array=struct.pack('<H', 16)
                    byte_array+=struct.pack('<H',12)
                    byte_array+=struct.pack('<H',np.uint16(LowerRateLimitEntry.get()))
                    byte_array+=struct.pack('<H',np.uint16(UpperRateLimitEntry.get()))
                    byte_array+=struct.pack('<H',0)
                    byte_array+=struct.pack('<H',np.uint16(FixedAVDelayEntry.get()))
                    byte_array+=struct.pack('<H',np.uint16(DynamicAVDelayEntry.get()))
                    byte_array+=struct.pack('<H',0)
                    byte_array+=struct.pack('<H', 0)
                    byte_array+=struct.pack('<H', np.uint16(1000*float(VentricularAmplitudeEntry.get())))
                    byte_array+=struct.pack('<H', 0)
                    byte_array+=struct.pack('<H',np.uint16(10*float(VentricularPulseWidthEntry.get())))
                    byte_array+=struct.pack('<H', 0)
                    byte_array+=struct.pack('<H',1000*float(VentricularSensitivityEntry.get()))
                    byte_array+=struct.pack('<H',np.uint16(VRPEntry.get()))
                    byte_array+=struct.pack('<H', 0)
                    byte_array+=struct.pack('<H', 0)
                    byte_array+=struct.pack('<H',np.uint16(PVARPExtension.get()))
                    byte_array+=struct.pack('<H', 0)
                    byte_array+=struct.pack('<H', np.uint16(RateSmoothEntry.get()))
                    byte_array+=struct.pack('<H', np.uint16(ATRDurationEntry.get()))
                    byte_array+=struct.pack('<H', np.uint16(ATRFallbackMEntry.get()))
                    byte_array+=struct.pack('<H', np.uint16(ATRFallbackTEntry.get()))
                    byte_array+=struct.pack('<H', np.uint16(ActivityThresholdEntry.get()))
                    byte_array+=struct.pack('<H', np.uint16(ReactionTimeEntry.get()))
                    byte_array+=struct.pack('<H', np.uint16(ResponseFactorEntry.get()))
                    byte_array+=struct.pack('<H', np.uint16(RecoveryTimeEntry.get()))




                    for k in range(2):
                        ser.write(byte_array)
                    print(byte_array)
                    time.sleep(2)
                    #print(ser.read(1))



                send=Button(VDDRConfigApp,text='Register Parameters',command=clicked_VDDRsend)
                send.place(x=50,y=550)

            if p.get()=="DOOR":
                DOORConfigApp=Toplevel(self)
                DOORConfigApp.title("Configuration for DOOR")
                DOORConfigApp.geometry("400x650")
                LowerRateLimitlabel= Label(DOORConfigApp, text="Lower Rate Limit[ppm]: ")
                LowerRateLimitlabel.place(x=10, y=10)
                LowerRateLimitEntry=Entry(DOORConfigApp)
                LowerRateLimitEntry.place(x=200,y=10)
                UpperRateLimitlabel= Label(DOORConfigApp, text="Upper Rate Limit[ppm]: ")
                UpperRateLimitlabel.place(x=10, y=40)
                UpperRateLimitEntry=Entry(DOORConfigApp)
                UpperRateLimitEntry.place(x=200,y=40)
                VentricularAmplitudelabel= Label(DOORConfigApp, text="Ventricular Amplitude[V]: ")
                VentricularAmplitudelabel.place(x=10, y=70)
                VentricularAmplitudeEntry=Entry(DOORConfigApp)
                VentricularAmplitudeEntry.place(x=200,y=70)
                VentricularPulseWidthlabel= Label(DOORConfigApp, text="Ventricular Pulse Width[ms]: ")
                VentricularPulseWidthlabel.place(x=10, y=100)
                VentricularPulseWidthEntry=Entry(DOORConfigApp)
                VentricularPulseWidthEntry.place(x=200,y=100)
                AtrialAmplitudelabel= Label(DOORConfigApp, text="Atrial Amplitude[V]: ")
                AtrialAmplitudelabel.place(x=10, y=130)
                AtrialAmplitudeEntry=Entry(DOORConfigApp)
                AtrialAmplitudeEntry.place(x=200,y=130)
                AtrialPulseWidthlabel= Label(DOORConfigApp, text="Atrial Pulse Width[ms]: ")
                AtrialPulseWidthlabel.place(x=10, y=160)
                AtrialPulseWidthEntry=Entry(DOORConfigApp)
                AtrialPulseWidthEntry.place(x=200,y=160)
                MaxRateLimitlabel= Label(DOORConfigApp, text="Max Sensor Rate[ppm]: ")
                MaxRateLimitlabel.place(x=10, y=190)
                MaxRateLimitEntry=Entry(DOORConfigApp)
                MaxRateLimitEntry.place(x=200,y=190)
                ActivityThresholdlabel= Label(DOORConfigApp, text="Activity Threshold: ")
                ActivityThresholdlabel.place(x=10, y=220)
                ActivityThresholdEntry=Entry(DOORConfigApp)
                ActivityThresholdEntry.place(x=200,y=220)
                ReactionTimelabel= Label(DOORConfigApp, text="Reaction Time[s]: ")
                ReactionTimelabel.place(x=10, y=250)
                ReactionTimeEntry=Entry(DOORConfigApp)
                ReactionTimeEntry.place(x=200,y=250)
                ResponseFactorlabel= Label(DOORConfigApp, text="Response Factor: ")
                ResponseFactorlabel.place(x=10, y=280)
                ResponseFactorEntry=Entry(DOORConfigApp)
                ResponseFactorEntry.place(x=200,y=280)
                RecoveryTimelabel= Label(DOORConfigApp, text="Recovery Time[min]: ")
                RecoveryTimelabel.place(x=10, y=310)
                RecoveryTimeEntry=Entry(DOORConfigApp)
                RecoveryTimeEntry.place(x=200,y=310)
                FixedAVDelaylabel= Label(DOORConfigApp, text="Fixed AV Delay[ms]: ")
                FixedAVDelaylabel.place(x=10, y=340)
                FixedAVDelayEntry= Entry(DOORConfigApp)
                FixedAVDelayEntry.place(x=200,y=340)

                def clicked_DOORsend( ):
                    if int(UpperRateLimitEntry.get())<int(LowerRateLimitEntry.get()):
                        messagebox.showinfo('Message', 'Invalid input, Upper Rate limit must be greater than Lower Rate limit')
                        return
                    if int(ReactionTimeEntry.get())<10 or int(ReactionTimeEntry.get())>50:
                        messagebox.showinfo('Message','Invalid Input for Reaction Time \nMust be within 10-50 seconds')
                        return
                    if int(ResponseFactorEntry.get())<1 or int(ResponseFactorEntry.get())>16:
                        messagebox.showinfo('Message','Invalid Input for the response factor\nMust be within 1-16')
                        return
                    if int(RecoveryTimeEntry.get())<2 or int(RecoveryTimeEntry.get())>16:
                        messagebox.showinfo('Message','Invalid Input for Recovery Time \nMust be within 1-5 minutes')
                        return
                    if int(ActivityThresholdEntry.get())<0 or int(ActivityThresholdEntry.get())>7:
                        messagebox.showinfo('Message','Invalid Input for Activity Threshold \nMust be within 0-7 corresponding to 0 for off up to 7 for very high')
                        return
                    if int(LowerRateLimitEntry.get())>175 or int(LowerRateLimitEntry.get())<30:
                        messagebox.showinfo('Message','Invalid Input for Lower Rate Limit\nMust be within 30-175ppm')
                        return
                    if int(UpperRateLimitEntry.get())>175 or int(UpperRateLimitEntry.get())<50:
                        messagebox.showinfo('Message','Invalid input for Upper Rate Limit\nMust be within 50-175ppm')
                        return
                    if (float(AtrialAmplitudeEntry.get()))>6.2 or (float(AtrialAmplitudeEntry.get()))<0.5:
                        messagebox.showinfo('Message','Invalid Input for Atrial Amplitude\nMust be within 0.5-3.2V (<6V for testing purposes)') # regulated
                        return
                    if float(AtrialPulseWidthEntry.get())>20.0 or float(AtrialPulseWidthEntry.get())<0.1:
                        messagebox.showinfo('Message','Invalid Input for Atrial Pulse Width\nMust be within 0.1-1.9ms (20ms max for testing purposes)')
                        return
                    if float(VentricularAmplitudeEntry.get())>7.0 or float(VentricularAmplitudeEntry.get())<0.5:
                        messagebox.showinfo('Message','Invalid Input for Ventricular Amplitude\nMust be within 3.5-7.0V')
                        return
                    if float(VentricularPulseWidthEntry.get())>20.0 or float(VentricularPulseWidthEntry.get())<0.1:
                        messagebox.showinfo('Message','Invalid Input for Ventricular Pulse Width\nMust be within 0.1-1.9ms(20ms max for testing purposes)')
                        return
                    if int(FixedAVDelayEntry.get())>300 or int(FixedAVDelayEntry.get())<70:
                        messagebox.showinfo('Message','Invalid input for Fixed AV Delay\nMust be within 70-300ms')
                        return

                    f=open(paramfilename,"a")
                    f.write("Pacing mode: DOOR \n")
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

                    f.write("Atrial Amplitude: ")
                    f.write(AtrialAmplitudeEntry.get())
                    f.write("\n")

                    f.write("Atrial Pulse Width: ")
                    f.write(AtrialPulseWidthEntry.get())

                    f.write("Fixed Delay: ")
                    f.write(FixedAVDelayEntry.get())

                    f.write("\n")

                    f.close()

                    data_array = np.arange(27)
                    data_array[0]=np.uint16(16)
                    data_array[1]=np.uint16(13)
                    data_array[2]=np.uint16(LowerRateLimitEntry.get())
                    data_array[3]=np.uint16(UpperRateLimitEntry.get())
                    data_array[4]=np.uint16(0)
                    data_array[5]=np.uint16(FixedAVDelayEntry.get())
                    data_array[6]=np.uint16(0)
                    data_array[7]=np.uint16(0)
                    data_array[8]=np.uint16(1000*float(AtrialAmplitudeEntry.get()))
                    data_array[9]=np.uint16(1000*float(VentricularAmplitudeEntry.get()))
                    data_array[10]=np.uint16(10*float(AtrialPulseWidthEntry.get()))
                    data_array[11]=np.uint16(10*float(VentricularPulseWidthEntry.get()))
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
                    data_array[23]=np.uint16(ActivityThresholdEntry.get())
                    data_array[24]=np.uint16(ReactionTimeEntry.get())
                    data_array[25]=np.uint16(ResponseFactorEntry.get())
                    data_array[26]=np.uint16(RecoveryTimeEntry.get())

                    print(data_array)

                    byte_array=struct.pack('<H', 16)
                    byte_array+=struct.pack('<H', 13)
                    byte_array+=struct.pack('<H',np.uint16(LowerRateLimitEntry.get()))
                    byte_array+=struct.pack('<H',np.uint16(UpperRateLimitEntry.get()))
                    byte_array+=struct.pack('<H', 0)
                    byte_array+=struct.pack('<H', np.uint16(FixedAVDelayEntry.get()))
                    byte_array+=struct.pack('<H', 0)
                    byte_array+=struct.pack('<H', 0)
                    byte_array+=struct.pack('<H', np.uint16(1000*float(AtrialAmplitudeEntry.get())))
                    byte_array+=struct.pack('<H', np.uint16(1000*float(VentricularAmplitudeEntry.get())))
                    byte_array+=struct.pack('<H', np.uint16(10*float(AtrialPulseWidthEntry.get())))
                    byte_array+=struct.pack('<H', np.uint16(10*float(VentricularPulseWidthEntry.get())))
                    byte_array+=struct.pack('<H', 0)
                    byte_array+=struct.pack('<H', 0)
                    byte_array+=struct.pack('<H', 0)
                    byte_array+=struct.pack('<H', 0)
                    byte_array+=struct.pack('<H', 0)
                    byte_array+=struct.pack('<H', 0)
                    byte_array+=struct.pack('<H', 0)
                    byte_array+=struct.pack('<H', 0)
                    byte_array+=struct.pack('<H', 0)
                    byte_array+=struct.pack('<H', 0)
                    byte_array+=struct.pack('<H', 0)
                    byte_array+=struct.pack('<H', np.uint16(ActivityThresholdEntry.get()))
                    byte_array+=struct.pack('<H', np.uint16(ReactionTimeEntry.get()))
                    byte_array+=struct.pack('<H', np.uint16(ResponseFactorEntry.get()))
                    byte_array+=struct.pack('<H', np.uint16(RecoveryTimeEntry.get()))

                    for k in range(2):
                        ser.write(byte_array)
                    print(byte_array)
                    time.sleep(2)
                    #print(ser.read(1))



                send=Button(DOORConfigApp,text='Register Parameters',command=clicked_DOORsend)
                send.place(x=50,y=340)



        def clicked_reg( ):
            f=open(userfilename,"a")
            f.close()
            count=0
            f=open(userfilename,"r")
            for line in f:
                if count < 9:
                    count += 1
                else:
                    messagebox.showinfo('Message', 'Maximum number of users reached.')
                    f.close()
                    return
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
