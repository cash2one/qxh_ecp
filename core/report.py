#coding=utf-8
from collections import defaultdict,OrderedDict
from datetime import datetime,timedelta

from extensions import db

from flask.ext.login import current_user

from flask import render_template,Blueprint,request
from utils.decorator import admin_required

from settings.constants import *

report = Blueprint('report',__name__,url_prefix='/report')

@report.route('/sale')
@admin_required
def sale_report():
    return render_template('report/sale_report.html')

@report.route('/sale/ddxsmxtj')
@admin_required
def sale_report_by_ddxsmxtj():
    _conditions = ['`order`.status<>103','`order`.status>1']

    if not current_user.is_admin and current_user.team:
        _conditions.append('`order`.`team` LIKE "'+current_user.team+'%"')

    op_id = request.args.get('op',0)
    if op_id:
        _conditions.append('`created_by`=%d'%int(op_id))

    express_id = request.args.get('express_id',0)
    if express_id:
        _conditions.append('`order`.`express_id`=%d'%int(express_id))


    _start_date = request.args.get('start_date','')
    if _start_date:
        _conditions.append('`order`.`created`>="%s"'%_start_date)

    _end_date = request.args.get('end_date','')
    if _end_date:
        _conditions.append('`order`.`created`<="%s"'%_end_date)

    if not _start_date and not _end_date:
        period = datetime.now().strftime('%Y-%m-%d')
        _conditions.append('`order`.`created`>="%s 00:00:00"'%period)
    else:
        period = '%s ~ %s'%(_start_date if _start_date else u'开始',_end_date if _end_date else u'现在')

    _sql = '''SELECT
`order`.team,
operator.nickname,
`order`.username,
`order`.order_id,
`order_items`.item_info,
`order`.item_fee-`order`.discount_fee as `fee`,
`order`.discount_fee,
`order`.express_id,
`order`.express_number,
`order`.`created`
 FROM `order`
JOIN operator ON `order`.created_by=`operator`.id
JOIN (SELECT `order_item`.`order_id` as oid,GROUP_CONCAT(CONCAT(`order_item`.name,'*',`order_item`.quantity) SEPARATOR '\n') as item_info FROM `order_item` GROUP BY `order_item`.`order_id`) AS order_items ON `order`.order_id=`order_items`.oid
WHERE %s ORDER BY `order`.team,`order`.`created`
    '''%' AND '.join(_conditions)
    _data = db.session.execute(_sql)
    _rows = []
    total_fee = 0
    for team,op_name,username,order_id,item_info,fee,discount_fee,express_id,express_number,created in _data:
        total_fee += fee
        _rows.append({'depart':DEPARTMENTS[team[0]] if team else '',
                       'team':TEAMS[team] if team and len(team)==2 else '',
                       'op_name':op_name,
                       'username':username,
                       'order_id':order_id,
                       'items':item_info,
                       'fee':fee,
                       'discount_fee':discount_fee,
                       'express_name':EXPRESS_CONFIG[express_id]['name'] if express_id else '',
                       'express_number':express_number if express_number else '',
                       'created':created
                       })
    _op_sql = '''SELECT id,nickname FROM `operator` WHERE role_id=101'''
    _ops = db.session.execute(_op_sql)
    return render_template('report/sale_report_by_ddxsmxtj.html',rows=_rows,ops=_ops,total_fee=total_fee,period=period)


@report.route('/sale/arrival_detail')
@admin_required
def sale_report_by_arrival_detail():
    period = ''
    _conditions = ['`arrival_time` IS NOT NULL']#'`order`.status IN (6,60,100)',

    if not current_user.is_admin and current_user.team:
        _conditions.append('`order`.`team` LIKE "'+current_user.team+'%"')

    op_id = request.args.get('op',0)
    if op_id:
        _conditions.append('`created_by`=%d'%int(op_id))

    express_id = request.args.get('express_id',0)
    if express_id:
        _conditions.append('`order`.`express_id`=%d'%int(express_id))

    _start_date = request.args.get('start_date','')
    if _start_date:
        _conditions.append('`arrival_time`>="%s"'%_start_date)

    _end_date = request.args.get('end_date','')
    if _end_date:
        _conditions.append('`arrival_time`<="%s"'%_end_date)

    if not _start_date and not _end_date:
        period = datetime.now().strftime('%Y-%m-%d')
        _conditions.append('`arrival_time`>="%s 00:00:00"'%period)
    else:
        period = '%s ~ %s'%(_start_date if _start_date else u'开始',_end_date if _end_date else u'现在')

    _itm_sql = '''SELECT operator.id,operator.nickname,`order`.team,`order`.username,`order`.order_id,`order_items`.item_info,`order`.item_fee-`order`.discount_fee,`order`.discount_fee,`order`.express_id,`order`.express_number,`arrival_time`,`user`.m1,`user`.m2,`user`.m3 FROM `order` JOIN `operator` ON `order`.created_by=`operator`.id
 JOIN `user` ON `order`.user_id=`user`.user_id
JOIN (SELECT `order_item`.`order_id` as oid,GROUP_CONCAT(CONCAT(`order_item`.name,'*',`order_item`.quantity) SEPARATOR '\n') as item_info FROM `order_item` GROUP BY `order_item`.`order_id`) AS order_items ON `order`.order_id=`order_items`.oid
WHERE %s
ORDER BY `arrival_time`'''%' AND '.join(_conditions)
    rows = db.session.execute(_itm_sql)
    _op_sql = '''SELECT id,nickname FROM `operator` WHERE role_id=101'''
    _ops = db.session.execute(_op_sql)
    _rows = []
    total_fee = 0
    for data in rows:
        _rows.append(data)
        total_fee += data[6]

    return render_template('report/sale_report_by_arrival_detail.html',rows=_rows,ops=_ops,total_fee=total_fee,period=period)


@report.route('/sale/arrival_total')
@admin_required
def sale_report_by_arrival_total():
    period = ''
    _conditions = ['`arrival_time` IS NOT NULL']#'`order`.status IN (6,60,100)',
    if not current_user.is_admin and current_user.team:
        _conditions.append('`order`.`team` LIKE "'+current_user.team+'%"')

    _s_start_date = request.args.get('s_start_date','')
    if _s_start_date:
        _conditions.append('`order`.`created`>="%s"'%_s_start_date)

    _s_end_date = request.args.get('s_end_date','')
    if _s_end_date:
        _conditions.append('`order`.`created`<="%s"'%_s_end_date)

    _start_date = request.args.get('start_date','')
    if _start_date:
        _conditions.append('`arrival_time`>="%s"'%_start_date)

    _end_date = request.args.get('end_date','')
    if _end_date:
        _conditions.append('`arrival_time`<="%s"'%_end_date)

    if not _start_date and not _end_date:
        period = datetime.now().strftime('%Y-%m-%d')
        _conditions.append('`arrival_time`>="%s 00:00:00"'%period)
    else:
        period = '%s ~ %s'%(_start_date if _start_date else u'开始',_end_date if _end_date else u'现在')

    _sql2 = '''SELECT SUBSTRING(`order`.team,1,1) AS `t`,DATE(`order`.arrival_time) AS dt,COUNT(distinct order_id),SUM(`order`.item_fee-`order`.discount_fee) FROM `order` WHERE `order`.team<>'' AND %s
GROUP BY t,dt'''%' AND '.join(_conditions)
    col_rows = db.session.execute(_sql2)

    details = defaultdict(list)
    fee_totals = defaultdict(int)
    num_totals = defaultdict(int)
    for team,dt,orders,fee in col_rows:
        fee_totals[team]+= fee
        num_totals[team]+= orders
        details[team].append((dt,orders,fee))

    rows = []
    for team,detail in details.iteritems():
        orders = num_totals[team]
        fee = fee_totals[team]
        rows.append({'team':team,'fee':fee,'orders':orders,'avg_fee':fee/orders if orders>0 else 0,
                      'detail':detail,'n':len(detail)+1})
    return render_template('report/sale_report_by_arrival_total.html',rows=rows,period=period)


