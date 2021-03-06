# -*- coding: utf-8 -*-
"""
Created on 2018/7/15

@author: will4906
"""

import psycopg2 as psql


def init_field(conn, cursor):
    def add_field(field):
        try:
            cursor.execute("ALTER TABLE {} ADD {} INT;".format(TABLE_NAME, field))
            conn.commit()
        except Exception as e:
            conn.rollback()
    add_field('stage_akin_by_min')
    add_field('stage_akin_by_min_without_limit')


if __name__ == '__main__':
    TABLE_NAME = 'head_project'
    conn = psql.connect(database="tmimic", user="postgres", password="1234")
    cursor = conn.cursor()
    init_field(conn, cursor)

    cursor.execute("UPDATE {} SET stage_akin_by_min = NULL;".format(TABLE_NAME))
    conn.commit()
    cursor.execute("UPDATE {} SET stage_akin_by_min = stage_akin_creat_by_min;".format(TABLE_NAME))
    conn.commit()
    cursor.execute('''
        UPDATE {} SET stage_akin_by_min = stage_kdigo_7day_admin_uo WHERE stage_kdigo_7day_admin_uo IS NOT NULL
        AND stage_kdigo_7day_admin_uo > stage_akin_creat_by_min AND stage_akin_creat_by_min >= 1;
        '''.format(TABLE_NAME))
    conn.commit()

    # cursor.execute("UPDATE {} SET stage_rifie_by_min = NULL;".format(TABLE_NAME))
    # conn.commit()
    # cursor.execute("UPDATE {} SET stage_rifie_by_min = stage_rifie_creat_by_min;".format(TABLE_NAME))
    # conn.commit()
    # cursor.execute('''
    #         UPDATE {} SET stage_rifie_by_min = stage_rifie_7day_admin_uo WHERE stage_rifie_7day_admin_uo IS NOT NULL
    #         AND stage_rifie_7day_admin_uo > stage_rifie_creat_by_min AND stage_rifie_creat_by_min >= 1;
    #         '''.format(TABLE_NAME))
    # conn.commit()
    """
    有限制和无限制的区别在于有限制的必须要求肌酐大于等于1，尿量的评级才生效
    """
    # 算kdigo无限制
    cursor.execute("UPDATE {} SET stage_akin_by_min_without_limit = NULL;".format(TABLE_NAME))
    conn.commit()
    cursor.execute("UPDATE {} SET stage_akin_by_min_without_limit = stage_akin_creat_by_min;".format(TABLE_NAME))
    conn.commit()
    cursor.execute('''
    UPDATE {} SET stage_akin_by_min_without_limit = stage_kdigo_7day_admin_uo WHERE stage_kdigo_7day_admin_uo IS NOT NULL
    AND stage_kdigo_7day_admin_uo > stage_akin_creat_by_min;
    '''.format(TABLE_NAME))
    conn.commit()

    # 算rifie无限制
    # cursor.execute("UPDATE {} SET stage_rifie_by_min_without_limit = NULL;".format(TABLE_NAME))
    # conn.commit()
    # cursor.execute("UPDATE {} SET stage_rifie_by_min_without_limit = stage_rifie_creat_by_min;".format(TABLE_NAME))
    # conn.commit()
    # cursor.execute('''
    #     UPDATE {} SET stage_rifie_by_min_without_limit = stage_rifie_7day_admin_uo WHERE stage_rifie_7day_admin_uo IS NOT NULL
    #     AND stage_rifie_7day_admin_uo > stage_rifie_creat_by_min;
    #     '''.format(TABLE_NAME))
    # conn.commit()
    



