
import SQL_util

name_cur = SQL_util.select('politician_code, name', 'politician')
politicians = [[code, name] for code, name in name_cur.fetchall()]

name_cur = SQL_util.select('politician_code, sum(cnt)', 'politician_part', 'politician_code > 0 group by politician_code')
cnts = [[code, cnt] for code, cnt in name_cur.fetchall()]

org_cur = SQL_util.select('org_code, sum(cnt)', 'org_part', 'org_code >= 0 group by org_code')
orgs = [[code, cnts] for code, cnts in org_cur.fetchall()]

# press_cur = SQL_util.select(' distinct press', 'articles')
# press_list = [press_item[0] for press_item in press_cur.fetchall()]
#
#
# for code, name in politicians:
#
#     for part in range(1, 4):
#         option = ' part = ' + str(part) + " and title like '%" + name + "%' "
#         stat = SQL_util.select('count(*)', 'articles', option).fetchone()[0]
#         if stat > 0 :
#             table = ' politician_part '
#             insert_data = str(part) + ', ' + str(code) + ', ' + str(stat)
#             if SQL_util.insert(insert_data, table) == False:
#                 setting = 'cnt = ' + str(stat)
#                 option = 'part = ' + str(part) + ' and politician_code = ' + str(code)
#                 SQL_util.update(setting, 'politician_part', option)


# for code, cnt in cnts:
#     if cnt > 0:
#
#         setting = 'total_count = ' + str(cnt)
#         option = 'politician_code =' + str(code)
#         SQL_util.update(setting, 'politician', option)

# for code, org in orgs:
#     for part in range(1, 10):
#         option = ' part = ' + str(part) + " and title like '%" + org + "%' "
#         stat = SQL_util.select('count(*)', 'articles', option).fetchone()[0]
#         if stat > 0:
#             t

# for code, org in orgs:
#     for part in range(1, 10):
#         option = ' part = ' + str(part) + " and title like '%" + org + "%' "
#         stat = SQL_util.select('count(*)', 'articles', option).fetchone()[0]
#         if stat > 0:
#             setting = 'cnt = ' + str(stat)
#             option = 'org_code = ' + str(code) + " and part = " + str(part)
#             SQL_util.update(setting, 'org_part', option)

for code, cnts in orgs:
    if cnts > 0:
        setting = 'total_count = ' + str(cnts)
        option = 'org_code = '+str(code)
        SQL_util.update(setting, 'org', option)