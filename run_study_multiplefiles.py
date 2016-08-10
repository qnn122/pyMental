from Study import Study
from matplotlib import pyplot as plt
import numpy as np

is_plotHB_raw = 0
is_plot2lvl = 1
is_plotHB_filt= 0
is_savefile = 0


# Initialize data
subject = 'Thien_'
date = '20160808_'
filename = ['./data/' + subject + date + '1170.TXT',
			'./data/' + subject + date + '1171.TXT']
labelfile = './data/' + subject + date + 'protocol.TXT'

study1 = Study(subject, filename)
marker = study1.dataset.event

# read label
study1.dataset.read_label(labelfile)


lvl1_trials = study1.get_trial_fromlabel(labelclass='E')
lvl2_trials = study1.get_trial_fromlabel(labelclass='I')
lvllegend = ['Motor Execution', 'Motor Imagery']
print 'Motor Execution: ', lvl1_trials
print 'Motor Imagery: ', lvl2_trials


# Just plot something
if is_plotHB_raw:
	df = study1.dataset.df
	print marker.index
	plt.figure(1)
	plt.subplot(211), study1.plot_Hb(df.T, 'oxyHb', marker=marker)
	plt.subplot(212), study1.plot_Hb(df.T, 'deoHb', marker=marker)


# Plot filtered signal
if is_plotHB_filt:
	study1.gen_filt()
	sig_filt = study1.dfbp_mva_sm 
	plt.figure(2)
	plt.subplot(211), study1.plot_Hb(sig_filt, 'oxyHb', marker=marker)
	plt.subplot(212), study1.plot_Hb(sig_filt, 'deoHb', marker=marker)


# Plot 2 levels of mental workload
Hbtype = 'oxyHb'
if is_plot2lvl:
	fig = plt.figure()
	fig.suptitle(subject + ' - ' + Hbtype, fontsize=14, fontweight='bold')
	for i in range(1, study1.dataset.numchan + 1):
		print '+++ Processing channel ', str(i)
		plt.subplot(3, 5, i*2), study1.plot_mean_2lvl('Channel ' + str(i), 
				Hbtype, lvl1_trials, lvl2_trials, lvllegend)

plt.show()


# Save file
if is_savefile:
	study1.split2trials() 	# make sure dfmi_Hbsorted has been created
	for i in ('oxyHb', 'deoHb'):
		filename = subject + date + i + '.TXT'
		study1.write_matrix(filename, i)

	# 
	np.savetxt(subject + date + 'label.TXT', study1.dataset.label, fmt='%s')
