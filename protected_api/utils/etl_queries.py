Q_GRID_STATS = """SELECT * FROM get_grid_stats_db('{zone_id}','{remote_db_name}');"""

Q_GRID_ALARMS = """SELECT * FROM get_grid_alarm_db('{zone_id}','{remote_db_name}');"""

Q_USER ="""SELECT
               {remote_db_name}_res_partner.name as name,
               concat(street,', ',city) AS address,
               string_agg({remote_db_name}_ep_contract.id::text,',') AS contracts,
               not(is_company) AS private
           FROM {remote_db_name}_res_partner
           JOIN {remote_db_name}_ep_contract ON {remote_db_name}_res_partner.id={remote_db_name}_ep_contract.partner_id
           WHERE {remote_db_name}_res_partner.id= {user_id}
           GROUP BY name, {remote_db_name}_res_partner.street, {remote_db_name}_res_partner.city,{remote_db_name}_res_partner.is_company;
"""

Q_PODS = """SELECT
                {remote_db_name}_ep_contract.id as contract_id,
                pod_code as pod,
                concat(pod_address,' ', pod_address2, ' ', pod_zip, ' ', pod_city) AS pod_address,
                {remote_db_name}_ep_contract.power_contract as power_contract,
                {remote_db_name}_ep_contract.power_available as power_available
            FROM {remote_db_name}_res_partner
            JOIN {remote_db_name}_ep_contract ON {remote_db_name}_res_partner.id={remote_db_name}_ep_contract.partner_id
            WHERE {remote_db_name}_res_partner.id= {user_id}
        """
        
Q_PODS_SP = """SELECT
                {remote_db_name}_ep_contract.id as contract_id,
                pod_code as pod,
                concat(pod_address,' ', pod_address2, ' ', pod_zip, ' ', pod_city) AS pod_address,
                {remote_db_name}_ep_contract.power_contract as power_contract,
                {remote_db_name}_ep_contract.power_available as power_available,
                {remote_db_name}_ep_contract.abilitazione_prepagata as abilitazione_prepagata,
                {remote_db_name}_ep_contract.credito_prepagata_reale as credito_prepagata_reale,
                {remote_db_name}_ep_contract.credito_prepagata_stima as credito_prepagata_stima
            FROM {remote_db_name}_res_partner
            JOIN {remote_db_name}_ep_contract ON {remote_db_name}_res_partner.id={remote_db_name}_ep_contract.partner_id
            WHERE {remote_db_name}_res_partner.id= {user_id}
        """

Q_SMARTMETERS = """SELECT
                {remote_db_name}_ep_contract.id as contract_id,
                count({remote_db_name}_sg_smartmeter.type) > 0 AS has_sm,
                string_agg({remote_db_name}_sg_smartmeter.type::text,',') AS types
            FROM {remote_db_name}_res_partner
            JOIN {remote_db_name}_ep_contract ON {remote_db_name}_res_partner.id={remote_db_name}_ep_contract.partner_id
            LEFT JOIN {remote_db_name}_sg_smartmeter_contract ON {remote_db_name}_sg_smartmeter_contract.contract_id={remote_db_name}_ep_contract.id
            LEFT JOIN {remote_db_name}_sg_smartmeter ON {remote_db_name}_sg_smartmeter_contract.smartmeter_id={remote_db_name}_sg_smartmeter.id
            WHERE {remote_db_name}_res_partner.id= {user_id}
            GROUP BY {remote_db_name}_ep_contract.id
        """

Q_INVOICE_LIST = """SELECT
                {remote_db_name}_ir_attachment.id as id,
                extract(epoch from {remote_db_name}_aeegsi_energia_bolletta.data_scadenza)::int as data_scadenza,
                {remote_db_name}_ir_attachment.name as name
            FROM {remote_db_name}_ir_attachment
            JOIN {remote_db_name}_aeegsi_energia_bolletta on {remote_db_name}_aeegsi_energia_bolletta.id = {remote_db_name}_ir_attachment.res_id
            WHERE
                {remote_db_name}_ir_attachment.res_model = 'aeegsi_energia.bolletta'
                and
                {remote_db_name}_aeegsi_energia_bolletta.contract_id = {contract_id}
                and
                file_type = 'application/pdf'
            ORDER BY data_scadenza DESC
        """

Q_INVOICE_FILE = """SELECT
                {remote_db_name}_ir_attachment.store_fname AS file
            FROM {remote_db_name}_ir_attachment
            JOIN {remote_db_name}_aeegsi_energia_bolletta ON {remote_db_name}_aeegsi_energia_bolletta.id = {remote_db_name}_ir_attachment.res_id
            WHERE
                {remote_db_name}_ir_attachment.res_model = 'aeegsi_energia.bolletta'
            AND
                {remote_db_name}_aeegsi_energia_bolletta.contract_id = {contract_id}
            AND
                {remote_db_name}_ir_attachment.id = {invoice_id}
        """

