MOTHERBOARDS='mb'
CPUS='cp'
HARDDRIVES='hd'
GRAPHICCARDS='gc'
RAM='ra'
LAPTOPS='la'
GAMINGLAPTOPS='gl'

CAT_CHOICES = (
    (MOTHERBOARDS, 'Placas base'),
    (CPUS, 'CPUs'),
    (HARDDRIVES, 'Discos Duros'),
    (GRAPHICCARDS, 'Tarjetas gráficas'),
    (RAM, 'RAM'),
    (LAPTOPS, 'Portátiles'),
    (GAMINGLAPTOPS, 'Portátiles Gaming'),
)

#Import:
#from .choices import *

#Model:
#categories = models.CharField(max_length=2, choices = CAT_CHOICES, default = LAPTOPS)