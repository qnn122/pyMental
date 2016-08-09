import numpy as np
import pandas as pd

# Visualization
import matplotlib.pyplot as plt
import matplotlib
matplotlib.style.use('ggplot')

# Signal processing
from scipy import signal

class Dataset():
	"""docstring for Dataset"""
	def __init__(self, filename):
		self.filename = filename
		self.HbTypes = ['oxyHb', 'deoHb', 'totHb']

		# Read number of channel and create columns label
		try: 	# TODO: handle error here, including filename not found
			#data_import = pd.read_csv(filename, skiprows=34, sep='\t') # only valid for FOIRE-3000
			numchan_import = pd.read_csv(filename, skiprows=32, nrows=1, sep='\t')
			self.numchan = int(numchan_import.values[0][0][-1])
			columnslbl = pd.MultiIndex.from_product([Dataset.mklbl('Channel ', self.numchan), self.HbTypes])

			# Read numtrial
			numtrial_row = pd.read_csv(filename, skiprows=11, nrows = 1, sep='\t', header=None,  index_col=0)
			self.numtrial =  int(numtrial_row.values[0][0])
			
		except:
			print 'Something wrong 1'

		# Import data and create dataframe
		try:
			self.data_import = pd.read_csv(filename, skiprows=35, sep='\t').as_matrix()
			self.df = pd.DataFrame(self.data_import[:, 4:], columns=columnslbl) # 3 first columns contains times series and marker -> remove
		except:
			print 'Something wrong 2'
		
		# Task's info
		self.task_id = self.data_import[:, 1] == 1
		self.len_task = np.sum(self.task_id)/self.numtrial


		# TODO: import Fs 
		ts = 0.055
		self.Fs = 1/ts
		self.time = pd.Series(self.data_import[:, 0]) 		# first columnn contains time series
		self.event = pd.Series(self.data_import[:, 1])		# second column = event vector
	
	def append_data(self, filename):
		# Read newd data file
		newdataset = Dataset(filename)

		# Update dataset variables
		print self.df.tail()
		self.df = self.df.append(newdataset.df)
		print self.df.tail()
		self.numtrial = self.numtrial + newdataset.numtrial
		
		self.task_id = np.append(self.task_id, newdataset.task_id)
		self.event = self.event.append(newdataset.event)

	def set_Fs(self, Fs):
		self.Fs = Fs

	@staticmethod
	def mklbl(prefix, n):
			# Method to make labels automatically
		return ["%s%s" %(prefix, i+1) for i in range(n)]


