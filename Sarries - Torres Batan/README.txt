UBA - FCEyN - DC
Introducciòn a las tecnologìas del habla
2° Cuatrimestre 2014
Prof. Agustìn Gravano


TP 1 - Torres Batàn y Sarriès

Praat 5.3.82


A continuaciòn listamos las etapas de elaboraciòn del presente tp.


*****************************
 (1) Grabación en portadora
*****************************
tamáta  takáta  tasáta  tapáta  taláta
támata  tákata  tásata  tápata  tálata
mata kata sata pata lata
katá


*****************************
 (2) Etiquetado
*****************************
am mA ak kA as sA ap pA al lA
Am ma Ak ka As sa Ap pa Al la
-m -k -s -p -l a-
A- 


*****************************
 (3) Script generador de Wavs
*****************************
Se generaron 27 archivos wav
con el script provisto
(save_labeled_intervals_to_wav_sound_files.praat)


*****************************
 (4) Python
*****************************
 (4.a) Parseo de cadena y síntesis
       Somos optimistas en cuanto a la cadena de entrada y salida. Prete
       tendemos que esté bien formada, pero en caso contrario existirá un error
       en el parseo. Con respecto al archivo de salida no realizamos ningún
       chequeo de que sea correcto. Para a concatenación, una vez que esté 
       creado el script de praat, lo ejecutamos. Este script abre cada 
       difono y los renombra. Una vez abiertos, los selecciona y concatena con 
       Concatenate recoverably.
 (4.b) Modificaciòn pitch para pregunta
       Creamos una clase que manejará todas las modificaciones 
       posibles para con el pitch. Además de ofrecernos operaciones 
       basicas como el mínimo, el máximo y el promedio, permite ejecutar 
       funciones sobre segmentos determinados para cumplir con el objetivo.
       Entre ellas están 'flatten', 'average' y 'linear' aunque aplicando linear 
       sucesivas veces en un determinado segmento podrá hacer variar el pitch no
       linealmente.
       Nuestra idea fue, entonces, aplicar una función flatten o average
       al string ya sintetizado. Esto pudimos observar que funcionaba, tanto
       el flatten como la función de promedio que amenizaba las diferencias 
       de pitch. Luego, podríamos modificar el pitch progresivamente hasta
       alcanzar una entonación hacia el final de la oración (donde podríamos
       modificarla ya no progresivamente, sino en forma abrupta) para simular
       que fuera una pregunta. No obtuvimos grandes resultados al momento
       de escucharlos, si bien los cambios se reflejan en los archivos 
       .PitchTier.
       Nos dimos cuenta además que las letras acentuadas, en nuestro caso, 
       interfieren con el deseo de darle entonación al final de la oración.
       Sabemos que hay preguntas, por ejemplo en inglés, que poseen diferentes 
       tipos de entonación, las que empiezan con how, which, what, etc., poseen
       entonación al principio, sin embargo no las tuvimos en cuenta.

