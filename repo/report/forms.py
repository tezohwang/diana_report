import datetime

# 입력 폼 선언

# 이메일 폼 선언
def create_mail(user_id, content):
    form = ''
    # 리포트와 날짜 정보
    form += '<h1>Diana Report - {}</h1>'.format(datetime.datetime.now().strftime('%Y-%m-%d'))
    # 페이스북 데이터가 있으면, 작성한다.
    if content['facebook']:
        # 페이스북 표시
        form += '<h3>페이스북</h3>'
        for insight in content['facebook']:
            # 계정 아이디
            form += '<p>Account ID: {}</p>'.format(insight['account_id'])
            # 캠페인 이름
            form += '<p>Campaign: {}</p>'.format(insight['campaign_name'])
            # 캠페인 아이디
            form += '<p>Campaign ID: {}</p>'.format(insight['campaign_id'])
            # 인사이트 데이터
            form += '<p>비용: {}</p>'.format(insight['spend'])
            form += '<p>노출: {}</p>'.format(insight['impressions'])
            form += '<p>도달: {}</p>'.format(insight['reach'])
            form += '<p>CPP: {}</p>'.format(insight['cpp'])
            form += '<p>빈도: {}</p>'.format(insight['frequency'])
            form += '<p>클릭: {}</p>'.format(insight['clicks'])
            form += '<p>CPC: {}</p>'.format(insight['cpc'])
            form += '<p>광고일자: {}</p>'.format(insight['date_start'])
            
    
    # 네이버 데이터가 있으면, 작성한다.
    if content['naver']:
        # 네이버 표시
        form += '<h3>네이버</h3>'
        for insight in content['naver']:
            # 계정 아이디
            form += '<p>Account ID: {}</p>'.format(insight['network_id'])
            # 캠페인 이름
            form += '<p>Campaign: {}</p>'.format(insight['campaign_name'])
            # 캠페인 아이디
            form += '<p>Campaign ID: {}</p>'.format(insight['campaign_id'])
            # 인사이트 데이터
            form += '<p>비용: {}</p>'.format(insight['salesAmt'])
            form += '<p>노출: {}</p>'.format(insight['impCnt'])
            form += '<p>클릭: {}</p>'.format(insight['clkCnt'])
            form += '<p>클릭률: {}</p>'.format(insight['ctr'])
            form += '<p>CPC: {}</p>'.format(insight['cpc'])
            # 전환은 있을 경우에만
            try:
                form += '<p>전환: {}</p>'.format(insight['ccnt'])
            except Exception as e:
                print(e)
                form += '<p>전환: {}</p>'.format(0)
            form += '<p>광고일자: {}</p>'.format(insight['dateStart'])

    # 애드워즈 데이터가 있으면, 작성한다.
    if content['adwords']:
        # 애드워즈 표시
        form += '<h3>구글 애드워즈</h3>'
        for insight in content['adwords']:
            # 계정 아이디
            form += '<p>Account ID: {}</p>'.format(insight['network_id'])
            # 캠페인 이름
            form += '<p>Campaign: {}</p>'.format(insight['campaign'])
            # 캠페인 아이디
            form += '<p>Campaign ID: {}</p>'.format(insight['campaign_id'])
            # 인사이트 데이터
            form += '<p>비용: {}</p>'.format(insight['cost'])
            form += '<p>노출: {}</p>'.format(insight['impressions'])
            form += '<p>클릭: {}</p>'.format(insight['clicks'])
            form += '<p>클릭률: {}</p>'.format(insight['ctr'])
            form += '<p>CPC: {}</p>'.format(insight['avg_cpc'])
            form += '<p>평균순위: {}</p>'.format(insight['avg_position'])
            form += '<p>광고일자: {}</p>'.format(insight['dateStart'])

    return form
    