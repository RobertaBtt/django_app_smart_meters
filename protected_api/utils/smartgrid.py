"""
Accesso alle stored procedures sul db della smartgrid
"""

import datetime
import etl_queries
import psycopg2
import psycopg2.extras

class Smartgrid(object):

    def __init__(self, remote_database_name = ''):
        # PSQL CONN PARAMETERS
        DB_HOST = 'HOST.rds.amazonaws.com'
        DB_USER = 'USER'
        DB_PASS = 'PWD'
        DB_NAME = 'smartgrid'
        DB_CONN_TIMEOUT = 20
        dns = "dbname={db} user={user} host={host} password={pswd} connect_timeout={to}"
        CONN_STRING = dns.format(db=DB_NAME, user=DB_USER, host=DB_HOST, pswd=DB_PASS, to=DB_CONN_TIMEOUT)
        self.connected = False
        try:
            self.CONN = psycopg2.connect(CONN_STRING)
            self.connected = True
        except Exception as e:
            message = "smartgrid connection error: %s" % str(e)
            raise Exception(message)

        if remote_database_name:
            self.remote_db_name = remote_database_name
        else:
            self.remote_db_name = 'test'

    def getStats(self, zone_id):
        """
        returns statistical info about the grid for the given zone
        :param zone_id: id of the zone
        :type zone_id: str
        :return: a dictionary containing the data
        :rtype: dict
        """
        if not self.connected:
            return None

        with self.CONN.cursor(cursor_factory=psycopg2.extras.DictCursor) as cur:
            query = etl_queries.Q_GRID_STATS.format(zone_id=zone_id, remote_db_name=self.remote_db_name)
            cur.execute(query)
            for res in cur:
                data = {
                        'timestamp': (datetime.datetime.now()).isoformat(),
                        'meters_no':res['meters_no'],
                        'pot_attiva_immessa':res['pot_attiva_immessa'],
                        'pot_attiva_prelevata': res['pot_attiva_prelevata'],
                        'pot_immessa_max': res['pot_immessa_max'],
                        'pot_prelevata_max': res['pot_prelevata_max'],
                        'meter_no_online': res['meter_no_online'],
                        'meter_no_offline': res['meter_no_offline'],
                        'allarmi_no': res['allarmi_no'],
                }
                return data

    def getAlarms(self, zone_id):
        """
        returns  info about the grid alarms for the given zone
        :param zone_id: id of the zone
        :type zone_id: str
        :return: a dictionary containing the data
        :rtype: dict
        """
        if not self.connected:
            return None

        with self.CONN.cursor(cursor_factory=psycopg2.extras.DictCursor) as cur:
            query = etl_queries.Q_GRID_ALARMS.format(zone_id=zone_id, remote_db_name=self.remote_db_name)
            print "Query: Q_GRID_ALARMS:", query

            cur.execute(query)
            for res in cur:
                print "res:", res
                data = {
                        'timestamp': (datetime.datetime.now()).isoformat(),
                        'sm_id':res['sm_id'],
                        'offline':res['offline'],
                        'manumission': res['manumission'],
                        'excess_power': res['excess_power'],
                }
                return data

    def getUser(self, user_id):
        """
        returns info anagraphic data about the give user
        :param user_id: id of the user
        :type user_id: str
        :return: a dictionary containing the data
        :rtype: dict
        """
        if not self.connected:
            raise Exception('smartgrid not connected')

        with self.CONN.cursor(cursor_factory=psycopg2.extras.DictCursor) as cur:
            query = etl_queries.Q_USER.format(user_id=user_id, remote_db_name=self.remote_db_name)
            cur.execute(query)
            res = cur.fetchone()
            if res is None:
                return None
            else:
                return {'name': res['name'], 'address': res['address'], 'is_private': res['private'], 'contracts': res['contracts'].split(','),}


    def getContracts(self, user_id):
        if not self.connected:
            raise Exception('smartgrid not connected')

        contracts_info = self.getContractsInfo(user_id)
        try:
            smartmeters_info = self.getSmartmetersInfo(user_id)
            sm_dict = {}
            for sm in smartmeters_info:
                sm_dict[sm['contract_id']] = sm

            for contract in contracts_info:
                contract['has_sm'] = sm_dict[contract['contract_id']]['has_sm']
                contract['types'] = sm_dict[contract['contract_id']]['types']
            return contracts_info

        except Exception as e:
            for contract in contracts_info:
                contract['has_sm'] = False
                contract['types'] = ''
            return contracts_info


    def getContractsInfo(self, user_id):
        if not self.connected:
            raise Exception('smartgrid not connected')

        with self.CONN.cursor(cursor_factory=psycopg2.extras.DictCursor) as cur:
            if 'partner' in self.remote_db_name or 'company' in self.remote_db_name:
                query = etl_queries.Q_PODS_SP.format(user_id=user_id, remote_db_name=self.remote_db_name)
            else:
                query = etl_queries.Q_PODS.format(user_id=user_id, remote_db_name=self.remote_db_name)
            cur.execute(query)
            return [dict(res) for res in cur]

    def getSmartmetersInfo(self, user_id):
        if not self.connected:
            raise Exception('smartgrid not connected')

        with self.CONN.cursor(cursor_factory=psycopg2.extras.DictCursor) as cur:
            query = etl_queries.Q_SMARTMETERS.format(user_id=user_id, remote_db_name=self.remote_db_name)
            cur.execute(query)
            return [dict(res) for res in cur]


    def getUserId(self, fiscal_sn, verification_code):
        if not self.connected:
            raise Exception('smartgrid not connected')

        with self.CONN.cursor(cursor_factory=psycopg2.extras.DictCursor) as cur:
            query = etl_queries.Q_REGISTER.format(fiscal_sn=fiscal_sn, verification_code=verification_code, remote_db_name=self.remote_db_name)
            cur.execute(query)
            for res in cur:
                return res['id']
            else:
                return None

    def getMeasures(self, contract_id):
        if not self.connected:
            raise Exception('smartgrid not connected')

        with self.CONN.cursor(cursor_factory=psycopg2.extras.DictCursor) as cur:
            query = etl_queries.Q_MEASURES.format(contract_id=contract_id, num_hours=48, remote_db_name=self.remote_db_name)
            cur.execute(query)
            data = []
            for res in cur:
                data.append({'n':res[0], 'h': res[1], 'p': res[2]})
        return data

    def getAlarmSmartmeter(self, contract_id):
        if not self.connected:
            raise Exception('smartgrid not connected')

        with self.CONN.cursor(cursor_factory=psycopg2.extras.DictCursor) as cur:
            query = etl_queries.Q_ALARMS_CONTRACT.format(contract_id=contract_id,  remote_db_name=self.remote_db_name)
            cur.execute(query)
            for res in cur:
                data = {
                        'timestamp': (datetime.datetime.now()).isoformat(),
                        'sm_id':res['sm_id'],
                        'offline':res['offline'],
                        'manumission': res['manumission'],
                        'excess_power': res['excess_power'],
                }
                return data


    def getMessages(self, user_id):
        if not self.connected:
            raise Exception('smartgrid not connected')

        with self.CONN.cursor(cursor_factory=psycopg2.extras.DictCursor) as cur:
            query = etl_queries.Q_MESSAGES.format(user_id=user_id, remote_db_name=self.remote_db_name)
            cur.execute(query)
            data = []
            for res in cur:
                data.append(
                    {'id': res[0], 'body': res[1], 'title':res[2], 'time':res[3],}
                )
            return data

    def getPotenze(self, contract_id):
        if not self.connected:
            raise Exception('smartgrid not connected')

        with self.CONN.cursor(cursor_factory=psycopg2.extras.DictCursor) as cur:
            query = etl_queries.Q_POWERS.format(contract_id=contract_id, remote_db_name=self.remote_db_name)
            cur.execute(query)
            res = cur.fetchone()
        if res is None:
            return None
        else:
            return {'pa': res['pa'], 'pp': res['pp'], 'pr': res['pr'],'pau': res['pau']}

    def getData(self, nome_campo_select, nome_tabella, nome_campo_where, valore_campo_where):

        if not self.connected:
            raise Exception('smartgrid not connected')
        print nome_campo_select + " " + nome_tabella + " " + nome_campo_where + " "  + valore_campo_where

        with self.CONN.cursor(cursor_factory=psycopg2.extras.DictCursor) as cur:

            query = etl_queries.query_get_data.format(
                nome_campo_select=nome_campo_select,
                nome_tabella=nome_tabella,
                nome_campo_where = nome_campo_where,
                valore_campo_where = valore_campo_where)

            cur.execute(query)
            res = cur.fetchone()
        if res is None:
            return None
        else:

            return { 'valore' : res[0],
                    'measurement_ts': res[1]}

    def scanSmartmeters(self, nome_tabella):
        if not self.connected:
            raise Exception('smartgrid not connected')

        with self.CONN.cursor(cursor_factory=psycopg2.extras.DictCursor) as cur:
            if nome_tabella == 'sg_21':
                query = etl_queries.query_scan_smartmeters_mono_fase.format()
            elif nome_tabella == 'sg_18':
                query = etl_queries.query_scan_smartmeters_tri_fase.format()

            cur.execute(query)
            return cur.fetchall()

    def getSmartmeterData(self, sender_id, nome_tabella, data_da, data_a):

        if not self.connected:
            raise Exception('smartgrid not connected')


        with self.CONN.cursor(cursor_factory=psycopg2.extras.DictCursor) as cur:

            if nome_tabella == 'sg_21':
                query = etl_queries.query_get_smartmeter_data_mono.format(
                    data_da = data_da,
                    data_a = data_a,
                    sender_id = sender_id)

            elif nome_tabella == 'sg_18':
                query = etl_queries.query_get_smartmeter_data_tri.format(
                    data_da=data_da,
                    data_a = data_a,
                    sender_id = sender_id)

            print "Ecco la query di getSmartmeterData: ", query

            cur.execute(query)
            return cur.fetchall()

    def getTransmissionsCount(self, nome_tabella, data_da, data_a):

        if not self.connected:
            raise Exception('smartgrid not connected')

        with self.CONN.cursor(cursor_factory=psycopg2.extras.DictCursor) as cur:

            #query_get_smartmeters_count_mono
            #select count(*), sender_id from sg_21 where measurement_ts > '2017-07-25 23:59:59' and measurement_ts < '2017-08-03 00:00:00' group by sender_id

            if nome_tabella == 'sg_21':
                query = etl_queries.query_get_smartmeters_count_mono.format(
                    data_da = data_da,
                    data_a = data_a)

            elif nome_tabella == 'sg_18':
                query = etl_queries.query_get_smartmeters_count_tri.format(
                    data_da=data_da,
                    data_a = data_a)

            print "Ecco la query di getTransmissionsCount: ", query

            cur.execute(query)
            return cur.fetchall()

    def getLastTransmission(self, sender_id, nome_tabella):

        if not self.connected:
            raise Exception('smartgrid not connected')

        with self.CONN.cursor(cursor_factory=psycopg2.extras.DictCursor) as cur:

            #query_get_last_transmission_mono
            #select sender_id, measurement_ts, energia_attiva_prelievo, potenza_attiva  from sg_21 where sender_id = '3614BBBK4274' order by measurement_ts desc limit 1

            if nome_tabella == 'sg_21':
                query = etl_queries.query_get_last_transmission_mono.format(
                    sender_id = sender_id)

            elif nome_tabella == 'sg_18':
                query = etl_queries.query_get_last_transmission_tri.format(
                    sender_id = sender_id)

            print "Ecco la query di getLastTransmission: ", query

            cur.execute(query)
            return cur.fetchall()


    def getContractStatistics(self, contract_id):
        if not self.connected:
            raise Exception('smartgrid not connected')

        with self.CONN.cursor(cursor_factory=psycopg2.extras.DictCursor) as cur:
            query = etl_queries.Q_CONTRACT_STATISTICS.format(contract_id=contract_id, remote_db_name=self.remote_db_name)
            cur.execute(query)
            res = cur.fetchall()
        if res is None:
            return None
        else:
            #ricostruisce il dato in caso di eventuali mancanze
            current_month = datetime.date.today().month
            months = (range(1,13)[current_month:] + range(1,13)[0:current_month])[::-1]
            month_idx=0
            f1=[0]*12
            f2=[0]*12
            f3=[0]*12

            for el in res:
                res_month = el[1]
                if month_idx > 11:
                    break
                real_month = months[month_idx]

                while real_month != res_month:
                    month_idx += 1
                    if month_idx > 11:
                        break
                    real_month = months[month_idx]

                f1[month_idx] = el[3]
                f2[month_idx] = el[4]
                f3[month_idx] = el[5]
                month_idx += 1

            return {'f1':f1[::-1], 'f2':f2[::-1], 'f3':f3[::-1]}

    def getInvoiceList(self, contract_id):
        """

        :param smartgrid_client_id:
        :param contract_id:
        :return:
        """
        if not self.connected:
            raise Exception('smartgrid not connected')

        with self.CONN.cursor(cursor_factory=psycopg2.extras.DictCursor) as cur:
            query = etl_queries.Q_INVOICE_LIST.format(contract_id=contract_id, remote_db_name=self.remote_db_name)
            cur.execute(query)
            return cur.fetchall()

    def getInvoiceFileName(self, contract_id, invoice_id):
        """

        :param smartgrid_client_id:
        :param contract_id:
        :param invoice_id:
        :return: the invoice file name
        :rtype: str
        """
        if not self.connected:
            raise Exception('smartgrid not connected')

        with self.CONN.cursor(cursor_factory=psycopg2.extras.DictCursor) as cur:
            query = etl_queries.Q_INVOICE_FILE.format(contract_id=contract_id, invoice_id= invoice_id, remote_db_name=self.remote_db_name)
            cur.execute(query)
            res = cur.fetchone()
            return res[0] if res else res


    def checkContract(self, contract_id, user_id):
        """

        :param contract_id:
        :param user_id:
        :return:
        """
        if not self.connected:
            raise Exception('smartgrid not connected')

        if contract_id is None or user_id is None:
            return False

        with self.CONN.cursor(cursor_factory=psycopg2.extras.DictCursor) as cur:
            query = etl_queries.Q_CONTRACT_CHECK.format(user_id=user_id, contract_id=contract_id, remote_db_name=self.remote_db_name)
            cur.execute(query)
            res = cur.fetchone()
            return res['num'] == 1