class Study(): # TODO: Class con cua Dataset?
	"""docstring for Study"""
	def __init__(self, subject_name, filename):
		self.subject_name = subject_name

		if type(filename) == str:
			self.dataset = Dataset(filename)
		elif type(filename) == list:
			self.dataset = Dataset(filename[0])
			numfile = len(filename)
			for i in range(numfile)[1:numfile]:
				self.dataset.append_data(filename[i])

		'''Signal processing parameters'''
		# bandpass filter
		self.up_Fcut = 0.01
		self.low_Fcut = 0.5

		# moving averaging
		self.mov_win = 5

	''' =========== Filter ================'''
	@staticmethod
	def filtfilt_df(df, a, b):
		'''signal.filtfilt for data frame'''
		dfout = df.copy()
		for i, data in df.iterrows():
			dfout.loc[i] = signal.filtfilt(b, a, data)
		return dfout

	def bp_filt(self, df):
		'''bandpass filter'''
		cutfreq = np.array([self.up_Fcut, self.low_Fcut])
		b, a = signal.ellip(4, 0.1, 40, 
							cutfreq*2/self.dataset.Fs, btype='bandpass')
		output = self.filtfilt_df(df, a, b)
		return output

	def mva_filt(self, df):
		''' moving averaging filter '''
		a = np.array([1]);
		temp = self.dataset.Fs * self.mov_win
		b = np.zeros((int(np.ceil(temp)),))
		b[0:int(np.ceil(temp))]= 1.0/(temp)
		output = self.filtfilt_df(df, a, b)
		return output

	@classmethod
	def smooth_df(self, df, window_len=31):
		import sigpro as sp
		df = df
		dfout = df.copy()
		for i, data in df.iterrows():
			dfout.loc[i] = sp.smooth(data, window_len)
		return dfout

	@classmethod
	def nmlShiftAll(self, df):
		''' Normalizing and shifting in all trial '''
		nml = lambda x: (x - x.mean()) / x.std() #normalization
		shift = lambda x: x - x[0]
		dfout = df.copy()
		idx = pd.IndexSlice
		for i in df.columns.levels[0]:
			a = df.loc[idx[:,:], idx[i, :]]
			a = a.apply(nml, axis=1)
			dfout.loc[idx[:,:], idx[i, :]] = a.apply(shift, axis=1)
			#print i
		return dfout

	''' ========== Parameters ============= '''
	def set_bp_para(self, up_Fcut, low_Fcut):
		'''Set bandpass filter's parameters'''
		self.up_Fcut = up_Fcut
		self.low_Fcut = low_Fcut

	def set_mov_para(self, mov_win):
		'''Set moving averaging's parameters'''
		self.mov_win = mov_win

	# TODO: implement this one
	def get_number_labels(self):
		'''Return number of labels'''
		pass

	''' =========== Visualization ================'''
	@staticmethod
	def plot_Hb(df, hbtype, marker=pd.Series()):
		''' Plot the whole data frame according to given Hb type '''
		df_swap = df.swaplevel(0, 1, axis=0)
		df_Hbtype = df_swap.loc[hbtype]
		df_Hbtype.T.plot(y = [i for i, data in df_Hbtype.iterrows()],
						ax = plt.gca())

		if marker.any():
			#taskmasker = marker.index[marker.values==1]
			y = np.array(df_Hbtype.values)
			uplim = np.max(y)*1.2
			lowlim = np.min(y)*1.2
		plt.fill_between(np.array(marker.index), uplim, lowlim, 
								where=np.array(marker.values==1), 
								interpolate=True,
								color='blue', alpha=0.2)


	''' =========== Testing ================'''


	''' ========= Comprehensive investigation ====== '''
	def plot_mean_2mwl(self, Hbtype, lvl1trials, lvl2trials):
		''' plot mean of a Hb type, between 2 mental worload level '''
		pass

	@staticmethod
	def calc_mean(series_Hb, lvl_trials, len_task):
		data = series_Hb.values
		numtrial = len(lvl_trials)
		data = np.reshape(data, (numtrial, len_task))
		df = pd.DataFrame(data.T, index = [x for x in range(len_task)], columns = lvl_trials)
		return df

	def gen_filt(self):
		# General filtering
		self.dfbp = self.bp_filt(self.dataset.df.T)
		self.dfbp_mva = self.mva_filt(self.dfbp)
		self.dfbp_mva_sm = self.smooth_df(self.dfbp_mva, 511)

	# TODO: implement this one
	def plot_mean_2lvl_temp(self, chan, Hbtype, twolabels, legends=None):
		'''Plot folding everage of 2 mental workload levels
		Example:
			twolabel = ['E', 'I']
			legends = ['Motor Execution', 'Motor Imagery']
		'''
		pass

	def plot_mean_2lvl(self, chan, Hbtype, lvl1_trials, lvl2_trials):
		# General filtering
		self.gen_filt()

		# Split data into chunks
		data_filt = self.dfbp_mva_sm.as_matrix()

		task = data_filt.T[self.dataset.task_id, :]

		# Create trial-based data frame
		miTrial = pd.MultiIndex.from_product([Dataset.mklbl('Trial ', self.dataset.numtrial),
											[x for x in range(self.dataset.len_task)]])

		print 'Plot folding average between 2 mental workload. It may take a while...'

		miChHb = pd.MultiIndex.from_product([Dataset.mklbl('Channel ', self.dataset.numchan),
											['oxyHb', 'deoHb', 'totHb']])

		
		dfmi = pd.DataFrame(task, index = miTrial, columns = miChHb)
		
		# Sort Hb types in order to perfome slicing
		dfmi_Hbsorted = dfmi.T.sort_index().sort_index(axis=1) # EXTREMELY IMPORTANT

		# Normalizing and shifting
		dfmi_nmlShift = self.nmlShiftAll(dfmi_Hbsorted) # the function is quite slow
		
		# Slit into chunks accurding to mwl
		idx = pd.IndexSlice

		# paradigm: low-high-low-high-low
		lvl1 = dfmi_nmlShift.loc[idx[:, :], 
								idx[lvl1_trials, :]]
		lvl2 = dfmi_nmlShift.loc[idx[:, :], 
								idx[lvl2_trials, :]]

		# plot oxyHb, for example
		oxyHblvl1 = lvl1.loc[idx[chan, Hbtype], idx[:, :]]
		oxyHblvl1mean = self.calc_mean(oxyHblvl1, lvl1_trials, self.dataset.len_task)

		deno = np.sqrt(oxyHblvl1mean.shape[1])
		m1 = oxyHblvl1mean.apply(np.sum, axis=1)
		s1 = oxyHblvl1mean.apply(np.std, axis=1) / deno

		oxyHblvl2 = lvl2.loc[idx[chan, Hbtype], idx[:, :]]
		oxyHblvl2mean = self.calc_mean(oxyHblvl2, lvl2_trials, self.dataset.len_task)

		deno = np.sqrt(oxyHblvl2mean.shape[1])
		m2 = oxyHblvl2mean.apply(np.sum, axis=1)
		s2 = oxyHblvl2mean.apply(np.std, axis=1) / deno
		
		# Visualization 
		line_lvl2 = plt.plot(m2.index, m2, 'r', label='Level 2')
		plt.fill_between(s2.index, m2-2*s2, m2+2*s2, color='r', alpha=0.2)

		line_lvl1 = plt.plot(m1.index, m1, 'b', label='Level 1')
		plt.fill_between(s1.index, m1-2*s1, m1+2*s1, color='b', alpha=0.2)
		plt.title(chan + ', ' + Hbtype)
		plt.legend()

		