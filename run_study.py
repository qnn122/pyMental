from Study import Study
from matplotlib import pyplot as plt

is_plotHB_raw = 1
is_plot2lvl = 0
is_plotHB_filt= 0

# Initialize data
subject = 'Y'
# filename = './160804/Y_20160804_1152.TXT'
filename = './data/Thien_20160808_1170.TXT'

#filename = 'cQuyen.TXT'
study1 = Study(subject, filename)
marker = study1.dataset.event


# Just plot something
if is_plotHB_raw:
	df = study1.dataset.df
	plt.figure(1)
	plt.subplot(211), study1.plot_Hb(df.T, 'oxyHb', marker=marker)
	plt.subplot(212), study1.plot_Hb(df.T, 'deoHb', marker=marker)

# Plot 2 levels of mental workload
if is_plot2lvl:
	lvl1_trials = ['Trial 1', 'Trial 4'] # exe
	lvl2_trials = ['Trial 2', 'Trial 3'] # ima
	plt.figure()
	plt.subplot(321), study1.plot_mean_2lvl('Channel 1', 'oxyHb', lvl1_trials, lvl2_trials)
	plt.subplot(322), study1.plot_mean_2lvl('Channel 2', 'oxyHb', lvl1_trials, lvl2_trials)
	plt.subplot(323), study1.plot_mean_2lvl('Channel 3', 'oxyHb', lvl1_trials, lvl2_trials)
	plt.subplot(324), study1.plot_mean_2lvl('Channel 4', 'oxyHb', lvl1_trials, lvl2_trials)
	plt.subplot(325), study1.plot_mean_2lvl('Channel 5', 'oxyHb', lvl1_trials, lvl2_trials)
	plt.subplot(326), study1.plot_mean_2lvl('Channel 6', 'oxyHb', lvl1_trials, lvl2_trials)

# Plot filtered signal
if is_plotHB_filt:
	study1.gen_filt()
	sig_filt = study1.dfbp_mva_sm 
	plt.figure(2)
	plt.subplot(211), study1.plot_Hb(sig_filt, 'oxyHb', marker=marker)
	plt.subplot(212), study1.plot_Hb(sig_filt, 'deoHb', marker=marker)

plt.show()

'''
plt.figure('Oxygenated Hb of all channels')
Study.plot_Hb(study1.dataset.df.T, 'oxyHb')
plt.show()
'''
