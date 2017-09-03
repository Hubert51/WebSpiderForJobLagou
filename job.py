class Job(object):
	# Init the job record
	# _jogTitle: string, _jobDescription: string, _salary: string
	# _companyName: string, _dataSource: string
	def __init__(self,_jobTitle,_jobDescription,_salary,_companyName,_dataSource):
		self.jobTitle = _jobTitle
		self.jobDescription = _jobDescription
		self.salary = _salary
		self.companyName = _companyName
		self.dataSource = _dataSource


	# Convert to json object
	# jobObject: dictionary 
	def toJson(self):
		jobObject = dict()
		jobObject["jobTitle"] = self.jobTitle
		jobObject["jobDescription"] = self.jobDescription
		jobObject["salary"] = self.salary
		jobObject["companyName"] = self.companyName
		jobObject["dataSource"] = self.dataSource
		return(jobObject)

	# for debug
	def getDescription(self):
		print(self.jobDescription)