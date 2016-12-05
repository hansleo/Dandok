import SQL_util

name_cur = SQL_util.select('politician_code, name', 'politician')
politicians = [[code, name] for code, name in name_cur.fetchall()]

for politician in politicians:
				name = politician[1]
				code = politician[0]
				cnt = SQL_util.select('count(*)', 'articles', " (part = 1 or part = 2 or part = 3 ) and (summary like '%" + name + "%' or title like '%" + name + "%' )").fetchone()[0]
				SQL_util.update_count('cnt = '+str(cnt), 'politician', ' politician_code = '+str(code))
