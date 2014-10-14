import os
import re
import sys
import math

class PitchManager:
    """Clase que maneja el pitch tier de una sintesis"""
    def __init__(self, soundSynthesis, pitchRange=(50,300)):
        """Inicializamos la clase. self.pitchier
        los obtemos parseando el archivo .PitchTier"""
        self.synthesis = soundSynthesis
        self.pitchTier = []
        self.range = pitchRange
        #praat extraer-pitch-track.praat 12345.wav 12345.PitchTier 50 300
        #try:
        print("* Running: 'praat scripts/extraer-pitch-track.praat ../scripts/"+
              self.synthesis +".wav " + self.synthesis +
              ".PitchTier " + str(pitchRange[0]) + " " +
              str(pitchRange[1])+"'" )
        
        os.system("praat scripts/extraer-pitch-track.praat ../scripts/"+
                  self.synthesis +".wav " + self.synthesis +
                  ".PitchTier " + str(pitchRange[0]) + " " + str(pitchRange[1]))
        
        f = open("scripts/" + self.synthesis + ".PitchTier","r")
        for line in f:
            if line.startswith('    number'):
                 number = re.search('([0-9]+.[0-9]+)',line)
            if line.startswith('    value'):
                value = re.search('([0-9]+.[0-9]+)',line)
                self.pitchTier.append( [float(number.group(1)), \
                                        float(value.group(1))] )
        f.close()
        
    # except:
    #     print ("Can't open file")
    
    def maxPitch(self):
        return max(self.pitchTier)
    
    def minPitch(self):
        return min(self.pitchTier)
    
    def meanPitch(self):
        sum = 0
        for i in range(0,len(self.pitchTier)):
            sum += self.pitchTier[i][1]
        return sum/len(self.pitchTier)
    
    def modifyPitch(self, opt,limite, first, last, style="asc"):
        """Este metodo modifica el pitch tier referido a la sintesis
        que hicimos previamente. Para ello se especifica una opcion
        que varia entre flatten (asigna un determinado pitch a cada punto),
        average (setea el pitch cercano a la media) y linear (modifica el pitch
        con una funcion linear)
        Limite refiere a la maxima frecuencia fundamental que queramos alcanzar.
        First y last definen un segmento donde aplicar las modificaciones.
        Style tiene coherencia cuando se selecciona la opcion linear para
        definir si es ascendente o descendente."""
        start=0
        end=1
        
        if last < first:
            exit(2)
        
        aux = 0
        for i in range(0,len(self.pitchTier)):
            if first <=  float('%.2f'%(self.pitchTier[i][0])) and aux==0:
                start = i #self.pitchTier[i][0]
                aux=1
            elif last <= float('%.2f'%(self.pitchTier[i][0])) and aux==1:
                end = i
                break;
            elif i == len(self.pitchTier)-1 and aux==1 :
                end = i
                break;
        
        if opt=='flatten':
            for i in range(0, len(self.pitchTier)):
                    self.pitchTier[i][1] = float(limite)
        
        if opt == 'average':
            avg = float(self.meanPitch())
            for i in range(start, end):
                    self.pitchTier[i][1] = self.pitchTier[i][1] - \
                            (1.0 * (self.pitchTier[i][1] - avg)/2)
        
        if opt == 'linear':
            avg = float(self.meanPitch())
            rate = (limite - avg) / (end - start)
            # print "** " + str(avg)
            # print "** rate" +str(rate)
            # print "** start:" + str(start)
            # print "** end:" + str(end)
            if style == "asc":
                for i in range(start, end):
                    self.pitchTier[i][1] = self.pitchTier[i-1][1] + rate
                self.pitchTier[end][1] = self.pitchTier[end-1][1] + rate
            elif style == "dsc":
                self.pitchTier[start][1] = limite
                for i in range(start+1, end):
                    self.pitchTier[i][1] = self.pitchTier[i-1][1] - rate
                    
                self.pitchTier[end][1] = self.pitchTier[end-1][1] + rate
    
    def savePitch(self):
        """Guarda el archivo modificado de .PitchTier"""
        index = 0
        #Creamos el archivo modificado
        fw = open('scripts/' + self.synthesis + '-mod.PitchTier', 'w')
        with open('scripts/' + self.synthesis + '.PitchTier') as fr:
            for line in fr:
                if line.startswith('    value ='):
                    linestring = re.split(' = ',line)
                    newstring = linestring[0]+ ' = ' \
                                +str(self.pitchTier[index][1])
                    fw.write(newstring+' \n')
                    index += 1
                else:
                    fw.write(line)
        fw.close()
        
        #praat reemplazar-pitch-track.praat 12345.wav
        #                12345-mod.PitchTier 12345-mod.wav 50 300
        #Ejecutamos el script para reemplazar el Pitch Track
        print("* Running: 'praat scripts/reemplazar-pitch-track.praat ../scripts/"+
              self.synthesis +".wav " + self.synthesis +
              "-mod.PitchTier " + self.synthesis +"-mod.wav "
              + str(self.range[0]) + " " + str(self.range[1]) + "'" )
        
        os.system("praat scripts/reemplazar-pitch-track.praat ../scripts/"+
              self.synthesis +".wav " + self.synthesis +
              "-mod.PitchTier " + self.synthesis +"-mod.wav " +
                  str(self.range[0]) + " " + str(self.range[1]))
    
    def getSynthesis(self):
        return self.synthesis
    
    def getPitchTier(self):
        return self.pitchTier


