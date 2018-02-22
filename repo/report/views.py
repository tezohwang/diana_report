from django.shortcuts import render

from .database import db
from .constant import FETCH, MAIL
from .forms import create_mail

import datetime, smtplib

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.header import Header


# Route Views
def index(request):
    context = {}
    return render(request, 'report/index.html', context)


# Controll Views
def get_user_id_list():
    users = list(db['users'].find())
    user_id_list = []
    for user in users:
        if not user['user_id'] in user_id_list:
            user_id_list.append(user['user_id'])
    return user_id_list

def fetch_facebook_data(user_id, content):
    content['facebook'] = []
    yesterday = datetime.datetime.now() - datetime.timedelta(days=FETCH['from_days'])
    # 어제부터 노출 된 적이 있는 캠페인들
    campaigns_on_from_yesterday = db['fbadcampaigns'].find(
        {
            "user_id":user_id,
            "stop_time":{"$gte":yesterday}
        }
    )
    # 어제 노출된 적 있는 캠페인들의 인사이트 값 가져오기
    for campaign in campaigns_on_from_yesterday:
        insights_of_campaign = list(db['fbinsights'].find(
            {
                "campaign_id":campaign['campaign_id'],
                # "date_stop":yesterday,
                "date_stop":{"$gte":yesterday},
                "impressions":{"$gt":FETCH['min_imp_limit']}
            }
        ))
        for insight in insights_of_campaign:
            insight['campaign_name'] = campaign['name']
            content['facebook'].append(insight)
    print(content['facebook'])
    print("fetch_facebook_data done")
    return content

def fetch_naver_data(user_id, content):
    yesterday = datetime.datetime.now() - datetime.timedelta(days=FETCH['from_days'])
    # 어제부터 노출 된 적이 있는 캠페인들
    campaigns_on_from_yesterday = list(db['nvcampaigns'].find(
        {
            "user_id":user_id,
            # "dateEnd":yesterday,
            "dateEnd":{"$gte":yesterday},
            "impCnt":{"$gt":FETCH['min_imp_limit']}
        }
    ))
    content['naver'] = campaigns_on_from_yesterday
    print(content['naver'])
    print("fetch_naver_data done")
    return content

def fetch_adwords_data(user_id, content):
    yesterday = datetime.datetime.now() - datetime.timedelta(days=FETCH['from_days'])
    # 어제부터 노출 된 적이 있는 캠페인들
    campaigns_on_from_yesterday = list(db['gacampaigns'].find(
        {
            "user_id":user_id,
            # "dateEnd":yesterday,
            "dateEnd":{"$gte":yesterday},
            "impressions":{"$gt":FETCH['min_imp_limit']}
        }
    ))
    content['adwords'] = campaigns_on_from_yesterday
    print(content['adwords'])
    print("fetch_adwords_data done")
    return content

def send_mail(user_id, content):
    # 모든 채널에 대한 데이터가 없으면, 메일을 보내지 않는다.
    if not any([content['facebook'], content['naver'], content['adwords']]):
        return print("No data of each channel")
    smtp = smtplib.SMTP_SSL('smtp.gmail.com', 465)
    smtp.login(MAIL['login_id'], MAIL['login_pw'])

    msg = MIMEMultipart('alternative')
    msg['Subject'] = 'Diana Report on {}'.format(datetime.datetime.now() - datetime.timedelta(days=FETCH['from_days']))
    msg['From'] = MAIL['from']
    recipients = MAIL['recipients']
    msg['To'] = ','.join(recipients)
    html = create_mail(user_id, content)
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
        send_mail(user_id, content)
        # print(user_id, content)
    return print("process done")
