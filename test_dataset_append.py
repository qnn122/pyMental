from Study import Study
filename1 = './160804/Y_20160804_1147.TXT'
filename2 = './160804/Y_20160804_1152.TXT'

# Start loading all at a time
studyall = Study('Y', [filename1, filename2])

def print_info(study, mess):
	print mess
	print 'df: ', 		study.dataset.df.shape

	print 'numtrial: ',	study.dataset.numtrial

	print 'task_id: ', 	study.dataset.task_id.shape

	print 'event: ',	study.dataset.event.shape

	print '-------------------------------'

print_info(studyall, 'All dataset at atime')

# load data one by one
studyeach = Study('Y', filename1)
print_info(studyeach, 'First file')

studyeach.dataset.append_data(filename2)
print_info(studyeach, 'After file2 added')