@report.route('/sale/return_detail')
@admin_required
def sale_report_by_return_detail():
    period = ''
    _conditions = ['`order`.status IN (102,104)','`end_time` IS NOT NULL']

    if not current_user.is_admin and current_user.team:
        _conditions.append('`order`.`team` LIKE "'+current_user.team+'%"')

    op_id = request.args.get('op',0)
    if op_id:
        _conditions.append('`order`.`created_by`=%d'%int(op_id))

    express_id = request.args.get('express_id',0)
    if express_id:
        _conditions.append('`order`.`express_id`=%d'%int(express_id))



    is_arrival = request.args.get('is_arrival',0)
    if is_arrival:
        is_arrival = int(is_arrival)
        if is_arrival == 1:
            _conditions.append('`order`.`arrival_time` is not null')
        elif is_arrival == 2:
            _conditions.append('`order`.`arrival_time` is null')

    _s_start_date = request.args.get('s_start_date','')
    if _s_start_date:
        _conditions.append('`order`.`created`>="%s"'%_s_start_date)

    _s_end_date = request.args.get('s_end_date','')
    if _s_end_date:
        _conditions.append('`order`.`created`<="%s"'%_s_end_date)


    _start_date = request.args.get('start_date','')
    if _start_date:
        _conditions.append('`end_time`>="%s"'%_start_date)

    _end_date = request.args.get('end_date','')
    if _end_date:
        _conditions.append('`end_time`<="%s"'%_end_date)

    if not _start_date and not _end_date:
        period = datetime.now().strftime('%Y-%m-%d')
        _conditions.append('`end_time`>="%s 00:00:00"'%period)
    else:
        period = '%s ~ %s'%(_start_date if _start_date else u'开始',_end_date if _end_date else u'现在')

    _itm_sql = '''SELECT operator.id,operator.nickname,`order`.team,`order`.username,`order`.order_id,`order_items`.item_info,`order`.item_fee-`order`.discount_fee,`order`.discount_fee,`order`.express_id,`order`.express_number,`end_time` FROM `order` JOIN `operator` ON `order`.created_by=`operator`.id
JOIN (SELECT `order_item`.`order_id` as oid,GROUP_CONCAT(CONCAT(`order_item`.name,'*',`order_item`.quantity) SEPARATOR '\n') as item_info FROM `order_item` GROUP BY `order_item`.`order_id`) AS order_items ON `order`.order_id=`order_items`.oid
WHERE %s
ORDER BY `end_time`'''%' AND '.join(_conditions)
    rows = db.session.execute(_itm_sql)

    _op_sql = '''SELECT id,nickname FROM `operator` WHERE role_id=101'''
    _ops = db.session.execute(_op_sql)
    _rows = []
    total_fee = 0
    for data in rows:
        _rows.append(data)
        total_fee += data[6]

    return render_template('report/sale_report_by_return_detail.html',rows=_rows,ops=_ops,total_fee=total_fee,period=period)


@report.route('/sale/return_total')
@admin_required
def sale_report_by_return_total():
    period = ''
    _conditions = ['`order`.status IN (102,104)','`end_time` IS NOT NULL']

    if not current_user.is_admin and current_user.team:
        _conditions.append('`order`.`team` LIKE "'+current_user.team+'%"')

    _s_start_date = request.args.get('s_start_date','')
    if _s_start_date:
        _conditions.append('`order`.`created`>="%s"'%_s_start_date)

    _s_end_date = request.args.get('s_end_date','')
    if _s_end_date:
        _conditions.append('`order`.`created`<="%s"'%_s_end_date)

    _start_date = request.args.get('start_date','')
    if _start_date:
        _conditions.append('`end_time`>="%s"'%_start_date)

    is_arrival = request.args.get('is_arrival',0)
    if is_arrival:
        is_arrival = int(is_arrival)
        if is_arrival == 1:
            _conditions.append('`order`.`arrival_time` is not null')
        elif is_arrival == 2:
            _conditions.append('`order`.`arrival_time` is null')

    _end_date = request.args.get('end_date','')
    if _end_date:
        _conditions.append('`end_time`<="%s"'%_end_date)

    if not _start_date and not _end_date:
        period = datetime.now().strftime('%Y-%m-%d')
        _conditions.append('`end_time`>="%s 00:00:00"'%period)
    else:
        period = '%s ~ %s'%(_start_date if _start_date else u'开始',_end_date if _end_date else u'现在')

    _sql2 = '''SELECT SUBSTRING(team,1,1) AS `t`,DATE(`order`.end_time) AS dt,COUNT(distinct order_id),SUM(`order`.item_fee-`order`.discount_fee) FROM `order` WHERE `order`.team<>'' AND %s
GROUP BY t,dt'''%' AND '.join(_conditions)
    col_rows = db.session.execute(_sql2)

    details = defaultdict(list)
    fee_totals = defaultdict(int)
    num_totals = defaultdict(int)
    for team,dt,orders,fee in col_rows:
        fee_totals[team]+= fee
        num_totals[team]+= orders
        details[team].append((dt,orders,fee))

    rows = []
    for team,detail in details.iteritems():
        orders = num_totals[team]
        fee = fee_totals[team]
        rows.append({'team':team,'fee':fee,'orders':orders,'avg_fee':fee/orders if orders>0 else 0,
                     'detail':detail,'n':len(detail)+1})
    return render_template('report/sale_report_by_return_total.html',rows=rows,period=period)


@report.route('/sale/ygxs')
@admin_required
def sale_report_by_ygxs():
    period = ''
    _conditions = ['status NOT IN (1,103)']#['status IN (2,3,40,4,5,6,60,100)']

    if not current_user.is_admin and current_user.team:
        _conditions.append('`order_team` LIKE "'+current_user.team+'%"')

    _start_date = request.args.get('start_date','')
    if _start_date:
        _conditions.append('`created`>="%s"'%_start_date)

    _end_date = request.args.get('end_date','')
    if _end_date:
        _conditions.append('`created`<="%s"'%_end_date)

    if not _start_date and not _end_date:
        _conditions.append('`order_date`="%s"'%datetime.now().strftime('%y%m%d'))
        period = datetime.now().strftime('%Y-%m-%d')
    else:
        period = '%s ~ %s'%(_start_date if _start_date else u'开始',_end_date if _end_date else u'现在')

    _itm_sql = '''SELECT
                    operator_id,
                    item_name,
                    price,
                    SUM(quantity),
                    SUM(fee)
                FROM
                    `operator_order_items`
                WHERE
                    %s
                GROUP BY
                    operator_id,
                    item_name,
                    price'''%' AND '.join(_conditions)
    op_items = db.session.execute(_itm_sql)

    _op_items = defaultdict(list)
    for op_id,item_name,price,quantity,fee in op_items:
        _op_items[op_id].append((item_name,price,quantity,fee))

    _count_sql = '''SELECT order_team,operator_id,nickname,count(DISTINCT order_id),SUM(fee) from operator_order_items WHERE %s GROUP BY order_team,operator_id,nickname ORDER BY order_team'''%' AND '.join(_conditions)

    rows=[]
    op_counts = db.session.execute(_count_sql)
    total_orders = 0
    total_fee = 0
    for team,op_id,nickname,order_nums,fee in op_counts:
        total_orders += order_nums
        total_fee += fee
        _items = _op_items[op_id]
        rows.append({'team':team,'op_id':op_id,'nickname':nickname,'order_nums':order_nums,'total_fee':fee,'items':_items,'n':len(_items)+1})
    return render_template('report/sale_report_by_ygxs.html',rows=rows,period=period,total_orders=total_orders,total_fee=total_fee)


@report.route('/sale/ygdhtj')
@admin_required
def sale_report_by_ygdhtj():
    period = ''
    _conditions = ['`arrival_time` IS NOT NULL']#'status IN (6,60,100)'#['status IN (2,3,40,4,5,6,60,100)']

    if not current_user.is_admin and current_user.team:
        _conditions.append('`order_team` LIKE "'+current_user.team+'%"')


    _s_start_date = request.args.get('s_start_date','')
    if _s_start_date:
        _conditions.append('`created`>="%s"'%_s_start_date)

    _s_end_date = request.args.get('s_end_date','')
    if _s_end_date:
        _conditions.append('`created`<="%s"'%_s_end_date)


    _start_date = request.args.get('start_date','')
    if _start_date:
        _conditions.append('`arrival_time`>="%s"'%_start_date)

    _end_date = request.args.get('end_date','')
    if _end_date:
        _conditions.append('`arrival_time`<="%s"'%_end_date)

    if not _start_date and not _end_date:
        period = datetime.now().strftime('%Y-%m-%d')
        _conditions.append('`arrival_time`>="%s 00:00:00"'%period)
    else:
        period = '%s ~ %s'%(_start_date if _start_date else u'开始',_end_date if _end_date else u'现在')

    op_id = request.args.get('op',0)
    if op_id:
        _conditions.append('`operator_id`=%d'%int(op_id))

    _itm_sql = '''SELECT
                    operator_id,
                    order_team,
                    item_name,
                    price,
                    SUM(quantity),
                    SUM(fee)
                FROM
                    `operator_order_items`
                WHERE
                    %s
                GROUP BY
                    operator_id,
                    order_team,
                    item_name,
                    price'''%' AND '.join(_conditions)
    #return _itm_sql
    op_items = db.session.execute(_itm_sql)

    _op_items = defaultdict(list)
    for op_id,team,item_name,price,quantity,fee in op_items:
        _op_items['%s-%s'%(op_id,team)].append((item_name,price,quantity,fee))

    _count_sql = '''SELECT order_team,operator_id,nickname,count(DISTINCT order_id),SUM(fee) from operator_order_items WHERE %s GROUP BY order_team,operator_id,nickname ORDER BY order_team'''%' AND '.join(_conditions)

    _op_sql = '''SELECT id,nickname FROM `operator` WHERE role_id=101'''
    _ops = db.session.execute(_op_sql)

    rows=[]
    op_counts = db.session.execute(_count_sql)
    total_orders = 0
    total_fee = 0
    for team,op_id,nickname,order_nums,fee in op_counts:
        total_orders += order_nums
        total_fee += fee
        _items = _op_items['%s-%s'%(op_id,team)]
        rows.append({'team':team,'op_id':op_id,'nickname':nickname,'order_nums':order_nums,'total_fee':fee,'items':_items,'n':len(_items)+1})
        # _fee = sum(map(lambda i:i[3],_items))
        # if _fee<>fee:
        #     print nickname,_fee,fee
    return render_template('report/sale_report_by_ygdhtj.html',rows=rows,ops=_ops,period=period,total_orders=total_orders,total_fee=total_fee)


