from scrapy.spiders import CrawlSpider, Rule, BaseSpider, Spider
from scrapy.selector import Selector
from scrapy.http import HtmlResponse, FormRequest, Request

from courses.items import PrattCourse

class PrattSpider(Spider):
	# Static Variables
	name = 'pratt'
	allowed_domains = ['pratt.edu']
	start_url = 'https://www.pratt.edu/eescripts/courselookup.php' 
 	start_urls  = [start_url]

 	# Process the School Form
	def parse(self, response):
 		# Get the options of the school choice form
 		school_form_options = response.xpath('//select[@name="schoolchoice"]/option').extract()
 		form_data = {}
 		form_data['schoolchoice'] = []
 		for option in school_form_options:
 			if 'value="0"' not in str(option): # We do not want the first option
 				form_data['schoolchoice'] = [(str(option).split('\"')[1])]
		 		yield FormRequest.from_response(
		            response=response,
		            formid='Schools',
		            formdata=form_data,
		            callback=self.parse_dept_form,
		        )

 	# Process the Department Form
	def parse_dept_form(self, response): 
 		# Get the options of the department choice form
 		department_form_options = response.xpath('//select[@name="departmentchoice"]/option').extract()
 		form_data = {}
 		form_data['departmentchoice'] = []
 		for option in department_form_options:
 			if 'value="0"' not in str(option): # We do not want the first option
 				form_data['departmentchoice'] = [(str(option).split('\"')[1])]
				yield FormRequest.from_response(
			        response=response,
			        formid='Departments',
			        formdata=form_data,
			        callback=self.parse_course_form,
		    	)

    # Process the Course Form
	def parse_course_form(self, response):
		course_form_options = response.xpath('//select[@name="coursechoice"]/option').extract()
		form_data = {}
		form_data['coursechoice'] = []
		for option in course_form_options:
			if 'value="0"' not in str(option): # We do not want the first option
 				form_data['coursechoice'] = [(str(option).split('\"')[1])]
				yield FormRequest.from_response(
			        response=response,
			        formid='Courses',
			        formdata=form_data,
			        callback=self.yield_course,
				)

 	# Process the course
 	def yield_course(self, response):
 		course_div = response.xpath('//*[@id="showClass"]').extract()
 		course = PrattCourse()
 		course['site'] = 'www.pratt.edu'
 		course['institution'] = 'Pratt Institutions'
 		course['school'] = str(course_div).split('</h2>')[1].split('<br>')[0].replace('\\n', '').replace('\\t', '').replace('&amp','&')
 		course['course_name'] = response.xpath('//h2/text()').extract()[0]
 		course['course_id'] = response.xpath('//h3/text()').extract()[0]
 		course['course_description'] = str(course_div).split('</h3>')[1].split('<br>')[0].replace('\\n', '').replace('\\t', '')
 		# Some courses do not have sections being offered. Only extract the first section if present, for now
 		try:
 			course['course_section'] = str(course_div).split('Section</span>')[1].split('<br>')[1]
 		except IndexError:
 			course['course_section'] = ""
 		try:
 			course['course_section_credit'] = str(course_div).split('Credits')[1].split('<br>')[1]
 		except IndexError:
 			course['course_section_credit'] = ""
 		try:
 			course['course_section_start'] = str(course_div).split('Start Date ')[1].split('<br>')[1].split('<nobr>')[1].split('</nobr>')[0]
 		except IndexError:
 			course['course_section_start'] = ""
 		try:
 			course['course_section_end'] = str(course_div).split('End Date ')[1].split('<br>')[1].split('</td>')[0]
 		except IndexError:
 			course['course_section_end'] = ""
 		yield course
