import datetime

# 입력 폼 선언

# 이메일 폼 선언
def create_mail(user_id, content):
    form = ''
    # 리포트와 날짜 정보
    form += '<h1>Diana Report - {}</h1>'.format((datetime.datetime.now() - datetime.timedelta(days=1)).strftime('%Y-%m-%d'))
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
        if content['naver']['campaigns']:
            # form += '<h4>캠페인</h4>'
            form += '''
                <table style="width:100%;">
                <tr>
                    <th colspan="10" style="background-color: #00ff00;">캠페인</th>
                </tr>
                <tr>
                    <th>캠페인</th>
                    <th>비용</th>
                    <th>노출</th>
                    <th>클릭</th>
                    <th>클릭률</th>
                    <th>CPC</th>
                    <th>전환</th>
                </tr>
            '''
            for campaign in content['naver']['campaigns']:
                # tr
                form += '<tr>'
                # 계정 아이디
                # form += '<td>{}</td>'.format(campaign['network_id'])
                # 캠페인 이름 & 아이디
                form += '<td>{}</td>'.format(campaign['campaign_name'])
                # form += '<td>{}</td>'.format(campaign['campaign_id'])
                # 인사이트 데이터
                form += '<td>{}</td>'.format(format(int(campaign['salesAmt']), ','))
                form += '<td>{}</td>'.format(format(int(campaign['impCnt']), ','))
                form += '<td>{}</td>'.format(format(int(campaign['clkCnt']), ','))
                form += '<td>{}</td>'.format(campaign['ctr'])
                form += '<td>{}</td>'.format(format(int(campaign['cpc']), ','))
                # 전환은 있을 경우에만
                try:
                    form += '<td>{}</td>'.format(format(int(campaign['ccnt']), ','))
                except Exception as e:
                    form += '<td>{}</td>'.format(0)
                # form += '<td>{}</td>'.format(campaign['dateStart'])
                # /tr
                form += '</tr>'
            form += '</table>'

        if content['naver']['adgroups']:
            # form += '<h4>광고그룹</h4>'
            form += '''
                <table style="width:100%;">
                <tr>
                    <th colspan="10" style="background-color: #00ff00;">광고그룹</th>
                </tr>
                <tr>
                    <th>광고그룹</th>
                    <th>비용</th>
                    <th>노출</th>
                    <th>클릭</th>
                    <th>클릭률</th>
                    <th>CPC</th>
                    <th>전환</th>
                </tr>
            '''
            for adgroup in content['naver']['adgroups']:
                # tr
                form += '<tr>'
                # 계정 아이디
                # form += '<td>{}</td>'.format(adgroup['network_id'])
                # 광고그룹 이름 & 아이디
                form += '<td>{}</td>'.format(adgroup['adgroup_name'])
                # form += '<td>{}</td>'.format(adgroup['adgroup_id'])
                # 인사이트 데이터
                form += '<td>{}</td>'.format(format(int(adgroup['salesAmt']), ','))
                form += '<td>{}</td>'.format(format(int(adgroup['impCnt']), ','))
                form += '<td>{}</td>'.format(format(int(adgroup['clkCnt']), ','))
                form += '<td>{}</td>'.format(adgroup['ctr'])
                form += '<td>{}</td>'.format(format(int(adgroup['cpc']), ','))
                # 전환은 있을 경우에만
                try:
                    form += '<td>{}</td>'.format(format(int(adgroup['ccnt']), ','))
                except Exception as e:
                    form += '<td>{}</td>'.format(0)
                # form += '<td>{}</td>'.format(adgroup['dateStart'])
                # /tr
                form += '</tr>'
            form += '</table>'

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

    html_before = '''
    <!DOCTYPE html>
    <html>
    <head>
    <meta content="text/html; charset=utf-8" http-equiv="Content-Type"/>
    <style>
    table, th, td {border: 1px solid black; border-collapse: collapse;}
    td {text-align: center;}
    tr:nth-child(even) {background-color: #eee;}
    </style>
    </head>
    <body>
    '''
    html_after = '''
    </body>
    </html>
    '''
    html = html_before + form + html_after

    return html
    