@report.route('/sale/staff')
@admin_required
def sale_report_by_staff():
    period = ''
    _conditions = ['`order`.status NOT IN (1,103)']#['`order`.status IN (2,3,40,4,5,6,60,100)']

    if not current_user.is_admin and current_user.team:
        _conditions.append('`order`.`team` LIKE "'+current_user.team+'%"')


    _start_date = request.args.get('start_date','')
    if _start_date:
        _conditions.append('`order`.`created`>="%s"'%_start_date)

    _end_date = request.args.get('end_date','')
    if _end_date:
        _conditions.append('`order`.`created`<="%s"'%_end_date)

    if not _start_date and not _end_date:
        _conditions.append('`order`.`date`="%s"'%datetime.now().strftime('%y%m%d'))
        period = datetime.now().strftime('%Y-%m-%d')
    else:
        period = '%s ~ %s'%(_start_date if _start_date else u'开始',_end_date if _end_date else u'现在')

    _sql = '''SELECT
`operator`.id,`operator`.nickname,`order`.`team`,COUNT(`order`.order_id) AS `order_nums`,SUM(`order`.item_fee-`order`.discount_fee) AS `total_fee`,
SUM(CASE WHEN `order`.item_fee<=`order`.discount_fee THEN 1 ELSE 0 END) AS `zero_order_nums`
FROM `order` LEFT JOIN `operator` ON `order`.created_by = `operator`.id
WHERE %s
GROUP BY `operator`.id,`operator`.nickname,`order`.`team` ORDER BY `order`.`team`'''%' AND '.join(_conditions)
    rows = db.session.execute(_sql)
    total_orders = 0
    total_fee = 0
    _rows = []
    for r in rows:
        _rows.append(r)
        total_orders += r[3]
        total_fee += r[4]

    _sql2 = '''SELECT `order`.team,operator.id,operator.nickname,DATE(`order`.created) AS dt,COUNT(distinct order_id),SUM(`order`.item_fee-`order`.discount_fee) FROM `order` JOIN `operator` ON `order`.created_by=`operator`.id
WHERE %s
GROUP BY `order`.team,operator.id,operator.nickname,dt ORDER BY `order`.team,dt'''%' AND '.join(_conditions)
    col_rows = db.session.execute(_sql2)

    details = defaultdict(list)
    fee_totals = defaultdict(int)
    num_totals = defaultdict(int)
    op_infos = {}
    for team,op_id,op_name,dt,orders,fee in col_rows:
        fee_totals[op_id]+= fee
        num_totals[op_id]+= orders
        details[op_id].append((dt,orders,fee))
        if not op_infos.has_key(op_id):
            op_infos[op_id] = (team,op_name)


    rows2 = []
    for op_id,data in op_infos.iteritems():
        orders = num_totals[op_id]
        fee = fee_totals[op_id]
        team,op_name = data
        detail = details[op_id]
        rows2.append({'team':team,'id':op_id,'op_name':op_name,'fee':fee,'orders':orders,'avg_fee':fee/orders if orders>0 else 0,
                      'detail':detail,'n':len(detail)+1})

    rows2 = sorted(rows2,key=lambda d:d['team'])
    return render_template('report/sale_report_by_staff.html',rows=_rows,rows2=rows2,period=period,total_orders=total_orders,total_fee=total_fee)

@report.route('/sale/team')
@admin_required
def sale_report_by_team():
    period = ''
    _conditions = ['`order`.status NOT IN (1,103)']#['`order`.status IN (2,3,40,4,5,6,60,100)']

    if not current_user.is_admin and current_user.team:
        _conditions.append('`order`.`team` LIKE "'+current_user.team+'%"')

    _start_date = request.args.get('start_date','')
    if _start_date:
        _conditions.append('`order`.`created`>="%s"'%_start_date)

    _end_date = request.args.get('end_date','')
    if _end_date:
        _conditions.append('`order`.`created`<="%s"'%_end_date)

    if not _start_date and not _end_date:
        _conditions.append('`order`.`date`="%s"'%datetime.now().strftime('%y%m%d'))
        period = datetime.now().strftime('%Y-%m-%d')
    else:
        period = '%s ~ %s'%(_start_date if _start_date else u'开始',_end_date if _end_date else u'现在')

    _sql = '''SELECT
`order`.team,COUNT(`order`.order_id) AS `order_nums`,SUM(`order`.item_fee-`order`.discount_fee) AS `total_fee`,
 SUM(CASE WHEN `order`.item_fee<=`order`.discount_fee THEN 1 ELSE 0 END) AS `zero_order_nums` FROM `order` LEFT JOIN `operator` ON `order`.created_by = `operator`.id
WHERE %s
GROUP BY `order`.team'''%' AND '.join(_conditions)
    rows = db.session.execute(_sql)
    total_orders = 0
    total_fee = 0
    _rows = []
    for r in rows:
        _rows.append(r)
        total_orders += r[1]
        total_fee += r[2]


    _sql2 = '''SELECT SUBSTRING(`order`.team,1,1) AS `t`,DATE(`order`.created) AS dt,SUM(CASE WHEN `order`.item_fee<=`order`.discount_fee THEN 0 ELSE 1 END) AS `order_nums`,SUM(`order`.item_fee-`order`.discount_fee) FROM `order` WHERE `order`.team<>'' AND %s
GROUP BY t,dt'''%' AND '.join(_conditions)
    col_rows = db.session.execute(_sql2)

    details = defaultdict(list)
    fee_totals = defaultdict(int)
    num_totals = defaultdict(int)
    for team,dt,orders,fee in col_rows:
        orders = int(orders)
        fee_totals[team]+= fee
        num_totals[team]+= orders
        details[team].append((dt,orders,fee))

    rows2 = []
    for team,detail in details.iteritems():
        orders = num_totals[team]
        fee = fee_totals[team]
        rows2.append({'team':team,'fee':fee,'orders':orders,'avg_fee':fee/orders if orders>0 else 0,
                      'detail':detail,'n':len(detail)+1})
    return render_template('report/sale_report_by_team.html',rows=_rows,rows2=rows2,period=period,total_orders=total_orders,total_fee=total_fee)

@report.route('/sale/item')
@admin_required
def sale_report_by_item():
    period = ''
    _conditions = ['`order`.status NOT IN (1,103)']#['`order`.status IN (2,3,40,4,5,6,60,100)']

    if not current_user.is_admin and current_user.team:
        _conditions.append('`order`.`team` LIKE "'+current_user.team+'%"')
    else:
        _depart = request.args.get('depart','')
        if _depart:
            _conditions.append('`order`.team LIKE "%s%%"'%_depart)

    _start_date = request.args.get('start_date','')
    if _start_date:
        _conditions.append('`order`.`created`>="%s"'%_start_date)

    _end_date = request.args.get('end_date','')
    if _end_date:
        _conditions.append('`order`.`created`<="%s"'%_end_date)

    if not _start_date and not _end_date:
        _conditions.append('`order`.`date`="%s"'%datetime.now().strftime('%y%m%d'))
        period = datetime.now().strftime('%Y-%m-%d')
    else:
        period = '%s ~ %s'%(_start_date if _start_date else u'开始',_end_date if _end_date else u'现在')


    _sql = '''SELECT `sku_item`.`category_id`,`order_item`.`sku_id`,`order_item`.name,SUM(`order_item`.quantity),SUM(`order_item`.fee)
    FROM `order_item`
    JOIN (SELECT `order_id` FROM `order` WHERE %s) AS `orders` ON `order_item`.order_id=`orders`.order_id
    LEFT JOIN (SELECT `item`.`category_id`,`sku`.id AS `sku_id` FROM `item` JOIN `sku` ON `item`.id=`sku`.item_id) AS `sku_item` ON `sku_item`.sku_id=`order_item`.sku_id
    GROUP BY `sku_item`.`category_id`,`order_item`.`sku_id`,`order_item`.name'''%' AND '.join(_conditions)

    rows = db.session.execute(_sql)
    detail = defaultdict(list)
    for category_id,sku_id,item_name,quantity,fee in rows:
        detail[category_id].append({'sku_id':sku_id,'item_name':item_name,'quantity':quantity,'fee':fee})

    data = []
    for c_id,items in detail.iteritems():
        data.append({'category_id':c_id,'category_name':ITEM_CATEGORYS[c_id],
                     'items':items,'quantity':sum(map(lambda s:s['quantity'],items)),
                     'fee':sum(map(lambda s:s['fee'],items)),
                     'num':len(items)})
    return render_template('report/sale_report_by_item.html',data=data,period=period)


@report.route('/financial')
@admin_required
def financial_report():
    return render_template('report/financial_report.html')



