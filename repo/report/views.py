from django.shortcuts import render

from .database import connect_db
from .constant import FETCH, MAIL, RECOMMEND
from .forms import create_mail, create_mail_2

import datetime, smtplib, numpy

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.header import Header

# Route Views
def index(request):
	context = {}
	return render(request, 'report/index.html', context)


# Controll Views
def get_yesterday_and_today(days):
	yesterday_date = datetime.datetime.now().date() - datetime.timedelta(days=days)
	today_date = datetime.datetime.now().date()
	reset_time = datetime.time(0,0,0)
	yesterday_datetime = datetime.datetime.combine(yesterday_date, reset_time)
	today_datetime = datetime.datetime.combine(today_date, reset_time)
	return yesterday_datetime, today_datetime

def get_user_id_list():
	users = list(connect_db('diana')['users'].find())
	user_id_list = []
	for user in users:
		if not user['user_id'] in user_id_list:
			user_id_list.append(user['user_id'])
	return user_id_list

def fetch_facebook_data(user_id, content):
	content['facebook'] = []
	yesterday, today = get_yesterday_and_today(FETCH['from_days'])
	# 어제부터 노출 된 적이 있는 캠페인들
	campaigns_on_from_yesterday = connect_db('diana')['fbadcampaigns'].find(
		{
			"user_id":user_id,
			"stop_time":{"$gte":yesterday, "$lt":today}
		}
	)
	# 어제 노출된 적 있는 캠페인들의 인사이트 값 가져오기
	for campaign in campaigns_on_from_yesterday:
		insights_of_campaign = list(connect_db('diana')['fbinsights'].find(
			{
				"campaign_id":campaign['campaign_id'],
				# "date_stop":yesterday,
				"date_stop":{"$gte":yesterday, "$lt":today},
				"impressions":{"$gte":FETCH['min_imp_limit']}
			}
		))
		for insight in insights_of_campaign:
			insight['campaign_name'] = campaign['name']
			content['facebook'].append(insight)
	# print(content['facebook'])
	print("fetch_facebook_data done")
	return content

def fetch_naver_data(user_id, content):
	content['naver'] = {}
	yesterday, today = get_yesterday_and_today(FETCH['from_days'])
	# 어제부터 노출 된 적이 있는 캠페인들
	campaigns_on_from_yesterday = list(connect_db('diana')['nvcampaigns'].find(
		{
			"user_id":user_id,
			# "dateEnd":yesterday,
			"dateEnd":{"$gte":yesterday, "$lt":today},
			"impCnt":{"$gte":FETCH['min_imp_limit']}
		}
	))
	if campaigns_on_from_yesterday:
		content['naver']['campaigns'] = campaigns_on_from_yesterday

	# 어제부터 노출 된 적이 있는 광고그룹들
	adgroups_on_from_yesterday = list(connect_db('diana')['nvadgroups'].find(
		{
			"user_id":user_id,
			# "dateEnd":yesterday,
			"dateEnd":{"$gte":yesterday, "$lt":today},
			"impCnt":{"$gte":FETCH['min_imp_limit']}
		}
	))
	if adgroups_on_from_yesterday:
		content['naver']['adgroups'] = adgroups_on_from_yesterday

	# print(content['naver'])
	print("fetch_naver_data done")
	return content

def fetch_naver_data_by_networkid(network_id, content):
	content['naver'] = {}
	yesterday, today = get_yesterday_and_today(FETCH['from_days'])
	# 어제부터 노출 된 적이 있는 캠페인들
	campaigns_on_from_yesterday = list(connect_db('diana')['nvcampaigns'].find(
		{
			"network_id":network_id,
			# "dateEnd":yesterday,
			"dateEnd":{"$gte":yesterday, "$lt":today},
			"impCnt":{"$gte":FETCH['min_imp_limit']}
		}
	))
	if campaigns_on_from_yesterday:
		content['naver']['campaigns'] = campaigns_on_from_yesterday

	# 어제부터 노출 된 적이 있는 광고그룹들
	adgroups_on_from_yesterday = list(connect_db('diana')['nvadgroups'].find(
		{
			"network_id":network_id,
			# "dateEnd":yesterday,
			"dateEnd":{"$gte":yesterday, "$lt":today},
			"impCnt":{"$gte":FETCH['min_imp_limit']}
		}
	))
	if adgroups_on_from_yesterday:
		content['naver']['adgroups'] = adgroups_on_from_yesterday

	# print(content['naver'])
	print("fetch_naver_data done")
	return content

def fetch_adwords_data(user_id, content):
	content['adwords'] = []
	yesterday, today = get_yesterday_and_today(FETCH['from_days'])
	# 어제부터 노출 된 적이 있는 캠페인들
	campaigns_on_from_yesterday = list(connect_db('diana')['gacampaigns'].find(
		{
			"user_id":user_id,
			# "dateEnd":yesterday,
			"dateEnd":{"$gte":yesterday, "$lt":today},
			"impressions":{"$gte":FETCH['min_imp_limit']}
		}
	))
	content['adwords'] = campaigns_on_from_yesterday
	# print(content['adwords'])
	print("fetch_adwords_data done")
	return content

