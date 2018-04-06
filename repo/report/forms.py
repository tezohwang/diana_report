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

# 이메일 폼 업데이트 18.04.05
def create_mail_2(user_id, content):
    if not content['naver']:
        return False
    form = ''
    # html 시작
    form += '<html>'
    # head 파트
    form += '''
    <head>
        <meta content="text/html; charset=utf-8" http-equiv="Content-Type"/>
        <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">
        <style>
            td, th {
                border: 1px solid rgba(0, 0, 0, 0.1);
                border-collapse: collapse;
                text-align: center;
                padding: 5px;
            }
            tr:nth-child(even) {background-color: #f1fbf2;}
        </style>
    </head>
    '''
    # body 파트 상단
    form += '''
    <body>
        <div>
            <table style="width:100%; border:1px solid rgba(0,0,0,0.1);border-collapse:collapse;font-family:Helvetica;text-indent:0px;text-transform:none;font-size:20px;white-space:normal;word-spacing:0px;width:759px">
                <tr>
                    <td style="background-color:#52A4FC;color:#000000;padding:20px;">
                        <img alt="logo"
                            src="https://s3.ap-northeast-2.amazonaws.com/wizpace/diana_notification/diana_logo_white.png"
                            width="120" style="display: block;"/>
                    </td>
                </tr>
                <tr>
                    <td style="background-color:#FFFFFF;color:#333333;padding:0px; text-align: center;position: relative; border-color: #FFFFFF">
                        <h1 style="padding-top: 60px">{} <br> Diana Report</h1>
                        <hr width="20%" color="#00c73c">
                        <p style="padding-top: 20px"><b>Diana ID: {}</b></p>
                        <img alt="graph Image"
                            src="https://s3.ap-northeast-2.amazonaws.com/wizpace/diana_notification/header_image2.png"
                            width="100%" height="auto"/>
                    </td>
                </tr>
            </table>
            <br>
        </div>
        <div>
            <img alt="naver_logo" src="https://s3.ap-northeast-2.amazonaws.com/wizpace/diana_notification/naver_logo.png" width="120" style="display: block;padding: 5px;"/>
        </div>
    '''.format((datetime.datetime.now() - datetime.timedelta(days=1)).strftime('%Y-%m-%d'), content['user_id'])

    if not 'campaigns' in content['naver']:
        return False
    if content['naver']['campaigns']:
        # body > content 시작
        form += '''
        <div>
            <table style="width:100%; border:1px solid rgba(0,0,0,0.1);border-collapse:collapse;font-family:Helvetica;font-size:12px;font-style:normal;font-variant-caps:normal;font-weight:normal;letter-spacing:normal;text-align:start;text-indent:0px;text-transform:none;white-space:normal;word-spacing:0px;width:759px">
                <tbody>
        '''
        # body > content > '캠페인 영역 라인 표시'
        form += '''
        <tr>
            <th colspan="10"
                style="border:1px solid #52A4FC;border-collapse:collapse;background-color:#52A4FC;color: #FFFFFF;padding: 5px;font-size: 13px">
                캠페인
            </th>
        </tr>
        <tr style="color:#00c73c;">
        '''
        form += '''
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
        # 애드그룹이 있으면 작성
        if content['naver']['adgroups']:
            form += '''
                <table style="width:100%; border:1px solid rgba(0,0,0,0.1);border-collapse:collapse;font-family:Helvetica;font-size:12px;font-style:normal;font-variant-caps:normal;font-weight:normal;letter-spacing:normal;text-align:start;text-indent:0px;text-transform:none;white-space:normal;word-spacing:0px;width:759px">
                <tbody>
                <tr>
                    <th colspan="10"
                        style="border:1px solid #52A4FC;border-collapse:collapse;background-color:#52A4FC;color: #FFFFFF;padding: 5px;font-size: 13px">
                        광고그룹
                    </th>
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
        # 키워드 이슈가 있으면 작성
        if content['naver']['issues']:
            form += '''
                <table style="width:100%; border:1px solid rgba(0,0,0,0.1);border-collapse:collapse;font-family:Helvetica;font-size:12px;font-style:normal;font-variant-caps:normal;font-weight:normal;letter-spacing:normal;text-align:start;text-indent:0px;text-transform:none;white-space:normal;word-spacing:0px;width:759px">
                <tbody>
                <tr>
                    <th colspan="10"
                        style="border:1px solid #52A4FC;border-collapse:collapse;background-color:#52A4FC;color: #FFFFFF;padding: 5px;font-size: 13px">
                        키워드
                    </th>
                </tr>
                <tr>
                    <th>키워드명</th>
                    <th>주요 이슈</th>
                </tr>
            '''
            for issue_obj in content['naver']['issues']:
                # tr
                form += '<tr>'
                # 키워드 이름
                form += '<td>{}</td>'.format(issue_obj['keyword_name'])
                # 이슈 데이터
                form += '<td>{}</td>'.format(issue_obj['issue'])
                form += '</tr>'
        form += '</table>'
    form += '''
    </body>
    </html>
    '''
    return form