@report.route('/financial/sale')
@admin_required
def financial_report_by_sale():
    _conditions = ['`order`.delivery_time IS NOT NULL','`order`.order_type<100']

    order_type = request.args.get('order_type',0)
    if order_type:
        _conditions.append('`order`.order_type=%s'%order_type)

    _start_date = request.args.get('start_date','')
    if _start_date:
        _conditions.append('`order`.delivery_time>="%s"'%_start_date)

    _end_date = request.args.get('end_date','')
    if _end_date:
        _conditions.append('`order`.delivery_time<="%s"'%_end_date)

    express_id = request.args.get('express_id',0)
    if express_id:
        _conditions.append('`order`.express_id=%s'%express_id)

    if not _start_date and not _end_date:
        _today = datetime.now().strftime('%Y-%m-%d')
        _conditions.append('`order`.delivery_time>="%s 00:00:00"'%_today)
        period = _today
    else:
        period = '%s ~ %s'%(_start_date if _start_date else u'开始',_end_date if _end_date else u'现在')

    _sql2 = '''SELECT
                `order`.express_id,
                COUNT(DISTINCT `order`.order_id),SUM(`order`.item_fee-`order`.discount_fee) as sumfee FROM `order`
                WHERE
                %s
                GROUP BY `order`.express_id'''%' AND '.join(_conditions)
    orders = db.session.execute(_sql2)
    #print _sql2
    totalree = []#所有订单总额
    totalorders = []#所有订单数

    item_type = request.args.get('item_type','')
    if item_type:
        item_type = int(item_type)
        if item_type == 1:_conditions.append('`order_item`.fee>0')
        elif item_type == 2:_conditions.append('`order_item`.fee=0')

    _sql = '''SELECT
                `order`.express_id,
                `order_item`.name,
                `order_item`.price,
                SUM(`order_item`.quantity),
                SUM(`order_item`.fee)
            FROM `order_item`
            JOIN `order` ON `order_item`.order_id=`order`.order_id
            WHERE
            %s
            GROUP BY `order`.express_id,`order_item`.name,`order_item`.price ORDER BY `order`.express_id'''%' AND '.join(_conditions)
    print _sql
    data = db.session.execute(_sql)
    return render_template('report/financial_report_by_fh.html',totalorders=totalorders,totalree=totalree,data=data,orders=orders,period=period)


@report.route('/financial/return')
@admin_required
def financial_report_by_return():
    _conditions = ['`order`.status IN (102,104)','`order`.order_type<100']

    op_id = request.args.get('op',0)
    if op_id:
        _conditions.append('`created_by`=%d'%int(op_id))

    express_id = request.args.get('express_id',0)
    if express_id:
        _conditions.append('`order`.`express_id`=%d'%int(express_id))

    _s_start_date = request.args.get('s_start_date','')
    if _s_start_date:
        _conditions.append('`order`.`delivery_time`>="%s"'%_s_start_date)

    _s_end_date = request.args.get('s_end_date','')
    if _s_end_date:
        _conditions.append('`order`.`delivery_time`<="%s"'%_s_end_date)

    order_type = request.args.get('order_type',0)
    if order_type:
        _conditions.append('`order`.order_type=%s'%order_type)

    _start_date = request.args.get('start_date','')
    if _start_date:
        _conditions.append('`order`.end_time>="%s"'%_start_date)

    _end_date = request.args.get('end_date','')
    if _end_date:
        _conditions.append('`order`.end_time<="%s"'%_end_date)

    if not _start_date and not _end_date:
        _today = datetime.now().strftime('%Y-%m-%d')
        _conditions.append('`order`.end_time>="%s 00:00:00"'%_today)
        period = _today
    else:
        period = '%s ~ %s'%(_start_date if _start_date else u'开始',_end_date if _end_date else u'现在')

    _sql2 = '''SELECT
                `order`.express_id,
                COUNT(DISTINCT `order`.order_id),SUM(`order`.item_fee) as sumfee FROM `order`
                WHERE
                %s
                GROUP BY `order`.express_id'''%' AND '.join(_conditions)
    orders = db.session.execute(_sql2)
    totalree = []#所有订单总额
    totalorders = []#所有订单数


    item_type = request.args.get('item_type','')
    if item_type:
        item_type = int(item_type)
        if item_type == 1:_conditions.append('`order_item`.fee>0')
        elif item_type == 2:_conditions.append('`order_item`.fee=0')

    _sql = '''SELECT
                `order`.express_id,
                `order_item`.name,
                `order_item`.price,
                SUM(`order_item`.quantity),
                SUM(`order_item`.fee)
            FROM `order_item`
            JOIN `order` ON `order_item`.order_id=`order`.order_id
            WHERE
            %s
            GROUP BY `order`.express_id,`order_item`.name,`order_item`.price ORDER BY `order`.express_id'''%' AND '.join(_conditions)
    data = db.session.execute(_sql)
    _op_sql = '''SELECT id,nickname FROM `operator` WHERE role_id=101'''
    _ops = db.session.execute(_op_sql)

    return render_template('report/financial_report_by_fh.html',totalorders=totalorders,ops=_ops,totalree=totalree,data=data,orders=orders,period=period)


@report.route('/financial/dzbb')
@admin_required
def financial_report_by_dzbb():
    period = ''
    _conditions = ['`order_log`.to_status=60','`order_log`.`order_id` = `order`.`order_id`','`order`.order_type<100']
    _start_date = request.args.get('start_date','')
    if _start_date:
        _conditions.append('`order_log`.`operate_time`>="%s"'%_start_date)

    _end_date = request.args.get('end_date','')
    if _end_date:
        _conditions.append('`order_log`.`operate_time`<="%s"'%_end_date)

    if not _start_date and not _end_date:
        _today = datetime.now().strftime('%Y-%m-%d')
        _conditions.append('`order_log`.`operate_time`>="%s 00:00:00"'%_today)
        _conditions.append('`order_log`.`operate_time`<="%s 23:59:59"'%_today)
        period = _today
    else:
        period = '%s ~ %s'%(_start_date if _start_date else u'开始',_end_date if _end_date else u'现在')

    _s_start_date = request.args.get('s_start_date','')
    if _s_start_date:
        _conditions.append('`order`.`delivery_time`>="%s"'%_s_start_date)

    _s_end_date = request.args.get('s_end_date','')
    if _s_end_date:
        _conditions.append('`order`.`delivery_time`<="%s"'%_s_end_date)

    express_id = request.args.get('express_id',0)
    if express_id:
        _conditions.append('`order`.express_id=%s'%express_id)

    _sql = '''SELECT `tmp_order`.express_id,`tmp_order`.order_id,order_item.sku_id,order_item.name,SUM(`order_item`.quantity),SUM(`order_item`.fee) FROM `order_item`
JOIN (SELECT `order`.order_id,`order`.express_id FROM `order` JOIN `order_log` ON %s) AS `tmp_order` ON `tmp_order`.`order_id`=`order_item`.order_id
GROUP BY `tmp_order`.express_id,order_item.sku_id,order_item.name ORDER BY `tmp_order`.express_id'''%' AND '.join(_conditions)
    #return _sql
    rows = db.session.execute(_sql)
    data = []
    for express_id,order_id,sku_id,item_name,quantity,fee in rows:
        data.append({'express_name':EXPRESS_CONFIG[express_id]['name'],
                     'item_name':item_name,
                     'quantity':quantity,
                     'fee':fee})
    return render_template('report/financial_report_by_dzbb.html',data=data,period=period)


@report.route('/financial/paidan')
@admin_required
def financial_report_by_paidan():
    period = ''
    _conditions = ['`order`.order_type<100']
    _start_date = request.args.get('start_date','')
    if _start_date:
        _conditions.append('`order`.delivery_time>="%s"'%_start_date)

    _end_date = request.args.get('end_date','')
    if _end_date:
        _conditions.append('`order`.delivery_time<="%s"'%_end_date)

    if not _start_date and not _end_date:
        _today = datetime.now().strftime('%Y-%m-%d')
        _conditions.append('`order`.delivery_time>="%s 00:00:00"'%_today)
        period = _today
    else:
        period = '%s ~ %s'%(_start_date if _start_date else u'开始',_end_date if _end_date else u'现在')

    express_id = request.args.get('express_id',0)
    if express_id:
        _conditions.append('`order`.express_id=%s'%express_id)

    _sql = '''SELECT `order`.order_type,`operator`.nickname,`order`.team,`order`.delivery_time,`order`.order_id,`express_id`,`express_number`,`ship_to`,`province`,`city`,`district`,`street1`,`order`.item_fee-`order`.discount_fee,`order_item`.name,`order_item`.price,`order_item`.quantity,`order_item`.fee FROM `order_item`
JOIN `order` ON `order_item`.order_id=`order`.order_id AND `order`.delivery_time IS NOT NULL
JOIN `address` ON `order`.shipping_address_id=`address`.id
JOIN `operator` ON `operator`.id=`order`.created_by
WHERE %s
ORDER BY `order`.delivery_time'''%' AND '.join(_conditions)
    rows = db.session.execute(_sql)
    data = OrderedDict()
    for order_type,op_name,team,delivery_time,order_id,express_id,express_number,ship_to,province,city,district,street1,fee,item_name,price,quantity,item_fee in rows:
        if not data.has_key(order_id):
            data[order_id] = {'eid':express_id,
                              'op':op_name,
                              'team':DEPARTMENTS.get(team[0],'') if team else '',
                              'ename':EXPRESS_CONFIG[int(express_id)]['name'],
                              'enum':express_number,
                              'ordertype':ORDER_TYPES[order_type],
                              'fee':fee,
                              'id':order_id,
                              'date':delivery_time.strftime("%Y-%m-%d"),
                              'items':[],
                              'ship_to':ship_to,
                              'province':province,
                              'city':city,
                              'district':district,
                              'street1':street1
                              }
        data[order_id]['items'].append({'name':item_name,'num':quantity,'fee':item_fee,'price':price})
    _data = data.values()
    _data = sorted(_data,key=lambda d:d['eid'])
    return render_template('report/financial_report_by_paidan.html',data=_data,period=period)


