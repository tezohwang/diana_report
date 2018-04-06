from django.shortcuts import render

from .database import connect_db
from .constant import FETCH, MAIL
from .forms import create_mail, create_mail_2

import datetime, smtplib

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
    print(content['facebook'])
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

    print(content['naver'])
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

    print(content['naver'])
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
    print(content['adwords'])
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
    print(user_id_list)
    for user_id in user_id_list:
        content = {'user_id':user_id}
        fetch_facebook_data(user_id, content)
        fetch_naver_data(user_id, content)
        fetch_adwords_data(user_id, content)
        # should get from DB
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
            send_mail(network_id, user_email, content)
    return print("autobid_noti done - {}".format(datetime.datetime.now()))
