from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

from .database import connect_db
from .constant import FETCH, MAIL, RECOMMEND
from .forms import create_mail

import datetime
import smtplib
import numpy
import json

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.header import Header

# Route Views


@csrf_exempt
def recommend(request):
    if request.method == "POST":
        req = json.loads(request.body.decode('utf-8'))
        db = connect_db('diana')
        nvaccounts = db['nvaccounts']
        keyword = {
            'keyword_id': req['keyword_id'],
            'name': req['name'],
        }
        content = {
            'naver': {
                'recos': [],
            },
            'username': req['username'],
        }
        nvstats = db['nvstats']
        recommend_keyword(content, nvstats, keyword)
        return HttpResponse(json.dumps(content['naver']).encode('utf-8'))
    return HttpResponse(json.dumps("error").encode('utf-8'))


def index(request):
    context = {}
    return render(request, 'report/index.html', context)


# Controll Views
def get_yesterday_and_today(days):
    yesterday_date = datetime.datetime.now().date() - datetime.timedelta(days=days)
    today_date = datetime.datetime.now().date()
    reset_time = datetime.time(0, 0, 0)
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
            "user_id": user_id,
            "stop_time": {"$gte": yesterday, "$lt": today}
        }
    )
    # 어제 노출된 적 있는 캠페인들의 인사이트 값 가져오기
    for campaign in campaigns_on_from_yesterday:
        insights_of_campaign = list(connect_db('diana')['fbinsights'].find(
            {
                "campaign_id": campaign['campaign_id'],
                # "date_stop":yesterday,
                "date_stop": {"$gte": yesterday, "$lt": today},
                "impressions": {"$gte": FETCH['min_imp_limit']}
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
    # 오늘 status가 ELIGIBLE(ON)인 캠페인들
    campaigns_on_today = list(connect_db('diana')['nvcampaigns'].find(
        {
            "user_id": user_id,
            "status": "ELIGIBLE",
        }
    ))
    if campaigns_on_today:
        content['naver']['campaigns'] = campaigns_on_today

    # 오늘 status가 ELIGIBLE(ON), 어제 stat이 있는 광고그룹들
    adgroups_on_today = list(connect_db('diana')['nvadgroups'].find(
        {
            "user_id": user_id,
            "status": "ELIGIBLE",
            "yesterday": {'$ne': {}}
        }
    ))
    if adgroups_on_today:
        content['naver']['adgroups'] = adgroups_on_today

    # print(content['naver'])
    print("fetch_naver_data done")
    return content


def fetch_naver_data_by_customer_id(customer_id, content):
    content['naver'] = {}
    # 오늘 status가 ELIGIBLE(ON)인 캠페인들
    campaigns_on_today = list(connect_db('diana')['nvcampaigns'].find(
        {
            "customer_id": customer_id,
            "status": "ELIGIBLE",
        }
    ))
    if campaigns_on_today:
        content['naver']['campaigns'] = campaigns_on_today

    # 오늘 status가 ELIGIBLE(ON), 어제 stat이 있는 광고그룹들
    adgroups_on_today = list(connect_db('diana')['nvadgroups'].find(
        {
            "customer_id": customer_id,
            "status": "ELIGIBLE",
            "status_reason": "ELIGIBLE",
            "yesterday": {'$ne': {}}
        }
    ))
    if adgroups_on_today:
        content['naver']['adgroups'] = adgroups_on_today

    # print(content['naver'])
    print("fetch_naver_data done")
    return content


def fetch_adwords_data(user_id, content):
    content['adwords'] = []
    yesterday, today = get_yesterday_and_today(FETCH['from_days'])
    # 어제부터 노출 된 적이 있는 캠페인들
    campaigns_on_from_yesterday = list(connect_db('diana')['gacampaigns'].find(
        {
            "user_id": user_id,
            # "dateEnd":yesterday,
            "dateEnd": {"$gte": yesterday, "$lt": today},
            "impressions": {"$gte": FETCH['min_imp_limit']}
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
    msg['Subject'] = 'Diana Naver Report on {}'.format((datetime.datetime.now(
    ) - datetime.timedelta(days=FETCH['from_days'])).strftime('%Y-%m-%d'))
    msg['From'] = MAIL['from']
    recipients = user_email
    msg['To'] = ','.join(recipients)
    html = create_mail(user_id, content)
    if not html:
        print(user_id)
        print(user_email)
        print(content)
        return print("send_mail failed")
    msg.attach(MIMEText(html, 'html'))
    smtp.sendmail(msg['From'], recipients, msg.as_string())
    smtp.quit()
    return print("send_mail done")


def process():
    user_id_list = get_user_id_list()
    for user_id in user_id_list:
        content = {'user_id': user_id}
        # fetch_facebook_data(user_id, content)
        fetch_naver_data(user_id, content)
        # fetch_adwords_data(user_id, content)
        user_email = ['tony.hwang@wizpace.com', 'support@wizpace.com']
        # send_mail(user_id, user_email, content)
    return print("process done - {}".format(datetime.datetime.now()))


def autobid_noti():
    db = connect_db('autobidding')
    users = list(db['users'].find())
    for user in users:
        customer_id = str(user['customer_id'])
        content = {
            'customer_id': customer_id,
            'username': user['user_id'],
            'facebook': [],
            'adwords': [],
        }
        fetch_naver_data_by_customer_id(customer_id, content)
        # should get from DB
        # user_email = ['tony.hwang@wizpace.com']
        user_email = ['tony.hwang@wizpace.com', 'support@wizpace.com']
        if user_email:
            if 'campaigns' in content['naver']:
                content['naver']['campaigns'] = sorted(
                    content['naver']['campaigns'], key=lambda campaign: campaign['name'])
            if 'adgroups' in content['naver']:
                content['naver']['adgroups'] = sorted(
                    content['naver']['adgroups'], key=lambda adgroup: adgroup['name'])
            # print(content)
            content = recommend_entity(content)
            # print(content)
            send_mail(customer_id, user_email, content)
    return print("autobid_noti done - {}".format(datetime.datetime.now()))


def recommend_entity(content):
    content['naver']['recos'] = []
    db = connect_db('diana')
    nvkeywords = db['nvkeywords']
    nvstats = db['nvstats']
    # 현재까지 1000원 이상 사용한 키워드 리스트
    keyword_list = list(nvkeywords.find(
        {
            'customer_id': content['customer_id'],
            'last_month.spend': {'$gte': RECOMMEND['spend'][content['username']]},
        },
    ))
    print('키워드 리스트: ', keyword_list)
    for keyword in keyword_list:
        recommend_keyword(content, nvstats, keyword)
    return content


def recommend_keyword(content, nvstats, keyword):
    # 7일전부터 어제까지의 데이터
    data_7days = list(nvstats.find(
        {
            'res_id': keyword['keyword_id'],
            'type': 'keyword',
                    'date_end': {'$gte': (datetime.datetime.now() - datetime.timedelta(days=7))}
        }
    ))
    # print(data_7days)

    # 지난 7일간 1000원 이상 사용했지만, 전환이 전혀 없는 키워드 검출
    sum_ccnts = sum([data['ccnt']
                     for data in data_7days if 'ccnt' in data])
    sum_spends = sum([data['spend']
                      for data in data_7days if 'spend' in data])
    if sum_ccnts == 0 and sum_spends >= RECOMMEND['no_ccnt_spend'][content['username']]:
        content['naver']['recos'].append(
            {
                'keyword_id': keyword['keyword_id'],
                'name': keyword['name'],
                'reco': '7일간 소진 비용({}원) 대비 전환이 전혀 없습니다.'.format(sum_spends, ','),
            }
        )

    # 지난 7일간 CPC 대비 CTR이 가장 좋은 순위를 추천
    ctr_by_cpc = []
    for data in data_7days:
        if 'ctr' in data and 'cpc' in data:
            if data['ctr'] * data['cpc']:
                ctr_by_cpc.append(data['ctr']/data['cpc'])

    if ctr_by_cpc:
        max_index = ctr_by_cpc.index(max(ctr_by_cpc))
        best_rank = data_7days[max_index]['average_rank']
        if best_rank:
            content['naver']['recos'].append(
                {
                    'keyword_id': keyword['keyword_id'],
                    'name': keyword['name'],
                    'reco': '7일간 최적 효율 순위는 {}위 입니다'.format(best_rank),
                }
            )

    # 지난 7일간 평균 CPC 대비 어제 CPC가 급상승(2배 이상)한 키워드 검출 (CPC가 0인 데이터는 제외)
    if data_7days:

        cpc_for_7days = []
        for data in data_7days:
            if 'cpc' in data:
                if data['cpc']:
                    cpc_for_7days.append(data['cpc'])
        avg_cpc_for_7days = numpy.mean(cpc_for_7days)

        if all([avg_cpc_for_7days, 'cpc' in data_7days[-1]]):
            if data_7days[-1]['cpc'] > avg_cpc_for_7days * RECOMMEND['avg_cpc_times'][content['username']]:
                content['naver']['recos'].append(
                    {
                        'keyword_id': keyword['keyword_id'],
                        'name': keyword['name'],
                        'reco': '7일간 평균({}원)에 비해 CPC({}원)가 급상승 했습니다'.format(round(avg_cpc_for_7days, 2), data_7days[-1]['cpc']),
                    }
                )

    # 지난 7일간 평균 CPM 대비 어제 CPM이 급상승(2배 이상)한 키워드 검출 (CPM이 0인 데이터는 제외)
    if data_7days:
        cpm_for_7days = []
        for data in data_7days:
            if 'impressions' in data and 'spend' in data:
                if data['impressions'] * data['spend']:
                    cpm_for_7days.append(data['spend']/data['impressions'])
        avg_cpm_for_7days = numpy.mean(cpm_for_7days)

        if all([avg_cpm_for_7days, 'spend' in data_7days[-1], 'impressions' in data_7days[-1]]):
            if data_7days[-1]['spend']/data_7days[-1]['impressions'] > avg_cpm_for_7days * RECOMMEND['avg_cpm_times'][content['username']]:
                content['naver']['recos'].append(
                    {
                        'keyword_id': keyword['keyword_id'],
                        'name': keyword['name'],
                        'reco': '7일간 평균({}원)에 비해 노출 경쟁(CPM, {}원)이 급상승 했습니다'.format(round(avg_cpm_for_7days, 2), round(data_7days[-1]['spend']/data_7days[-1]['impressions'], 2)),
                    }
                )

    # 지난 7일간 평균 Impressions 대비 어제 Impressions 급상승(2배 이상)한 키워드 검출 (Impressions이 0인 데이터는 제외)
    if data_7days:
        imp_for_7days = []
        for data in data_7days:
            if 'impressions' in data:
                if data['impressions']:
                    imp_for_7days.append(data['impressions'])
        avg_imp_for_7days = numpy.mean(imp_for_7days)

        if all([avg_imp_for_7days, 'impressions' in data_7days[-1]]):
            if data_7days[-1]['impressions'] > avg_imp_for_7days * RECOMMEND['avg_imp_times'][content['username']]:
                content['naver']['recos'].append(
                    {
                        'keyword_id': keyword['keyword_id'],
                        'name': keyword['name'],
                        'reco': '7일간 평균({}회)에 비해 노출({}회)이 급상승 했습니다'.format(round(avg_imp_for_7days, 2), data_7days[-1]['impressions']),
                    }
                )
    return content


def save_recommend_keywords():
    db = connect_db('diana')
    nvkeywords = db['nvkeywords']
    nvaccounts = db['nvaccounts']
    keyword_list = nvkeywords.find({"status": "ELIGIBLE"})

    for keyword in keyword_list:
        print("키워드 - {}".format(keyword['name']))

        recos = []
        username = nvaccounts.find_one({"client_customer_id": keyword['customer_id']})[
            'client_login_id']
        last_week = keyword['last_week']
        yesterday = keyword['yesterday']

        # 지난 7일간 1000원 이상 사용했지만, 전환이 전혀 없는 키워드 검출
        if last_week['ccnt'] == 0 and last_week['spend'] >= RECOMMEND['no_ccnt_spend'][username]:
            reco = '7일간 소진 비용({}원) 대비 전환이 전혀 없습니다.'.format(
                last_week['spend'], ',')
            recos.append(reco)

        # 지난 7일간 평균 CPC 대비 어제 CPC가 급상승(2배 이상)한 키워드 검출 (CPC가 0인 데이터는 제외)
        if yesterday['cpc'] > last_week['cpc'] * RECOMMEND['avg_cpc_times'][username]:
            reco = '7일간 평균({}원) 대비 1일 전 CPC({}원)가 급상승했습니다.'.format(
                round(last_week['cpc'], 2), round(yesterday['cpc'], 2))
            recos.append(reco)

        # 지난 7일간 평균 CPM 대비 어제 CPM이 급상승(2배 이상)한 키워드 검출 (CPM이 0인 데이터는 제외)
        if yesterday['cpm'] > last_week['cpm'] * RECOMMEND['avg_cpc_times'][username]:
            reco = '7일간 평균({}원) 대비 1일 전 CPM({}원)이 급상승했습니다.'.format(
                round(last_week['cpm'], 2), round(yesterday['cpm'], 2))
            recos.append(reco)

        # 지난 7일간 평균 Impressions 대비 어제 Impressions 급상승(2배 이상)한 키워드 검출 (Impressions이 0인 데이터는 제외)
        if yesterday['impressions'] > last_week['impressions'] * RECOMMEND['avg_cpc_times'][username]:
            reco = '7일간 평균({}회) 대비 1일 전 노출({}회)이 급상승했습니다.'.format(
                last_week['impressions'], yesterday['impressions'])
            recos.append(reco)

        nvkeywords.update_one(
            {"keyword_id": keyword['keyword_id']},
            {"$set": {"recommendation": recos}}
        )
        print(recos)

    return print("save_recommend_keywords done - {}".format(datetime.datetime.now()))