@report.route('/financial/paidan/tuihuo')
@admin_required
def financial_report_by_paidan_tuihuo():
    period = ''
    _conditions = ['`order`.status>100','`order`.order_type<100']
    _start_date = request.args.get('start_date','')
    if _start_date:
        _conditions.append('`order`.end_time>="%s"'%_start_date)

    _end_date = request.args.get('end_date','')
    if _end_date:
        _conditions.append('`order`.end_time<="%s"'%_end_date)

    if not _start_date and not _end_date:
        _today = datetime.now().strftime('%Y-%m-%d')
        _conditions.append('`order`.end_time>="%s 00:00:00"'%_today)
        period = _today
    else:
        period = '%s ~ %s'%(_start_date if _start_date else u'开始',_end_date if _end_date else u'现在')

    _s_start_date = request.args.get('s_start_date','')
    if _s_start_date:
        _conditions.append('`order`.`delivery_time`>="%s"'%_s_start_date)

    _s_end_date = request.args.get('s_end_date','')
    if _s_end_date:
        _conditions.append('`order`.`delivery_time`<="%s"'%_s_end_date)

    express_id = request.args.get('express_id',0)
    if express_id:
        _conditions.append('`order`.express_id=%s'%express_id)

    _sql = '''SELECT `operator`.nickname,`order`.`team`,`order`.delivery_time,`order`.end_time,`order`.order_id,`express_id`,`express_number`,`ship_to`,`province`,`city`,`district`,`street1`,`order`.item_fee-`order`.discount_fee,`order_item`.name,`order_item`.price,`order_item`.quantity,`order_item`.in_quantity,`order_item`.fee FROM `order_item`
JOIN `order` ON `order_item`.order_id=`order`.order_id AND `order`.delivery_time IS NOT NULL AND `order`.arrival_time IS NULL
JOIN `address` ON `order`.shipping_address_id=`address`.id
JOIN `operator` ON `operator`.id=`order`.created_by
WHERE %s
ORDER BY `order`.end_time'''%' AND '.join(_conditions)
    rows = db.session.execute(_sql)
    data = OrderedDict()
    for op_name,team,delivery_time,end_time,order_id,express_id,express_number,ship_to,province,city,district,street1,fee,item_name,price,quantity,in_quantity,item_fee in rows:
        if not data.has_key(order_id):
            data[order_id] = {'eid':express_id,
                              'op':op_name,
                              'team':DEPARTMENTS.get(team[0],'') if team else '',
                              'ename':EXPRESS_CONFIG[int(express_id)]['name'],
                              'enum':express_number,
                              'fee':fee,
                              'id':order_id,
                              'date':end_time.strftime("%Y-%m-%d"),
                              'delivery_time':delivery_time.strftime("%Y-%m-%d"),
                              'items':[],
                              'ship_to':ship_to,
                              'province':province,
                              'city':city,
                              'district':district,
                              'street1':street1
            }
        data[order_id]['items'].append({'name':item_name,'num':quantity,'in':in_quantity,'fee':item_fee,'price':price})
    _data = data.values()
    _data = sorted(_data,key=lambda d:d['eid'])
    return render_template('report/financial_report_by_paidan_tuihuo.html',data=_data,period=period)



@report.route('/financial/qianshou')
@admin_required
def financial_report_by_qianshou():
    period = ''
    _conditions = ['`order`.order_type<100']
    _start_date = request.args.get('start_date','')
    if _start_date:
        _conditions.append('`order`.arrival_time>="%s"'%_start_date)

    _end_date = request.args.get('end_date','')
    if _end_date:
        _conditions.append('`order`.arrival_time<="%s"'%_end_date)

    if not _start_date and not _end_date:
        _today = datetime.now().strftime('%Y-%m-%d')
        _conditions.append('`order`.arrival_time>="%s 00:00:00"'%_today)
        period = _today
    else:
        period = '%s ~ %s'%(_start_date if _start_date else u'开始',_end_date if _end_date else u'现在')

    _s_start_date = request.args.get('s_start_date','')
    if _s_start_date:
        _conditions.append('`order`.`delivery_time`>="%s"'%_s_start_date)

    _s_end_date = request.args.get('s_end_date','')
    if _s_end_date:
        _conditions.append('`order`.`delivery_time`<="%s"'%_s_end_date)

    express_id = request.args.get('express_id',0)
    if express_id:
        _conditions.append('`order`.express_id=%s'%express_id)

    _sql = '''SELECT `operator`.nickname,`order`.delivery_time,`order`.team,`order`.arrival_time,`order`.order_id,`express_id`,`express_number`,`ship_to`,`province`,`city`,`district`,`street1`,`order`.item_fee-`order`.discount_fee,`order_item`.name,`order_item`.price,`order_item`.quantity,`order_item`.fee,`user`.m1,`user`.m2,`user`.m3 FROM `order_item`
JOIN `order` ON `order_item`.order_id=`order`.order_id AND `order`.arrival_time IS NOT NULL
 JOIN `user` ON `order`.user_id=`user`.user_id
JOIN `operator` ON `operator`.id=`order`.created_by
JOIN `address` ON `order`.shipping_address_id=`address`.id
WHERE %s
ORDER BY `order`.arrival_time'''%' AND '.join(_conditions)
    #return _sql
    rows = db.session.execute(_sql)
    data = OrderedDict()
    for op_name,delivery_time,team,arrival_time,order_id,express_id,express_number,ship_to,province,city,district,street1,fee,item_name,price,quantity,item_fee,m1,m2,m3 in rows:
        if not data.has_key(order_id):
            data[order_id] = {'eid':express_id,
                              'op':op_name,
                              'team':DEPARTMENTS.get(team[0],'') if team else '',
                              'ename':EXPRESS_CONFIG[int(express_id)]['name'],
                              'enum':express_number,
                              'fee':fee,
                              'id':order_id,
                              'date':arrival_time.strftime("%Y-%m-%d"),
                              'delivery_time':delivery_time.strftime("%Y-%m-%d"),
                              'items':[],
                              'ship_to':ship_to,
                              'province':province,
                              'city':city,
                              'district':district,
                              'street1':street1,
                              'm1':m1,
                              'm2':m2,
                              'm3':m3
            }
        data[order_id]['items'].append({'name':item_name,'num':quantity,'fee':item_fee,'price':price})
    _data = data.values()
    _data = sorted(_data,key=lambda d:d['eid'])
    return render_template('report/financial_report_by_qianshou.html',data=_data,period=period)


@report.route('/financial/qianshou/tuihuo')
@admin_required
def financial_report_by_qianshou_tuihuo():
    period = ''
    _conditions = ['`order`.status>100','`order`.express_number IS NOT NULL','`order`.order_type<100']
    _start_date = request.args.get('start_date','')
    if _start_date:
        _conditions.append('`order`.end_time>="%s"'%_start_date)

    _end_date = request.args.get('end_date','')
    if _end_date:
        _conditions.append('`order`.end_time<="%s"'%_end_date)

    if not _start_date and not _end_date:
        _today = datetime.now().strftime('%Y-%m-%d')
        _conditions.append('`order`.end_time>="%s 00:00:00"'%_today)
        period = _today
    else:
        period = '%s ~ %s'%(_start_date if _start_date else u'开始',_end_date if _end_date else u'现在')

    _s_start_date = request.args.get('s_start_date','')
    if _s_start_date:
        _conditions.append('`order`.`delivery_time`>="%s"'%_s_start_date)

    _s_end_date = request.args.get('s_end_date','')
    if _s_end_date:
        _conditions.append('`order`.`delivery_time`<="%s"'%_s_end_date)

    express_id = request.args.get('express_id',0)
    if express_id:
        _conditions.append('`order`.express_id=%s'%express_id)

    _sql = '''SELECT `operator`.nickname,`order`.delivery_time,`order`.team,`order`.end_time,`order`.order_id,`express_id`,`express_number`,`ship_to`,`province`,`city`,`district`,`street1`,`order`.item_fee-`order`.discount_fee,`order_item`.name,`order_item`.price,`order_item`.quantity,`order_item`.in_quantity,`order_item`.fee FROM `order_item`
JOIN `order` ON `order_item`.order_id=`order`.order_id AND `order`.arrival_time IS NOT NULL
JOIN `operator` ON `operator`.id=`order`.created_by
JOIN `address` ON `order`.shipping_address_id=`address`.id
WHERE %s
ORDER BY `order`.end_time'''%' AND '.join(_conditions)
    rows = db.session.execute(_sql)
    data = OrderedDict()
    for op_name,delivery_time,team,end_time,order_id,express_id,express_number,ship_to,province,city,district,street1,fee,item_name,price,quantity,in_quantity,item_fee in rows:
        if not data.has_key(order_id):
            data[order_id] = {'eid':express_id,
                              'op':op_name,
                              'team':DEPARTMENTS.get(team[0],'') if team else '',
                              'ename':EXPRESS_CONFIG[int(express_id)]['name'],
                              'enum':express_number,
                              'fee':fee,
                              'id':order_id,
                              'date':end_time.strftime("%Y-%m-%d"),
                              'delivery_time':delivery_time.strftime("%Y-%m-%d"),
                              'items':[],
                              'ship_to':ship_to,
                              'province':province,
                              'city':city,
                              'district':district,
                              'street1':street1
            }
        data[order_id]['items'].append({'name':item_name,'num':quantity,'in_num':in_quantity,'fee':item_fee,'price':price})
    _data = data.values()
    _data = sorted(_data,key=lambda d:d['eid'])
    return render_template('report/financial_report_by_qianshou_tuihuo.html',data=_data,period=period)


