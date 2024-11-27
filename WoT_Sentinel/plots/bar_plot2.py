import matplotlib
import matplotlib.pyplot as plt
import numpy as np


#cien_means, cien_std = (0.230291446, 0.144851883, 0.762915174, 2.314443469), (0.171028159, 0.010563822, 0.045962008, 0.567992473)
#diez_means, diez_std = (0.155614956, 0.197297904, 0.772110624, 2.531072231), (0.03096019, 0.071763149, 0.049616018, 0.662386991)
#uno_means, uno_std = (0.183372209, 0.173916689, 0.852517469, 2.17397783), (0.096294131, 0.070904674, 0.262669636, 0.123134517)

#vc1-dst1 . vc5-dst1 . vc1-dst5 . vc10-dst1 . vc1-dst10 . vc5-dst5 . vc5-dst10 . vc10-dst10

#100 seg: vc1-dst1 . vc5-dst1 . vc1-dst5 . vc5-dst5
#10 seg: vc1-dst1 . vc5-dst1 . vc1-dst5 . vc5-dst5
#1 seg: vc1-dst1 . vc5-dst1 . vc1-dst5 . vc5-dst5

##################################
#ECG

"""cien_means, cien_std = (0.230291446, 0.144851883, 0.762915174, 2.314443469), (0.171028159, 0.010563822, 0.045962008, 0.567992473)
diez_means, diez_std = (0.155614956, 0.197297904, 0.772110624, 2.531072231), (0.03096019, 0.071763149, 0.049616018, 0.662386991)
uno_means, uno_std = (0.183372209, 0.173916689, 0.852517469, 2.17397783), (0.096294131, 0.070904674, 0.262669636, 0.123134517)"""

##################################

##################################
#MemApp

"""cien_means, cien_std = (0.143027385, 0.935568333, 1.24334542, 4.122532988), (0.010816799, 0.229174175, 0.9274929, 0.412518365)
diez_means, diez_std = (0.170036292, 1.196656794, 1.477276393, 4.503934077), (0.028655508, 1.087765314, 0.841005064, 0.487230687)
uno_means, uno_std = (0.257074167, 1.171701193, 1.226343305,5.415435791), (0.194768924, 0.48565946, 0.623777443,0.693827058)"""

##################################
#FsApp

"""cien_means, cien_std = (0.170066516, 0.775165017, 0.952091694, 4.35834074), (0.040565232, 0.548718067, 0.168181943, 0.649327767)
diez_means, diez_std = (0.166865683, 0.928705525, 0.920640254, 4.152433127), (0.030370593, 0.34801043, 0.229765211, 0.678806921)
uno_means, uno_std = (0.198870978, 0.799012507, 0.910565406,3.830225486), (0.042426417, 0.062537548, 0.284423455, 0.155986101)"""

##################################

#NetApp

cien_means, cien_std = (0.210776011, 0.759634336, 0.787637313, 4.080220699), (0.068946864, 0.02064752, 0.03223707, 0.154622193)
diez_means, diez_std = (0.170659471, 0.770427966, 0.811584735, 4.092077255), (0.048247236, 0.03327214, 0.073892714, 0.321211189)
uno_means, uno_std = (0.161504975, 0.799621428, 0.777250528, 5.190755582), (0.023861418, 0.156878218, 0.047850146, 1.698380096)

##################################

#CpuApp

cien_means, cien_std = (0.158907731, 0.792095741, 0.772070249, 3.811247428), (0.003688347, 0.032098105, 0.092117608, 0.199235184)
diez_means, diez_std = (0.17053411, 0.847257018, 0.918765712, 4.312494653), (0.043155424, 0.332101676, 0.186913408, 1.131958832)
uno_means, uno_std = (0.178309623, 0.820418278, 0.758198159, 5.812238503), (0.04951761, 0.203545975, 0.057503489, 4.319107023)

##################################


ind = np.arange(len(cien_means))  # the x locations for the groups
width = 0.20  # the width of the bars
ind2 = np.arange(len(diez_means))
width2 = 0.60

fig, ax = plt.subplots()
rects1 = ax.bar(ind - width/2, cien_means, width, yerr=cien_std,
                label='100 seg')
rects2 = ax.bar(ind + width/2, diez_means, width, yerr=diez_std,
                label='10 seg')
rects3 = ax.bar(ind2 + width2/2, uno_means, width, yerr=uno_std,
                label='1 seg')

# Add some text for labels, title and custom x-axis tick labels, etc.
#ax.set_xlabel("Number of virtual containers per DST")
#ax.set_ylabel('Time in seconds')
ax.set_xlabel("Número de contenedores virtuales por DST")
ax.set_ylabel('Tiempo en segundos')
ax.set_xticks(ind)
ax.set_xticklabels(('vc1-dst1', 'vc5-dst1', 'vc1-dst5', 'vc5-dst5'))
ax.legend()

"""
def autolabel(rects, xpos='center'):
    ha = {'center': 'center', 'right': 'left', 'left': 'right'}
    offset = {'center': 0, 'right': 1, 'left': -1}

    for rect in rects:
        height = rect.get_height()
        ax.annotate('{}'.format(height),
                    xy=(rect.get_x() + rect.get_width() / 2, height),
                    xytext=(offset[xpos]*3, 3),  # use 3 points offset
                    textcoords="offset points",  # in both directions
                    ha=ha[xpos], va='bottom')


autolabel(rects1, "left")
autolabel(rects2, "right")
"""
fig.tight_layout()

plt.savefig('consume-cpuapp.pdf',bbox_inches='tight')