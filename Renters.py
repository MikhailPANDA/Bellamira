# coding: utf8

from Common import *

from datetime import *

import time


class Renter:
    form = web.form.Form(
        web.form.Textbox('name', description='Название группы'), web.form.Dropdown('drop', [], description='Руководитель'),
        web.form.Checkbox('other', description='Новый?'), web.form.Textbox('FIO', description='ФИО нового руководителя'),
        web.form.Textbox('phone', description='Телефон'), web.form.Textbox('link', description='Ссылка в соц. сетях')
    )

    form2 = web.form.Form(web.form.Textbox('date', description='Дата'),
                          web.form.Textbox('sum', description='Сумма'))

    form3 = web.form.Form(web.form.Textbox('name', description='Название'),
                          web.form.Dropdown('drop2', [], description='Зал'),
                          web.form.Dropdown('drop', [], description='Группа'),
                          web.form.Textbox('start_time', pattern="\\d{1,2}\/\\d{1,2}\/\\d{4}\\s\\d{1,2}:\\d{1,2}",
                                           size="16", maxlength="16", id="st_t", description='Время начала'),
                          web.form.Textbox('end_time', pattern="\\d{1,2}\/\\d{1,2}\/\\d{4}\\s\\d{1,2}:\\d{1,2}",
                                           size="16", maxlength="16", id="end_t", description='Время окончания'))

    form4 = web.form.Form(web.form.Dropdown('drop', [], description='Зал'), web.form.Dropdown('drop2', [], description='День недели'),
                          web.form.Textbox('startTime', description='Время начала', pattern="\\d{1,2}:\\d{1,2}",
                                           size="5", maxlength="5"),
                          web.form.Textbox('endTime', description='Время окончания', pattern="\\d{1,2}:\\d{1,2}",
                                           size="5", maxlength="5"),
                          web.form.Textbox('cost', description='Стоимость часа'))

    def GET(self, renter_id):
        groups = db.select("renters_group", where='renter_id = $renter_id', vars=locals())
        people = db.query('Select * from people where id in (select people_id from group_people where renter_id = '
                          + str(renter_id) + ')');
        renter = db.select("renters", where="id=$renter_id", vars=locals())[0]
        renter_man = db.select("people", where="id = $renter.people_id", vars=locals())[0]
        pays = db.select("pays", where='renter_id = $renter_id', vars=locals())
        rate = db.select('rate_renter', where='renter_id=$renter_id', vars=locals())
        events_groups = db.query(
            'SELECT using_hall.[name], using_hall.[hall_id], using_hall.[group_id], using_hall.[start_time], using_hall.[end_time], renters_group.[renter_id] AS renter, renters_group.[name] AS group_name, hall.[name] AS hall_name FROM renters_group INNER JOIN using_hall ON renters_group.[id] = using_hall.[group_id] INNER JOIN hall ON using_hall.[hall_id] = hall.[id]')
        cost_table = db.query(
            'SELECT using_hall.[hall_id], using_hall.[group_id], using_hall.[start_time], using_hall.[end_time], renters_group.[renter_id] AS RENTER, rate_renter.[days_of_week] AS DAYS_IND_RATE, rate_renter.[start_time] AS ST_T_IND_RATE, rate_renter.[end_time] AS EN_T_IND_RATE, rate_renter.[cost] AS IND_COST, time_zone.[days_of_week] AS DAYS_ST_RATE, time_zone.[start_time] AS ST_T_ST_RATE, time_zone.[end_time] AS EN_T_ST_RATE, time_zone.[cost] AS STAND_COST FROM using_hall INNER JOIN renters_group ON using_hall.[group_id] = renters_group.[id] INNER JOIN rate_renter ON renters_group.[renter_id] = rate_renter.[renter_id] INNER JOIN time_zone ON using_hall.[hall_id] = time_zone.[hall_id]')
        days = db.select('days_of_week', vars=locals())

        form = self.form()
        form.drop.args = getdropValues()
        form2 = self.form2()
        form3 = self.form3()
        templ = getdropValues3()
        form3.drop2.args = getdropValues3()
        form3.drop.args = getdropValues2()
        form4 = self.form4()
        temp = getdropValues3()
        form4.drop.args = temp
        form4.drop2.args = getdropValues4()

        uppd_ev_groups = []
        for e in events_groups:
            e['start_time'] = datetime.fromtimestamp(e['start_time']).strftime("%d/%m/%Y (%a) %H:%M")
            e['end_time'] = datetime.fromtimestamp(e['end_time']).strftime("%d/%m/%Y (%a) %H:%M")
            print "HEEEEEEEEEEEEEEEEEERRRRRRREEEEEEEEEEEEEE   сравнение.", type(e['renter']), e['renter'], "|", type(renter_id), renter_id
            if e['renter'] == int(renter_id):
                uppd_ev_groups.append(e)
                print "HEEEEEERRRREEEEE ИТератор в добавил v uppd!!"
        print "HERREEE ИТератор прошел цикл|", uppd_ev_groups


        updated_rate = []

        for r in rate:
            hours = r['start_time'] / 3600
            minutes = r['start_time'] % 3600 / 60
            r['start_time'] = "%02d:%02d" % (hours, minutes)
            hours = r['end_time'] / 3600
            minutes = r['end_time'] % 3600 / 60
            r['end_time'] = "%02d:%02d" % (hours, minutes)
            if days != None:
                for d in days:
                    print "HHHEEEERRRRRREEEEEEEE   |", type(r['days_of_week']), r['days_of_week'], "|||",type(d['no']), d['no']
                    if int(r['days_of_week']) == d['no']:
                        r['days_of_week'] = d['name']


            for t in temp:
                if t[0] == r['hall_id']:
                    r['hall_id'] = t[1]
                    updated_rate.append(r)
        updeted_pays = []
        print "HEEEEEEEEEEEEEEEEEERRRRRRREEEEEEEEEEEEEEEEEE ИТератор перед pays|"
        for p in pays:
            p['date'] = datetime.fromtimestamp(p['date']).strftime("%d/%m/%Y (%a) %H:%M")
            updeted_pays.append(p)

        if cost_table and rate != None:
            a = ""
            for c in cost_table:
                c['start_time'] = datetime.fromtimestamp(c['start_time'])
                c['end_time'] = datetime.fromtimestamp(c['end_time'])
                for r in rate:
                    if c['hall_id'] == r['hall_id']:
                        if c['start_time'].weekday() == r['days_of_week']:
                            if not c['start_time'] and c['end_time'] > r['start_time'] and r['end_time'] or c['start_time'] and c['end_time'] < r['start_time'] and r['end_time']:
                                a = "есть пересечение"
                                if not r['start_time'] > c['start_time'] and c['end_time'] < r['end_time'] or r['start_time'] < c['start_time'] and c['end_time'] > r['end_time']:# если не соблюдается - сложить все часы этого тарифа и умножить на cost, если соблюдается - искать пересекающиеся и считать
                                    print "HERE !!! |", a, "|искать часы"
                                print "here  !весь охват тарифа!|", a
        print "HEEEEEEEEEEEEEEEEEERRRRRRREEEEEEEEEEEEEEEEEE ИТератор перед return|"
        return render.renter(renter, renter_man, groups, people, updated_rate, updeted_pays, uppd_ev_groups, form, form2, form3, form4)

    def POST(self, renter_id):
        print "ИТЕРАТОР В КЛАССЕ РЕНТЕР _ ПОСТ"
        form = self.form()
        form2 = self.form2()
        form3 = self.form3()
        form4 = self.form4()
        if not form.validates():
            raise web.seeother('/renter/' + str(renter_id) + "/", True)
        if not form2.validates():
            raise web.seeother('/renter/' + str(renter_id) + "/", True)
        if not form3.validates():
            raise web.seeother('/renter/' + str(renter_id) + "/", True)
        if not form4.validates():
            raise web.seeother('/renter/' + str(renter_id) + "/", True)

        people_id = form.d.drop
        if people_id != "-1" or form.d.FIO != "":
            if form.d.name != None:

                print "HEEEEEEEEEEEEEEEEEERRRRRRREEEEEEEEEEEEEEEEEEEEEEEEEEE FORM1111111 !!!!!!!!!"

                people_id = getNextId('people')
                element = {"FIO": form.d.FIO,
                           "phone": form.d.phone,
                           "link": form.d.link,
                           "id": people_id}
                db.multiple_insert('people', values=[element])
                ids = getNextId('renters_group')
                element = {"name": form.d.name,
                           "people_id": people_id,
                           "renter_id": renter_id,
                           "id": ids}
                print "            HERE 1                HERE  73           HERE           73    ", element
                db.multiple_insert("renters_group", values=[element])
                print "                here 2         here 75               here          75|", renter_id, "|", ids, "|", people_id
                db.insert('group_people', renter_id=renter_id, group_id=ids, people_id=people_id)

        if form2.d.sum != None:
            print "HEEEEEEEEEEEEEEEEEERRRRRRREEEEEEEEEEEEEEEEEEEEEEEEEEE FORM2222222 !!!!!!!!!"
            dt_pays = datetime.now()
            print "HERE    HERE HERE |", dt_pays
            dt_p = time.mktime(dt_pays.timetuple())
            print "HERE    HERE HERE |", dt_p
            element = {"id": getNextId("pays"),
                       "date": form2.d.date,
                       "renter_id": renter_id,
                       "sum": form2.d.sum}
            db.multiple_insert('pays', values=[element])
            raise web.seeother('/renter/' + str(renter_id) + "/", True)

        if form3.d.startTime and form3.d.endTime != None:
            if form3.d.drop != "-1":
                start_dt_string2 = datetime.strptime(form3.d.start_time, "%d/%m/%Y %H:%M")
                start_dt_unix2 = time.mktime(start_dt_string2.timetuple())
                end_dt_string2 = datetime.strptime(form3.d.end_time, "%d/%m/%Y %H:%M")
                end_dt_unix2 = time.mktime(end_dt_string2.timetuple())
                element2 = {"id": getNextId("using_hall"),
                            "name": form3.d.name,
                            "group_id": form3.d.drop,
                            # "hall_id": hall_id,!!!!!!
                            "start_time": start_dt_unix2,
                            "end_time": end_dt_unix2}
                db.multiple_insert('using_hall', values=[element2])

        if form4.d.drop != "-1" and renter_id != "-1" and form4.d.cost != None and form4.d.drop2 != "-1" :
            print "HEEEEEEEEEEEEEEEEEERRRRRRREEEEEEEEEEEEEEEEEEEEEEEEEEE FORM444444444 !!!!!!!!!"
            HALL_ID = form4.d.drop
            rate_id = getNextId('rate_renter')

            stT = form4.d.startTime
            enT = form4.d.endTime
            stSec = int(stT[0:2]) * 3600 + int(stT[3:5]) * 60
            enSec = int(enT[0:2]) * 3600 + int(enT[3:5]) * 60
            element2 = {"hall_id": HALL_ID,
                        "renter_id": renter_id,
                        "days_of_week": form4.d.drop2,
                        "start_time": stSec,
                        "end_time": enSec,
                        "cost": form4.d.cost,
                        "id": rate_id
                        }
            db.multiple_insert('rate_renter', values=[element2])
        raise web.seeother('/renter/' + str(renter_id) + "/", True)