############################################################################################

@report.route('/logistics')
@admin_required
def logistics_report():
    return render_template('report/logistics_report.html')


@report.route('/logistics/wlfhhz')
@admin_required
def logistics_report_by_wlfhhz():
    period = ''
    _conditions = ['`order`.delivery_time IS NOT NULL']
    _start_date = request.args.get('start_date','')
    if _start_date:
        _conditions.append('`order`.delivery_time>="%s"'%_start_date)

    _end_date = request.args.get('end_date','')
    if _end_date:
        _conditions.append('`order`.delivery_time<="%s"'%_end_date)

    store_id = request.args.get('store_id','')
    if store_id:
        _conditions.append('`order`.store_id=%s'%int(store_id))

    if not _start_date and not _end_date:
        _today = datetime.now().strftime('%Y-%m-%d')
        _conditions.append('`order`.delivery_time>="%s 00:00:00"'%_today)
        period = _today
    else:
        period = '%s ~ %s'%(_start_date if _start_date else u'开始',_end_date if _end_date else u'现在')

    express_id = request.args.get('express_id',0)
    if express_id:
        _conditions.append('`order`.express_id=%s'%express_id)

    _sql = '''SELECT `order`.express_id,`order_item`.sku_id,`order_item`.name,SUM(`order_item`.quantity),SUM(`order_item`.fee) FROM
`order_item`
JOIN `order` ON order_item.order_id=`order`.order_id WHERE %s GROUP BY `order`.express_id,`order_item`.sku_id,`order_item`.name'''%' AND '.join(_conditions)
    rows = db.session.execute(_sql)
    data = []
    for express_id,sku_id,name,qty,fee in rows:
        data.append({'ename':EXPRESS_CONFIG[int(express_id)]['name'],'name':name,'qty':qty,'fee':fee})
    return render_template('report/logistics_report_by_wlfhhz.html',data=data,period=period)



@report.route('/logistics/day/delivery')
@admin_required
def logistics_report_by_day_delivery():
    period = ''
    _conditions = ['`order`.delivery_time IS NOT NULL']
    _start_date = request.args.get('start_date','')
    if _start_date:
        _conditions.append('`order`.delivery_time>="%s"'%_start_date)

    _end_date = request.args.get('end_date','')
    if _end_date:
        _conditions.append('`order`.delivery_time<="%s"'%_end_date)

    store_id = request.args.get('store_id','')
    if store_id:
        _conditions.append('`order`.store_id=%s'%int(store_id))

    if not _start_date and not _end_date:
        _today = datetime.now().strftime('%Y-%m-%d')
        _conditions.append('`order`.delivery_time>="%s 00:00:00"'%_today)
        period = _today
    else:
        period = '%s ~ %s'%(_start_date if _start_date else u'开始',_end_date if _end_date else u'现在')

    express_id = request.args.get('express_id',0)
    if express_id:
        _conditions.append('`order`.express_id=%s'%express_id)

    _sql = '''SELECT `order`.order_id,`order`.store_id,`order`.express_id,`order`.express_number,`order`.`payment_type`,`order`.item_fee-`order`.discount_fee,`order`.`delivery_time`,`order_item`.name,`order_item`.quantity,`order_item`.fee FROM
`order_item`
JOIN `order` ON order_item.order_id=`order`.order_id WHERE %s'''%' AND '.join(_conditions)
    rows = db.session.execute(_sql)
    data = OrderedDict()
    for order_id,store_id,express_id,express_number,payment_type,fee,dt,item_name,quantity,item_fee in rows:
        if not data.has_key(order_id):
            data[order_id] = {'eid':express_id,
                              'store_name':STORES[store_id],
                              'ename':EXPRESS_CONFIG[int(express_id)]['name'],
                              'enum':express_number,
                              'fee':fee,
                              'id':order_id,
                              'payment':ORDER_PAYMENTS[payment_type],
                              'date':dt.strftime("%Y-%m-%d"),
                              'items':[]}
        data[order_id]['items'].append({'name':item_name,'num':quantity,'fee':item_fee})

    _data = data.values()
    _data = sorted(_data,key=lambda d:d['eid'])
    return render_template('report/logistics_report_by_day_deliver.html',data=_data,period=period)


from utils.tools import c_dict

@report.route('/logistics/io')
@admin_required
def logistics_report_by_io():
    period = ''
    _conditions = []
    _start_date = request.args.get('start_date','')
    if _start_date:
        _conditions.append('`stock_inventory`.`date`>="%s"'%_start_date)

    _end_date = request.args.get('end_date','')
    if _end_date:
        _conditions.append('`stock_inventory`.`date`<="%s"'%_end_date)

    store_id = request.args.get('store_id','')
    if store_id:
        _conditions.append('`stock_inventory`.store_id=%s'%int(store_id))

    if not _start_date and not _end_date:
        _yestoday = (datetime.now()+timedelta(days=-1)).strftime('%Y-%m-%d')
        _conditions.append('`stock_inventory`.`date`>="%s"'%_yestoday)
        period = _yestoday
    else:
        period = '%s ~ %s'%(_start_date if _start_date else u'开始',_end_date if _end_date else u'现在')

    _sql = '''SELECT `sku_id`,`store_id`,`sku`.`name`,`ins`,`in_quantity`,`outs`,`out_quantity`,`stock_inventory`.`quantity`,`date`
     FROM `stock_inventory` JOIN `sku` ON `stock_inventory`.`sku_id`=`sku`.`id` WHERE %s ORDER BY `store_id`,`sku_id`,`date`
    '''%' AND '.join(_conditions)
    #return _sql
    rows = db.session.execute(_sql)
    data = []
    for sku_id,store_id,name,ins,in_quantity,outs,out_quantity,quantity,date in rows:
        _ins = defaultdict(int)
        _outs = defaultdict(int)
        if ins:_ins.update(eval('{%s}' % ins,c_dict))
        if outs:_outs.update(eval('{%s}' % outs,c_dict))
        data.append({'date':date,'store':STORES[store_id],'name':name,'in_quantity':in_quantity,'ins':_ins,'out_quantity':out_quantity,'outs':_outs,'quantity':quantity})
    return render_template('report/logistics_report_by_io.html',data=data,period=period)


@report.route('/logistics/loss')
@admin_required
def logistics_report_by_loss():
    period = ''
    _conditions = ['loss.status=9']

    _channel = request.args.get('channel','')
    if _channel:
        _conditions.append('`loss`.`channel`>="%s"'%_channel)

    _start_date = request.args.get('start_date','')
    if _start_date:
        _conditions.append('`loss`.`created`>="%s"'%_start_date)

    _end_date = request.args.get('end_date','')
    if _end_date:
        _conditions.append('`loss`.`created`<="%s"'%_end_date)

    if not _start_date and not _end_date:
        _today = datetime.now().strftime('%Y-%m-%d')
        _conditions.append('`loss`.`created`>="%s 00:00:00"'%_today)
        _conditions.append('`loss`.`created`<="%s 23:59:59"'%_today)
        period = _today
    else:
        period = '%s ~ %s'%(_start_date if _start_date else u'开始',_end_date if _end_date else u'现在')

    _sql = '''SELECT `sku`.id,`sku`.`name`,`loss`.degree,SUM(`loss`.quantity) FROM `loss` JOIN `sku` ON `loss`.sku_id=`sku`.id
WHERE %s
GROUP BY `sku`.id,`sku`.`name`,`loss`.degree'''%' AND '.join(_conditions)
    rows = db.session.execute(_sql)
    data = {}
    for sku_id,name,degree,quantity in rows:
        if not data.has_key(sku_id):
            data[sku_id] = {'sku_id':sku_id,'name':name,'total':0}
            for k in LOSS_DEGREES.keys():
                data[sku_id][str(k)] = 0
        data[sku_id][str(degree)] += quantity
        data[sku_id]['total'] += quantity
    return render_template('report/logistics_report_by_loss.html',data=data,period=period)