# Funcion para generar el script de Praat que sintetiza la cadena de entrada
# Devuelve una tupla con las lecturas y las selecciones, asi una vez
# concatenadas se podra ejecutar.
def generateScript(diPhone, reads, selects, count):
    if len(diPhone) == 1 and count == 0:
        reads += 'Read from file: "sounds/-'+ diPhone  +'.wav" \n'
        reads += 'Rename: "difono'+ str(count) +'"\n'
        selects += 'select Sound difono'+ str(count) +'\n'
    elif len(diPhone) == 1 and count != 0:
        reads += 'Read from file: "sounds/'+ diPhone +'-.wav"\n'
        reads += 'Rename: "difono'+ str(count) +'"\n'
        selects += 'plus Sound difono'+ str(count) +'\n'
    else:
        reads += 'Read from file: "sounds/'+ diPhone +'.wav"\n'
        reads += 'Rename: "difono'+ str(count) +'"\n'
        selects += 'plus Sound difono'+ str(count) +'\n'
    return (reads, selects)
    

# Obtiene tiempos donde comienza cada segmento
# referido a un difono
def processSegments():
    f = open('scripts/SegmentList.txt', 'r')
    segment = []
    start = False
    par = False
    
    segment.append(0)
    for line in f:
        if not line.startswith('"difono') and start:
            if par:
                line = line.split('\n')
                segment.append(float(line[0]))
                par = False
            else:
                par = True
        elif line.startswith('"difono') and not start:
            start = True
    f.close()
    return segment
    

# Comienzo de programa"
def main(argv):
    string = ''
    outputfile = ''
    
    if len(argv) != 2:
        print "Cantidad insuficiente de parametros."
        sys.exit(2)
    else:
        string = argv[0]
        outputfile = argv[1].split('.')[0]
        ext = argv[1].split('.')[1]
    
    # Armado de la secuencia de difonos correspondiente
    # a la cadena que se va a sintetizar
    sil = re.findall("([m|k|s|p|l][a|A]|\?)",string)
    sil1 = re.findall("([a|A][m|k|s|p|l]|[m|k|s|p|l|a|A])",string)
    
    for i,v in enumerate(sil):
        sil1.insert(2*i+1,v)
    
    qm = sil1.pop()
    diPhones = sil1[0:len(sil1)]
    print "* Processing string to Di'Phones:"
    print "  " + str(diPhones)
    
    # Analisis del string para determinar si
    # es necesario modificar la prosodia
    if qm == '?':
        setProsody = True
        print "* Setting Prosody"
    else:
        setProsody = False
    
    if diPhones[len(diPhones)-1] == 'A':
        accentInLast = True
        print "* Last vocal has accent: " + diPhones[len(diPhones)-1]
    else:
        accentInLast = False
    
    # Generar script de Praat que sintetiza la cadena de entrada
    reads = ''
    selects = ''
    count = 0
    
    for diPhone in diPhones:
        (reads,selects) = generateScript(diPhone, reads, selects, count)
        count+=1
    
    selects += 'Concatenate recoverably\n'
    selects += 'select Sound chain\n'
    selects += 'Save as WAV file... scripts/chain.wav'
    selects += '\nselect TextGrid chain\n'
    selects += 'Save as short text file... scripts/SegmentList.txt'
    
    #Guardamos y ejecutamos el script.
    f = open('synthesis.praat', 'w')
    f.write(reads)
    f.write(selects)
    f.close()
    os.system("praat synthesis.praat")
    
    #Modificamos la prosodia
    if setProsody:
        # segment guarda la longitud de los difonos
        # de la cadena procesada
        segments = processSegments()

        # creamos una instancia para manejar el pitch
        s=PitchManager('chain', (50,200))
        lsegments = len(segments)
        
        #Modificamos el pitch
        s.modifyPitch('average', 0, 0, lsegments)
        for i in range(0, lsegments):
            if accentInLast and i == lsegments - 4:
                s.modifyPitch('linear', 200, segments[i],segments[i+3])
            elif not accentInLast:
                if i == lsegments-1:
                    s.modifyPitch('linear', 120, \
                                  segments[int(1*lsegments/2)],segments[i])
                    
                    s.modifyPitch('linear',200, \
                                  segments[int(3*lsegments/4)],segments[i])

        s.savePitch()
        os.system('mv '+   'scripts/chain-mod' + '.' +ext + ' '+ outputfile + '.'+ ext )
    else:
        os.system('mv '+   'scripts/chain' + '.' +ext + ' '+ outputfile + '.'+ ext )
        
if __name__ == "__main__":
    main(sys.argv[1:])

