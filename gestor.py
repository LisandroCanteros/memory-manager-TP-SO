from os import system, name

def clear():
    if name == 'nt':
        _ = system('cls')

    else:
        _ = system('clear')

procesos = []
particiones = [{'particion':1, 'tamaño':60, 'estado':'libre', 'fragmentacion': 0},
               {'particion':2, 'tamaño':120, 'estado':'libre', 'fragmentacion': 0},
               {'particion':3, 'tamaño':250, 'estado':'libre', 'fragmentacion': 0}]

instante = 0
cpu = False

def cargar_procesos():                                      #función que solicita información del proceso al usuario y carga cada proceso en una lista.
    print("[CARGA DE PROCESOS]")
   
    nro_proc = int(input("Ingrese número de procesos (máx 10):\t"))
    clear()
    while (nro_proc > 10):
        print("El número de procesos no puede ser mayor a 10")
        nro_proc = int(input("Ingrese numero de procesos:\t"))
        
    for i in range(nro_proc):
        print("[CARGA DE PROCESOS]")
        idp = input("Ingrese ID del proceso:\t")
        tamaño = int(input("Ingrese tamaño del proceso (máx 250):\t"))
        while(tamaño > 250):
            tamaño = int(input('''El tamaño del proceso no puede ser mayor a 250.\nPor favor, ingrese un valor menor o igual a 250\t'''))
        arribo = int(input("Ingrese tiempo de arribo del proceso:\t"))
        while(instante > arribo):
            print("\nEl tiempo de arribo no puede ser menor a %s, el instante actual\n" % instante)
            arribo = int(input("Por favor, ingrese un nuevo tiempo de arribo:\t"))
        irrupcion = int(input("Ingrese tiempo de irrupción del proceso:\t"))
        procesos.append({'id': idp,'tamaño': tamaño, 'tarribo': arribo, 'tirrup': irrupcion, 'estado':'listo', 'particion':'N/A', 'ingreso':'N/A'})
            
        clear()
        
cargar_procesos()

procesos = sorted(procesos, key=lambda d: (d['tirrup'],d['tarribo']))   #ordenar los procesos en la lista,
                                                                        #primero por su tiempo de irrupción, y segundo por su tiempo de arribo.

print('PROCESOS CARGADOS POR EL USUARIO')          #imprimir procesos cargados por el usuario.
copia = procesos
for i in copia:
    print('ID:', i['id'], '|| TAMAÑO:', i['tamaño'], '|| ARRIBO:', i['tarribo'], '|| IRRUPCIÓN:', i['tirrup'])

input("\nPresiones enter para comenzar.")

