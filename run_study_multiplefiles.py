from Study import Study
from matplotlib import pyplot as plt

is_plotHB_raw = 1
is_plot2lvl = 0
is_plotHB_filt= 0

# Initialize data
subject = 'Y'
# filename = ['./160804/Y_20160804_1152.TXT',
# 			'./160804/Y_20160804_1147.TXT']
filename = './data/Khoai_20160808_1165.TXT'
#filename = 'cQuyen.TXT'
study1 = Study(subject, filename)
marker = study1.dataset.event


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

plt.show()