#add by john
@report.route('/financial/dzbbmx')
@admin_required
def financial_report_by_dzbbmx():
    period = ''
    _conditions = ['`order`.order_type<100']
    _start_date = request.args.get('start_date','')
    #_conditions.append('`order`.status=60')
    if _start_date:
        _conditions.append('`order_log`.`operate_time`>="%s"'%_start_date)

    _end_date = request.args.get('end_date','')
    if _end_date:
        _conditions.append('`order_log`.`operate_time`<="%s"'%_end_date)

    if not _start_date and not _end_date:
        _today = datetime.now().strftime('%Y-%m-%d')
        _conditions.append('`order_log`.`operate_time`>="%s 00:00:00"'%_today)
        _conditions.append('`order_log`.`operate_time`<="%s 23:59:59"'%_today)
        period = _today
    else:
        period = '%s ~ %s'%(_start_date if _start_date else u'开始',_end_date if _end_date else u'现在')
    
    _s_start_date = request.args.get('s_start_date','')
    if _s_start_date:
        _conditions.append('`order`.`delivery_time`>="%s"'%_s_start_date)
    
    _s_end_date = request.args.get('s_end_date','')
    if _s_end_date:
        _conditions.append('`order`.`delivery_time`<="%s"'%_s_end_date)
    
    express_id = request.args.get('express_id',0)
    if express_id:
        _conditions.append('`order`.express_id=%s'%express_id)

    _sql = '''SELECT `operator`.nickname,`order`.delivery_time,`order`.arrival_time,`order`.team,`order_log`.operate_time,`order`.order_id,`express_id`,`express_number`,`ship_to`,`province`,`city`,`district`,`street1`,`order`.item_fee-`order`.discount_fee,`order_item`.name,`order_item`.price,`order_item`.quantity,`order_item`.fee FROM `order_item`
JOIN `order` ON `order_item`.order_id=`order`.order_id
JOIN `operator` ON `operator`.id=`order`.operator_id
JOIN `address` ON `order`.shipping_address_id=`address`.id
JOIN `order_log` ON `order_log`.to_status=60 and `order_log`.order_id=`order`.order_id
WHERE %s
ORDER BY `order_log`.operate_time desc'''%' AND '.join(_conditions)
    #return _sql
    rows = db.session.execute(_sql)
    data = OrderedDict()
    for op_name,delivery_time,arrival_time,team,operate_time,order_id,express_id,express_number,ship_to,province,city,district,street1,fee,item_name,price,quantity,item_fee in rows:
        if not data.has_key(order_id):
            data[order_id] = {'eid':express_id,
                              'op':op_name,
                              'team':DEPARTMENTS.get(team[0],'') if team else '',
                              'ename':EXPRESS_CONFIG[int(express_id)]['name'],
                              'enum':express_number,
                              'fee':fee,
                              'id':order_id,
                              'date':operate_time.strftime("%Y-%m-%d"),
                              'delivery_time':delivery_time.strftime("%Y-%m-%d"),
                              'arrival_time':arrival_time,
                              'items':[],
                              'ship_to':ship_to,
                              'province':province,
                              'city':city,
                              'district':district,
                              'street1':street1
            }
        data[order_id]['items'].append({'name':item_name,'num':quantity,'fee':item_fee,'price':price})
    _data = data.values()
    _data = sorted(_data,key=lambda d:d['eid'])
    return render_template('report/financial_report_by_dzbbmx.html',data=_data,period=period)

#物流派单表统计
@report.route('/financia/paidan/tongji')
@admin_required
def financial_report_by_paidantongji():
    period = ''
    _conditions = ['`order`.order_type<100']

    if not current_user.is_admin and current_user.team:
        _conditions.append('`order`.`team` LIKE "'+current_user.team+'%"')

    _start_date = request.args.get('start_date','')
    if _start_date:
        _conditions.append('`order`.`delivery_time`>="%s"'%_start_date)

    _end_date = request.args.get('end_date','')
    if _end_date:
        _conditions.append('`order`.`delivery_time`<="%s"'%_end_date)

    express_id = request.args.get('express_id',0)
    if express_id:
        _conditions.append('`order`.express_id=%s'%express_id)

    if not _start_date and not _end_date:
        _today = datetime.now().strftime('%Y-%m-%d')
        _conditions.append('`order`.delivery_time>="%s 00:00:00"'%_today)
        period = _today        
    else:
        period = '%s ~ %s'%(_start_date if _start_date else u'开始',_end_date if _end_date else u'现在')

    _sql = '''SELECT
`order`.team,COUNT(`order`.order_id) AS `order_nums`,SUM(`order`.item_fee-`order`.discount_fee) AS `total_fee`,
 SUM(CASE WHEN `order`.item_fee<=`order`.discount_fee THEN 1 ELSE 0 END) AS `zero_order_nums`,`order`.express_id FROM `order` LEFT JOIN `operator` ON `order`.created_by = `operator`.id
WHERE %s
GROUP BY `order`.team,`order`.express_id ORDER BY `order`.express_id,`order`.team'''%' AND '.join(_conditions)
    #return _sql
    rows = db.session.execute(_sql)
    total_orders = 0
    total_fee = 0
    _rows = []
    for r in rows:
        _rows.append(r)
        total_orders += r[1]
        total_fee += r[2]
    return render_template('report/financial_report_by_paidantongji.html',rows=_rows,period=period,total_orders=total_orders,total_fee=total_fee)

#物流派单退货统计
@report.route('/financial/paidan/tuihuo/tongji')
@admin_required
def financial_report_by_paidantuihuotongji():
    _conditions = ['`order`.status>100','`order`.order_type<100']
    period = ''
    _start_date = request.args.get('start_date','')
    if _start_date:
        _conditions.append('`order`.end_time>="%s"'%_start_date)

    _end_date = request.args.get('end_date','')
    if _end_date:
        _conditions.append('`order`.end_time<="%s"'%_end_date)

    if not _start_date and not _end_date:
        _today = datetime.now().strftime('%Y-%m-%d')
        _conditions.append('`order`.end_time>="%s 00:00:00"'%_today)
        period = _today
    else:
        period = '%s ~ %s'%(_start_date if _start_date else u'开始',_end_date if _end_date else u'现在')

    _s_start_date = request.args.get('s_start_date','')
    if _s_start_date:
        _conditions.append('`order`.`delivery_time`>="%s"'%_s_start_date)

    _s_end_date = request.args.get('s_end_date','')
    if _s_end_date:
        _conditions.append('`order`.`delivery_time`<="%s"'%_s_end_date)

    express_id = request.args.get('express_id',0)
    if express_id:
        _conditions.append('`order`.express_id=%s'%express_id)

    _sql = '''SELECT
`order`.team,COUNT(`order`.order_id) AS `order_nums`,SUM(`order`.item_fee-`order`.discount_fee) AS `total_fee`,
 SUM(CASE WHEN `order`.item_fee<=`order`.discount_fee THEN 1 ELSE 0 END) AS `zero_order_nums`,`order`.express_id FROM `order` LEFT JOIN `operator` ON `order`.created_by = `operator`.id
JOIN `address` ON `order`.shipping_address_id=`address`.id
WHERE %s  AND `order`.delivery_time IS NOT NULL AND `order`.arrival_time IS NULL
GROUP BY `order`.team,`order`.express_id ORDER BY `order`.express_id,`order`.team'''%' AND '.join(_conditions)
    #return _sql
    rows = db.session.execute(_sql)
    total_orders = 0
    total_fee = 0
    _rows = []
    for r in rows:
        _rows.append(r)
        total_orders += r[1]
        total_fee += r[2]
    return render_template('report/financial_report_by_paidan_tuihuotongji.html',rows=_rows,period=period,total_orders=total_orders,total_fee=total_fee)

#物流签收表统计
@report.route('/financia/qianshou/tongji')
@admin_required
def financial_report_by_qianshoutongji():
    _conditions = ['`order`.order_type<100']
    _start_date = request.args.get('start_date','')
    if _start_date:
        _conditions.append('`order`.arrival_time>="%s"'%_start_date)

    _end_date = request.args.get('end_date','')
    if _end_date:
        _conditions.append('`order`.arrival_time<="%s"'%_end_date)

    if not _start_date and not _end_date:
        _today = datetime.now().strftime('%Y-%m-%d')
        _conditions.append('`order`.arrival_time>="%s 00:00:00"'%_today)
        period = _today
    else:
        period = '%s ~ %s'%(_start_date if _start_date else u'开始',_end_date if _end_date else u'现在')

    _s_start_date = request.args.get('s_start_date','')
    if _s_start_date:
        _conditions.append('`order`.`delivery_time`>="%s"'%_s_start_date)

    _s_end_date = request.args.get('s_end_date','')
    if _s_end_date:
        _conditions.append('`order`.`delivery_time`<="%s"'%_s_end_date)

    express_id = request.args.get('express_id',0)
    if express_id:
        _conditions.append('`order`.express_id=%s'%express_id)
    

    _sql = '''SELECT
`order`.team,COUNT(`order`.order_id) AS `order_nums`,SUM(`order`.item_fee-`order`.discount_fee) AS `total_fee`,
 SUM(CASE WHEN `order`.item_fee<=`order`.discount_fee THEN 1 ELSE 0 END) AS `zero_order_nums`,`order`.express_id FROM `order` LEFT JOIN `operator` ON `order`.created_by = `operator`.id
JOIN `address` ON `order`.shipping_address_id=`address`.id
WHERE %s AND `order`.arrival_time IS NOT NULL
GROUP BY `order`.team,`order`.express_id ORDER BY `order`.express_id,`order`.team'''%' AND '.join(_conditions)
    #return _sql    
    rows = db.session.execute(_sql)
    total_orders = 0
    total_fee = 0
    _rows = []
    for r in rows:
        _rows.append(r)
        total_orders += r[1]
        total_fee += r[2]
    return render_template('report/financial_report_by_qianshoutongji.html',rows=_rows,period=period,total_orders=total_orders,total_fee=total_fee)

#会员客户数量统计
@report.route('/sale/user_total')
@admin_required
def sale_report_by_user_total():
    _conditions = []
    _start_date = request.args.get('start_date','')
    if _start_date:
        _conditions.append('`user_statistics`.tjdate>="%s"'%_start_date)

    _end_date = request.args.get('end_date','')
    if _end_date:
        _conditions.append('`user_statistics`.tjdate<="%s"'%_end_date)

    if not _start_date and not _end_date:
        _today = datetime.now().strftime('%Y-%m-%d')
        _conditions.append('`user_statistics`.tjdate>="%s"'%_today)
        period = _today
    else:
        period = '%s ~ %s'%(_start_date if _start_date else u'开始',_end_date if _end_date else u'现在')


    _sql = '''SELECT * FROM user_statistics
 WHERE %s order by tjdate desc'''%' AND '.join(_conditions)
        
    
    #return _sql    
    rows = db.session.execute(_sql)
    total_new_users = 0
    total_giveup_users = 0
    _rows = []
    for r in rows:
        _rows.append(r)
        total_new_users += r[1]
        total_giveup_users += r[2]
    return render_template('report/sale_report_by_user_total.html',rows=_rows,period=period,total_new_users=total_new_users,total_giveup_users=total_giveup_users)