while(1):
    clear()
    
    print('PROCESOS CARGADOS POR EL USUARIO')          #imprimir procesos cargados por el usuario.
    for i in copia:
        print('ID:', i['id'], '|| TAMAÑO:', i['tamaño'], '|| ARRIBO:', i['tarribo'], '|| IRRUPCIÓN:', i['tirrup'])

    print("////////////////////////////////////////////////////////\n")
    
    for i in range(len(procesos)):                              #asigna los procesos a una particion de acuerdo a su tamaño
       if (procesos[i]['estado'] == 'listo' and procesos[i]['tarribo'] <= instante ):                   #proceso listo y tiempo de arribo menor o igual al instante

            if (procesos[i]['tamaño'] <= particiones[0]['tamaño']) and (particiones[0]['estado'] == 'libre'):   #tamaño menor a la partición y partición libre
                particiones[0]['estado'] = 'ocupado'
                particiones[0]['fragmentacion'] = particiones[0]['tamaño']-procesos[i]['tamaño']
                
                procesos[i]['estado'] = 'memoria'
                procesos[i]['particion'] = 0
              
            
                
            elif (procesos[i]['tamaño'] <= particiones[1]['tamaño']) and (particiones[1]['estado'] == 'libre'):
                particiones[1]['estado'] = 'ocupado'
                particiones[1]['fragmentacion'] = particiones[1]['tamaño']-procesos[i]['tamaño']
                
                procesos[i]['estado'] = 'memoria'
                procesos[i]['particion'] = 1
             

                
            elif (procesos[i]['tamaño'] <= particiones[2]['tamaño']) and (particiones[2]['estado'] == 'libre'):
                particiones[2]['estado'] = 'ocupado'
                particiones[2]['fragmentacion'] = particiones[2]['tamaño']-procesos[i]['tamaño']
                
                procesos[i]['estado'] = 'memoria'
                procesos[i]['particion'] = 2
           
                
    for i in range(len(procesos)):              #si la CPU está libre, se la asigna al proceso que tenga menor tiempo de irrupción.
        if (procesos[i]['tarribo'] <= instante) and (procesos[i]['estado'] == 'memoria') and (cpu == False):
            procesos[i]['estado'] = 'ejecutandose'
            procesos[i]['ingreso'] = instante
            cpu = True

    print("\t===>Instante: ", instante)
            
    print('[COLA DE LISTOS]')                   #imprimir cola de listos
    for i in procesos:
        if i['estado'] != 'ejecutandose' and i['tarribo'] <= instante:
            print('ID:', i['id'], '|| TAMAÑO:', i['tamaño'], '|| ARRIBO:', i['tarribo'], '|| IRRUPCIÓN:', i['tirrup'])
                
    print('\n[PROCESOS EN MEMORIA]')            #imprimir procesos en memoria, su partición y la fragmentación interna.
    for i in procesos:
        if ((i['estado'] == 'memoria' or i['estado'] == 'ejecutandose') and (i['tarribo'] <= instante)):
            print('Partición ', i['particion'], '(', particiones[i['particion']]['tamaño'],'K):\t Fragmentación interna: ',particiones[i['particion']]['fragmentacion'],'K')
            print('ID:', i['id'], '|| TAMAÑO:', i['tamaño'], '|| ARRIBO:', i['tarribo'], '|| IRRUPCIÓN:', i['tirrup'])
            print('\n')


    
    print('[PROCESO EN EJECUCIÓN]')                   #imprimir proceso en ejecución
    for i in procesos:
        if i['estado'] == 'ejecutandose':
            print('ID:', i['id'], '|| TAMAÑO:', i['tamaño'], '|| ARRIBO:', i['tarribo'], '|| IRRUPCIÓN:', i['tirrup'])
                                           
    n = len(procesos)
    i = 0
    while (i < n):                                                          #ciclo que verifica si un proceso alcanzó su tiempo de irrupción
        if ((procesos[i]['estado'] == 'ejecutandose') and (procesos[i]['ingreso'] + procesos[i]['tirrup'] -1) == instante):
            temp = procesos[i]['particion']                                 #temp contiene el indice de la partición a la cual el proceso fue asignado
            particiones[temp]['estado'] = 'libre'                           #y es usado para poner la particion a libre cuando el proceso termine de ejecutarse
            particiones[temp]['fragmentacion'] = 0
            procesos.pop(i)                                                 #elimina procesos de la lista si alcanzaron su tiempo de irrupción
            cpu = False
            n -= 1
            i -= 1
        i += 1
        

        
    for i in range(len(particiones)):                           #comienza swap out
        particiones[i]['estado'] = 'libre'                      #desasignar los procesos de las particiones
        particiones[i]['fragmentacion'] = 0

    for i in range(len(procesos)):                              #excepto el proceso en ejecución
        if procesos[i]['estado'] != 'ejecutandose':             # (los procesos que fueron desasignados vuelven a cargarse en la próxima iteración,
            procesos[i]['estado'] = 'listo'                     # de esta manera, si en el instante actual ingresó un proceso con menor tiempo de irrupción
            procesos[i]['particion'] = 'N/A'                    # que los que ya estaban, podrá cargarse en memoria y ejecutarse primero)

        else:
            particiones[procesos[i]['particion']]['estado'] = 'ocupado'
            particiones[procesos[i]['particion']]['fragmentacion'] = particiones[procesos[i]['particion']]['tamaño'] - procesos[i]['tamaño']

                                                                #fin swap out                

    procesos = sorted(procesos, key=lambda d: (d['tirrup']))

   
    input("\nPresiones enter para avanzar un instante.")
    print("////////////////////////////////////////////////////////\n")
    instante += 1
    if (len(procesos) == 0):                            #cuando la lista de procesos esté vacía, salir del ciclo principal y terminar ejecución
            break
    
print("\t===>Instante: ", instante)
input("\nEjecución finalizada. Presione enter para terminar.")


