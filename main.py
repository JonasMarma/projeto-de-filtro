#import numpy as np
#from scipy.io import wavfile
import pyaudio

FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 8000
CHUNK = 1024
RECORD_SECONDS = 30

p = pyaudio.PyAudio()

# Iniciar uma stream de ouput no output_device_id especificado
def start_out_stream(outDevice):
    stream = p.open(format=FORMAT, channels=1, rate=8000, output_device_index=outDevice, output=True)
    return stream

# Iniciar uma stream de input no input_device_id especificado
def start_input_stream(inDevice):
    stream = p.open(format=FORMAT, channels=1, rate=8000, input_device_index=inDevice, input=True)
    return stream

# Listar os dispositivos de audio conectados
def listar_devices():
    info = p.get_host_api_info_by_index(0)
    num_devices = info.get('deviceCount')

    print('Foram detectados os seguintes dispositivos:')

    print('INPUT')
    for i in range(0, num_devices):
        if (p.get_device_info_by_host_api_device_index(0, i).get('maxInputChannels')) > 0:
            print("ID: ", i, " : ", p.get_device_info_by_host_api_device_index(0, i).get('name'))

    print('OUTPUT')
    for i in range(0, num_devices):
        if (p.get_device_info_by_host_api_device_index(0, i).get('maxOutputChannels')) > 0:
            print("ID: ", i, " : ", p.get_device_info_by_host_api_device_index(0, i).get('name'))


####################################

# Caminho dos dados:
# Microfone Real --in_stream--> Este programa --out_stream--> Input do VB-audio --> Output do VB-audio (micrfone virtual)

####################################

listar_devices()

input_ID = int(input("Por favor, informe o ID do seu microfone:\n"))
output_ID = int(input("Por favor, informe o ID do dispositivo de output de audio CABLE:\n"))

# Iniciar as streams de audio

# O output desse programa é a porta criada pelo VB-Audio
# Essa porta é vista pelo programa como uma caixa de som normal
# Mas na verdade, o VB-audio desvia os dados que chegam para uma porta de microfone virtual
# Esse micrfone virtual deve ser configurado commo input do programa de audio final (exemplo: Google Meets)
#https://vb-audio.com/Cable/
out_stream = start_out_stream(output_ID)

# Stream para a entrada e audio do microfone real
in_stream = start_input_stream(input_ID)

# Ouvir e reproduzir o miucrofone por 30 segundos
for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
    # Ler o microfone
    data = in_stream.read(CHUNK)
    
    # FAZER AQUI  FILTRAGEM!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    # (ou não)

    # Escrever no cabo
    out_stream.write(data)

print("FIM")

# Fechar streams
out_stream.stop_stream()
out_stream.close()

in_stream.stop_stream()
in_stream.close()

p.terminate()