#外呼统计
@report.route('/outbound/tongji')
@admin_required
def jiexian_tongji():
    _conditions = []
    _start_date = request.args.get('start_date','')
    if _start_date:
        _conditions.append('`outbound`.created>="%s"'%_start_date)

    _end_date = request.args.get('end_date','')
    if _end_date:
        _conditions.append('`outbound`.created<="%s"'%_end_date)

    if not _start_date and not _end_date:
        _today = datetime.now().strftime('%Y-%m-%d')
        _conditions.append('`outbound`.created>="%s 00:00:00"'%_today)
        period = _today
    else:
        period = '%s ~ %s'%(_start_date if _start_date else u'开始',_end_date if _end_date else u'现在')


    _sql1 = '''SELECT COUNT(distinct outbound.user_id) user_ids FROM `outbound` 
join `user` on `user`.user_id = `outbound`.user_id
 WHERE %s'''%' AND '.join(_conditions)
    
    _sql2 = '''SELECT COUNT(distinct user_id) from `order` where user_id in (SELECT `outbound`.user_id FROM `outbound` 
         WHERE date(`order`.created)=date(`outbound`.created) and %s)'''%' AND '.join(_conditions)
    
    _sql3 = '''SELECT COUNT(distinct user_id) from `order` where user_id in (SELECT `outbound`.user_id FROM `outbound` 
         WHERE date(`order`.created)>date(`outbound`.created) and %s)'''%' AND '.join(_conditions)
    
    _sql4 = '''SELECT COUNT(distinct outbound.user_id) user_ids FROM `outbound` 
join `user` on `user`.user_id = `outbound`.user_id
         WHERE  `user`.order_num=0 and %s'''%' AND '.join(_conditions)
    
    _sql5 = '''SELECT group_concat(distinct user_id) from `order` where user_id in (SELECT `outbound`.user_id FROM `outbound` 
join `user` on `user`.user_id = `outbound`.user_id
         WHERE date(`order`.created)=date(`outbound`.created) and %s)'''%' AND '.join(_conditions)
        
    
    _sql6 = '''SELECT group_concat(distinct outbound.user_id) user_ids FROM `outbound` 
    join `user` on `user`.user_id = `outbound`.user_id
     WHERE %s'''%' AND '.join(_conditions)
    

    
    _sql = _sql1+' union all '+_sql2+' union all '+_sql3+' union all '+_sql4#+' union all '+_sql6
    #return _sql4
    rows = db.session.execute(_sql)
    return render_template('report/user_report_by_outbound.html',rows=rows,period=period)
#心力健统计
@report.route('/xlj/tongji')
@admin_required
def xlj_tongji():
    _conditions = ["`user`.origin=11"]
    _start_date = request.args.get('start_date','')
    if _start_date:
        _conditions.append('`user`.join_time>="%s"'%_start_date)

    _end_date = request.args.get('end_date','')
    if _end_date:
        _conditions.append('`user`.join_time<="%s"'%_end_date)

    if not _start_date and not _end_date:
        _today = datetime.now().strftime('%Y-%m-%d')
        _conditions.append('`user`.join_time>="%s 00:00:00"'%_today)
        period = _today
    else:
        period = '%s ~ %s'%(_start_date if _start_date else u'开始',_end_date if _end_date else u'现在')


    _sql1 = '''SELECT COUNT(distinct user.user_id) user_ids FROM `user`
 WHERE %s'''%' AND '.join(_conditions)
    
    _sql2 = '''SELECT COUNT(distinct user.user_id) from `user` join `order` on user.user_id=`order`.user_id 
         WHERE user.user_id in (select a.user_id from (select count(*) as cc,user_id from `order` where is_xlj=1 and `order`.status>1 group by user_id) a where a.cc=1) AND %s'''%' AND '.join(_conditions)
    
    
    _sql3 = '''SELECT COUNT(distinct user.user_id) from `user` join `order` on user.user_id=`order`.user_id 
         WHERE user.user_id in (select a.user_id from (select count(*) as cc,user_id from `order` where is_xlj=1 and `order`.status>1 group by user_id) a where a.cc=2) AND %s'''%' AND '.join(_conditions)
    
    _sql4 = '''SELECT COUNT(distinct user.user_id) from `user` join `order` on user.user_id=`order`.user_id 
         WHERE user.user_id in (select a.user_id from (select count(*) as cc,user_id from `order` where is_xlj=1 and `order`.status>1 group by user_id) a where a.cc=3) AND %s'''%' AND '.join(_conditions)
    
    
    _sql5 = '''SELECT COUNT(distinct user.user_id) from `user` join `order` on user.user_id=`order`.user_id 
         WHERE user.user_id in (select a.user_id from (select count(*) as cc,user_id from `order` where is_xlj=1 and `order`.status>1 group by user_id) a where a.cc>3) AND %s'''%' AND '.join(_conditions)
    
    _sql6 = '''SELECT COUNT(distinct user.user_id) from `user` 
         WHERE user.user_id not in (select user_id from `order` where is_xlj=1 and `order`.status>1 ) AND %s'''%' AND '.join(_conditions)
    
    
    
    
    _sql = _sql1+' union all '+_sql2+' union all '+_sql3+' union all '+_sql4+' union all '+_sql5+' union all '+_sql6
    #return _sql2
    rows = db.session.execute(_sql)
    return render_template('report/user_report_by_xlj.html',rows=rows,period=period)
#心力健统计2
@report.route('/xlj/tongji2')
@admin_required
def xlj_tongji2():
    _conditions = ["`user`.origin=11"]
    _xljmedia = request.args.get('xljmedia','')
    if _xljmedia:
        _xljmedia = int(_xljmedia)
        _conditions.append('`user`.m1="%s"'%XLJ_MEDIA[_xljmedia])

    _start_date = request.args.get('start_date','')
    if _start_date:
        _conditions.append('`user`.join_time>="%s"'%_start_date)

    _end_date = request.args.get('end_date','')
    if _end_date:
        _conditions.append('`user`.join_time<="%s"'%_end_date)

    if not _start_date and not _end_date:
        _today = datetime.now().strftime('%Y-%m-%d')
        _conditions.append('`user`.join_time>="%s 00:00:00"'%_today)
        period = _today
    else:
        period = '%s ~ %s'%(_start_date if _start_date else u'开始',_end_date if _end_date else u'现在')


    _sql1 = '''SELECT COUNT(distinct user.user_id) user_ids FROM `user`
 WHERE %s'''%' AND '.join(_conditions)
    #return _sql1
    _sql2 = '''SELECT COUNT(distinct user.user_id) from `user` join `order` on user.user_id=`order`.user_id 
         WHERE `order`.order_type=15 AND %s'''%' AND '.join(_conditions)
    #return _sql2
    
    _sql3 = '''SELECT COUNT(distinct `order`.order_id) from `order` join `user` on user.user_id=`order`.user_id 
         WHERE `order`.order_type=14 AND %s'''%' AND '.join(_conditions)
    
    _sql4 = '''SELECT sum(`order`.item_fee-`order`.discount_fee) from `user` join `order` on user.user_id=`order`.user_id 
         WHERE `order`.order_type=15 AND %s'''%' AND '.join(_conditions)
    
    
    _sql5 = '''SELECT round(avg(`order`.item_fee-`order`.discount_fee),2) from `order` join `user` on user.user_id=`order`.user_id 
         WHERE `order`.order_type=15 AND %s'''%' AND '.join(_conditions)
    #return _sql5
    _sql6 = '''SELECT COUNT(distinct user.user_id) from `user` join `order` on user.user_id=`order`.user_id 
         WHERE `order`.order_type=14 AND `order`.status=108 AND %s'''%' AND '.join(_conditions)
    
    _sql7 = '''SELECT COUNT(distinct user.user_id) from `user` join `order` on user.user_id=`order`.user_id 
         WHERE `order`.order_type=16 AND %s'''%' AND '.join(_conditions)
    
    _sql8 = '''SELECT COUNT(distinct `order`.order_id) from `user` join `order` on user.user_id=`order`.user_id 
         WHERE `order`.order_type=16 AND %s'''%' AND '.join(_conditions)
    
    _sql9 = '''SELECT sum(`order`.item_fee-`order`.discount_fee) from `user` join `order` on user.user_id=`order`.user_id 
         WHERE `order`.order_type=16 AND %s'''%' AND '.join(_conditions)
    
    _sql10 = '''SELECT round(avg(`order`.item_fee-`order`.discount_fee),2) from `order` join `user` on user.user_id=`order`.user_id 
         WHERE `order`.order_type=16 AND %s'''%' AND '.join(_conditions)

    
    
    
    
    
    
    
    _sql = _sql1+' union all '+_sql2+' union all '+_sql3+' union all '+_sql4+' union all '+_sql5+' union all '+_sql6+' union all '+_sql7+' union all '+_sql8+' union all '+_sql9+' union all '+_sql10
    #return _sql
    rows = db.session.execute(_sql)
    return render_template('report/user_report_by_xljbb.html',rows=rows,period=period)