class Renters:

    form = web.form.Form(
        web.form.Textbox('name', description='Название организации'), web.form.Textbox('renter_link', description='Ссылка'),
        web.form.Textbox('renter_phone', description='Телефон'), web.form.Dropdown('drop', [(-1, "Add")], description='Выберите руководителя'),
        web.form.Checkbox('other', description='Новый руководитель'), web.form.Textbox('FIO', description='ФИО руководителя'),
        web.form.Textbox('phone', description='Телефон'), web.form.Textbox('link', description='Ссылка в соц. сетях')
    )

    def GET(self):
        based = db.select("renters", order='id')
        form = self.form()
        form.drop.args = getdropValues();
        return render.renters(form, based, db)

    def POST(self):
        form = self.form()
        if not form.validates():
            raise web.seeother('/renters/', True)
        if form.d.FIO == "" and form.d.name=="":
            raise web.seeother('/renters/', True)
        people_id = form.d.drop
        if people_id == "-1" and form.d.FIO != "":
            people_id = getNextId('people')
            element = {"FIO": form.d.FIO,
                   "phone": form.d.phone,
                   "link": form.d.link,
                   "id": people_id}
            db.multiple_insert('people', values=[element])
        ids = getNextId('renters')
        element = {"name": form.d.name,
                   "phone": form.d.renter_phone,
                   "link": form.d.renter_link,
                   "people_id": people_id,
                   "id": ids}
        db.multiple_insert("renters", values=[element])
        db.insert('group_people', renter_id=ids, people_id=people_id)
        raise web.seeother('/renters/', True)


class DelRenter:

    def GET(self, renter_id):
        print "                   HEREEEEEEEEEEEEEE          |",  renter_id
        db.delete('renters', where='id=$renter_id', vars=locals())
        raise web.seeother('/renters/', True)