Q_CONTRACT_CHECK = """SELECT
                count(*) as num
            FROM {remote_db_name}_ep_contract
            WHERE partner_id={user_id} AND id={contract_id};"""

Q_CONTRACT_STATISTICS = """SELECT
        concat(year,to_char(month,'09')) as date, month, year, kwh_f1, kwh_f2, kwh_f3
    FROM
        {remote_db_name}_ep_contract_statistics_month
    WHERE
        contract_id = {contract_id}
    order by date DESC limit 12"""

Q_REGISTER = """SELECT
                id
            FROM
                {remote_db_name}_res_partner
            WHERE
                piva_fiscal_code='{fiscal_sn}'
                AND
                client_code='{verification_code}'
        """

Q_MESSAGES = """SELECT
                id, message, name as title,
                extract(epoch from write_date)::int as write_date
            FROM {remote_db_name}_sg_message
            WHERE partner_id={user_id} OR partner_id IS NULL
            ORDER BY write_date DESC; """


####################################################################################################
#STORED PROCEDURES
####################################################################################################
#Q_MESSAGES = """SELECT * FROM get_write_date_message_db({user_id}, '{remote_db_name}'); """

Q_POWERS = """SELECT * FROM get_potenze2_db({contract_id},'{remote_db_name}');"""

Q_MEASURES = """SELECT row_number() over() as n, * FROM get_measures_nh({contract_id}, {num_hours}, '{remote_db_name}'); """

Q_ALARMS_CONTRACT = """SELECT  * FROM get_alarm_sm({contract_id},  '{remote_db_name}'); """
#Q_MEASURES = """SELECT * FROM get_measures2_db({contract_id}, '{remote_db_name}'); """

# query generica per selezionare un campo di una tabella dove un campo vale una certa cosa.

#-------------Roby----------------------------
query_get_data = """Select {nome_campo_select} as {nome_campo_select},
measurement_ts as measurement_ts from {nome_tabella}
where {nome_campo_where} = '{valore_campo_where}' order by measurement_ts desc limit 1 """

query_scan_smartmeters_mono_fase = """select count(*) as transmissions_number, sender_id from sg_21 group by sender_id """
query_scan_smartmeters_tri_fase = """select count(*) as transmissions_number, sender_id from sg_18 group by sender_id """

query_get_smartmeter_data_mono = """select sender_id, measurement_ts, energia_attiva_prelievo, potenza_attiva from sg_21 where measurement_ts >= '{data_da}' and
 measurement_ts <= '{data_a}' and sender_id = '{sender_id}' order by measurement_ts desc """
#esempio
# #select sender_id, measurement_ts, energia_attiva_prelievo, potenza_attiva from sg_21 where measurement_ts >= '2017-03-01 14:09:25'
# and measurement_ts <= '2017-03-01 14:36' and  sender_id = '3614BBBK4274'  order by measurement_ts desc

query_get_smartmeter_data_tri = """select sender_id, measurement_ts, energia_attiva_prelievo_sum, potenza_attiva_sum from sg_18 where measurement_ts >= '{data_da}' and
 measurement_ts <= '{data_a}' and sender_id = '{sender_id}' order by measurement_ts desc """

#esempio:
# select sender_id, measurement_ts, energia_attiva_prelievo_sum, potenza_attiva_sum from sg_18 where measurement_ts >= '2015-09-28 05:37:06'  and measurement_ts <= '2015-09-28 23:27:02'
# and sender_id = '3614BBBK4487'  order by measurement_ts

query_get_smartmeters_count_mono = """select sender_id, count(*) from sg_21 where  measurement_ts >= '{data_da}' and measurement_ts <= '{data_a}' group by sender_id"""
#esempio:
#select sender_id, count(*) from sg_21 where measurement_ts > '2017-07-25 23:59:59' and measurement_ts < '2017-08-03 00:00:00' group by sender_id

query_get_smartmeters_count_tri = """select sender_id, count(*) from sg_18 where  measurement_ts >= '{data_da}' and measurement_ts <= '{data_a}' group by sender_id"""


query_get_last_transmission_mono = """select sender_id, measurement_ts, energia_attiva_prelievo, potenza_attiva  from sg_21
where sender_id = '{sender_id}'  order by measurement_ts desc limit 1"""

query_get_last_transmission_tri = """select sender_id, measurement_ts, energia_attiva_prelievo_sum, potenza_attiva_sum  from sg_18
where sender_id = '{sender_id}'  order by measurement_ts desc limit 1"""
#esempio:
#            select sender_id, measurement_ts, energia_attiva_prelievo, potenza_attiva  from sg_21 where sender_id = '3614BBBK4274' order by measurement_ts desc limit 1
#---------------------------------------------------------------