def send_mail(user_id, user_email, content):
	# 모든 채널에 대한 데이터가 없으면, 메일을 보내지 않는다.
	if not any([content['facebook'], content['naver'], content['adwords']]):
		return print("No data of each channel")
	smtp = smtplib.SMTP_SSL('smtp.gmail.com', 465)
	smtp.login(MAIL['login_id'], MAIL['login_pw'])

	msg = MIMEMultipart('alternative')
	msg['Subject'] = 'Diana Naver Report on {}'.format((datetime.datetime.now() - datetime.timedelta(days=FETCH['from_days'])).strftime('%Y-%m-%d'))
	msg['From'] = MAIL['from']
	recipients = user_email
	msg['To'] = ','.join(recipients)
	html = create_mail_2(user_id, content)
	if not html:
		return print("send_mail failed")
	msg.attach(MIMEText(html, 'html'))
	smtp.sendmail(msg['From'], recipients, msg.as_string())
	smtp.quit()
	return print("send_mail done")

def process():
	user_id_list = get_user_id_list()
	# print(user_id_list)
	for user_id in user_id_list:
		content = {'user_id':user_id}
		# fetch_facebook_data(user_id, content)
		fetch_naver_data(user_id, content)
		# fetch_adwords_data(user_id, content)
		###### should get from DB ######
		user_email = ['tony.hwang@wizpace.com', 'support@wizpace.com']
		# user_email = ['tony.hwang@wizpace.com']
		send_mail(user_id, user_email, content)
		# print(user_id, content)
	return print("process done - {}".format(datetime.datetime.now()))

def autobid_noti():
	db = connect_db('autobidding')
	users = list(db['users'].find())
	for user in users:
		network_id = str(user['customer_id'])
		content = {
			'network_id':network_id,
			'user_id':user['user_id'],
			'facebook':[],
			'adwords': [],
		}
		fetch_naver_data_by_networkid(network_id, content)
		# should get from DB
		user_email = ['tony.hwang@wizpace.com', 'support@wizpace.com']
		# user_email = ['tony.hwang@wizpace.com']
		if user_email:
			if 'campaigns' in content['naver']:
				content['naver']['campaigns'] = sorted(content['naver']['campaigns'], key=lambda campaign: campaign['campaign_name'])
			if 'adgroups' in content['naver']:
				content['naver']['adgroups'] = sorted(content['naver']['adgroups'], key=lambda adgroup: adgroup['adgroup_name'])
			# print(content)
			content = recommend(content)
			# print(content)
			send_mail(network_id, user_email, content)
	return print("autobid_noti done - {}".format(datetime.datetime.now()))

def recommend(content):
	content['naver']['issues'] = []
	db = connect_db('diana')
	nvinsights = db['nvinsights']
	nvinsightsp = db['nvinsightsp']
	# 현재까지 1000원 이상 사용한 키워드 리스트
	keyword_list = list(nvinsightsp.find(
		{
			'network_id':content['network_id'],
			'salesAmt':{'$gte':RECOMMEND['salesAmt'][content['user_id']]},
		},
	))
	# print('키워드 리스트: ', keyword_list)
	for keyword in keyword_list:
		# 7일전부터 어제까지의 데이터
		data_7days = list(nvinsights.find(
			{
				'keyword_id':keyword['keyword_id'],
				'dateEnd':{'$gte':(datetime.datetime.now() - datetime.timedelta(days=7))}
			}
		))
		# print(data_7days)
		# 지난 7일간 1000원 이상 사용했지만, 전환이 전혀 없는 키워드 검출
		if sum([data['ccnt'] for data in data_7days]) == 0 and sum([data['salesAmt'] for data in data_7days]) >= RECOMMEND['no_ccnt_salesAmt'][content['user_id']]:
			content['naver']['issues'].append(
				{
					'keyword_id':keyword['keyword_id'],
					'keyword_name':keyword['keyword_name'],
					'issue':'7일간 소진 비용({}원) 대비 전환이 전혀 없습니다.'.format(sum([data['salesAmt'] for data in data_7days]), ','),
				}
			)
		# 지난 7일간 CPC 대비 CTR이 가장 좋은 순위를 추천
		ctr_by_cpc = [data['ctr']/(data['cpc'] + 0.0001) for data in data_7days if data['cpc']]
		if ctr_by_cpc:
			max_index = ctr_by_cpc.index(max(ctr_by_cpc))
			best_rank = data_7days[max_index]['avgRnk']
			if best_rank:
				content['naver']['issues'].append(
					{
						'keyword_id':keyword['keyword_id'],
						'keyword_name':keyword['keyword_name'],
						'issue':'7일간 최적 효율 순위는 {}위 입니다'.format(best_rank),
					}
				)
		# 지난 7일간 평균 CPC 대비 어제 CPC가 급상승(2배이상)한 키워드 검출
		if data_7days:
			avg_cpc_for_7days = numpy.mean([data['cpc'] for data in data_7days])
			if data_7days[-1]['cpc'] >= avg_cpc_for_7days * RECOMMEND['avg_cpc_times'][content['user_id']] and avg_cpc_for_7days * data_7days[-1]['cpc']:
				content['naver']['issues'].append(
					{
						'keyword_id':keyword['keyword_id'],
						'keyword_name':keyword['keyword_name'],
						'issue':'7일간 평균({}원)에 비해 CPC({}원)가 급상승 했습니다'.format(round(avg_cpc_for_7days, 2), data_7days[-1]['cpc']),
					}
				)
	
	return content


